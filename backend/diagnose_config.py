"""诊断后端配置"""
import sys
import os

# 添加项目路径
sys.path.insert(0, os.path.dirname(__file__))

print("=" * 60)
print("后端配置诊断")
print("=" * 60)

# 1. 检查环境变量
print("\n1. 环境变量检查:")
print("-" * 60)
print(f"OPENAI_API_KEY: {os.getenv('OPENAI_API_KEY', 'NOT SET')[:50]}...")
print(f"OPENAI_BASE_URL: {os.getenv('OPENAI_BASE_URL', 'NOT SET')}")
print(f"OPENAI_MODEL: {os.getenv('OPENAI_MODEL', 'NOT SET')}")

# 2. 加载应用配置
print("\n2. 应用配置 (Settings):")
print("-" * 60)
try:
    from app.core.config import settings
    print(f"OPENAI_API_KEY: {settings.OPENAI_API_KEY[:50]}...")
    print(f"OPENAI_BASE_URL: {settings.OPENAI_BASE_URL}")
    print(f"OPENAI_MODEL: {settings.OPENAI_MODEL}")
except Exception as e:
    print(f"❌ 加载配置失败: {e}")

# 3. 测试 OpenAI 客户端初始化
print("\n3. OpenAI 客户端初始化:")
print("-" * 60)
try:
    from app.services.ai.openai_service import OpenAIService
    service = OpenAIService()
    print(f"✅ OpenAI Service 初始化成功")
    print(f"Base URL: {service.client.base_url}")
    print(f"Model: {service.default_model}")
    print(f"API Key: {service.client.api_key[:50]}...")
except Exception as e:
    print(f"❌ OpenAI Service 初始化失败: {e}")
    import traceback
    traceback.print_exc()

# 4. 测试实际 API 调用
print("\n4. 测试实际 API 调用:")
print("-" * 60)
try:
    import asyncio
    from app.services.ai.openai_service import OpenAIService
    
    async def test_call():
        service = OpenAIService()
        try:
            result = []
            async for chunk in service.stream_complete(
                context="你好",
                prompt="续写",
                max_tokens=50
            ):
                result.append(chunk)
            
            full_text = "".join(result)
            if full_text:
                print(f"✅ API 调用成功")
                print(f"返回内容: {full_text[:100]}")
            else:
                print(f"⚠️ API 返回为空")
                
        except Exception as e:
            print(f"❌ API 调用失败: {e}")
            import traceback
            traceback.print_exc()
    
    asyncio.run(test_call())
    
except Exception as e:
    print(f"❌ 测试失败: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
print("诊断完成")
print("=" * 60)
