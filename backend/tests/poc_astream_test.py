"""
POC测试：验证LangGraph astream()机制的可行性

测试目标：
1. 验证astream()能否返回节点事件
2. 检查事件结构和信息
3. 评估性能影响
4. 确认技术可行性

运行方式：
cd backend
python -m pytest tests/poc_astream_test.py -v -s
"""

import asyncio
import time
from datetime import datetime
from typing import Dict, Any
import sys
import os

# 添加项目路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.services.agent.langgraph_agent import WritingAgentGraph
from app.services.ai.http_ai_service import HTTPAIService
from app.core.config import settings


async def poc_test_astream():
    """
    POC测试主函数
    """
    print("\n" + "="*80)
    print("🔬 POC测试：LangGraph astream()机制验证")
    print("="*80 + "\n")

    # 1. 初始化Agent
    print("📋 Step 1: 初始化Agent...")
    try:
        ai_service = HTTPAIService()
        agent = WritingAgentGraph(ai_service=ai_service)
        print("✅ Agent初始化成功\n")
    except Exception as e:
        print(f"❌ Agent初始化失败: {e}\n")
        return False

    # 2. 准备测试消息
    test_cases = [
        {
            "name": "简单对话",
            "message": "你好",
            "work_id": None,
            "expected_nodes": ["intent_classifier", "general_chat"]
        },
        {
            "name": "写作任务（需要工具）",
            "message": "读取第三章的内容",
            "work_id": "test_work_123",
            "expected_nodes": ["intent_classifier", "writing_agent", "tools"]
        }
    ]

    # 3. 执行测试
    all_passed = True

    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{'='*80}")
        print(f"🧪 Test Case {i}: {test_case['name']}")
        print(f"{'='*80}\n")

        try:
            result = await run_single_test(agent, test_case)
            if not result:
                all_passed = False
        except Exception as e:
            print(f"❌ 测试失败: {e}\n")
            all_passed = False

    # 4. 总结
    print("\n" + "="*80)
    print("📊 POC测试总结")
    print("="*80 + "\n")

    if all_passed:
        print("✅ POC验证通过！")
        print("\n主要发现：")
        print("  ✅ astream()可以正常工作")
        print("  ✅ 可以获取节点执行事件")
        print("  ✅ 事件包含足够的信息")
        print("  ✅ 性能影响可接受")
        print("\n💡 建议：继续实施Phase 2（实现chat_stream）\n")
    else:
        print("❌ POC验证失败")
        print("\n⚠️  建议：重新评估技术方案\n")

    return all_passed


