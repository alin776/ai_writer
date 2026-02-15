"""
批量执行并校验 5 条复杂 Prompt 是否“通过”。

通过标准：
1) 能成功调用 /api/v1/agent/chat/stream 获得最终内容；
2) 每条 Prompt 输出满足对应硬性字段规则（search_keywords/证据定位/结论/分页等）。

用法：
    python scripts/validate_complex_prompts.py --token <TOKEN> --work-id <WORK_ID>
    python scripts/validate_complex_prompts.py --username <EMAIL> --password <PWD> --work-id <WORK_ID>
    python scripts/validate_complex_prompts.py --token <TOKEN> --work-id <WORK_ID> --strict
"""

import argparse
import json
import re
import sys
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple

import httpx


@dataclass
class PromptCase:
    case_id: str
    title: str
    prompt: str
    validator: Callable[[str], List[str]]


@dataclass
class CaseResult:
    case_id: str
    title: str
    passed: bool
    errors: List[str]
    output_preview: str
    output_chars: int
    conversation_id: Optional[str]
    raw_event_count: int
    request_error: Optional[str] = None


def _extract_search_keywords(text: str) -> List[str]:
    lowered = text.lower()
    key_pos = lowered.find("search_keywords")
    segment = text
    if key_pos >= 0:
        segment = text[key_pos:key_pos + 1200]

    m = re.search(r"search_keywords\s*[:：]\s*\[([^\]]+)\]", segment, flags=re.IGNORECASE | re.DOTALL)
    array_body = ""
    if m:
        array_body = m.group(1)
    else:
        m2 = re.search(r"\[([^\]]+)\]", segment, flags=re.DOTALL)
        if m2:
            array_body = m2.group(1)

    if not array_body:
        return []

    quoted = re.findall(r"[\"“”'‘’]([^\"“”'‘’]{1,80})[\"“”'‘’]", array_body)
    if quoted:
        return [q.strip() for q in quoted if q.strip()]

    raw_items = [x.strip() for x in array_body.split(",")]
    return [x for x in raw_items if x]


def _count_chapter_paragraph_refs(text: str) -> int:
    patterns = [
        r"第\s*\d+\s*章.{0,20}(第\s*\d+\s*段|段落号\s*[:：]?\s*\d+)",
        r"章节号\s*[:：]?\s*\d+.{0,20}段落号\s*[:：]?\s*\d+",
        r"章\s*[:：]?\s*\d+.{0,20}段\s*[:：]?\s*\d+",
    ]
    total = 0
    for p in patterns:
        total += len(re.findall(p, text))
    return total


def _contains_any(text: str, items: List[str]) -> bool:
    return any(item in text for item in items)


def _validate_case_1(text: str) -> List[str]:
    errs: List[str] = []
    kws = _extract_search_keywords(text)
    if not (8 <= len(kws) <= 12):
        errs.append(f"search_keywords 数量不在 8~12（当前 {len(kws)}）")
    if "支持自洽" not in text:
        errs.append("缺少“支持自洽”栏")
    if "仍未解释的断点" not in text:
        errs.append("缺少“仍未解释的断点”栏")
    if not re.search(r"结论\s*[:：]?\s*(自洽|不自洽|证据不足)", text):
        errs.append("缺少三选一结论（自洽/不自洽/证据不足）")
    conf = re.search(r"置信度\s*[:：]?\s*(\d{1,3})", text)
    if not conf:
        errs.append("缺少置信度数值")
    else:
        score = int(conf.group(1))
        if score < 0 or score > 100:
            errs.append("置信度不在 0~100")
    if _count_chapter_paragraph_refs(text) < 3:
        errs.append("证据定位不足（章节/段落号引用少于3处）")
    return errs


