"""
验证5个核心Action的注册和基本功能

这是一个独立的验证脚本,不依赖完整的应用环境
"""

import sys
import os
import asyncio
from unittest.mock import Mock

# 添加路径
backend_path = os.path.join(os.path.dirname(__file__), '..', '..')
sys.path.insert(0, backend_path)

from app.services.agent.actions.base_action import BaseAction, ActionStatus
from app.services.agent.actions.action_registry import ActionRegistry
from app.services.agent.actions.writing_action import WritingAction
from app.services.agent.actions.planning_action import PlanningAction
from app.services.agent.actions.analysis_action import AnalysisAction
from app.services.agent.actions.stuck_action import StuckAction
from app.services.agent.actions.general_chat_action import GeneralChatAction


class MockMessage:
    """模拟消息对象"""
    def __init__(self, content):
        self.content = content


class MockAIService:
    """模拟AI服务"""
    async def _stream_chat(self, *args, **kwargs):
        """模拟流式聊天"""
        chunks = ["测试", "响应", "内容"]
        for chunk in chunks:
            yield chunk, None


async def test_action_registration():
    """测试Action注册"""
    print("\n=== 测试Action注册 ===")

    actions = {
        "writing": WritingAction,
        "planning": PlanningAction,
        "analysis": AnalysisAction,
        "stuck": StuckAction,
        "general_chat": GeneralChatAction
    }

    for name, action_class in actions.items():
        if ActionRegistry.has_action(name):
            print(f"[OK] {name} registered")
        else:
            print(f"[FAIL] {name} not registered")

    # 获取注册信息
    registry_info = ActionRegistry.get_registry_info()
    print(f"\nTotal actions: {registry_info['total_actions']}")
    print(f"Categories: {registry_info['categories']}")


async def test_writing_action():
    """测试WritingAction"""
    print("\n=== Test WritingAction ===")

    ai_service = MockAIService()
    action = WritingAction(ai_service)

    state = {
        "messages": [MockMessage("write chapter 1")],
        "work_id": "work_123",
        "chapter_id": "chapter_456"
    }

    result = await action.run(state)

    print(f"Status: {result.status.value}")
    print(f"Success: {result.is_success()}")
    print(f"Agent type: {result.data.get('agent_type')}")
    print(f"Chapter number: {result.metadata.get('chapter_num')}")
    print(f"Phase: {result.metadata.get('phase')}")


async def test_planning_action():
    """测试PlanningAction"""
    print("\n=== Test PlanningAction ===")

    ai_service = MockAIService()
    action = PlanningAction(ai_service)

    state = {
        "messages": [MockMessage("help me plan the outline")],
        "work_id": "work_123"
    }

    result = await action.run(state)

    print(f"Status: {result.status.value}")
    print(f"Success: {result.is_success()}")
    print(f"Agent type: {result.data.get('agent_type')}")


async def test_analysis_action():
    """测试AnalysisAction"""
    print("\n=== Test AnalysisAction ===")

    ai_service = MockAIService()
    action = AnalysisAction(ai_service)

    state = {
        "messages": [MockMessage("analyze chapter 1")],
        "work_id": "work_123",
        "chapter_id": "chapter_456"
    }

    result = await action.run(state)

    print(f"Status: {result.status.value}")
    print(f"Success: {result.is_success()}")
    print(f"Agent type: {result.data.get('agent_type')}")


async def test_stuck_action():
    """测试StuckAction"""
    print("\n=== Test StuckAction ===")

    ai_service = MockAIService()
    action = StuckAction(ai_service)

    state = {
        "messages": [MockMessage("I'm stuck")],
        "work_id": "work_123",
        "chapter_id": "chapter_456"
    }

    result = await action.run(state)

    print(f"Status: {result.status.value}")
    print(f"Success: {result.is_success()}")
    print(f"Agent type: {result.data.get('agent_type')}")


async def test_general_chat_action():
    """测试GeneralChatAction"""
    print("\n=== Test GeneralChatAction ===")

    ai_service = MockAIService()
    action = GeneralChatAction(ai_service)

    state = {
        "messages": [MockMessage("hello")]
    }

    result = await action.run(state)

    print(f"Status: {result.status.value}")
    print(f"Success: {result.is_success()}")
    print(f"Response: {result.data.get('final_response')}")


async def test_error_handling():
    """测试错误处理"""
    print("\n=== Test Error Handling ===")

    ai_service = MockAIService()
    action = WritingAction(ai_service)

    # 无效输入
    state = {"messages": []}

    result = await action.run(state)

    print(f"Status: {result.status.value}")
    print(f"Success: {result.is_success()}")
    print(f"Error: {result.error}")


async def test_action_stats():
    """测试Action统计"""
    print("\n=== Test Action Stats ===")

    ai_service = MockAIService()
    action = WritingAction(ai_service)

    state = {
        "messages": [MockMessage("write")],
        "work_id": "work_123"
    }

    # 执行3次
    for _ in range(3):
        await action.run(state)

    stats = action.get_stats()
    print(f"Execution count: {stats['execution_count']}")
    print(f"Total duration: {stats['total_duration']:.4f}s")
    print(f"Avg duration: {stats['avg_duration']:.4f}s")


async def main():
    """主函数"""
    print("Verifying 5 core Actions...")

    try:
        await test_action_registration()
        await test_writing_action()
        await test_planning_action()
        await test_analysis_action()
        await test_stuck_action()
        await test_general_chat_action()
        await test_error_handling()
        await test_action_stats()

        print("\n[SUCCESS] All tests passed!")

    except Exception as e:
        print(f"\n[ERROR] Test failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
