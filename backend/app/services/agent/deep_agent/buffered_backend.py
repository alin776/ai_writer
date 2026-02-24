"""
BufferedFilesystemBackend — 带写缓冲 + 脚本执行的文件系统后端

继承 DeepAgents 的 FilesystemBackend，将 write/edit 操作缓冲到内存，
不直接落盘。用户审批后调用 flush() 写入磁盘或 discard() 丢弃。
同时实现 SandboxBackendProtocol，使 FilesystemMiddleware 启用 execute 工具。

核心思路：
- write() / edit() 不落盘，追加到 self._buffer 操作日志
- read() 先查缓冲区（通过 _replay），没有才读磁盘
- flush() 审批通过后将缓冲区全部写入磁盘
- discard() 审批拒绝丢弃全部缓冲区
- execute() 在 work_dir 内执行 shell 命令（受限沙箱）
"""

import json
import logging
import os
import re
import subprocess
import uuid
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from deepagents.backends.filesystem import (
    EditResult,
    FilesystemBackend,
    WriteResult,
    format_content_with_line_numbers,
    perform_string_replacement,
)
from deepagents.backends.protocol import ExecuteResponse, SandboxBackendProtocol

# ─── CJK 文本格式容错工具 ───

_logger = logging.getLogger(__name__)

# 全角空格 U+3000，中文排版常用段首缩进
_FULLWIDTH_SPACE = "\u3000"

# 模糊匹配：允许的最大字符差异比例
_FUZZY_THRESHOLD = 0.05  # 5%


def _build_format_transforms() -> list:
    """构建格式变换函数列表，供 _try_match_old_string 和组合容错复用。"""
    _strip_line_nums = lambda s: re.sub(r"^\s*\d+\t", "", s, flags=re.MULTILINE)
    return [
        # T0: 去行号
        _strip_line_nums,
        # T1: 全角空格归一化（3个以上连续全角空格 → 2个，处理 LLM 缩进加倍）
        lambda s: re.sub(r"\u3000{3,}", "\u3000\u3000", s),
        # T2: 全角→半角
        lambda s: s.replace(_FULLWIDTH_SPACE, " "),
        # T3: 半角→全角（行首两个半角 → 两个全角）
        lambda s: re.sub(r"^  (?! )", "\u3000\u3000", s, flags=re.MULTILINE),
        # T4: 双换行→单换行
        lambda s: re.sub(r"\n{2,}", "\n", s),
        # T5: 单换行→双换行
        lambda s: s.replace("\n", "\n\n"),
        # T6: 全角→半角 + 双换行→单换行
        lambda s: re.sub(r"\n{2,}", "\n", s.replace(_FULLWIDTH_SPACE, " ")),
        # T7: 半角→全角 + 双换行→单换行
        lambda s: re.sub(r"\n{2,}", "\n",
                         re.sub(r"^  (?! )", "\u3000\u3000", s, flags=re.MULTILINE)),
        # T8: 全角→半角 + 单换行→双换行
        lambda s: s.replace(_FULLWIDTH_SPACE, " ").replace("\n", "\n\n"),
        # T9: 去行号 + 双换行→单换行
        lambda s: re.sub(r"\n{2,}", "\n", _strip_line_nums(s)),
        # T10: 全角空格归一化 + 双换行→单换行
        lambda s: re.sub(r"\n{2,}", "\n", re.sub(r"\u3000{3,}", "\u3000\u3000", s)),
    ]


def _try_match_old_string(content: str, old_string: str) -> str | None:
    """尝试多种格式变换，找到 old_string 在 content 中能匹配的版本。

    LLM 复述文件内容时常见的格式走样：
    - 全角空格 → 半角空格（或反过来）
    - 段落间单换行 → 双换行（或反过来）
    - read_file 返回的行号前缀被误带入 old_string
    - 以上组合

    Returns:
        能在 content 中找到的变换后字符串，或 None
    """
    for transform in _build_format_transforms():
        candidate = transform(old_string)
        if candidate != old_string and candidate in content:
            return candidate

    return None


