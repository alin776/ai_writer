# -*- coding: utf-8 -*-
"""
Explore V6 单元测试

测试 ExploreV6 核心逻辑：单查询生成、LightRAG 调用、章节元数据补全、结果组装。
所有外部依赖（AI 服务、数据库、LightRAG）通过 mock 隔离。
使用 importlib 直接加载模块，避免 app.services.__init__ 导入链。
"""

import importlib
import importlib.util
import json
import sys
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

SOURCE_PATH = Path(__file__).resolve().parents[2] / "app/services/agent/tools/explore_v6.py"


def _load_module():
    """直接加载 explore_v6.py，绕过 app.services.__init__ 导入链。"""
    spec = importlib.util.spec_from_file_location("explore_v6_local", SOURCE_PATH)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


_mod = _load_module()
ExploreV6 = _mod.ExploreV6


# ---- 辅助 ----

def _make_chunk(text, chapter_id="", chapter_order=None, chapter_title=""):
    return {
        "text": text,
        "chapter_id": chapter_id,
        "chapter_order": chapter_order,
        "chapter_title": chapter_title,
    }


def _build_v6(**overrides):
    """构建 ExploreV6 实例。"""
    v6 = ExploreV6(
        work_id=overrides.get("work_id", "test-work-id"),
        target_task=overrides.get("target_task", "续写第6章"),
        retrieval_intent=overrides.get("retrieval_intent"),
        user_id=overrides.get("user_id", "test-user"),
    )
    return v6


# ================================================================
# 测试 1：单查询生成
# ================================================================

@pytest.mark.asyncio
async def test_generate_query_returns_string():
    """generate_query 应返回一条字符串查询。"""
    v6 = _build_v6(target_task="器灵等阶规律是什么")

    mock_ai = AsyncMock()
    mock_ai.call_ai = AsyncMock(return_value="器灵等阶 吞噬规则 废刀")

    with patch.object(_mod, "_get_ai_service", return_value=mock_ai):
        query = await v6.generate_query(
            chapters=[{"order": 1, "title": "第一章", "word_count": 3000}],
        )

    assert isinstance(query, str)
    assert "器灵" in query


# ================================================================
# 测试 2：AI 失败时回退到 target_task
# ================================================================

@pytest.mark.asyncio
async def test_generate_query_fallback_on_error():
    """AI 调用失败时，回退为 target_task。"""
    v6 = _build_v6(target_task="测试回退任务")

    mock_ai = AsyncMock()
    mock_ai.call_ai = AsyncMock(side_effect=Exception("AI 挂了"))

    with patch.object(_mod, "_get_ai_service", return_value=mock_ai):
        query = await v6.generate_query(chapters=[])

    assert query == "测试回退任务"


# ================================================================
# 测试 3：enrich_chunks 补全章节元数据
# ================================================================

@pytest.mark.asyncio
async def test_enrich_chunks():
    """enrich_chunks 应根据 chapter_id 补全 chapter_order 和 chapter_title。"""
    v6 = _build_v6()

    chunks = [
        _make_chunk("段融握紧了手中的废刀", chapter_id="ch-1"),
        _make_chunk("赵穆皱了皱眉", chapter_id="ch-2"),
        _make_chunk("未定位的chunk", chapter_id=""),
    ]
    chapters = [
        {"id": "ch-1", "order": 1, "title": "第一章", "word_count": 3000},
        {"id": "ch-2", "order": 2, "title": "第二章", "word_count": 4000},
    ]

    enriched = await v6.enrich_chunks(chunks, chapters)

    assert enriched[0]["chapter_order"] == 1
    assert enriched[0]["chapter_title"] == "第一章"
    assert enriched[1]["chapter_order"] == 2
    assert enriched[2].get("chapter_order") is None  # 未定位


# ================================================================
# 测试 4：_build_result 输出格式
# ================================================================

def test_build_result_format():
    """_build_result 应返回正确的字典格式。"""
    v6 = _build_v6()
    result = v6._build_result(
        evidences=[
            {"text": "test", "chapter_order": 1, "chapter_id": "ch-1"},
            {"text": "test2", "chapter_order": 2, "chapter_id": "ch-2"},
            {"text": "test3", "chapter_order": 1, "chapter_id": "ch-1"},
        ],
        chapters_info=[{"id": "ch-1", "order": 1, "title": "第一章", "word_count": 3000}],
        worldview={"characters": [{"name": "段融"}]},
        stop_reason="测试完成",
        duration_ms=100,
    )

    assert result["success"] is True
    assert isinstance(result["evidences"], list)
    assert isinstance(result["worldview"], dict)
    assert isinstance(result["stats"], dict)
    assert result["stats"]["explore_version"] == "v6"
    assert result["stop_reason"] == "测试完成"
    assert result["total_duration_ms"] == 100
    assert "context_for_task" in result
    assert "paragraphs" in result

    # chapters 应为 list
    assert isinstance(result["chapters"], list)
    assert len(result["chapters"]) == 1
    assert result["chapters"][0]["id"] == "ch-1"

    # locate_targets 按 chapter_id 去重
    assert isinstance(result["locate_targets"], list)
    assert len(result["locate_targets"]) == 2
    target_ids = {t["chapter_id"] for t in result["locate_targets"]}
    assert target_ids == {"ch-1", "ch-2"}


# ================================================================
# 测试 5：worldview 摘要
# ================================================================

def test_summarize_worldview():
    """_summarize_worldview 应压缩世界观数据为简短文本。"""
    worldview = {
        "characters": [{"name": "段融"}, {"name": "赵穆"}, {"name": "孔斌"}],
        "locations": [{"name": "天工坊"}],
        "settings": [],
    }
    summary = ExploreV6._summarize_worldview(worldview)
    assert "段融" in summary
    assert "赵穆" in summary
    assert "天工坊" in summary
    assert "settings" not in summary


# ================================================================
# 测试 6：源码中关键方法存在
# ================================================================

def test_source_has_expected_methods():
    """验证源码包含新方法，不包含旧方法。"""
    source = SOURCE_PATH.read_text(encoding="utf-8")
    # 新方法
    assert "def generate_query(" in source
    assert "def execute_query(" in source
    assert "def enrich_chunks(" in source
    assert "get_gateway()" in source
    # 旧方法已删除
    assert "def decompose_queries(" not in source
    assert "def execute_parallel(" not in source
    assert "def locate_chunks(" not in source
    assert "_load_chapter_cache" not in source
