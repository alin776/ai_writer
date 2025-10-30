"""
HITL与LangGraph集成

提供LangGraph中使用HITL的便捷方法
"""

from typing import Dict, Any, Optional, Callable
from .hitl import HITLManager, ApprovalRequest, ApprovalResponse, ApprovalStatus


class HITLNode:
    """
    HITL节点包装器
    可以在LangGraph工作流中插入人工批准点
    """

    def __init__(self, hitl_manager: HITLManager):
        """
        初始化HITL节点

        Args:
            hitl_manager: HITL管理器实例
        """
        self.hitl = hitl_manager

    def create_approval_node(
        self,
        title_fn: Callable[[Dict[str, Any]], str],
        description_fn: Callable[[Dict[str, Any]], str],
        action_fn: Callable[[Dict[str, Any]], Dict[str, Any]],
        alternatives_fn: Optional[Callable[[Dict[str, Any]], list]] = None
    ):
        """
        创建一个需要批准的节点函数

        Args:
            title_fn: 生成标题的函数
            description_fn: 生成描述的函数
            action_fn: 生成建议操作的函数
            alternatives_fn: 生成备选方案的函数（可选）

        Returns:
            Callable: 可用于LangGraph的节点函数
        """

        async def approval_node(state: Dict[str, Any]) -> Dict[str, Any]:
            """
            批准节点

            Args:
                state: LangGraph状态

            Returns:
                Dict: 更新后的状态
            """
            user_id = state.get("user_id")
            agent_id = state.get("agent_id", "default")

            # 生成批准请求内容
            title = title_fn(state)
            description = description_fn(state)
            proposed_action = action_fn(state)
            alternatives = alternatives_fn(state) if alternatives_fn else []

            # 创建批准请求
            request = self.hitl.create_approval_request(
                agent_id=agent_id,
                user_id=user_id,
                title=title,
                description=description,
                proposed_action=proposed_action,
                alternatives=alternatives,
                context=state.get("context", {}),
                checkpoint_data=state
            )

            # 更新状态
            state["pending_approval"] = request.request_id
            state["approval_required"] = True

            return state

        return approval_node

    def create_resume_node(self):
        """
        创建恢复执行的节点

        Returns:
            Callable: 可用于LangGraph的节点函数
        """

        async def resume_node(state: Dict[str, Any]) -> Dict[str, Any]:
            """
            恢复执行节点

            Args:
                state: LangGraph状态

            Returns:
                Dict: 更新后的状态
            """
            request_id = state.get("pending_approval")

            if not request_id:
                # 没有待批准请求，直接返回
                return state

            # 等待批准
            try:
                response = await self.hitl.wait_for_approval(request_id)

                if response.status == ApprovalStatus.APPROVED:
                    # 批准，使用原计划
                    state["approval_required"] = False
                    state["approved_action"] = state.get("proposed_action")

                elif response.status == ApprovalStatus.MODIFIED:
                    # 修改后批准，使用修改后的计划
                    state["approval_required"] = False
                    state["approved_action"] = response.modifications

                elif response.status == ApprovalStatus.REJECTED:
                    # 拒绝，需要重新规划
                    state["approval_required"] = False
                    state["rejection_reason"] = response.feedback
                    state["need_replan"] = True

                state["user_feedback"] = response.feedback

            except TimeoutError:
                # 超时
                state["approval_timeout"] = True
                state["approval_required"] = False

            return state

        return resume_node

    def create_conditional_hitl(
        self,
        condition_fn: Callable[[Dict[str, Any]], bool],
        **approval_kwargs
    ):
        """
        创建条件性的HITL节点
        只有满足条件时才需要批准

        Args:
            condition_fn: 判断是否需要批准的函数
            **approval_kwargs: 传递给create_approval_node的参数

        Returns:
            Callable: 节点函数
        """
        approval_node = self.create_approval_node(**approval_kwargs)

        async def conditional_node(state: Dict[str, Any]) -> Dict[str, Any]:
            """条件性批准节点"""
            if condition_fn(state):
                # 需要批准
                return await approval_node(state)
            else:
                # 不需要批准，直接继续
                state["approval_required"] = False
                return state

        return conditional_node


# ==================== 便捷函数 ====================

def create_outline_approval_node(hitl_manager: HITLManager):
    """
    创建大纲批准节点

    Args:
        hitl_manager: HITL管理器

    Returns:
        Callable: 大纲批准节点函数
    """
    hitl_node = HITLNode(hitl_manager)

    return hitl_node.create_approval_node(
        title_fn=lambda state: "大纲生成完成，请确认",
        description_fn=lambda state: f"我已经为您生成了{len(state.get('outline', []))}章的大纲，请查看是否符合您的预期。",
        action_fn=lambda state: {
            "type": "create_outline",
            "outline": state.get("outline", [])
        },
        alternatives_fn=lambda state: [
            {"type": "regenerate", "prompt": "重新生成更详细的大纲"},
            {"type": "regenerate", "prompt": "重新生成更简洁的大纲"}
        ]
    )


def create_worldview_approval_node(hitl_manager: HITLManager):
    """
    创建世界观批准节点

    Args:
        hitl_manager: HITL管理器

    Returns:
        Callable: 世界观批准节点函数
    """
    hitl_node = HITLNode(hitl_manager)

    return hitl_node.create_approval_node(
        title_fn=lambda state: "世界观设定完成，请确认",
        description_fn=lambda state: "我已经为您设定了小说的世界观，包括背景、设定等，请查看是否需要调整。",
        action_fn=lambda state: {
            "type": "create_worldview",
            "worldview": state.get("worldview", {})
        }
    )


def create_character_approval_node(hitl_manager: HITLManager):
    """
    创建角色批准节点

    Args:
        hitl_manager: HITL管理器

    Returns:
        Callable: 角色批准节点函数
    """
    hitl_node = HITLNode(hitl_manager)

    return hitl_node.create_approval_node(
        title_fn=lambda state: f"角色「{state.get('character_name', '未命名')}」创建完成",
        description_fn=lambda state: "我已经为您创建了角色卡片，请查看是否符合您的预期。",
        action_fn=lambda state: {
            "type": "create_character",
            "character": state.get("character", {})
        }
    )


def create_batch_operation_approval_node(hitl_manager: HITLManager):
    """
    创建批量操作批准节点

    Args:
        hitl_manager: HITL管理器

    Returns:
        Callable: 批量操作批准节点函数
    """
    hitl_node = HITLNode(hitl_manager)

    return hitl_node.create_approval_node(
        title_fn=lambda state: f"批量操作：{state.get('batch_operation_type', '未知操作')}",
        description_fn=lambda state: f"即将对{state.get('batch_count', 0)}个项目执行批量操作，请确认。",
        action_fn=lambda state: {
            "type": "batch_operation",
            "operation": state.get("batch_operation_type"),
            "targets": state.get("batch_targets", [])
        }
    )
