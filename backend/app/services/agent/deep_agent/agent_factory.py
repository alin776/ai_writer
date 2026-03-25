"""
Agent 工厂函数

组装 DeepAgents 写作 Agent 的全部组件：
- BufferedFilesystemBackend（缓冲写入）
- System Prompt（领域指导）
- RAG 语义搜索 Tool
- LLM（ChatOpenAI 实例）
- Skills（技能系统，复制到 work_dir 供 SkillsMiddleware 渐进披露）
"""

import logging
import shutil
from pathlib import Path
from shutil import copytree
from typing import Any

from langchain_openai import ChatOpenAI

from app.core.config import settings
from app.services.agent.deep_agent import DATA_ROOT
from app.services.agent.deep_agent.buffered_backend import BufferedFilesystemBackend
from app.services.agent.deep_agent.file_ops_tools import create_file_ops_tools
from app.services.agent.deep_agent.prompts import build_system_prompt
from app.services.agent.deep_agent.rag_tool import create_semantic_search_tool
from app.services.agent.deep_agent.web_tools import create_web_tools
from app.services.knowledge_templates import ensure_knowledge_templates

logger = logging.getLogger(__name__)

SKILLS_ROOT = Path(__file__).parent.parent / "skills"
WORK_SKILLS_DIR = ".skills"
DEFAULT_SKILL_SETS = ("quality", "review", "statistics", "process")

# Skills 分组目录名（与 skills/ 下的子目录对应）
_SKILL_GROUPS = [
    "core", "character", "structure", "craft",
    "worldbuilding", "application", "chinese-novel",
]


def _get_work_dir(user_id: str, work_id: str) -> Path:
    """获取作品工作目录路径。"""
    return DATA_ROOT / user_id / "works" / work_id


def _sync_skills_to_work_dir(
    work_dir: Path,
    enabled_skills: list[str] | None = None,
) -> list[str]:
    """将 skill 目录同步到 work_dir/skills/，供 SkillsMiddleware 读取。

    复制 SKILL.md 及其同级的 scripts/、references/、templates/、data/ 等资源。
    跳过已存在且内容相同的文件。

    Args:
        work_dir: 作品工作目录
        enabled_skills: 用户启用的 skill 名称列表。为 None 时复制全部（兼容旧逻辑）。

    Returns:
        可用的 skills 源路径列表（相对于 backend root，POSIX 格式）
    """
    if not SKILLS_ROOT.is_dir():
        logger.warning("Skills source directory not found: %s", SKILLS_ROOT)
        return []

    enabled_set = set(enabled_skills) if enabled_skills is not None else None
    dest_skills = work_dir / "skills"
    sources: list[str] = []
    found_names: set[str] = set()  # 跟踪磁盘上实际存在的 skill 目录名

    for group in _SKILL_GROUPS:
        src_group = SKILLS_ROOT / group
        if not src_group.is_dir():
            continue

        dst_group = dest_skills / group
        has_any = False

        for skill_dir in src_group.iterdir():
            if not skill_dir.is_dir() or skill_dir.name.startswith('.'):
                continue
            found_names.add(skill_dir.name)

            # 按 enabled_skills 过滤：只同步启用的 skill
            if enabled_set is not None and skill_dir.name not in enabled_set:
                # 清理 work_dir 中已存在但被禁用的 skill 目录
                dst_skill = dst_group / skill_dir.name
                if dst_skill.exists():
                    shutil.rmtree(dst_skill)
                continue

            has_any = True
            # 复制该 skill 目录下的所有文件
            for src_file in skill_dir.rglob("*"):
                if src_file.is_dir():
                    continue
                if any(part.startswith('.') or part == '__pycache__' for part in src_file.parts):
                    continue
                rel = src_file.relative_to(src_group)
                dst_file = dst_group / rel
                if dst_file.exists() and dst_file.read_bytes() == src_file.read_bytes():
                    continue
                dst_file.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src_file, dst_file)

        if has_any:
            sources.append(f"/skills/{group}/")
        elif enabled_set is not None and dst_group.exists():
            # 该 group 下所有 skill 都被禁用，清理残留的 group 目录
            shutil.rmtree(dst_group)

    # 警告：enabled_skills 中包含磁盘上不存在的 skill 名称（可能是拼写错误）
    if enabled_set is not None:
        unfound = enabled_set - found_names
        if unfound:
            logger.warning("Enabled skills not found on disk: %s", sorted(unfound))

    return sources


def create_writing_agent(
    work,
    user_id: str,
    checkpointer: Any = None,
    callbacks: list | None = None,
    enabled_skills: list[str] | None = None,
) -> tuple[Any, BufferedFilesystemBackend]:
    """创建写作 Agent。

    Args:
        work: Work ORM 实例
        user_id: 用户 ID（字符串）
        checkpointer: LangGraph checkpointer（可选）
        callbacks: LLM instance-level callbacks（可选，用于 token 统计）
        enabled_skills: 用户启用的 skill 名称列表（可选，None 表示全部启用）

    Returns:
        (agent, backend) 元组
        - agent: CompiledStateGraph，可调用 astream_events
        - backend: BufferedFilesystemBackend，用于审批操作
    """
    from deepagents import create_deep_agent

    work_id = str(work.id)
    work_dir = _get_work_dir(user_id, work_id)
    work_dir.mkdir(parents=True, exist_ok=True)
    try:
        ensure_knowledge_templates(work_dir)
    except Exception as exc:
        # Best effort: do not block agent startup if template bootstrap fails.
        logger.warning("Init knowledge templates skipped for work=%s: %s", work_id, exc)

    # 1. 同步 Skills 到 work_dir（仅启用的 skill，供 SkillsMiddleware 渐进披露）
    skill_sources = _sync_skills_to_work_dir(work_dir, enabled_skills=enabled_skills)

    # 2. 创建缓冲后端
    backend = BufferedFilesystemBackend(
        root_dir=str(work_dir),
        use_docker=settings.SANDBOX_USE_DOCKER,
        docker_image=settings.SANDBOX_DOCKER_IMAGE,
        host_data_root=settings.SANDBOX_HOST_DATA_ROOT,
    )

    # 3. 构建 system prompt
    system_prompt = build_system_prompt(work)

    # 4. 创建语义搜索工具
    search_tool = create_semantic_search_tool(work_id)
    file_ops_tools = create_file_ops_tools(backend)
    web_tools = create_web_tools(
        tavily_api_key=settings.TAVILY_API_KEY,
        jina_api_key=settings.JINA_API_KEY,
    )

    # 5. 构建 LLM（复用现有配置）
    llm = ChatOpenAI(
        model=settings.OPENAI_MODEL,
        api_key=settings.OPENAI_API_KEY,
        base_url=settings.OPENAI_BASE_URL,
        timeout=settings.OPENAI_TIMEOUT,
        use_responses_api=True,
        **({"callbacks": callbacks} if callbacks else {}),
    )

    # 6. 组装 Agent（skills 使用相对路径，在 backend 沙箱内可达）
    agent = create_deep_agent(
        model=llm,
        tools=[search_tool, *file_ops_tools, *web_tools],
        system_prompt=system_prompt,
        backend=backend,
        checkpointer=checkpointer,
        skills=skill_sources if skill_sources else None,
    )

    logger.info(
        "Created writing agent for work=%s user=%s dir=%s skills=%s",
        work_id, user_id, work_dir, skill_sources,
    )

    return agent, backend
