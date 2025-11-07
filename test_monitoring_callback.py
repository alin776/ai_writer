"""
测试 ChatOpenAI 监控集成

直接测试 WritingAgentGraph 的 chat 方法，验证 MonitoringCallbackHandler 是否正常工作
"""
import sys
import os
sys.path.insert(0, r"D:\Java\ai_writer\backend")

# 加载环境变量
from dotenv import load_dotenv
backend_dir = r"D:\Java\ai_writer\backend"
env_path = os.path.join(backend_dir, ".env")
load_dotenv(env_path)

import asyncio
from app.services.ai.http_ai_service import HTTPAIService
from app.services.agent.langgraph_agent import WritingAgentGraph


async def test_monitoring_callback():
    """测试 MonitoringCallbackHandler"""
    print("=" * 60)
    print("[TEST] ChatOpenAI Monitoring Callback Test")
    print("=" * 60)

    # 创建 AI Service
    ai_service = HTTPAIService()

    # 创建 Agent（use_chatgpt=True 启用 ChatOpenAI 模式）
    agent = WritingAgentGraph(ai_service=ai_service, use_chatgpt=True)

    print("\n[INFO] Agent 已创建（ChatOpenAI 模式）")
    print("[INFO] 准备发送测试消息...")

    try:
        # 发送简单测试消息
        result = await agent.chat(
            message="你好，请简单介绍一下自己",
            conversation_id="test_monitoring_001"
        )

        print(f"\n[SUCCESS] Agent 响应成功!")
        print(f"[RESPONSE] {result.get('response', 'N/A')[:200]}...")
        print(f"[METADATA] {result.get('metadata', {})}")

        print("\n" + "=" * 60)
        print("[RESULT] 测试完成！现在可以查看监控指标：")
        print("  curl http://localhost:8000/api/v1/monitoring/metrics")
        print("=" * 60)

        return True

    except Exception as e:
        print(f"\n[FAILED] 测试失败: {type(e).__name__}")
        print(f"[ERROR] {str(e)}")
        import traceback
        traceback.print_exc()
        return False

    finally:
        await ai_service.close()


if __name__ == "__main__":
    asyncio.run(test_monitoring_callback())