def _fuzzy_find_in_content(content: str, old_string: str) -> str | None:
    """通过前缀/后缀锚点定位，在 content 中找到与 old_string 对应的实际子串。

    处理 LLM 复述时产生的：
    - 字符级幻觉（如 原来→原先）
    - 字符插入/删除（如 也就是说→也就说）导致的级联偏移

    算法：
    1. 二分查找 old_string 在 content 中能匹配的最长前缀长度
    2. 二分查找 old_string 在 content 中能匹配的最长后缀长度
    3. 策略 A：等长提取 + 逐字符容差比对（处理少量替换）
    4. 策略 B：锚点区间提取（用前缀尾和后缀头在 content 中夹出实际区间，
       处理插入/删除导致长度不等的情况）

    Returns:
        content 中的实际子串，或 None
    """
    old_len = len(old_string)
    if old_len < 10:
        return None

    max_diff = max(3, int(old_len * _FUZZY_THRESHOLD))

    # ── 二分查找最长前缀 ──
    lo, hi, best_prefix = 10, old_len, 0
    while lo <= hi:
        mid = (lo + hi) // 2
        if old_string[:mid] in content:
            best_prefix = mid
            lo = mid + 1
        else:
            hi = mid - 1

    # ── 二分查找最长后缀 ──
    lo, hi, best_suffix = 10, old_len, 0
    while lo <= hi:
        mid = (lo + hi) // 2
        if old_string[-mid:] in content:
            best_suffix = mid
            lo = mid + 1
        else:
            hi = mid - 1

    _logger.warning("[FMT-FIX] fuzzy: best_prefix=%d/%d, best_suffix=%d/%d",
                    best_prefix, old_len, best_suffix, old_len)

    # ── 策略 A：等长提取 + 逐字符容差（处理少量字符替换） ──
    def _try_equal_length(pos: int) -> str | None:
        if pos < 0 or pos + old_len > len(content):
            return None
        candidate = content[pos:pos + old_len]
        diffs = sum(1 for a, b in zip(candidate, old_string) if a != b)
        if diffs <= max_diff:
            _logger.warning("[FMT-FIX] 策略A命中: pos=%d, diffs=%d", pos, diffs)
            return candidate
        return None

    if best_prefix >= 10:
        pos = content.find(old_string[:best_prefix])
        result = _try_equal_length(pos)
        if result:
            return result

    if best_suffix >= 10:
        pos = content.find(old_string[-best_suffix:])
        result = _try_equal_length(pos - (old_len - best_suffix))
        if result:
            return result

    # ── 策略 B：锚点区间提取（处理插入/删除导致的长度差异） ──
    # 需要前缀和后缀都有足够长的匹配锚点
    if best_prefix >= 10 and best_suffix >= 10:
        prefix_pos = content.find(old_string[:best_prefix])
        # 从前缀位置之后搜索后缀，避免匹配到前缀之前的重复片段
        suffix_pos = content.find(old_string[-best_suffix:], prefix_pos) if prefix_pos >= 0 else -1

        if prefix_pos >= 0 and suffix_pos >= 0:
            region_start = prefix_pos
            region_end = suffix_pos + best_suffix

            # 合理性检查：提取区间长度应与 old_string 长度接近（允许 20% 偏差）
            region_len = region_end - region_start
            len_ratio = region_len / old_len if old_len > 0 else 0

            _logger.warning(
                "[FMT-FIX] 策略B锚点: prefix_pos=%d, suffix_pos=%d, "
                "region=[%d:%d] len=%d, old_len=%d, ratio=%.2f",
                prefix_pos, suffix_pos, region_start, region_end,
                region_len, old_len, len_ratio,
            )

            if (region_start < suffix_pos  # 前缀在后缀之前
                    and 0.8 <= len_ratio <= 1.2):  # 长度偏差 ≤ 20%
                candidate = content[region_start:region_end]
                _logger.warning("[FMT-FIX] 策略B命中: 区间长度=%d, old长度=%d",
                                region_len, old_len)
                return candidate

    return None


