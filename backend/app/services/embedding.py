"""
共享 Embedding 模型加载器（单例）

统一全局只加载一个 SentenceTransformer 模型，避免多个模块各自加载导致内存翻倍。
"""
import logging
import os
import time
from pathlib import Path
from typing import Optional

# 提前配置 HuggingFace 端点与缓存目录
_default_hf_endpoint = os.getenv("HF_ENDPOINT", "https://hf-mirror.com")
os.environ.setdefault("HF_ENDPOINT", _default_hf_endpoint)
_hf_cache_dir = Path(__file__).resolve().parents[2] / "data" / "hf_cache"
_hf_cache_dir.mkdir(parents=True, exist_ok=True)
os.environ.setdefault("HF_HOME", str(_hf_cache_dir))
os.environ.setdefault("HF_HUB_CACHE", str(_hf_cache_dir))

from sentence_transformers import SentenceTransformer

logger = logging.getLogger(__name__)

MODEL_NAME = "BAAI/bge-small-zh-v1.5"
VECTOR_DIM = 512
CACHE_DIR = _hf_cache_dir

_global_model: Optional[SentenceTransformer] = None


def preload_model() -> None:
    """应用启动时预加载模型，避免首次调用时的 ~7 秒延迟。"""
    global _global_model
    if _global_model is not None:
        return
    logger.info("🔄 预加载 Embedding 模型: %s", MODEL_NAME)
    start = time.time()
    _global_model = SentenceTransformer(MODEL_NAME, cache_folder=str(CACHE_DIR))
    logger.info("✅ Embedding 模型预加载完成，耗时: %.2f 秒", time.time() - start)


def get_model() -> SentenceTransformer:
    """获取全局共享的 SentenceTransformer 实例（懒加载）。"""
    global _global_model
    if _global_model is None:
        preload_model()
    return _global_model
