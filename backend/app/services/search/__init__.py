# -*- coding: utf-8 -*-
"""
搜索相关服务聚合。

采用惰性导入，避免无关依赖影响模块加载。
"""

from typing import Any

__all__ = ["HybridRetriever", "OpenSearchChapterSearchService"]


def __getattr__(name: str) -> Any:
    if name == "HybridRetriever":
        from app.services.search.hybrid_retriever import HybridRetriever
        return HybridRetriever
    if name == "OpenSearchChapterSearchService":
        from app.services.search.opensearch_chapter_search_service import (
            OpenSearchChapterSearchService,
        )
        return OpenSearchChapterSearchService
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
