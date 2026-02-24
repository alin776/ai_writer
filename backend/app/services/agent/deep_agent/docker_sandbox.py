"""
DockerSandbox — 持久 Docker 容器沙盒

在隔离的 Docker 容器内执行 Agent 的 shell 命令，提供安全沙箱。
采用「懒初始化 + sleep infinity」模式：首次 execute 时创建容器，
后续命令通过 docker exec 注入，避免每次冷启动。

安全措施：
- network_mode="none"  禁止网络访问
- mem_limit="512m"     内存上限
- cpu_quota=50000      50% 单核 CPU
- user="nobody"        非 root 运行
"""

import logging
import uuid
from shlex import quote as _shell_quote

from pathlib import Path

_logger = logging.getLogger(__name__)


class DockerSandbox:
    """持久 Docker 容器沙盒，管理容器生命周期。"""

    # 容器内数据目录前缀（与 docker-compose.prod.yml 的 bind mount 对应）
    _CONTAINER_DATA_PREFIX = "/app/data"

    def __init__(self, work_dir: Path, image: str = "python:3.11-slim",
                 host_data_root: str = ""):
        self._work_dir = work_dir
        self._image = image
        self._host_data_root = host_data_root  # DooD 模式：宿主机上 /app/data 对应的真实路径
        self._container = None  # docker.models.containers.Container
        self._client = None     # docker.DockerClient
        self._container_name = f"sandbox-{uuid.uuid4().hex[:8]}"

    def _resolve_host_path(self) -> str:
        """将容器内 work_dir 翻译为 Docker daemon 可见的宿主机路径。

        DooD 模式下，后端自身运行在容器内，work_dir 是容器内路径
        （如 /app/data/users/123/works/456）。
        但 Docker daemon 运行在宿主机上，需要宿主机真实路径才能挂载 volume。

        做法：将容器内前缀 /app/data 替换为 SANDBOX_HOST_DATA_ROOT。
        示例：/app/data/users/123/works/456
              → /home/deploy/wenshu/backend-data/users/123/works/456
        """
        if not self._host_data_root:
            return str(self._work_dir)

        work_str = str(self._work_dir).replace("\\", "/")
        prefix = self._CONTAINER_DATA_PREFIX

        if work_str.startswith(prefix):
            relative = work_str[len(prefix):]  # e.g. "/users/123/works/456"
            host_path = self._host_data_root.rstrip("/") + relative
            return host_path

        # fallback: work_dir 不以 /app/data 开头（不应该发生），直接返回并告警
        _logger.warning(
            "[DockerSandbox] work_dir 不以 %s 开头，无法做路径翻译: %s",
            prefix, work_str,
        )
        return work_str

    @property
    def container_name(self) -> str:
        return self._container_name

    def ensure_running(self) -> None:
        """懒初始化：首次调用时创建并启动容器。

        幂等——如果容器已在运行则直接返回。
        """
        if self._container is not None:
            try:
                self._container.reload()
                if self._container.status == "running":
                    return
                # 容器存在但非 running（exited/paused），强制删除防止同名冲突
                try:
                    self._container.remove(force=True)
                except Exception:
                    pass
            except Exception:
                pass  # 容器已消失
            self._container = None

        import docker

        if self._client is None:
            self._client = docker.from_env()

        # 兜底：清理可能残留的同名容器（进程崩溃恢复场景）
        try:
            stale = self._client.containers.get(self._container_name)
            stale.remove(force=True)
        except docker.errors.NotFound:
            pass
        except Exception:
            pass

        host_path = self._resolve_host_path()
        _logger.info(
            "[DockerSandbox] Creating container %s (image=%s, work_dir=%s, host_path=%s)",
            self._container_name, self._image, self._work_dir, host_path,
        )

        self._container = self._client.containers.run(
            image=self._image,
            command="sleep infinity",
            detach=True,
            name=self._container_name,

            # 文件系统：work_dir 挂载为 /workspace（DooD 时用宿主机路径）
            volumes={host_path: {"bind": "/workspace", "mode": "rw"}},
            working_dir="/workspace",

            # 网络隔离
            network_mode="none",

            # 资源限制
            mem_limit="512m",
            cpu_period=100000,
            cpu_quota=50000,  # 50% 单核

            # 用户权限
            user="nobody",

            # 标签（便于批量清理残留容器）
            labels={"app": "ai-writer", "type": "sandbox"},
        )

        _logger.info(
            "[DockerSandbox] Container %s started (id=%s)",
            self._container_name, self._container.short_id,
        )

    def run(self, command: str, timeout: int = 60) -> tuple[str, int]:
        """在容器内执行命令，返回 (output, exit_code)。

        通过 docker exec 在持久容器内执行 shell 命令。
        使用 coreutils timeout 包装命令实现超时控制，
        demux=True 分离 stdout/stderr 并给 stderr 加前缀。
        """
        self.ensure_running()

        # 用 timeout 命令包装，确保容器内进程不会无限挂起
        # exit code 124 = timeout killed
        wrapped = f"timeout {timeout} sh -c {_shell_quote(command)}"

        exec_result = self._container.exec_run(
            ["sh", "-c", wrapped],
            workdir="/workspace",
            demux=True,  # 返回 (stdout_bytes, stderr_bytes)
        )

        exit_code = exec_result.exit_code
        stdout_bytes, stderr_bytes = exec_result.output

        # 安全 decode：demux 模式下任一流可能为 None
        parts: list[str] = []
        if stdout_bytes:
            parts.append(stdout_bytes.decode("utf-8", errors="replace"))
        if stderr_bytes:
            for line in stderr_bytes.decode("utf-8", errors="replace").strip().split("\n"):
                parts.append(f"[stderr] {line}")

        output = "\n".join(parts) if parts else "<no output>"

        _logger.debug(
            "[DockerSandbox] exec exit_code=%d output_len=%d cmd=%s",
            exit_code, len(output), command[:80],
        )

        return output, exit_code

    def cleanup(self) -> None:
        """停止并删除容器。静默处理已不存在的容器。"""
        if self._container is not None:
            try:
                self._container.stop(timeout=5)
            except Exception:
                pass  # 容器可能已停止
            try:
                self._container.remove(force=True)
            except Exception:
                pass  # 容器可能已删除
            _logger.info("[DockerSandbox] Container %s cleaned up", self._container_name)
            self._container = None

        if self._client is not None:
            try:
                self._client.close()
            except Exception:
                pass
            self._client = None

    @staticmethod
    def cleanup_stale_containers() -> int:
        """清理所有带 ai-writer sandbox 标签的残留容器（应用启动时调用）。

        用于处理服务器崩溃/重启后遗留的孤儿容器。
        """
        try:
            import docker
            client = docker.from_env()
            stale = client.containers.list(
                all=True,
                filters={"label": ["app=ai-writer", "type=sandbox"]},
            )
            count = len(stale)
            for c in stale:
                try:
                    c.remove(force=True)
                    _logger.info("[DockerSandbox] Cleaned stale container: %s", c.name)
                except Exception:
                    pass
            client.close()
            return count
        except Exception as e:
            _logger.debug("[DockerSandbox] cleanup_stale_containers skipped: %s", e)
            return 0