def _adapt_new_string(content: str, new_string: str) -> str:
    """将 new_string 的格式适配为 content 的排版风格。

    检测 content 使用的缩进和换行约定，统一 new_string 的格式。
    """
    result = new_string

    # 缩进适配：content 用全角缩进 → new_string 行首半角转全角
    if _FULLWIDTH_SPACE in content:
        result = re.sub(r"^  (?! )", "\u3000\u3000", result, flags=re.MULTILINE)

    # 换行适配：content 段落间无空行（全角缩进行紧邻） → 折叠双换行
    if re.search(r"[^\n]\n" + _FULLWIDTH_SPACE, content):
        result = re.sub(r"\n{2,}", "\n", result)

    return result


@dataclass
class BufferOp:
    """单条缓冲操作"""
    op_type: str  # "write" or "edit"
    path: str     # 虚拟路径（相对于 root_dir）
    content: str | None = None      # write 时的完整内容
    old_string: str | None = None   # edit 时的旧字符串
    new_string: str | None = None   # edit 时的新字符串
    replace_all: bool = False       # edit 时是否全部替换


class BufferedFilesystemBackend(FilesystemBackend, SandboxBackendProtocol):
    """带写缓冲 + 脚本执行能力的文件系统后端。

    Agent 执行期间的 write/edit 操作存入内存缓冲区，
    用户审批后调用 flush() 落盘或 discard() 丢弃。
    同时支持 execute() 命令执行，使 Skill 脚本可运行。
    """

    def __init__(self, root_dir: str | Path, *, timeout: float = 60.0,
                 max_output: int = 100_000,
                 use_docker: bool = False,
                 docker_image: str = "python:3.11-slim",
                 host_data_root: str = "",
                 **kwargs):
        kwargs.setdefault("virtual_mode", True)
        super().__init__(root_dir=root_dir, **kwargs)
        self._buffer: list[BufferOp] = []
        self._timeout = timeout
        self._max_output = max_output
        self._id = f"buffered-{uuid.uuid4().hex[:8]}"
        self._preflushed_paths: set[str] = set()          # 已预落盘的路径
        self._preflushed_originals: dict[str, str | None] = {}  # 路径 → 预落盘前的原始内容（None = 新文件）
        self._use_docker = use_docker
        self._docker_image = docker_image
        self._host_data_root = host_data_root
        self._sandbox = None  # DockerSandbox | None（懒初始化）

    @property
    def id(self) -> str:
        return self._id

    # ─── Windows 路径兼容 ───

    def ls_info(self, path: str) -> list:
        """ls_info with Windows path normalization for virtual mode.

        FilesystemBackend.ls_info() 在 virtual_mode 下通过字符串操作计算虚拟路径，
        但 Windows 上 str(Path(...)) 返回反斜杠，导致虚拟路径畸形
        (如 "/\\skills\\..." )，使 SkillsMiddleware 无法发现任何技能。
        这里在父类返回结果后统一将反斜杠归一化为正斜杠。
        """
        results = super().ls_info(path)
        if os.name == "nt":
            for item in results:
                if "path" in item:
                    item["path"] = item["path"].replace("\\", "/")
        return results

    def glob_info(self, pattern: str, path: str = "/") -> list:
        """glob_info with Windows path normalization.

        Same issue as ls_info: FilesystemBackend.glob_info() computes virtual
        paths via str(Path(...)), which produces backslashes on Windows.
        """
        results = super().glob_info(pattern, path)
        if os.name == "nt":
            for item in results:
                if "path" in item:
                    item["path"] = item["path"].replace("\\", "/")
        return results

    def grep_raw(self, pattern: str, path: str | None = None, glob: str | None = None) -> list | str:
        """grep_raw with Windows path normalization.

        grep_raw returns list[GrepMatch] on success or str on error.
        Only normalize paths when the result is a list.
        """
        results = super().grep_raw(pattern, path, glob)
        if os.name == "nt" and isinstance(results, list):
            for item in results:
                if "path" in item:
                    item["path"] = item["path"].replace("\\", "/")
        return results

    # ─── 脚本执行（SandboxBackendProtocol） ───

    def _resolve_script_path(self, script_ref: str) -> str | None:
        """将 SKILL.md 中的短路径 scripts/xxx.py 解析为实际路径。

        SKILL.md 指示 agent 用 ``python scripts/xxx.py``，但 cwd 是 work_dir 根，
        实际脚本在 ``skills/{group}/{skill}/scripts/xxx.py``。
        搜索 skills 子树找到唯一匹配并返回相对于 cwd 的路径。
        """
        candidate = self.cwd / script_ref
        if candidate.exists():
            return None  # 路径本身已正确，无需替换

        # 提取文件名，在 skills/**/scripts/ 下搜索
        script_name = Path(script_ref).name
        skills_dir = self.cwd / "skills"
        if not skills_dir.is_dir():
            return None

        matches = list(skills_dir.rglob(f"scripts/{script_name}"))
        if len(matches) == 1:
            return str(matches[0].relative_to(self.cwd)).replace("\\", "/")
        return None

    def _flush_for_execute(self) -> None:
        """将缓冲区文件预落盘，使 execute 子进程可见。幂等安全。

        用 _replay() 从 buffer 计算每个文件的最终状态并写入磁盘，
        不依赖当前磁盘内容，因此调用 N 次结果相同。
        不清空 _buffer — 缓冲区仍保留用于审批流程。
        """
        affected_paths = {op.path for op in self._buffer}
        for path in affected_paths:
            # 首次预落盘：保存原始内容用于 discard 回滚
            if path not in self._preflushed_originals:
                resolved = self._resolve_path(path)
                if resolved.exists():
                    self._preflushed_originals[path] = resolved.read_text(encoding="utf-8")
                else:
                    self._preflushed_originals[path] = None  # 新文件

            # 用 _replay() 计算最终状态并写入磁盘
            content = self._replay(path)
            if content is not None:
                resolved = self._resolve_path(path)
                resolved.parent.mkdir(parents=True, exist_ok=True)
                resolved.write_text(content, encoding="utf-8")
                self._preflushed_paths.add(path)

    def execute(self, command: str, *, timeout: int | None = None) -> ExecuteResponse:
        """在 work_dir 内执行 shell 命令（受限沙箱）。"""
        if not command or not isinstance(command, str):
            return ExecuteResponse(output="Error: empty command", exit_code=1)

        # ── 0. 将缓冲区文件临时落盘，使子进程可见 ──
        self._flush_for_execute()

        # ── 1. 虚拟绝对路径翻译 ──
        # Agent 生成 "/chapters/...", "/skills/..." 等虚拟绝对路径，
        # OS shell 会将 "/" 开头视为系统根目录，需翻译为 cwd 下的真实路径。
        cwd_str = str(self.cwd)
        _VDIRS = r"chapters|skills|knowledge|explorations|context|scripts"
        command = re.sub(
            rf'(?<=["\s])/(?=(?:{_VDIRS})(?:[/"\s\\]|$))',
            lambda _: cwd_str.rstrip("/\\") + "/",
            command,
        )
        # 处理命令开头的路径（如 /skills/...）
        if command.startswith("/") and not command.startswith("//"):
            first_seg = command.split("/")[1] if "/" in command[1:] else ""
            if first_seg in ("chapters", "skills", "knowledge", "explorations", "context", "scripts"):
                command = cwd_str.rstrip("/\\") + command

        # ── 2. Skill 短路径修正 ──
        # SKILL.md 写 "python scripts/xxx.py" 假定 cwd 在 skill 目录下，
        # 但实际 cwd 是 work_dir 根，脚本在 skills/{group}/{skill}/scripts/ 下。
        script_match = re.search(r'(?:^|[\s"])(scripts/[\w.\-/]+\.py)', command)
        if script_match:
            short_path = script_match.group(1)
            real_path = self._resolve_script_path(short_path)
            if real_path:
                command = command.replace(short_path, real_path, 1)

        effective_timeout = timeout if timeout is not None else self._timeout

        # ── Docker 沙盒执行分支 ──
        if self._use_docker:
            # 路径翻译：宿主机路径 → 容器内 /workspace
            cwd_posix = str(self.cwd).replace("\\", "/")
            command = command.replace(str(self.cwd), "/workspace")
            if cwd_posix != str(self.cwd):
                command = command.replace(cwd_posix, "/workspace")
            # 清理残余反斜杠（Windows 路径遗留），确保命令在 Linux 容器中合法
            command = command.replace("\\", "/")
            # 清理多余斜杠（Agent 偶尔生成 //chapters/ 等双斜杠路径）
            command = re.sub(r'(?<!:)/{2,}', '/', command)

            try:
                from app.services.agent.deep_agent.docker_sandbox import DockerSandbox

                if self._sandbox is None:
                    self._sandbox = DockerSandbox(
                        self.cwd, self._docker_image,
                        host_data_root=self._host_data_root,
                    )
                self._sandbox.ensure_running()
                output, exit_code = self._sandbox.run(
                    command, timeout=int(effective_timeout),
                )
            except Exception as e:
                return ExecuteResponse(output=f"Error (docker): {e}", exit_code=1)

            truncated = False
            if len(output) > self._max_output:
                output = output[:self._max_output] + \
                    f"\n...truncated at {self._max_output} bytes"
                truncated = True

            if exit_code != 0:
                output = f"{output.rstrip()}\n\nExit code: {exit_code}"

            return ExecuteResponse(
                output=output,
                exit_code=exit_code,
                truncated=truncated,
            )

        # ── 原有 subprocess 执行分支（向后兼容） ──
        # 清理多余斜杠（Agent 偶尔生成 //chapters/ 等双斜杠路径）
        command = re.sub(r'(?<!:)/{2,}', '/', command)
        try:
            result = subprocess.run(
                command, shell=True, capture_output=True, text=True,
                encoding="utf-8", errors="replace",
                timeout=effective_timeout, cwd=str(self.cwd),
                env={**os.environ, "PYTHONIOENCODING": "utf-8"},
            )
            output_parts = []
            if result.stdout:
                output_parts.append(result.stdout)
            if result.stderr:
                for line in result.stderr.strip().split("\n"):
                    output_parts.append(f"[stderr] {line}")
            output = "\n".join(output_parts) if output_parts else "<no output>"

            truncated = False
            if len(output) > self._max_output:
                output = output[:self._max_output] + \
                    f"\n...truncated at {self._max_output} bytes"
                truncated = True

            if result.returncode != 0:
                output = f"{output.rstrip()}\n\nExit code: {result.returncode}"

            return ExecuteResponse(
                output=output,
                exit_code=result.returncode,
                truncated=truncated,
            )
        except subprocess.TimeoutExpired:
            return ExecuteResponse(
                output=f"Error: timed out after {effective_timeout}s",
                exit_code=124,
            )
        except Exception as e:
            return ExecuteResponse(output=f"Error: {e}", exit_code=1)

    # ─── 沙盒清理 ───

    def cleanup_sandbox(self) -> None:
        """清理 Docker 沙盒容器（如果有）。"""
        if self._sandbox is not None:
            self._sandbox.cleanup()
            self._sandbox = None

    # ─── 重写写操作：缓冲不落盘 ───

    def write(self, file_path: str, content: str) -> WriteResult:
        """write 操作存入缓冲区，不落盘。"""
        # 检查磁盘上是否已存在
        resolved = self._resolve_path(file_path)
        if resolved.exists():
            return WriteResult(
                error=f"Cannot write to {file_path} because it already exists. "
                      "Read and then make an edit, or write to a new path."
            )

        # 检查缓冲区是否已 write 过同路径
        for op in self._buffer:
            if op.path == file_path and op.op_type == "write":
                return WriteResult(
                    error=f"Cannot write to {file_path} because it already exists "
                          "in the pending buffer."
                )

        self._buffer.append(BufferOp(
            op_type="write",
            path=file_path,
            content=content,
        ))
        return WriteResult(path=file_path, files_update=None)

    def edit(
        self,
        file_path: str,
        old_string: str,
        new_string: str,
        replace_all: bool = False,
    ) -> EditResult:
        """edit 操作存入缓冲区，不落盘。先验证 old_string 匹配。"""
        # 行号模式检测：[LINES:起始行-结束行]
        m = re.match(r'^\[LINES:(\d+)-(\d+)\]$', old_string.strip())
        if m:
            return self._edit_by_lines(file_path, int(m.group(1)), int(m.group(2)), new_string)

        # 通过 _replay 获取文件当前内容（含缓冲区）
        current = self._replay(file_path)
        if current is None:
            return EditResult(error=f"Error: File '{file_path}' not found")

        # 验证 old_string 存在且可替换
        result = perform_string_replacement(current, old_string, new_string, replace_all)

        # 精确匹配失败 → 逐级容错
        if isinstance(result, str):
            _logger.warning(
                "[FMT-FIX] 精确匹配失败，尝试容错。old_string 前80字符: %r, "
                "content 前80字符: %r",
                old_string[:80], current[:80],
            )

            # 第一级：格式变换（空格、换行）
            adapted_old = _try_match_old_string(current, old_string)

            # 第二级：模糊字符匹配（处理 LLM 字符幻觉）
            if not adapted_old:
                adapted_old = _fuzzy_find_in_content(current, old_string)
                if adapted_old:
                    _logger.warning("[FMT-FIX] 模糊字符匹配命中")

            # 第三级：格式变换 + 模糊字符匹配（处理两者同时发生）
            if not adapted_old:
                for transform in _build_format_transforms():
                    transformed = transform(old_string)
                    if transformed != old_string:
                        adapted_old = _fuzzy_find_in_content(current, transformed)
                        if adapted_old:
                            _logger.warning("[FMT-FIX] 格式变换+模糊匹配组合命中")
                            break

            _logger.warning("[FMT-FIX] 容错查找结果: %s",
                            f"found, 前50字符: {adapted_old[:50]!r}" if adapted_old else "未找到")

            # 诊断：当所有容错都失败时，记录详细信息
            if not adapted_old:
                probe = old_string[:30]
                probe_in = probe in current
                _logger.warning(
                    "[FMT-FIX] 诊断: old[:30] in content=%s, probe=%r, "
                    "content_len=%d, old_len=%d",
                    probe_in, probe, len(current), len(old_string),
                )
            if adapted_old:
                adapted_new = _adapt_new_string(current, new_string)
                result = perform_string_replacement(
                    current, adapted_old, adapted_new, replace_all
                )
                _logger.warning("[FMT-FIX] 容错替换结果: %s",
                                "成功" if not isinstance(result, str) else result)
                if not isinstance(result, str):
                    old_string = adapted_old
                    new_string = adapted_new

        if isinstance(result, str):
            return EditResult(error=result)

        _new_content, occurrences = result

        self._buffer.append(BufferOp(
            op_type="edit",
            path=file_path,
            old_string=old_string,
            new_string=new_string,
            replace_all=replace_all,
        ))
        return EditResult(path=file_path, files_update=None, occurrences=int(occurrences))

    def _edit_by_lines(
        self,
        file_path: str,
        start_line: int,
        end_line: int,
        new_string: str,
    ) -> EditResult:
        """按行号范围替换：读取文件 → 提取指定行 → 存入 buffer。

        old_string 存实际行文本（保证 get_changes() 返回真实文本供前端 diff）。
        """
        current = self._replay(file_path)
        if current is None:
            return EditResult(error=f"Error: File '{file_path}' not found")

        lines = current.split("\n")
        # 行号从 1 开始，转为 0-based
        si = start_line - 1
        ei = end_line  # end_line 包含在内，slice 到 ei

        if si < 0 or ei > len(lines) or si >= ei:
            return EditResult(
                error=f"Error: Invalid line range [{start_line}-{end_line}], "
                      f"file has {len(lines)} lines"
            )

        actual_old = "\n".join(lines[si:ei])
        adapted_new = _adapt_new_string(current, new_string)

        self._buffer.append(BufferOp(
            op_type="edit",
            path=file_path,
            old_string=actual_old,
            new_string=adapted_new,
            replace_all=False,
        ))

        _logger.info(
            "[LINES-EDIT] %s [%d-%d] → %d chars replaced by %d chars",
            file_path, start_line, end_line,
            len(actual_old), len(adapted_new),
        )
        return EditResult(path=file_path, files_update=None, occurrences=1)

    # ─── 重写读操作：优先读缓冲区 ───

    def read(
        self,
        file_path: str,
        offset: int = 0,
        limit: int = 2000,
    ) -> str:
        """读文件，优先查缓冲区（含 replay），没有才读磁盘。"""
        # 只有该文件在缓冲区中有操作时，才走 replay 路径
        has_buffer_ops = any(op.path == file_path for op in self._buffer)
        if has_buffer_ops:
            replayed = self._replay(file_path)
            if replayed is not None:
                lines = replayed.splitlines()
                start_idx = offset
                end_idx = min(start_idx + limit, len(lines))
                if start_idx >= len(lines):
                    return f"Error: Line offset {offset} exceeds file length ({len(lines)} lines)"
                selected = lines[start_idx:end_idx]
                return format_content_with_line_numbers(selected, start_line=start_idx + 1)

        # 缓冲区没有，走父类（读磁盘）
        return super().read(file_path, offset, limit)

    # ─── 核心重放逻辑 ───

    def _replay(self, file_path: str) -> str | None:
        """按序重放缓冲区操作，得到文件当前内容。

        三种情况：
        1. 缓冲区有 write → 从 write 的 content 开始，叠加后续 edit
        2. 缓冲区只有 edit → 先读磁盘内容，再依次 apply edit
        3. 缓冲区和磁盘都没有 → 返回 None

        Args:
            file_path: 虚拟路径

        Returns:
            重放后的文件内容，若文件既不在缓冲区也不在磁盘则返回 None
        """
        # 筛选出该文件的所有操作（保持顺序）
        ops = [op for op in self._buffer if op.path == file_path]

        # 确定初始内容
        content: str | None = None
        start_idx = 0

        for i, op in enumerate(ops):
            if op.op_type == "write":
                # 最后一次 write 作为基础（之前的 write 被覆盖）
                content = op.content or ""
                start_idx = i + 1

        # 如果缓冲区没有 write，尝试从磁盘读取
        if content is None:
            resolved = self._resolve_path(file_path)
            if not resolved.exists() or not resolved.is_file():
                return None
            try:
                content = resolved.read_text(encoding="utf-8")
                content = content.replace("\r\n", "\n")
            except (OSError, UnicodeDecodeError):
                return None

        # 从 start_idx 开始依次 apply edit
        for op in ops[start_idx:]:
            if op.op_type == "edit":
                result = perform_string_replacement(
                    content, op.old_string or "", op.new_string or "", op.replace_all
                )
                if not isinstance(result, str):
                    content, _ = result
                # 替换失败则跳过（不应发生，因为 edit() 已验证过）

        return content

    # ─── 审批操作 ───

    def get_changes(self) -> list[dict[str, Any]]:
        """返回待审批改动列表（JSON 可序列化）。"""
        from app.services.agent.deep_agent.frontmatter import parse_chapter

        changes = []
        for i, op in enumerate(self._buffer):
            item: dict[str, Any] = {
                "index": i,
                "op_type": op.op_type,
                "path": op.path,
            }
            if op.op_type == "write":
                item["content_preview"] = (op.content or "")[:200]
                item["content_length"] = len(op.content or "")
                # 从 frontmatter 提取章节标题，并用去掉 frontmatter 的正文作为 diff 内容
                parsed = parse_chapter(op.content or "")
                item["new_string"] = parsed["content"]
                if parsed["title"]:
                    item["chapter_title"] = parsed["title"]
            elif op.op_type == "edit":
                item["old_string"] = op.old_string
                item["new_string"] = op.new_string
            changes.append(item)
        return changes

    def flush(self) -> list[str]:
        """审批通过：将缓冲区全部写入磁盘。返回受影响的文件路径列表。"""
        import logging
        logger = logging.getLogger(__name__)

        if self._preflushed_paths:
            # 预落盘模式：用 _replay() 计算最终状态，一次性写入
            affected = set()
            all_paths = {op.path for op in self._buffer}
            for path in all_paths:
                try:
                    content = self._replay(path)
                    if content is not None:
                        resolved = self._resolve_path(path)
                        resolved.parent.mkdir(parents=True, exist_ok=True)
                        resolved.write_text(content, encoding="utf-8")
                        affected.add(path)
                except Exception as e:
                    logger.error(f"[BufferedBackend] flush(replay) 失败: {path}: {e}")
            self._buffer.clear()
            self._preflushed_paths.clear()
            self._preflushed_originals.clear()
            return list(affected)

        # 原有增量逻辑（未经 execute() 时走这条路径）
        affected = set()
        for op in self._buffer:
            try:
                if op.op_type == "write":
                    # 用父类的 write 落盘
                    resolved = self._resolve_path(op.path)
                    resolved.parent.mkdir(parents=True, exist_ok=True)
                    flags = os.O_WRONLY | os.O_CREAT | os.O_TRUNC
                    if hasattr(os, "O_NOFOLLOW"):
                        flags |= os.O_NOFOLLOW
                    fd = os.open(resolved, flags, 0o644)
                    with os.fdopen(fd, "w", encoding="utf-8") as f:
                        f.write(op.content or "")
                elif op.op_type == "edit":
                    # 读取当前磁盘内容（或之前 flush 的结果）做替换
                    resolved = self._resolve_path(op.path)
                    content = resolved.read_text(encoding="utf-8")
                    result = perform_string_replacement(
                        content, op.old_string or "", op.new_string or "", op.replace_all
                    )
                    if not isinstance(result, str):
                        new_content, _ = result
                        fd = os.open(resolved, os.O_WRONLY | os.O_TRUNC, 0o644)
                        with os.fdopen(fd, "w", encoding="utf-8") as f:
                            f.write(new_content)
                affected.add(op.path)
            except Exception as e:
                logger.error(f"[BufferedBackend] flush 操作失败: {op.op_type} {op.path}: {e}")
        self._buffer.clear()
        return list(affected)

    def flush_single(self, index: int) -> str | None:
        """单个接受：将指定索引的操作写入磁盘。返回受影响路径或 None。

        安全检查：如果该操作是 edit 且同一文件有更早的未落盘 write，
        则拒绝执行（返回 None），因为 edit 依赖 write 先落盘。
        """
        if index < 0 or index >= len(self._buffer):
            return None

        op = self._buffer[index]

        # 依赖检查：edit 不能脱离其 write 单独 flush
        if op.op_type == "edit":
            has_pending_write = any(
                self._buffer[i].path == op.path and self._buffer[i].op_type == "write"
                for i in range(index)
            )
            if has_pending_write:
                return None

        self._buffer.pop(index)
        if op.op_type == "write":
            resolved = self._resolve_path(op.path)
            resolved.parent.mkdir(parents=True, exist_ok=True)
            resolved.write_text(op.content or "", encoding="utf-8")
        elif op.op_type == "edit":
            resolved = self._resolve_path(op.path)
            content = resolved.read_text(encoding="utf-8")
            result = perform_string_replacement(
                content, op.old_string or "", op.new_string or "", op.replace_all
            )
            if not isinstance(result, str):
                new_content, _ = result
                resolved.write_text(new_content, encoding="utf-8")
        return op.path

    def discard(self) -> None:
        """审批拒绝：丢弃缓冲区，回滚预落盘文件。"""
        for path, original in self._preflushed_originals.items():
            resolved = self._resolve_path(path)
            try:
                if original is None:
                    # 新文件：删除
                    resolved.unlink(missing_ok=True)
                else:
                    # 已有文件被编辑：恢复原始内容
                    resolved.write_text(original, encoding="utf-8")
            except OSError:
                pass
        self._preflushed_paths.clear()
        self._preflushed_originals.clear()
        self._buffer.clear()

    def discard_single(self, index: int) -> bool:
        """单个拒绝：丢弃指定索引的操作。"""
        if index < 0 or index >= len(self._buffer):
            return False
        self._buffer.pop(index)
        return True

    # ─── 持久化（JSON 文件备份） ───

    def save_pending(self, filepath: Path) -> None:
        """将缓冲区序列化到 JSON 文件，服务器重启后可恢复。"""
        filepath.parent.mkdir(parents=True, exist_ok=True)
        data = {
            "cwd": str(self.cwd),
            "buffer": [asdict(op) for op in self._buffer],
        }
        filepath.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")

    @classmethod
    def load_pending(cls, filepath: Path) -> "BufferedFilesystemBackend | None":
        """从 JSON 文件恢复实例。文件不存在或损坏时返回 None。"""
        if not filepath.is_file():
            return None
        try:
            data = json.loads(filepath.read_text(encoding="utf-8"))
            instance = cls(root_dir=data["cwd"])
            instance._buffer = [BufferOp(**op) for op in data["buffer"]]
            return instance
        except Exception:
            return None
