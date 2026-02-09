# -*- coding: utf-8 -*-
"""Compatibility shim.

旧 adaptive_controller 已废弃，统一迁移到 intent_retrieval V3。
"""

from app.services.agent.utils.intent_retrieval import AdaptiveController, AdaptiveRewrite

__all__ = ["AdaptiveController", "AdaptiveRewrite"]
