# -*- coding: utf-8 -*-
"""
搜索相关服务聚合。

当前仅提供 HybridRetriever（向量 + 全文混合检索）。
"""

from app.services.search.hybrid_retriever import HybridRetriever

__all__ = ["HybridRetriever"]
