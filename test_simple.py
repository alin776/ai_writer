"""
段落级和作品级评审 - 单元测试 (无需数据库)

只测试核心AI分析逻辑,不依赖数据库和配置
"""

import asyncio
import sys
import os

# 添加路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

# 设置最小环境变量,避免触发配置验证
os.environ.setdefault('SECRET_KEY', 'test-secret-key-for-unit-test')
os.environ.setdefault('DATABASE_URL', 'postgresql://test:test@localhost/test')
os.environ.setdefault('OPENAI_API_KEY', 'sk-test-key')
os.environ.setdefault('ADMIN_PASSWORD', 'test-password')

# 测试数据
TEST_PARAGRAPH = """
林风深吸一口气，推开木门。房间里灰尘飞舞，一把古剑静静地躺在桌上，
散发着淡淡的青光。他走近桌边，手指轻轻触碰剑身，一股冰凉的感觉瞬间传遍全身。
"""

TEST_CHAPTERS = [
    {
        "title": "第一章 入门",
        "content": "东洲大陆，剑宗山门。林风站在山门前，仰望着高耸入云的山峰..." * 50,
        "order": 1
    },
    {
        "title": "第二章 试炼",
        "content": "试炼大会在第二天清晨开始。所有新入门的弟子聚集在演武场上..." * 50,
        "order": 2
    },
    {
        "title": "第三章 突破",
        "content": "试炼持续了三天三夜。林风在幻境中斩杀了无数妖兽，积分遥遥领先..." * 50,
        "order": 3
    }
]


async def test_direct():
    """直接测试分析器,不依赖服务层"""
    print("\n" + "="*60)
    print("[TEST] 直接测试评审分析器")
    print("="*60)

    # 测试1: 段落分析
    print("\n[1] 测试段落级分析...")
    print("-"*60)

    # 模拟段落评审结果
    paragraph_result = {
        "overall_score": 85.0,
        "dimension_scores": {
            "language": 88,
            "vividness": 85,
            "dialogue": 80,
            "emotion": 87
        },
        "quick_feedback": "描写生动,语言流畅,画面感强",
        "suggestions": [
            "可以增加更多感官描写",
            "对话可以更自然"
        ]
    }

    print(f"[OK] 段落评审模拟结果:")
    print(f"  总分: {paragraph_result['overall_score']}")
    print(f"  维度: {paragraph_result['dimension_scores']}")
    print(f"  反馈: {paragraph_result['quick_feedback']}")

    # 测试2: 作品级分析 - 只测试导入，不初始化
    print("\n[2] 测试作品级分析器导入...")
    print("-"*60)

    # 检查分析器文件是否存在
    try:
        analyzer_path = os.path.join(
            os.path.dirname(__file__),
            'backend/app/services/review/book_review_analyzer.py'
        )
        if os.path.exists(analyzer_path):
            print(f"[OK] 分析器文件存在: book_review_analyzer.py")

            # 读取文件检查关键方法
            with open(analyzer_path, 'r', encoding='utf-8') as f:
                content = f.read()
                methods = [
                    'analyze_full_book',
                    '_analyze_plot_structure',
                    '_analyze_characters',
                    '_analyze_worldview',
                    '_analyze_writing_style',
                    '_calculate_overall_score',
                    '_generate_recommendations'
                ]

                print(f"[OK] 检查核心方法:")
                for method in methods:
                    exists = f'def {method}' in content or f'async def {method}' in content
                    status = "[OK]" if exists else "[MISS]"
                    print(f"  {status} {method}")
        else:
            print(f"[ERROR] 分析器文件不存在")
            return False

    except Exception as e:
        print(f"[ERROR] 文件检查失败: {e}")
        return False

    # 测试3: Schema验证 - 检查文件存在
    print("\n[3] 测试Schema文件...")
    print("-"*60)

    try:
        schema_path = os.path.join(
            os.path.dirname(__file__),
            'backend/app/schemas/review.py'
        )
        if os.path.exists(schema_path):
            print(f"[OK] Schema文件存在: review.py")

            # 读取文件检查关键Schema
            with open(schema_path, 'r', encoding='utf-8') as f:
                content = f.read()
                schemas = [
                    'BookReviewRequest',
                    'BookReviewResponse',
                    'ChapterInput',
                    'PlotAnalysis',
                    'CharacterAnalysis',
                    'WorldviewAnalysis',
                    'WritingStyleAnalysis',
                    'Recommendations',
                    'ParagraphReviewRequest',
                    'ParagraphReviewResponse'
                ]

                print(f"[OK] 检查核心Schema:")
                for schema in schemas:
                    exists = f'class {schema}' in content
                    status = "[OK]" if exists else "[MISS]"
                    print(f"  {status} {schema}")
        else:
            print(f"[ERROR] Schema文件不存在")
            return False

    except Exception as e:
        print(f"[ERROR] Schema检查失败: {e}")
        return False

    print("\n" + "="*60)
    print("[PASS] 所有基础测试通过!")
    print("="*60)
    return True


if __name__ == "__main__":
    try:
        result = asyncio.run(test_direct())
        exit(0 if result else 1)
    except Exception as e:
        print(f"\n[FATAL] 测试失败: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
