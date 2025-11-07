"""
测试GeneralChatAction的prepare()方法

验证：
1. prepare()能正确返回system_prompt
2. metadata包含正确的agent_type
3. 输入验证正常工作
"""

import asyncio
import sys
import os

# 添加项目路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from langchain_core.messages import HumanMessage
from app.services.agent.actions.general_chat_action import GeneralChatAction


async def test_general_chat_prepare():
    """测试GeneralChatAction.prepare()方法"""

    print("\n" + "="*60)
    print("测试1: 正常情况 - 包含消息")
    print("="*60)

    # 创建Action实例（不需要ai_service）
    action = GeneralChatAction()

    # 准备测试state
    state = {
        "messages": [
            HumanMessage(content="你好"),
            HumanMessage(content="你能做什么？")
        ]
    }

    # 调用prepare
    result = await action.prepare(state)

    # 验证结果
    print(f"✅ 状态: {result.status}")
    print(f"✅ 成功: {result.success}")
    print(f"✅ system_prompt长度: {len(result.system_prompt) if result.system_prompt else 0}")
    print(f"✅ system_prompt预览: {result.system_prompt[:100] if result.system_prompt else 'N/A'}...")
    print(f"✅ metadata: {result.metadata}")

    assert result.success, "prepare()应该成功"
    assert result.system_prompt, "应该返回system_prompt"
    assert result.metadata.get("agent_type") == "general", "agent_type应该是general"
    assert result.metadata.get("message_count") == 2, "消息数应该是2"

    print("\n✅ 测试1通过！\n")

    # 测试2: 错误情况 - 没有消息
    print("="*60)
    print("测试2: 错误情况 - 没有消��")
    print("="*60)

    state_empty = {"messages": []}
    result_empty = await action.prepare(state_empty)

    print(f"✅ 状态: {result_empty.status}")
    print(f"✅ 成功: {result_empty.success}")
    print(f"✅ 错误信息: {result_empty.error}")

    assert not result_empty.success, "prepare()应该失败"
    assert result_empty.error, "应该返回错误信息"

    print("\n✅ 测试2通过！\n")

    # 测试3: 验证向后兼容性
    print("="*60)
    print("测试3: 向后兼容性 - is_success()方法")
    print("="*60)

    print(f"✅ result.is_success(): {result.is_success()}")
    print(f"✅ result.success: {result.success}")
    print(f"✅ 两者应该相等: {result.is_success() == result.success}")

    assert result.is_success() == result.success, "is_success()和success应该一致"

    print("\n✅ 测试3通过！\n")

    print("="*60)
    print("🎉 所有测试通过！")
    print("="*60)


if __name__ == "__main__":
    asyncio.run(test_general_chat_prepare())
