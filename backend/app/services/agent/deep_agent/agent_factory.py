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
from typing import Any

from langchain_openai import ChatOpenAI

from app.core.config import settings
from app.services.agent.deep_agent import DATA_ROOT
from app.services.agent.deep_agent.buffered_backend import BufferedFilesystemBackend
from app.services.agent.deep_agent.prompts import build_system_prompt
from app.services.agent.deep_agent.rag_tool import create_semantic_search_tool

logger = logging.getLogger(__name__)

SKILLS_ROOT = Path(__file__).parent.parent / "skills"

# Skills 分组目录名（与 skills/ 下的子目录对应）
_SKILL_GROUPS = [
    "core", "character", "structure", "craft",
    "worldbuilding",
]


def _get_work_dir(user_id: str, work_id: str) -> Path:
    """获取作品工作目录路径。"""
    return DATA_ROOT / user_id / "works" / work_id


def _sync_skills_to_work_dir(work_dir: Path) -> list[str]:
    """将完整 skill 目录同步到 work_dir/skills/，供 SkillsMiddleware 读取。

    复制 SKILL.md 及其同级的 scripts/、references/、templates/、data/ 等资源。
    跳过已存在且内容相同的文件。

    Returns:
        可用的 skills 源路径列表（相对于 backend root，POSIX 格式）
    """
    if not SKILLS_ROOT.is_dir():
        logger.warning("Skills source directory not found: %s", SKILLS_ROOT)
        return []

    dest_skills = work_dir / "skills"
    sources: list[str] = []

    for group in _SKILL_GROUPS:
        src_group = SKILLS_ROOT / group
        if not src_group.is_dir():
            continue

        dst_group = dest_skills / group
        # 复制每个 skill 目录下的所有文件（不仅是 SKILL.md）
        for src_file in src_group.rglob("*"):
            if src_file.is_dir():
                continue
            # 跳过隐藏文件和 __pycache__
            if any(part.startswith('.') or part == '__pycache__' for part in src_file.parts):
                continue
            rel = src_file.relative_to(src_group)
            dst_file = dst_group / rel
            if dst_file.exists() and dst_file.read_bytes() == src_file.read_bytes():
                continue
            dst_file.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src_file, dst_file)

        sources.append(f"/skills/{group}/")

    return sources


def create_writing_agent(
    work,
    user_id: str,
    checkpointer: Any = None,
    callbacks: list | None = None,
) -> tuple[Any, BufferedFilesystemBackend]:
    """创建写作 Agent。

    Args:
        work: Work ORM 实例
        user_id: 用户 ID（字符串）
        checkpointer: LangGraph checkpointer（可选）
        callbacks: LLM instance-level callbacks（可选，用于 token 统计）

    Returns:
        (agent, backend) 元组
        - agent: CompiledStateGraph，可调用 astream_events
        - backend: BufferedFilesystemBackend，用于审批操作
    """
    from deepagents import create_deep_agent

    work_id = str(work.id)
    work_dir = _get_work_dir(user_id, work_id)
    work_dir.mkdir(parents=True, exist_ok=True)

    # 1. 同步 Skills 到 work_dir（供 SkillsMiddleware 渐进披露）
    skill_sources = _sync_skills_to_work_dir(work_dir)

    # 2. 创建缓冲后端
    backend = BufferedFilesystemBackend(root_dir=str(work_dir))

    # 3. 构建 system prompt
    system_prompt = build_system_prompt(work)

    # 4. 创建语义搜索工具
    search_tool = create_semantic_search_tool(work_id)

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
        tools=[search_tool],
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