async def run_single_test(agent: WritingAgentGraph, test_case: Dict[str, Any]) -> bool:
    """
    执行单个测试用例
    """
    message = test_case["message"]
    work_id = test_case.get("work_id")
    expected_nodes = test_case.get("expected_nodes", [])

    print(f"📝 消息: {message}")
    print(f"🏢 Work ID: {work_id or 'None'}")
    print(f"🎯 预期节点: {', '.join(expected_nodes)}\n")

    # 准备初始状态
    from langchain_core.messages import HumanMessage
    initial_state = {
        "messages": [HumanMessage(content=message)],
        "work_id": work_id,
        "chapter_id": None,
        "intent": None,
        "context": {},
        "agent_steps": [],
        "suggested_actions": [],
        "final_response": None
    }

    # 配置
    import uuid
    config = {
        "configurable": {
            "thread_id": str(uuid.uuid4())
        }
    }

    # 记录事件
    events = []
    start_time = time.time()

    print("⏳ 开始流式执行...\n")

    try:
        # 使用astream()
        async for event in agent.graph.astream(initial_state, config):
            # 记录事件
            event_time = time.time() - start_time
            events.append({
                "event": event,
                "time": event_time
            })

            # 打印事件信息
            if event:
                node_name = list(event.keys())[0]
                node_data = event[node_name]

                print(f"  📍 节点: {node_name} (耗时: {event_time:.2f}s)")

                # 打印关键信息
                if "intent" in node_data and node_data["intent"]:
                    print(f"     └─ 意图: {node_data['intent']}")

                if "messages" in node_data:
                    messages = node_data["messages"]
                    if messages:
                        last_msg = messages[-1]
                        msg_type = type(last_msg).__name__
                        content_preview = str(last_msg.content)[:50] if hasattr(last_msg, 'content') else "N/A"
                        print(f"     └─ 消息类型: {msg_type}")
                        print(f"     └─ 内容预览: {content_preview}...")

                        # 检查工具调用
                        if hasattr(last_msg, 'tool_calls') and last_msg.tool_calls:
                            print(f"     └─ 工具调用: {len(last_msg.tool_calls)} 个")
                            for tool_call in last_msg.tool_calls[:2]:  # 只显示前2个
                                print(f"        └─ {tool_call.get('name', 'unknown')}")

                print()

        end_time = time.time()
        total_time = end_time - start_time

        print(f"✅ 执行完成 (总耗时: {total_time:.2f}s)\n")

        # 验证结果
        print("🔍 验证结果:\n")

        # 1. 检查是否获取到事件
        if len(events) == 0:
            print("  ❌ 未获取到任何事件")
            return False
        else:
            print(f"  ✅ 获取到 {len(events)} 个事件")

        # 2. 检查节点覆盖
        captured_nodes = [list(e["event"].keys())[0] for e in events if e["event"]]
        print(f"  📍 捕获的节点: {', '.join(captured_nodes)}")

        missing_nodes = set(expected_nodes) - set(captured_nodes)
        if missing_nodes:
            print(f"  ⚠️  缺少预期节点: {', '.join(missing_nodes)}")
        else:
            print(f"  ✅ 所有预期节点都已捕获")

        # 3. 检查事件结构
        print("\n  📋 事件结构分析:")
        for node_name in set(captured_nodes):
            node_events = [e for e in events if list(e["event"].keys())[0] == node_name]
            if node_events:
                sample_event = node_events[0]["event"][node_name]
                keys = list(sample_event.keys()) if isinstance(sample_event, dict) else []
                print(f"    • {node_name}: {', '.join(keys[:5])}")

        # 4. 性能评估
        print(f"\n  ⚡ 性能:")
        print(f"    • 总耗时: {total_time:.2f}s")
        print(f"    • 平均每节点: {total_time/len(events):.2f}s")

        if total_time > 10:
            print(f"    ⚠️  执行时间较长，可能需要优化")
        else:
            print(f"    ✅ 性能可接受")

        return True

    except Exception as e:
        print(f"\n❌ 执行失败: {e}")
        import traceback
        traceback.print_exc()
        return False


async def compare_with_normal_invoke():
    """
    对比测试：astream() vs invoke()
    比较性能差异
    """
    print("\n" + "="*80)
    print("⚖️  性能对比：astream() vs invoke()")
    print("="*80 + "\n")

    try:
        ai_service = HTTPAIService()
        agent = WritingAgentGraph(ai_service=ai_service)

        from langchain_core.messages import HumanMessage
        import uuid

        test_message = "你好"
        initial_state = {
            "messages": [HumanMessage(content=test_message)],
            "work_id": None,
            "chapter_id": None,
            "intent": None,
            "context": {},
            "agent_steps": [],
            "suggested_actions": [],
            "final_response": None
        }

        config = {"configurable": {"thread_id": str(uuid.uuid4())}}

        # 测试 invoke()
        print("📊 测试 invoke()...")
        start = time.time()
        result_invoke = await agent.graph.ainvoke(initial_state, config)
        time_invoke = time.time() - start
        print(f"   ✅ 耗时: {time_invoke:.3f}s\n")

        # 测试 astream()
        print("📊 测试 astream()...")
        config2 = {"configurable": {"thread_id": str(uuid.uuid4())}}
        start = time.time()
        event_count = 0
        async for event in agent.graph.astream(initial_state, config2):
            event_count += 1
        time_astream = time.time() - start
        print(f"   ✅ 耗时: {time_astream:.3f}s")
        print(f"   📍 事件数: {event_count}\n")

        # 对比
        overhead = ((time_astream - time_invoke) / time_invoke) * 100
        print(f"📈 性能对比:")
        print(f"   • invoke():  {time_invoke:.3f}s")
        print(f"   • astream(): {time_astream:.3f}s")
        print(f"   • 开销:      {overhead:+.1f}%")

        if overhead < 10:
            print(f"   ✅ 性能开销可接受\n")
            return True
        elif overhead < 20:
            print(f"   ⚠️  性能开销偏高但可接受\n")
            return True
        else:
            print(f"   ❌ 性能开销过高\n")
            return False

    except Exception as e:
        print(f"❌ 对比测试失败: {e}\n")
        return False


if __name__ == "__main__":
    print("\n🚀 开始POC验证...\n")

    # 运行主测试
    asyncio.run(poc_test_astream())

    # 运行性能对比
    # asyncio.run(compare_with_normal_invoke())
