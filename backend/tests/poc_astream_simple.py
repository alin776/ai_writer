"""
简化的POC测试：仅验证astream()机制，不依赖实际AI服务

目标：快速验证技术可行性
"""

import asyncio
from typing import TypedDict, Annotated, List, Any
from datetime import datetime
import operator


def test_astream_basic():
    """
    测试1：验证LangGraph的astream()基础机制
    """
    print("\n" + "="*80)
    print("🔬 测试1：验证LangGraph astream()基础机制")
    print("="*80 + "\n")

    try:
        from langgraph.graph import StateGraph, END
        from langchain_core.messages import HumanMessage, AIMessage

        # 定义简单的状态
        class SimpleState(TypedDict):
            messages: Annotated[List[Any], operator.add]
            intent: str
            counter: int

        # 定义节点函数
        def node_a(state: SimpleState):
            print("  🟢 执行 node_a")
            return {
                "messages": [AIMessage(content="Node A executed")],
                "counter": state.get("counter", 0) + 1
            }

        def node_b(state: SimpleState):
            print("  🔵 执行 node_b")
            return {
                "messages": [AIMessage(content="Node B executed")],
                "intent": "classified",
                "counter": state.get("counter", 0) + 1
            }

        def node_c(state: SimpleState):
            print("  🟣 执行 node_c")
            return {
                "messages": [AIMessage(content="Node C executed")],
                "counter": state.get("counter", 0) + 1
            }

        # 构建简单的图
        workflow = StateGraph(SimpleState)
        workflow.add_node("node_a", node_a)
        workflow.add_node("node_b", node_b)
        workflow.add_node("node_c", node_c)

        workflow.set_entry_point("node_a")
        workflow.add_edge("node_a", "node_b")
        workflow.add_edge("node_b", "node_c")
        workflow.add_edge("node_c", END)

        graph = workflow.compile()

        # 测试astream()
        print("📋 使用 astream() 执行图：\n")

        initial_state = {
            "messages": [HumanMessage(content="Test message")],
            "intent": "",
            "counter": 0
        }

        events = []

        async def run_stream():
            async for event in graph.astream(initial_state):
                events.append(event)
                if event:
                    node_name = list(event.keys())[0]
                    print(f"  📍 捕获事件 - 节点: {node_name}")
                    print(f"     └─ 事件数据keys: {list(event[node_name].keys())}")

        asyncio.run(run_stream())

        print(f"\n✅ 测试通过！")
        print(f"  • 捕获到 {len(events)} 个事件")
        print(f"  • 节点执行顺序: {[list(e.keys())[0] for e in events if e]}")

        return True

    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_astream_event_structure():
    """
    测试2：验证事件结构和数据内容
    """
    print("\n" + "="*80)
    print("🔬 测试2：验证事件结构")
    print("="*80 + "\n")

    try:
        from langgraph.graph import StateGraph, END
        from langchain_core.messages import HumanMessage, AIMessage
        import json

        class TestState(TypedDict):
            messages: Annotated[List[Any], operator.add]
            metadata: dict

        def classifier_node(state: TestState):
            return {
                "messages": [AIMessage(content="Intent classified as 'writing'")],
                "metadata": {"intent": "writing", "confidence": 0.95}
            }

        def agent_node(state: TestState):
            return {
                "messages": [AIMessage(content="Agent response: Processing your request...")],
                "metadata": {"status": "processing"}
            }

        workflow = StateGraph(TestState)
        workflow.add_node("classifier", classifier_node)
        workflow.add_node("agent", agent_node)
        workflow.set_entry_point("classifier")
        workflow.add_edge("classifier", "agent")
        workflow.add_edge("agent", END)

        graph = workflow.compile()

        initial_state = {
            "messages": [HumanMessage(content="Help me write")],
            "metadata": {}
        }

        print("📋 分析事件结构：\n")

        async def run_stream():
            async for event in graph.astream(initial_state):
                if event:
                    node_name = list(event.keys())[0]
                    node_data = event[node_name]

                    print(f"  📍 节点: {node_name}")
                    print(f"     └─ 数据类型: {type(node_data)}")
                    print(f"     └─ 包含keys: {list(node_data.keys()) if isinstance(node_data, dict) else 'N/A'}")

                    if "metadata" in node_data:
                        print(f"     └─ metadata: {json.dumps(node_data['metadata'], ensure_ascii=False)}")

                    if "messages" in node_data and node_data["messages"]:
                        msg = node_data["messages"][-1]
                        print(f"     └─ 最新消息: {msg.content[:50]}...")

                    print()

        asyncio.run(run_stream())

        print("✅ 事件结构验证通过！\n")
        return True

    except Exception as e:
        print(f"❌ 测试失败: {e}\n")
        import traceback
        traceback.print_exc()
        return False