def _validate_case_2(text: str) -> List[str]:
    errs: List[str] = []
    kws = _extract_search_keywords(text)
    if len(kws) < 10:
        errs.append(f"search_keywords 少于10个（当前 {len(kws)}）")
    if not re.search(r"\bT1\b|T1\s*[:：]", text):
        errs.append("缺少时间线 T1~Tn 格式")
    required_nodes = [
        "赵穆让段融擦刀",
        "读取好刀器灵",
        "吞噬发生",
        "刀不顺手",
        "浑圆桩",
    ]
    for node in required_nodes:
        if node not in text:
            errs.append(f"缺少关键节点：{node}")
    if "最关键的因果跳跃点" not in text:
        errs.append("缺少“最关键的因果跳跃点”小节")
    if _count_chapter_paragraph_refs(text) < 5:
        errs.append("时间线证据定位不足（章节/段落号引用少于5处）")
    return errs


def _validate_case_3(text: str) -> List[str]:
    errs: List[str] = []
    kws = _extract_search_keywords(text)
    if len(kws) == 0:
        errs.append("缺少 search_keywords")
    if not re.search(r"第\s*\d+\s*页\s*/\s*共\s*\d+\s*页", text):
        errs.append("缺少“第X页/共Y页”分页标记")
    for field in ["总命中数", "是否存在重复段落", "是否存在疑似漏召回"]:
        if field not in text:
            errs.append(f"缺少字段：{field}")
    if "无命中" in text and "关键词组合" not in text:
        errs.append("输出“无命中”时缺少“关键词组合”")
    if "无命中" not in text and _count_chapter_paragraph_refs(text) < 1:
        errs.append("有命中结果但未给章节/段落定位")
    return errs


def _validate_case_4(text: str) -> List[str]:
    errs: List[str] = []
    kws = _extract_search_keywords(text)
    required_kw = ["器灵等阶", "吞噬要求", "吞噬效果", "牛尾刀", "五虎群羊刀"]
    for kw in required_kw:
        if kw not in text:
            errs.append(f"正文缺少关键词：{kw}")
    if len(kws) > 0:
        for kw in required_kw:
            if kw not in kws:
                errs.append(f"search_keywords 中缺少：{kw}")
    else:
        errs.append("缺少 search_keywords")

    table_fields = ["条目ID", "器物", "等阶", "要求", "效果", "来源"]
    has_table_like = ("|" in text and all(field in text for field in table_fields))
    if not has_table_like:
        errs.append("缺少结构化表格字段（条目ID/器物/等阶/要求/效果/来源）")
    if "一致性检查" not in text:
        errs.append("缺少“一致性检查”")
    if "最终结论" not in text:
        errs.append("缺少“最终结论”")
    return errs


def _validate_case_5(text: str) -> List[str]:
    errs: List[str] = []
    kws = _extract_search_keywords(text)
    if len(kws) < 8:
        errs.append(f"search_keywords 少于8个（当前 {len(kws)}）")
    required_kw = ["精神力2级", "未满足", "吞噬", "第3章"]
    for kw in required_kw:
        if kw not in text:
            errs.append(f"缺少关键术语：{kw}")
    if not _contains_any(text, ["支持A的证据", "支持命题A", "支持A"]):
        errs.append("缺少“支持A的证据”小节")
    if not _contains_any(text, ["反驳A的证据", "反驳命题A", "反驳A"]):
        errs.append("缺少“反驳A的证据”小节")
    if not re.search(r"结论\s*[:：]?\s*(真|假|证据不足)", text):
        errs.append("缺少结论（真/假/证据不足）")
    if not _contains_any(text, ["最少还缺", "还缺哪一类信息", "最少还缺哪一类信息"]):
        errs.append("缺少“命题A成立还缺什么信息”")
    if _count_chapter_paragraph_refs(text) < 2:
        errs.append("证据定位不足（章节/段落号引用少于2处）")
    return errs


PROMPT_1 = """你是“只读取证分析器”，只能基于《一夕千悟，从杂役弟子开始》原文回答，禁止脑补。
任务：核验“牛尾刀器灵等阶悖论”是否自洽。
要求：
1) 先输出你本次检索计划的 search_keywords 数组（8~12个）。
2) 找出并列出所有与以下链路相关的命中段落：废刀读取器灵 -> 赵穆好刀读取器灵 -> 段融推测“兵刃用得越久滋养器灵” -> 立即吞噬成功。
3) 每条证据必须给出：章节号、段落号、原文摘录（20~60字）、该证据支持的结论。
4) 输出“支持自洽的证据”和“仍未解释的断点”两栏。
5) 最后给一个结论：自洽 / 不自洽 / 证据不足（三选一），并给置信度（0~100）。"""

