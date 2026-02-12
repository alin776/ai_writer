# -*- coding: utf-8 -*-
"""
Explore V6 单元测试

测试 ExploreV6 核心逻辑：单查询生成、LightRAG 调用、章节元数据补全、
段落级定位、结果组装。
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
# 测试 4：_match_paragraph 段落匹配
# ================================================================

def test_match_paragraph_finds_first_complete():
    """无 query_hint 时回退到最长匹配。"""
    paragraphs = [
        {"index": 0, "text": "这是第一段，很长的段落内容。", "node_id": "aaa"},
        {"index": 1, "text": "第二段内容在这里。", "node_id": "bbb"},
        {"index": 2, "text": "第三段也很精彩。", "node_id": "ccc"},
    ]
    # chunk 包含第二段和第三段（第一段被截断了）
    chunk_text = "...长的段落内容。第二段内容在这里。第三段也很精彩。后续内容..."

    result = ExploreV6._match_paragraph(chunk_text, paragraphs)
    # 第一段不完整（缺"这是第一段，很"），第二段完整匹配
    assert result == 1


def test_match_paragraph_returns_none_on_no_match():
    """无匹配时返回 None。"""
    paragraphs = [
        {"index": 0, "text": "完全不相关的内容。", "node_id": "aaa"},
    ]
    chunk_text = "这段话和段落没有任何关系"

    result = ExploreV6._match_paragraph(chunk_text, paragraphs)
    assert result is None


def test_match_paragraph_skips_short():
    """跳过过短的段落（<6字符）。"""
    paragraphs = [
        {"index": 0, "text": "短", "node_id": "aaa"},
        {"index": 1, "text": "这是足够长的段落内容。", "node_id": "bbb"},
    ]
    chunk_text = "短这是足够长的段落内容。后面的文字"

    result = ExploreV6._match_paragraph(chunk_text, paragraphs)
    assert result == 1  # 跳过"短"，匹配第二段


def test_match_paragraph_prefers_query_relevant():
    """chunk 跨多段时，优先选与 query_hint 字符重叠最多的段落。"""
    paragraphs = [
        {"index": 0, "text": "赵穆每天晚上都会去后院练刀。", "node_id": "a"},
        {"index": 1, "text": "他已经坚持了三个月，风雨无阻。", "node_id": "b"},
        {"index": 2, "text": "今晚练到一半，人刀相应的感觉突然消失了。", "node_id": "c"},
        {"index": 3, "text": "赵穆停下来，皱起眉头反复思量。", "node_id": "d"},
    ]
    # chunk 包含全部四段
    chunk_text = (
        "赵穆每天晚上都会去后院练刀。"
        "他已经坚持了三个月，风雨无阻。"
        "今晚练到一半，人刀相应的感觉突然消失了。"
        "赵穆停下来，皱起眉头反复思量。"
    )
    # 用户关心 "人刀相应的感觉消失了"
    result = ExploreV6._match_paragraph(
        chunk_text, paragraphs, query_hint="人刀相应的感觉消失了"
    )
    assert result == 2  # 选中 index 2（含"人刀相应"关键字符）


# ================================================================
# 测试 5：locate_in_chapters 段落级定位
# ================================================================

@pytest.mark.asyncio
async def test_locate_in_chapters():
    """locate_in_chapters 应补全 paragraph_index / node_id / anchors。"""
    v6 = _build_v6()

    chunks = [
        {
            "chapter_id": "ch-1",
            "text": "村里住着数百户人家。少年林风，今年十六岁。",
        },
    ]

    mock_paragraphs = [
        {"index": 0, "text": "青云山脚下，有一个名叫青云村的小村庄。", "node_id": "n0", "preview": ""},
        {"index": 1, "text": "村里住着数百户人家。", "node_id": "n1", "preview": ""},
        {"index": 2, "text": "少年林风，今年十六岁。", "node_id": "n2", "preview": ""},
        {"index": 3, "text": "这一天，林风挑着水桶去打水。", "node_id": "n3", "preview": ""},
    ]

    with patch.object(v6, "_load_chapter_content", return_value="<p>fake</p>"):
        with patch("app.services.agent.tools.locate_tools._split_paragraphs", return_value=mock_paragraphs):
            result = await v6.locate_in_chapters(chunks)

    c = result[0]
    # _match_paragraph 返回最长匹配（最具体段落），
    # chunk 中 "少年林风，今年十六岁。"(11字) > "村里住着数百户人家。"(10字)
    assert c["paragraph_index"] == 2
    assert c["node_id"] == "n2"
    assert c["located_text"] == "少年林风，今年十六岁。"
    assert c["before_anchor"] == "村里住着数百户人家。"
    assert c["after_anchor"] == "这一天，林风挑着水桶去打水。"


# ================================================================
# 测试 6：_build_result 包含段落级字段
# ================================================================

def test_build_result_with_paragraph_info():
    """_build_result 的 locate_targets 应包含 paragraph_index / node_id。"""
    v6 = _build_v6()
    result = v6._build_result(
        evidences=[
            {
                "text": "test", "chapter_order": 1, "chapter_id": "ch-1",
                "paragraph_index": 5, "node_id": "abc",
                "located_text": "test para", "before_anchor": "prev", "after_anchor": "next",
            },
            {
                "text": "test2", "chapter_order": 1, "chapter_id": "ch-1",
                "paragraph_index": 8, "node_id": "def",
                "located_text": "test para2", "before_anchor": "", "after_anchor": "",
            },
        ],
        chapters_info=[{"id": "ch-1", "order": 1, "title": "第一章", "word_count": 3000}],
        worldview={},
        stop_reason="测试",
        duration_ms=50,
    )

    targets = result["locate_targets"]
    assert len(targets) == 2  # 同一章节不同段落 → 两个 target
    assert targets[0]["paragraph_index"] == 5
    assert targets[0]["node_id"] == "abc"
    assert targets[0]["text"] == "test para"
    assert targets[0]["before_anchor"] == "prev"
    assert targets[1]["paragraph_index"] == 8


def test_build_result_dedup_same_paragraph():
    """同一 chapter_id + 同一 paragraph_index 应去重。"""
    v6 = _build_v6()
    result = v6._build_result(
        evidences=[
            {"text": "a", "chapter_order": 1, "chapter_id": "ch-1", "paragraph_index": 3},
            {"text": "b", "chapter_order": 1, "chapter_id": "ch-1", "paragraph_index": 3},
        ],
        chapters_info=[], worldview={}, stop_reason="", duration_ms=0,
    )
    assert len(result["locate_targets"]) == 1


# ================================================================
# 测试 7：worldview 摘要
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
# 测试 8：源码中关键方法存在
# ================================================================

def test_source_has_expected_methods():
    """验证源码包含新方法，不包含旧方法。"""
    source = SOURCE_PATH.read_text(encoding="utf-8")
    # 新方法
    assert "def generate_query(" in source
    assert "def execute_query(" in source
    assert "def enrich_chunks(" in source
    assert "def locate_in_chapters(" in source
    assert "def _match_paragraph(" in source
    assert "def _load_chapter_content(" in source
    assert "get_gateway()" in source
    # 旧方法已删除
    assert "def decompose_queries(" not in source
    assert "def execute_parallel(" not in source
    assert "def locate_chunks(" not in source
    assert "_load_chapter_cache" not in source
