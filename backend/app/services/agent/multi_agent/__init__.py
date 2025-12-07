"""Multi-Agent 写作系统

基于 5 角色协作的智能写作框架：
- 大纲师 (OutlineAgent): 生成章节大纲
- 主笔 (WriterAgent): 撰写内容
- 角色守护 (CharacterGuard): 检查角色一致性
- 逻辑审计 (LogicAuditor): 检查逻辑连贯性
- 总编 (EditorAgent): 最终修订和整合
"""

from .executor import MultiAgentExecutor, MULTI_AGENT_STAGES, TOTAL_STAGES

__all__ = ["MultiAgentExecutor", "MULTI_AGENT_STAGES", "TOTAL_STAGES"]