def test_astream_performance():
    """
    测试3：性能对比 astream() vs invoke()
    """
    print("\n" + "="*80)
    print("🔬 测试3：性能对比")
    print("="*80 + "\n")

    try:
        from langgraph.graph import StateGraph, END
        from langchain_core.messages import HumanMessage, AIMessage
        import time

        class PerfState(TypedDict):
            messages: Annotated[List[Any], operator.add]
            count: int

        def fast_node(state: PerfState):
            return {
                "messages": [AIMessage(content=f"Fast node {state.get('count', 0)}")],
                "count": state.get("count", 0) + 1
            }

        # 构建图（3个节点）
        workflow = StateGraph(PerfState)
        for i in range(3):
            workflow.add_node(f"node_{i}", fast_node)

        workflow.set_entry_point("node_0")
        workflow.add_edge("node_0", "node_1")
        workflow.add_edge("node_1", "node_2")
        workflow.add_edge("node_2", END)

        graph = workflow.compile()

        initial_state = {
            "messages": [HumanMessage(content="Test")],
            "count": 0
        }

        # 测试 invoke()
        print("📊 测试 invoke()...")
        start = time.time()
        result_invoke = asyncio.run(graph.ainvoke(initial_state))
        time_invoke = time.time() - start
        print(f"   ✅ 耗时: {time_invoke:.3f}s\n")

        # 测试 astream()
        print("📊 测试 astream()...")
        start = time.time()
        event_count = 0

        async def run_stream():
            nonlocal event_count
            async for event in graph.astream(initial_state):
                event_count += 1

        asyncio.run(run_stream())
        time_astream = time.time() - start
        print(f"   ✅ 耗时: {time_astream:.3f}s")
        print(f"   📍 事件数: {event_count}\n")

        # 计算开销
        if time_invoke > 0:
            overhead = ((time_astream - time_invoke) / time_invoke) * 100
            print(f"📈 性能分析:")
            print(f"   • invoke():  {time_invoke:.3f}s")
            print(f"   • astream(): {time_astream:.3f}s")
            print(f"   • 开销:      {overhead:+.1f}%")

            if overhead < 20:
                print(f"   ✅ 性能开销可接受\n")
                return True
            else:
                print(f"   ⚠️  性能开销偏高\n")
                return False
        else:
            print("   ✅ 两者性能相当\n")
            return True

    except Exception as e:
        print(f"❌ 测试失败: {e}\n")
        import traceback
        traceback.print_exc()
        return False


def main():
    """
    运行所有POC测试
    """
    print("\n" + "=" * 80)
    print("开始LangGraph astream() POC验证")
    print("=" * 80 + "\n")

    results = {
        "基础机制": test_astream_basic(),
        "事件结构": test_astream_event_structure(),
        "性能对比": test_astream_performance()
    }

    print("\n" + "="*80)
    print("📊 POC测试总结")
    print("="*80 + "\n")

    for test_name, passed in results.items():
        status = "✅ 通过" if passed else "❌ 失败"
        print(f"  {status}  {test_name}")

    print("\n" + "="*80)

    if all(results.values()):
        print("\n[SUCCESS] POC验证完全通过！\n")
        print("[CONCLUSION]")
        print("  1. [OK] astream()机制可以正常工作")
        print("  2. [OK] 可以捕获节点执行事件")
        print("  3. [OK] 事件包含完整的状态数据")
        print("  4. [OK] 性能开销可接受")
        print("\n[RECOMMEND] 继续实施 Phase 2（实现chat_stream方法）\n")
        return True
    else:
        print("\n[WARNING] 部分测试失败\n")
        print("[NOTE] 检查失败的测试项，评估是否需要调整方案\n")
        return False


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
