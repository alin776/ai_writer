"""Multi-Agent Prompt 模板"""

from .outline_prompt import OUTLINE_PROMPT
from .writer_prompt import WRITER_PROMPT
from .character_guard_prompt import CHARACTER_GUARD_PROMPT
from .logic_auditor_prompt import LOGIC_AUDITOR_PROMPT
from .editor_prompt import EDITOR_PROMPT

__all__ = [
    "OUTLINE_PROMPT",
    "WRITER_PROMPT",
    "CHARACTER_GUARD_PROMPT",
    "LOGIC_AUDITOR_PROMPT",
    "EDITOR_PROMPT",
]
