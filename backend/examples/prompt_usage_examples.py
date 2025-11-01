"""
Prompt 库使用示例

展示如何使用 Prompt 库进行网文创作
"""

import asyncio
import sys
from pathlib import Path
from typing import Dict, Optional

# 添加项目路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from app.services.agent.prompts import (
    NovelPhase,
    SceneType,
    ContentCreationPrompts,
    NovelPlanningPrompts,
    PromptOptimizer
)
from app.services.agent.prompt_library import (
    prompt_library,
    get_content_prompt,
    get_planning_prompt
)


# ==================== 示例 1: 基础使用 ====================

def example_1_basic_usage():
    """示例 1: 基础使用 - 获取系统 Prompt"""
    print("=" * 60)
    print("示例 1: 获取基础的内容创作 System Prompt")
    print("=" * 60)

    # 方式 1: 直接从类获取
    system_prompt = ContentCreationPrompts.get_system_prompt()
    print(f"System Prompt 长度: {len(system_prompt)} 字符")
    print(f"\n前 200 字符:\n{system_prompt[:200]}...\n")

    # 方式 2: 从 Prompt 库获取
    system_prompt_2 = prompt_library.get_prompt('content_creation', 'system')
    print(f"从库获取的 Prompt 相同: {system_prompt == system_prompt_2}")


# ==================== 示例 2: 阶段 Prompt ====================

def example_2_phase_prompts():
    """示例 2: 获取不同阶段的 Prompt"""
    print("\n" + "=" * 60)
    print("示例 2: 获取不同阶段的创作 Prompt")
    print("=" * 60)

    # 获取 "转" 阶段的 Prompt
    climax_prompt = ContentCreationPrompts.get_phase_prompt(
        NovelPhase.CLIMAX,
        context={
            'target_length': 3000,
            'current_chapter': 25,
            'total_chapters': 50
        }
    )

    print(f"\n【转 - 冲突升级阶段】")
    print(f"Prompt 长度: {len(climax_prompt)} 字符")
    print(f"\n前 300 字符:\n{climax_prompt[:300]}...\n")


# ==================== 示例 3: 场景模板 ====================

def example_3_scene_templates():
    """示例 3: 使用场景模板"""
    print("\n" + "=" * 60)
    print("示例 3: 使用打脸场景模板")
    print("=" * 60)

    # 获取打脸场景模板
    slap_face_prompt = ContentCreationPrompts.get_scene_prompt('slap_face')

    print(f"\n【打脸场景模板】")
    print(f"Prompt 长度: {len(slap_face_prompt)} 字符")
    print(f"\n完整内容:\n{slap_face_prompt}\n")


# ==================== 示例 4: 组合 Prompts ====================

def example_4_combined_prompts():
    """示例 4: 组合多个 Prompt"""
    print("\n" + "=" * 60)
    print("示例 4: 组合多个 Prompt (系统 + 阶段 + 场景)")
    print("=" * 60)

    # 组合: 系统 Prompt + 开端阶段 + 打脸场景
    combined = ContentCreationPrompts.get_combined_prompt(
        phase=NovelPhase.OPENING,
        scene_type='slap_face',
        user_preferences="增加武侠元素,主角使用剑法"
    )

    print(f"\n组合后的 Prompt 长度: {len(combined)} 字符")
    print(f"\n前 500 字符:\n{combined[:500]}...\n")


# ==================== 示例 5: 添加用户偏好 ====================

def example_5_user_preferences():
    """示例 5: 添加用户偏好"""
    print("\n" + "=" * 60)
    print("示例 5: 添加用户偏好")
    print("=" * 60)

    base_prompt = ContentCreationPrompts.get_system_prompt()

    # 定义用户偏好
    user_prefs = {
        'style': '轻松幽默',
        'focus': ['打脸', '升级', '智斗'],
        'avoid': ['虐主', '圣母', '感情戏过多'],
        'special_requirements': '主角要展现高智商,多用计谋而非蛮力'
    }

    # 添加用户偏好
    enhanced = PromptOptimizer.add_user_preferences(base_prompt, user_prefs)

    print(f"\n原始 Prompt 长度: {len(base_prompt)}")
    print(f"增强后 Prompt 长度: {len(enhanced)}")
    print(f"\n增加的部分:\n{enhanced[len(base_prompt):]}\n")


# ==================== 示例 6: 质量反馈循环 ====================

