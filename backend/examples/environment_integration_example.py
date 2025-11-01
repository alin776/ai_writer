"""
Environment层集成示例
展示如何在LangGraph中使用MessageBus和StateManager
"""

import asyncio
from typing import Dict, Any
from app.services.agent.environment import (
    get_message_bus,
    Message,
    MessageType,
    StateManager
)
from app.services.agent.actions import ActionStatus


class EnvironmentIntegrationExample:
    """Environment层集成示例"""

    def __init__(self, redis_client=None):
        """
        初始化示例

        Args:
            redis_client: 可选的Redis客户端
        """
        # 获取全局消息总线
        self.message_bus = get_message_bus()

        # 创建状态管理器
        self.state_manager = StateManager(redis_client=redis_client)

        # 设置消息订阅
        self._setup_message_subscribers()

    def _setup_message_subscribers(self):
        """设置消息订阅"""

        # 订阅Action开始事件
        async def on_action_started(msg: Message):
            print(f"[事件] Action开始: {msg.content.get('action')}")

        # 订阅Action完成事件
        async def on_action_completed(msg: Message):
            print(f"[事件] Action完成: {msg.content.get('action')}, "
                  f"状态: {msg.content.get('status')}")

        # 订阅Action失败事件
        async def on_action_failed(msg: Message):
            print(f"[事件] Action失败: {msg.content.get('action')}, "
                  f"错误: {msg.content.get('error')}")

        self.message_bus.subscribe(
            MessageType.ACTION_STARTED.value,
            on_action_started
        )
        self.message_bus.subscribe(
            MessageType.ACTION_COMPLETED.value,
            on_action_completed
        )
        self.message_bus.subscribe(
            MessageType.ACTION_FAILED.value,
            on_action_failed
        )

    async def simulate_writing_action(self, conversation_id: str):
        """
        模拟写作Action的执行流程

        展示:
        1. 发布Action开始事件
        2. 使用StateManager管理状态
        3. 执行Action逻辑
        4. 发布Action完成事件
        """
        action_name = "writing"

        # 1. 发布Action开始事件
        await self.message_bus.publish(Message(
            topic=MessageType.ACTION_STARTED.value,
            sender="langgraph",
            content={
                "action": action_name,
                "conversation_id": conversation_id
            }
        ))

        try:
            # 2. 获取当前状态
            state = await self.state_manager.get_state(conversation_id)
            print(f"\n[状态] 当前状态: work_id={state.get('work_id')}")

            # 3. 模拟Action执行
            await asyncio.sleep(0.1)  # 模拟处理时间

            # 4. 更新状态
            await self.state_manager.update_state(
                conversation_id,
                {
                    "work_id": "work_123",
                    "chapter_id": "chapter_456",
                    "final_response": "模拟的写作内容..."
                },
                persist_to_redis=True
            )

            # 5. 发布Action完成事件
            await self.message_bus.publish(Message(
                topic=MessageType.ACTION_COMPLETED.value,
                sender="langgraph",
                content={
                    "action": action_name,
                    "status": ActionStatus.COMPLETED.value,
                    "conversation_id": conversation_id
                }
            ))

            print(f"[成功] {action_name} Action执行成功")

        except Exception as e:
            # 发布Action失败事件
            await self.message_bus.publish(Message(
                topic=MessageType.ACTION_FAILED.value,
                sender="langgraph",
                content={
                    "action": action_name,
                    "error": str(e),
                    "conversation_id": conversation_id
                }
            ))

            print(f"[失败] {action_name} Action执行失败: {e}")

    async def run_example(self):
        """运行示例"""
        print("=" * 60)
        print("Environment层集成示例")
        print("=" * 60)

        conversation_id = "test_conversation_001"

        # 模拟写作Action
        print("\n【步骤1】模拟写作Action执行")
        await self.simulate_writing_action(conversation_id)

        # 等待事件处理
        await asyncio.sleep(0.2)

        # 查看状态
        print("\n【步骤2】查看最终状态")
        final_state = await self.state_manager.get_state(conversation_id)
        print(f"  - work_id: {final_state.get('work_id')}")
        print(f"  - chapter_id: {final_state.get('chapter_id')}")
        print(f"  - final_response: {final_state.get('final_response')}")

        # 查看消息历史
        print("\n【步骤3】查看消息历史")
        history = self.message_bus.get_history()
        for i, msg in enumerate(history, 1):
            print(f"  {i}. [{msg.topic}] {msg.sender}: {msg.content}")

        # 查看统计
        print("\n【步骤4】查看统计信息")
        stats = self.message_bus.get_stats()
        print(f"  - 总主题数: {stats['total_topics']}")
        print(f"  - 总订阅者: {stats['total_subscribers']}")
        print(f"  - 历史消息数: {stats['history_count']}")

        print("\n" + "=" * 60)
        print("示例执行完成!")
        print("=" * 60)


async def main():
    """主函数"""
    example = EnvironmentIntegrationExample()
    await example.run_example()


if __name__ == "__main__":
    asyncio.run(main())
