"""
快速测试脚本 - 使用gemini-2.5-flash-lite

专为快速验证设计：
- 使用轻量级模型
- 15轮对话（而非30轮）
- 简短消息
- 预计耗时: 2-3分钟
"""

import asyncio
import sys
import os
import io

# 🔧 修复Windows控制台编码问题
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# 🔧 先加载环境变量
from dotenv import load_dotenv
backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
env_path = os.path.join(backend_dir, '.env')
load_dotenv(env_path)

sys.path.insert(0, backend_dir)

from app.services.agent.langgraph_agent import WritingAgentGraph
from app.services.ai.http_ai_service import HTTPAIService
from app.services.context import ContextManager, MemoryContextStore, TokenBudget
from test_config import TEST_CONFIG, SHORT_TEST_MESSAGES


class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'


def print_success(msg):
    print(f"{Colors.GREEN}✓ {msg}{Colors.ENDC}")


def print_warning(msg):
    print(f"{Colors.YELLOW}⚠ {msg}{Colors.ENDC}")


def print_error(msg):
    print(f"{Colors.RED}✗ {msg}{Colors.ENDC}")


def print_info(msg):
    print(f"{Colors.BLUE}ℹ {msg}{Colors.ENDC}")


def print_header(msg):
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}")
    print(f"{msg}")
    print(f"{'='*60}{Colors.ENDC}\n")


async def quick_test():
    """快速测试 - 15轮对话"""

    print_header("快速测试：15轮对话 (gemini-2.5-flash-lite)")

    # 创建AI服务和Agent
    print_info(f"模型: {TEST_CONFIG['model_name']}")
    print_info(f"测试轮数: {len(SHORT_TEST_MESSAGES)}")
    print_info(f"Token预算: {TEST_CONFIG['token_budget']}\n")

    ai_service = HTTPAIService(enable_model_selector=False)
    agent = WritingAgentGraph(ai_service, use_chatgpt=False)

    # 使用快速配置
    token_budget = TokenBudget(total=TEST_CONFIG['token_budget'])
    agent.context_manager = ContextManager(
        store=MemoryContextStore(),
        token_budget=token_budget
    )

    conversation_id = "quick_test_001"
    token_history = []

    # 执行15轮对话
    for turn, message in enumerate(SHORT_TEST_MESSAGES, 1):
        print(f"\n{Colors.BOLD}[{turn}/{len(SHORT_TEST_MESSAGES)}]{Colors.ENDC} {message}")

        result = await agent.chat_stream(
            message=message,
            conversation_id=conversation_id
        )

        # 获取上下文状态
        context = await agent.context_manager.store.load(conversation_id)
        token_count = context.get_total_tokens()
        token_history.append(token_count)

        # 输出简要信息
        response_preview = result['response'][:60] if result.get('response') else "无响应"
        print(f"  {Colors.GREEN}→{Colors.ENDC} {response_preview}...")
        print(f"  {Colors.BLUE}Token:{Colors.ENDC} {token_count}/{token_budget.total} ({token_count/token_budget.total*100:.0f}%)")

    # 最终结果
    print_header("测试完成")

    final_context = await agent.context_manager.store.load(conversation_id)
    final_tokens = final_context.get_total_tokens()
    final_messages = len(final_context.short_memory.messages)

    print(f"{Colors.BOLD}最终状态:{Colors.ENDC}")
    print(f"  Token: {final_tokens}/{token_budget.total} ({final_tokens/token_budget.total*100:.1f}%)")
    print(f"  消息数: {final_messages}")
    print(f"  摘要: {'有' if final_context.summary_memory.summary else '无'}")

    # 验证
    checks = []

    if final_tokens < token_budget.total * 0.9:
        print_success(f"Token控制: {final_tokens} < {token_budget.total * 0.9:.0f}")
        checks.append(True)
    else:
        print_error(f"Token过高: {final_tokens}")
        checks.append(False)

    if final_messages <= 12:
        print_success(f"消息限制: {final_messages} <= 12")
        checks.append(True)
    else:
        print_error(f"消息过多: {final_messages}")
        checks.append(False)

    if len(SHORT_TEST_MESSAGES) == len(token_history):
        print_success("对话完整: 所有轮次完成")
        checks.append(True)
    else:
        print_error("对话中断")
        checks.append(False)

    print(f"\n{Colors.BOLD}{'='*60}{Colors.ENDC}")
    if all(checks):
        print(f"{Colors.GREEN}{Colors.BOLD}✅ 快速测试通过！{Colors.ENDC}")
        return 0
    else:
        print(f"{Colors.RED}{Colors.BOLD}❌ 快速测试失败！{Colors.ENDC}")
        return 1


async def main():
    try:
        return await quick_test()
    except Exception as e:
        print_error(f"测试异常: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