def example_6_quality_feedback():
    """示例 6: 使用质量反馈(质量循环)"""
    print("\n" + "=" * 60)
    print("示例 6: 添加质量反馈用于重试")
    print("=" * 60)

    base_prompt = ContentCreationPrompts.get_phase_prompt(NovelPhase.DEVELOPMENT)

    # 模拟质量评估的反馈
    feedback = """
质量评估结果:
- 总分: 7.2/10
- 连贯性: 6.5/10 - 与前文衔接不够自然
- 对话: 7.0/10 - 对话略显平淡,缺少火药味
- 场景描写: 8.0/10 - 场景描写生动

改进建议:
1. 增强与前文的衔接,回顾上章结尾
2. 对话要更犀利,增加冲突感
3. 保持场景描写的水准
"""

    # 添加反馈
    enhanced = PromptOptimizer.add_quality_feedback(base_prompt, feedback)

    print(f"\n添加反馈后 Prompt 长度: {len(enhanced)}")
    print(f"\n反馈部分:\n{enhanced[len(base_prompt):]}\n")


# ==================== 示例 7: 使用 Prompt 库 ====================

def example_7_prompt_library():
    """示例 7: 使用 Prompt 库管理系统"""
    print("\n" + "=" * 60)
    print("示例 7: 使用 Prompt 库管理系统")
    print("=" * 60)

    # 列出所有可用的 Prompts
    all_prompts = prompt_library.list_available_prompts()
    print("\n【所有可用的 Prompt 类别】")
    for category, subcategories in all_prompts.items():
        print(f"\n{category}:")
        for sub in subcategories[:5]:  # 只显示前5个
            print(f"  - {sub}")
        if len(subcategories) > 5:
            print(f"  ... 还有 {len(subcategories) - 5} 个")

    # 使用便捷函数获取 Prompt
    content_prompt = get_content_prompt(
        phase=NovelPhase.CLIMAX,
        scene_type='battle',
        user_preferences={'style': '热血'},
        context={'target_length': 3000}
    )

    print(f"\n使用便捷函数获取的 Prompt 长度: {len(content_prompt)}")


# ==================== 示例 8: 规划类 Prompts ====================

def example_8_planning_prompts():
    """示例 8: 使用规划类 Prompts"""
    print("\n" + "=" * 60)
    print("示例 8: 使用规划类 Prompts")
    print("=" * 60)

    # 获取世界观构建 Prompt
    world_prompt = get_planning_prompt('world')
    print(f"\n【世界观构建 Prompt】")
    print(f"长度: {len(world_prompt)} 字符")
    print(f"\n前 300 字符:\n{world_prompt[:300]}...\n")

    # 获取角色设计 Prompt
    character_prompt = get_planning_prompt('character')
    print(f"\n【角色设计 Prompt】")
    print(f"长度: {len(character_prompt)} 字符")
    print(f"\n前 300 字符:\n{character_prompt[:300]}...\n")


# ==================== 示例 9: 追踪使用统计 ====================

def example_9_usage_tracking():
    """示例 9: 追踪 Prompt 使用统计"""
    print("\n" + "=" * 60)
    print("示例 9: Prompt 使用统计追踪")
    print("=" * 60)

    # 模拟使用多个 Prompts 并追踪质量
    prompts_to_test = [
        ('content_creation.system', 8.5),
        ('content_creation.phase_opening', 9.0),
        ('content_creation.phase_climax', 9.2),
        ('content_creation.scene_slap_face', 8.8),
    ]

    print("\n模拟追踪 Prompt 使用效果:")
    for prompt_id, quality in prompts_to_test:
        prompt_library.track_prompt_usage(prompt_id, quality)
        print(f"  - {prompt_id}: 质量 {quality}/10")

    # 获取统计
    print("\n【使用统计】")
    stats = prompt_library.get_usage_stats()
    for prompt_id, stat in stats.items():
        if stat['usage_count'] > 0:
            print(f"\n{prompt_id}:")
            print(f"  使用次数: {stat['usage_count']}")
            print(f"  平均质量: {stat['avg_quality']:.2f}/10")

    # 获取最佳 Prompts
    print("\n【效果最好的 Prompts (Top 3)】")
    best = prompt_library.get_best_prompts('content_creation', top_n=3)
    for i, item in enumerate(best, 1):
        print(f"{i}. {item['prompt_id']}")
        print(f"   平均质量: {item['avg_quality']:.2f}/10")
        print(f"   使用次数: {item['usage_count']}")


# ==================== 示例 10: 自定义 Prompt ====================

