"""节点元数据配置

定义每个LangGraph节点的权重、预估时间和友好描述，
用于进度跟踪和用户反馈。

⚠️ 重要说明：权重动态归一化
- 此文件中的progress_weight是相对权重，不需要总和为1.0
- ProgressTracker会在运行时自动归一化权重，确保总和为1.0
- 例如：writing场景 [intent_classifier(0.15) + writing_agent(0.65)] = 0.80
  实际运行时会归一化为 [0.1875 + 0.8125] = 1.0
- 这样设计的好处是可以灵活组合节点，无需手动调整权重

Created: 2025-11-10
Updated: 2025-11-11 - 添加权重归一化说明
"""

from typing import Dict, Any, TypedDict


class NodeMetadata(TypedDict):
    """节点元数据类型定义"""
    name: str              # 节点友好名称
    description: str       # 节点描述（给用户看）
    estimated_time: int    # 预估执行时间（秒）
    progress_weight: float # 进度权重（0-1，所有节点总和应该为1）
    category: str          # 节点类别（用于分组）


# 🎯 核心配置：节点元数据
NODE_METADATA: Dict[str, NodeMetadata] = {
    # === 分析类节点 ===
    "intent_classifier": {
        "name": "🧠 意图分析",
        "description": "正在分析您的需求...",
        "estimated_time": 5,
        "progress_weight": 0.15,  # 15% - ✅ 修复：调整权重使总和=1
        "category": "analysis"
    },

    # === Agent类节点 ===
    "writing_agent": {
        "name": "✍️ 创作中",
        "description": "正在为您创作内容...",
        "estimated_time": 30,
        "progress_weight": 0.65,  # 65% - ✅ 修复：写作是主要任务
        "category": "generation"
    },

    "planning_agent": {
        "name": "📋 规划中",
        "description": "正在制定计划...",
        "estimated_time": 20,
        "progress_weight": 0.65,  # 65% - ✅ 修复：规划是主要任务
        "category": "planning"
    },

    "analysis_agent": {
        "name": "📊 分析中",
        "description": "正在分析内容...",
        "estimated_time": 25,
        "progress_weight": 0.65,  # 65% - ✅ 修复：分析是主要任务
        "category": "analysis"
    },

    "stuck_agent": {
        "name": "💡 思考中",
        "description": "正在为您寻找灵感...",
        "estimated_time": 15,
        "progress_weight": 0.65,  # 65% - ✅ 修复：处理卡壳
        "category": "assistance"
    },

    "general_chat": {
        "name": "💬 对话中",
        "description": "正在回复您的消息...",
        "estimated_time": 10,
        "progress_weight": 0.65,  # 65% - ✅ 修复：一般对话
        "category": "chat"
    },

    # === 工具类节点 ===
    "tools": {
        "name": "🔧 调用工具",
        "description": "正在使用工具处理...",
        "estimated_time": 15,
        "progress_weight": 0.20,  # 20% - ✅ 修复：工具执行（可选节点）
        "category": "tool_execution"
    },

    # === 默认节点（兜底） ===
    "__default__": {
        "name": "⏳ 处理中",
        "description": "正在处理...",
        "estimated_time": 10,
        "progress_weight": 0.10,  # 10% - 默认权重
        "category": "other"
    }
}


def get_node_info(node_name: str) -> NodeMetadata:
    """获取节点元数据

    Args:
        node_name: 节点名称

    Returns:
        NodeMetadata: 节点元数据（如果不存在则返回默认值）
    """
    return NODE_METADATA.get(node_name, NODE_METADATA["__default__"])


def get_node_display_name(node_name: str) -> str:
    """获取节点友好名称

    Args:
        node_name: 节点名称

    Returns:
        str: 节点友好名称
    """
    return get_node_info(node_name)["name"]


def get_node_description(node_name: str) -> str:
    """获取节点描述

    Args:
        node_name: 节点名称

    Returns:
        str: 节点描述
    """
    return get_node_info(node_name)["description"]


def validate_weights() -> Dict[str, Any]:
    """验证所有节点的权重配置

    检查：
    1. 权重是否在0-1范围内
    2. 预估时间是否为正数

    Returns:
        Dict: 验证结果，包含warnings和errors
    """
    warnings = []
    errors = []

    for node_name, metadata in NODE_METADATA.items():
        # 跳过默认节点
        if node_name == "__default__":
            continue

        # 检查权重范围
        weight = metadata["progress_weight"]
        if not (0 <= weight <= 1):
            errors.append(
                f"节点 {node_name} 的权重 {weight} 不在 [0, 1] 范围内"
            )

        # 检查预估时间
        time = metadata["estimated_time"]
        if time <= 0:
            errors.append(
                f"节点 {node_name} 的预估时间 {time} 必须大于0"
            )

        # 检查必填字段
        required_fields = ["name", "description", "estimated_time", "progress_weight", "category"]
        for field in required_fields:
            if field not in metadata:
                errors.append(
                    f"节点 {node_name} 缺少必填字段 {field}"
                )

    return {
        "valid": len(errors) == 0,
        "warnings": warnings,
        "errors": errors
    }


def get_scenario_nodes(scenario: str) -> list[str]:
    """获取特定场景下会经过的节点

    Args:
        scenario: 场景类型 (writing/planning/analysis/stuck/general/writing_with_tools等)

    Returns:
        list: 节点名称列表
    """
    # ✅ 修复：删除不存在的节点，调整权重使总和=1.0
    scenarios = {
        # 基础场景（不含工具调用）- 权重总和 = 0.15 + 0.65 = 0.80
        "writing": ["intent_classifier", "writing_agent"],
        "planning": ["intent_classifier", "planning_agent"],
        "analysis": ["intent_classifier", "analysis_agent"],
        "stuck": ["intent_classifier", "stuck_agent"],
        "general": ["intent_classifier", "general_chat"],

        # 含工具调用的场景 - 权重总和 = 0.15 + 0.65 + 0.20 = 1.00
        "writing_with_tools": ["intent_classifier", "writing_agent", "tools"],
        "planning_with_tools": ["intent_classifier", "planning_agent", "tools"],
        "analysis_with_tools": ["intent_classifier", "analysis_agent", "tools"],
    }

    return scenarios.get(scenario, ["intent_classifier"])


def calculate_scenario_total_weight(scenario: str) -> float:
    """计算特定场景的总权重

    Args:
        scenario: 场景类型

    Returns:
        float: 场景总权重
    """
    nodes = get_scenario_nodes(scenario)
    total_weight = sum(get_node_info(node)["progress_weight"] for node in nodes)
    return total_weight


if __name__ == "__main__":
    # 验证配置
    result = validate_weights()

    if result["valid"]:
        print("✅ 节点元数据配置验证通过")
    else:
        print("❌ 节点元数据配置验证失败")
        for error in result["errors"]:
            print(f"  - {error}")

    if result["warnings"]:
        print("\n⚠️ 警告:")
        for warning in result["warnings"]:
            print(f"  - {warning}")

    # 显示各场景的总权重
    print("\n📊 场景权重分布:")
    for scenario in ["writing", "planning", "analysis", "stuck", "general", "react", "planning_mode"]:
        total = calculate_scenario_total_weight(scenario)
        nodes = get_scenario_nodes(scenario)
        print(f"  {scenario:15} : {total:.2f} ({len(nodes)} 节点)")
