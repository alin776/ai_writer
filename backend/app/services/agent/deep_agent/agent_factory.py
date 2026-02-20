"""
Agent 工厂函数

组装 DeepAgents 写作 Agent 的全部组件：
- BufferedFilesystemBackend（缓冲写入）
- System Prompt（领域指导）
- RAG 语义搜索 Tool
- LLM（ChatOpenAI 实例）
"""

import logging
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
from app.services.knowledge_templates import ensure_knowledge_templates

logger = logging.getLogger(__name__)

SKILLS_ROOT = Path(__file__).parent.parent / "skills"
WORK_SKILLS_DIR = ".skills"
DEFAULT_SKILL_SETS = ("quality", "review", "statistics", "process")


def _get_work_dir(user_id: str, work_id: str) -> Path:
    """获取作品工作目录路径。"""
    return DATA_ROOT / user_id / "works" / work_id


def _sync_skills_to_work_dir(work_dir: Path) -> list[str]:
    """Copy built-in skills into the per-work sandbox and return virtual paths."""
    target_root = work_dir / WORK_SKILLS_DIR
    target_root.mkdir(parents=True, exist_ok=True)

    skill_paths: list[str] = []
    for skill_set in DEFAULT_SKILL_SETS:
        source_dir = SKILLS_ROOT / skill_set
        if not source_dir.exists():
            logger.warning("Skill source directory missing: %s", source_dir)
            continue

        copytree(source_dir, target_root / skill_set, dirs_exist_ok=True)
        # BufferedFilesystemBackend runs in virtual_mode, so skills must live inside root.
        skill_paths.append(f"/{WORK_SKILLS_DIR}/{skill_set}")

    return skill_paths


def create_writing_agent(
    work,
    user_id: str,
    checkpointer: Any = None,
) -> tuple[Any, BufferedFilesystemBackend]:
    """创建写作 Agent。

    Args:
        work: Work ORM 实例
        user_id: 用户 ID（字符串）
        checkpointer: LangGraph checkpointer（可选）

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

    # 1. 创建缓冲后端
    backend = BufferedFilesystemBackend(root_dir=str(work_dir))
    skill_paths = _sync_skills_to_work_dir(work_dir)

    # 2. 构建 system prompt
    system_prompt = build_system_prompt(work)

    # 3. 创建语义搜索工具
    search_tool = create_semantic_search_tool(work_id)
    file_ops_tools = create_file_ops_tools(backend)

    # 4. 构建 LLM（复用现有配置）
    llm = ChatOpenAI(
        model=settings.OPENAI_MODEL,
        api_key=settings.OPENAI_API_KEY,
        base_url=settings.OPENAI_BASE_URL,
        timeout=settings.OPENAI_TIMEOUT,
        use_responses_api=True,
    )

    # 5. 组装 Agent
    agent = create_deep_agent(
        model=llm,
        tools=[search_tool, *file_ops_tools],
        system_prompt=system_prompt,
        backend=backend,
        checkpointer=checkpointer,
        skills=skill_paths,
    )

    logger.info(
        "Created writing agent for work=%s user=%s dir=%s",
        work_id, user_id, work_dir,
    )

    return agent, backend