PROMPT_2 = """你是小说事实审计员。请对“段融从擦刀到一夕千悟”做因果时间线追踪，禁止总结成泛泛剧情。
要求：
1) 先给出 search_keywords（不少于10个，含人物名、术语名、动作名）。
2) 只采纳原文证据，按时间顺序输出 T1~Tn。
3) 每个时间点必须包含：事件、触发原因、直接结果、证据定位（章节+段落号+短引）。
4) 必须覆盖这5个关键节点：赵穆让段融擦刀、段融读取好刀器灵、吞噬发生、赵穆夜练“刀不顺手”、段融梦中见内息并次日站浑圆桩。
5) 最后输出“最关键的因果跳跃点（最多3个）”并解释为何是跳跃点。"""

PROMPT_3 = """请执行一次“全量命中验证”，目标是检验你是否会漏掉后续命中。
任务：找出文本中所有同时提及“孔斌、李充、张征”三人的段落（必须同段同时出现）。
硬性要求：
1) 先输出 search_keywords。
2) 必须返回“全部命中”，不允许只给前几条；如果结果较多，请按“第X页/共Y页”分页展示。
3) 每条结果字段固定为：章节号、段落号、命中原文、命中关键词列表。
4) 末尾输出：总命中数、是否存在重复段落、是否存在疑似漏召回（给出判断理由）。
5) 若无命中，必须输出“无命中”并给出你实际执行过的关键词组合。"""

PROMPT_4 = """你是设定抽取器。请抽取当前文本里所有“器灵结构化条目”并做一致性检查。
目标条目包括：器物、器灵等阶、吞噬要求、吞噬效果。
要求：
1) 先输出 search_keywords（必须包含“器灵等阶/吞噬要求/吞噬效果/牛尾刀/五虎群羊刀”）。
2) 把所有命中段落按“条目组”归并，输出为表格：条目ID、器物、等阶、要求、效果、来源（章节+段落号）。
3) 不允许合并近义句，不允许改写术语。
4) 进行一致性检查：同一器物是否出现多版本；若有冲突，列出冲突证据对。
5) 输出最终结论：当前文本中“可吞噬前提”和“实际吞噬发生”是否一致。"""

PROMPT_5 = """请做一次“反向事实校验”：
命题A：段融在第3章已经明确突破精神力2级，并再次吞噬了二阶器灵。
任务：判断命题A真伪，并给出反证链。
要求：
1) 先输出 search_keywords（至少8个，含“精神力2级”“未满足”“吞噬”“第3章”）。
2) 给出所有支持A的证据（如果没有就明确写“无”）。
3) 给出所有反驳A的证据，必须逐条定位到章节+段落号并附短引。
4) 输出结论：真/假/证据不足，并说明是“直接反证”还是“缺失证据导致不成立”。
5) 最后追加“若要把A变成真，文本最少还缺哪一类信息”。"""


PROMPT_CASES: List[PromptCase] = [
    PromptCase("P1", "器灵等阶悖论自洽性", PROMPT_1, _validate_case_1),
    PromptCase("P2", "擦刀到千悟因果线", PROMPT_2, _validate_case_2),
    PromptCase("P3", "三人同段全量命中", PROMPT_3, _validate_case_3),
    PromptCase("P4", "器灵结构化抽取一致性", PROMPT_4, _validate_case_4),
    PromptCase("P5", "命题A反向事实校验", PROMPT_5, _validate_case_5),
]


def _join_url(base_url: str, path: str) -> str:
    return base_url.rstrip("/") + path