def example_10_custom_prompt():
    """示例 10: 注册和使用自定义 Prompt"""
    print("\n" + "=" * 60)
    print("示例 10: 注册自定义 Prompt")
    print("=" * 60)

    # 定义自定义场景 Prompt
    custom_scene = """
【修仙场景 - 渡劫】

渡劫场景创作要点:

1. 前期准备(20%):
   - 选择渡劫地点
   - 准备各种丹药法宝
   - 好友护法
   - 敌人窥视

2. 雷劫降临(30%):
   - 天象异变,乌云密布
   - 第一道天雷威力描写
   - 主角应对展示实力
   - 众人震惊反应

3. 劫难重重(30%):
   - 雷劫层层加强(九九八十一道)
   - 主角险象环生但化险为夷
   - 底牌逐一展现
   - 敌人暗中出手被化解

4. 渡劫成功(20%):
   - 最后一击,惊天动地
   - 突破成功,实力暴涨
   - 天地异象庆贺
   - 地位提升,震撼全场
"""

    # 注册自定义 Prompt
    prompt_library.register_prompt('custom', 'tribulation_scene', custom_scene)
    print("已注册自定义 Prompt: custom.tribulation_scene")

    # 获取并使用
    custom = prompt_library.get_prompt('custom', 'tribulation_scene')
    print(f"\n自定义 Prompt 长度: {len(custom)} 字符")
    print(f"\n内容:\n{custom}\n")

    # 查看所有自定义 Prompts
    custom_prompts = prompt_library.list_available_prompts('custom')
    print(f"所有自定义 Prompts: {custom_prompts}")


# ==================== 示例 11: 完整创作流程 ====================

def example_11_complete_workflow():
    """示例 11: 完整的内容创作流程"""
    print("\n" + "=" * 60)
    print("示例 11: 完整的章节创作流程")
    print("=" * 60)

    # 假设我们要创作第 25 章(转阶段,打脸场景)
    chapter_num = 25
    phase = NovelPhase.CLIMAX
    scene_type = 'slap_face'

    print(f"\n任务: 创作第 {chapter_num} 章")
    print(f"阶段: {phase.value}")
    print(f"场景: {scene_type}")

    # Step 1: 获取基础 Prompt
    print("\n--- Step 1: 组合基础 Prompt ---")
    base_prompt = get_content_prompt(
        phase=phase,
        scene_type=scene_type,
        user_preferences={
            'style': '热血',
            'focus': ['打脸', '实力碾压'],
            'avoid': ['拖沓']
        },
        context={
            'target_length': 3000,
            'current_chapter': chapter_num,
            'total_chapters': 50,
            'previous_content': '上一章主角被众人嘲笑...'
        }
    )
    print(f"组合后的 Prompt 长度: {len(base_prompt)} 字符")

    # Step 2: 模拟第一次生成 (假设质量不够)
    print("\n--- Step 2: 第一次生成 (模拟) ---")
    first_generation = "第一次生成的内容..."  # 这里会实际调用 LLM
    print(f"生成内容长度: {len(first_generation)} 字符")
    print("质量评分: 7.5/10 (假设)")

    # Step 3: 添加质量反馈,准备重试
    print("\n--- Step 3: 添加质量反馈,准备重试 ---")
    feedback = "对话不够犀利,打脸力度不够,建议增强主角的霸气"
    retry_prompt = PromptOptimizer.add_quality_feedback(base_prompt, feedback)
    print(f"重试 Prompt 长度: {len(retry_prompt)} 字符")

    # Step 4: 第二次生成 (模拟)
    print("\n--- Step 4: 第二次生成 (模拟) ---")
    second_generation = "第二次生成的内容..."  # 这里会实际调用 LLM
    print(f"生成内容长度: {len(second_generation)} 字符")
    print("质量评分: 9.0/10 (假设)")

    # Step 5: 记录使用统计
    print("\n--- Step 5: 记录使用统计 ---")
    prompt_library.track_prompt_usage(
        f'content_creation.phase_{phase.value}',
        9.0
    )
    print(f"已记录使用统计: phase_{phase.value}, 质量 9.0/10")


# ==================== 运行所有示例 ====================

def run_all_examples():
    """运行所有示例"""
    print("\n" + "=" * 60)
    print("Prompt 库使用示例集")
    print("=" * 60)

    examples = [
        ("基础使用", example_1_basic_usage),
        ("阶段 Prompt", example_2_phase_prompts),
        ("场景模板", example_3_scene_templates),
        ("组合 Prompts", example_4_combined_prompts),
        ("用户偏好", example_5_user_preferences),
        ("质量反馈", example_6_quality_feedback),
        ("Prompt 库", example_7_prompt_library),
        ("规划 Prompts", example_8_planning_prompts),
        ("使用统计", example_9_usage_tracking),
        ("自定义 Prompt", example_10_custom_prompt),
        ("完整流程", example_11_complete_workflow),
    ]

    for name, func in examples:
        try:
            func()
        except Exception as e:
            print(f"\n❌ 示例 '{name}' 执行失败: {e}")

    print("\n" + "=" * 60)
    print("所有示例执行完毕!")
    print("=" * 60)


if __name__ == "__main__":
    run_all_examples()