def login_get_token(client: httpx.Client, base_url: str, username: str, password: str, timeout: float) -> str:
    url = _join_url(base_url, "/api/v1/auth/login")
    payload = {"username": username, "password": password, "remember_me": False}
    resp = client.post(url, json=payload, timeout=timeout)
    if resp.status_code >= 400:
        raise RuntimeError(f"登录失败: status={resp.status_code}, body={resp.text[:300]}")
    data = resp.json()
    token = data.get("access_token")
    if not token:
        raise RuntimeError("登录成功但未返回 access_token")
    return token


def _extract_content_piece(event: Dict[str, Any]) -> str:
    piece = event.get("data", event.get("content", ""))
    if isinstance(piece, dict):
        if isinstance(piece.get("content"), str):
            return piece.get("content", "")
        if isinstance(piece.get("text"), str):
            return piece.get("text", "")
        return ""
    if piece is None:
        return ""
    return str(piece)


def stream_chat_once(
    client: httpx.Client,
    base_url: str,
    token: str,
    payload: Dict[str, Any],
    timeout: float,
) -> Tuple[str, Optional[str], int, Optional[str]]:
    url = _join_url(base_url, "/api/v1/agent/chat/stream")
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    chunks: List[str] = []
    conversation_id: Optional[str] = None
    event_count = 0
    request_error: Optional[str] = None

    with client.stream("POST", url, json=payload, headers=headers, timeout=timeout) as resp:
        if resp.status_code >= 400:
            raise RuntimeError(f"请求失败: status={resp.status_code}, body={resp.text[:500]}")

        for raw_line in resp.iter_lines():
            if not raw_line:
                continue
            line = raw_line.decode("utf-8", errors="replace") if isinstance(raw_line, bytes) else str(raw_line)
            if not line.startswith("data: "):
                continue
            data_str = line[6:].strip()
            if not data_str or data_str == "[DONE]":
                continue

            try:
                event = json.loads(data_str)
            except json.JSONDecodeError:
                continue

            event_count += 1
            if not conversation_id and isinstance(event, dict):
                conversation_id = event.get("conversation_id")

            etype = event.get("type")
            if etype == "content":
                piece = _extract_content_piece(event)
                if piece:
                    chunks.append(piece)
            elif etype == "error":
                request_error = (
                    event.get("error")
                    or event.get("message")
                    or str(event.get("data") or "")
                )
            elif etype == "done":
                break

    return "".join(chunks).strip(), conversation_id, event_count, request_error


def run_cases(args: argparse.Namespace) -> Tuple[List[CaseResult], Dict[str, Any]]:
    client = httpx.Client()
    try:
        token = args.token
        if not token:
            if not args.username or not args.password:
                raise RuntimeError("未提供 token，且缺少 username/password")
            token = login_get_token(
                client=client,
                base_url=args.base_url,
                username=args.username,
                password=args.password,
                timeout=args.timeout,
            )

        material_hint = ""
        if args.material_path:
            material_hint = f"\n素材路径（供你理解任务背景）：{args.material_path}"

        results: List[CaseResult] = []
        overall_pass = True

        for case in PROMPT_CASES:
            message = case.prompt + material_hint
            payload = {
                "message": message,
                "work_id": args.work_id,
                "chapter_id": args.chapter_id,
                "conversation_id": None,  # 每条用独立会话，避免上下文串扰
                "context": {
                    "test_mode": "complex_prompt_validation",
                    "prompt_case_id": case.case_id,
                    "tool_policy": args.tool_policy,
                },
                "tool_policy": args.tool_policy,
            }
            output_text = ""
            conversation_id = None
            raw_event_count = 0
            request_error = None
            validation_errors: List[str] = []

            try:
                output_text, conversation_id, raw_event_count, request_error = stream_chat_once(
                    client=client,
                    base_url=args.base_url,
                    token=token,
                    payload=payload,
                    timeout=args.timeout,
                )
                if request_error:
                    validation_errors.append(f"流式返回错误事件: {request_error}")
                if not output_text:
                    validation_errors.append("未收到最终内容（content为空）")
                else:
                    validation_errors.extend(case.validator(output_text))
            except Exception as exc:
                validation_errors.append(f"请求异常: {exc}")

            passed = len(validation_errors) == 0
            if args.strict and not passed:
                overall_pass = False
            elif not args.strict and request_error:
                overall_pass = False

            results.append(
                CaseResult(
                    case_id=case.case_id,
                    title=case.title,
                    passed=passed,
                    errors=validation_errors,
                    output_preview=(output_text[:240] + "...") if len(output_text) > 240 else output_text,
                    output_chars=len(output_text),
                    conversation_id=conversation_id,
                    raw_event_count=raw_event_count,
                    request_error=request_error,
                )
            )

        summary = {
            "base_url": args.base_url,
            "work_id": args.work_id,
            "chapter_id": args.chapter_id,
            "strict": args.strict,
            "tool_policy": args.tool_policy,
            "total_cases": len(results),
            "passed_cases": sum(1 for r in results if r.passed),
            "failed_cases": sum(1 for r in results if not r.passed),
            "overall_pass": overall_pass and all(r.passed for r in results),
        }
        return results, summary
    finally:
        client.close()


def print_report(results: List[CaseResult], summary: Dict[str, Any]) -> None:
    print("=" * 72)
    print("[复杂Prompt验收] 结果摘要")
    print("=" * 72)
    print(
        f"base_url={summary['base_url']} work_id={summary['work_id']} chapter_id={summary['chapter_id']}"
    )
    print(
        f"strict={summary['strict']} total={summary['total_cases']} pass={summary['passed_cases']} fail={summary['failed_cases']}"
    )
    print("-" * 72)
    for r in results:
        status = "PASS" if r.passed else "FAIL"
        print(f"[{status}] {r.case_id} {r.title}")
        print(
            f"  output_chars={r.output_chars} events={r.raw_event_count} conversation_id={r.conversation_id}"
        )
        if r.errors:
            for err in r.errors:
                print(f"  - {err}")
        if r.output_preview:
            print(f"  preview: {r.output_preview}")
    print("-" * 72)
    print(f"overall_pass={summary['overall_pass']}")
    print("=" * 72)


def save_json_report(args: argparse.Namespace, results: List[CaseResult], summary: Dict[str, Any]) -> Path:
    report_path = Path(args.report_path).resolve()
    report_path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "summary": summary,
        "results": [asdict(r) for r in results],
    }
    report_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return report_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate 5 complex prompts via agent SSE API")
    parser.add_argument("--base-url", default="http://localhost:8000", help="后端地址")
    parser.add_argument("--token", default="", help="Bearer token（优先）")
    parser.add_argument("--username", default="", help="登录用户名（未提供 token 时使用）")
    parser.add_argument("--password", default="", help="登录密码（未提供 token 时使用）")
    parser.add_argument("--work-id", default="", help="作品ID（建议必填）")
    parser.add_argument("--chapter-id", default="", help="章节ID（可选）")
    parser.add_argument("--material-path", default="", help="素材路径（仅作为提示附加到 prompt）")
    parser.add_argument(
        "--tool-policy",
        default="auto",
        choices=["auto", "no_tool", "cache_only"],
        help="工具策略",
    )
    parser.add_argument("--timeout", type=float, default=300.0, help="单次请求超时（秒）")
    parser.add_argument("--strict", action="store_true", help="严格模式：任一规则失败即总失败")
    parser.add_argument(
        "--report-path",
        default="backend/log/complex_prompt_validation_report.json",
        help="JSON报告输出路径",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if not args.work_id:
        print("[WARN] 未传 work_id，模型可能无法基于目标小说检索，建议补充 --work-id。")

    try:
        results, summary = run_cases(args)
    except Exception as exc:
        print(f"[ERROR] 执行失败: {exc}")
        return 2

    print_report(results, summary)
    report_file = save_json_report(args, results, summary)
    print(f"[INFO] 报告已写入: {report_file}")
    return 0 if summary["overall_pass"] else 1


if __name__ == "__main__":
    sys.exit(main())
