"""
HTTP-based AI Service (Bypass Cloudflare blocking)

Direct httpx calls to OpenAI API, not using openai-python SDK
"""

import httpx
import json
import logging
from typing import AsyncGenerator
from app.core.config import settings
from app.services.ai.prompts import get_prompts_manager

logger = logging.getLogger(__name__)


class HTTPAIService:
    """基于 HTTP 的 AI 服务 - 直接调用 API 绕过 Cloudflare"""
    
    def __init__(self):
        """Initialize HTTP client and prompts manager"""
        self.api_key = settings.OPENAI_API_KEY
        self.base_url = settings.OPENAI_BASE_URL
        self.model = settings.OPENAI_MODEL
        self.prompts = get_prompts_manager()
        
        # 创建持久化客户端，模拟普通浏览器/应用
        self.client = httpx.AsyncClient(
            headers={
                "User-Agent": "okhttp/4.12.0",
                "Accept": "application/json",
                "Accept-Encoding": "gzip, deflate",
                "Connection": "keep-alive",
            },
            timeout=httpx.Timeout(60.0, connect=10.0),
            follow_redirects=True,
            http2=False,  # 使用 HTTP/1.1
        )
        
        logger.info(
            f"HTTP AI Service 初始化成功，Base URL: {self.base_url}, "
            f"Model: {self.model}"
        )
    
    async def close(self):
        """关闭 HTTP 客户端"""
        await self.client.aclose()
    
    async def _stream_chat(
        self,
        messages: list,
        max_tokens: int = 1000,
        temperature: float = 0.7
    ) -> AsyncGenerator[str, None]:
        """
        通用流式聊天方法
        
        Args:
            messages: 消息列表
            max_tokens: 最大token数
            temperature: 温度参数
            
        Yields:
            str: 流式响应的文本片段
        """
        url = f"{self.base_url}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": True
        }
        
        logger.info(
            f"开始调用 AI API: model={self.model}, "
            f"max_tokens={max_tokens}, temp={temperature}"
        )
        
        try:
            async with self.client.stream("POST", url, json=payload, headers=headers) as response:
                if response.status_code != 200:
                    error_text = await response.aread()
                    error_msg = error_text.decode('utf-8', errors='ignore')[:500]
                    logger.error(f"API 错误: {response.status_code}, {error_msg}")
                    raise Exception(f"API 请求失败: {response.status_code}")
                
                logger.info("API 流式响应已建立，开始接收数据...")
                chunk_count = 0
                
                async for line in response.aiter_lines():
                    line = line.strip()
                    
                    # SSE 格式: data: {...}
                    if not line or not line.startswith("data: "):
                        continue
                    
                    # 移除 "data: " 前缀
                    data_str = line[6:]
                    
                    # 结束标记
                    if data_str == "[DONE]":
                        logger.info(f"API 响应完成，共接收 {chunk_count} 个数据块")
                        break
                    
                    try:
                        data = json.loads(data_str)
                        
                        # 提取内容
                        if "choices" in data and len(data["choices"]) > 0:
                            choice = data["choices"][0]
                            
                            if "delta" in choice and "content" in choice["delta"]:
                                content = choice["delta"]["content"]
                                
                                if content and not self._should_filter(content):
                                    chunk_count += 1
                                    yield content
                    
                    except json.JSONDecodeError as e:
                        logger.warning(f"JSON 解析错误: {e}, 数据: {data_str[:100]}")
                        continue
        
        except httpx.HTTPError as e:
            logger.error(f"HTTP 请求错误: {type(e).__name__}: {str(e)}")
            raise Exception(f"网络请求失败: {str(e)}")
        
        except Exception as e:
            logger.error(f"AI API 调用错误: {type(e).__name__}: {str(e)}")
            raise
    
    async def stream_complete(
        self,
        context: str,
        prompt: str = "续写",
        style: str = "",
        max_tokens: int = 500,
        temperature: float = 0.7
    ) -> AsyncGenerator[str, None]:
        """AI 续写（流式响应）"""
        # 区分自动补全和正式续写
        is_autocomplete = max_tokens <= 150
        
        if is_autocomplete:
            system_prompt = self._build_autocomplete_system_prompt()
            logger.info(f"AI自动补全请求 - 上下文长度: {len(context)}")
        else:
            system_prompt = self._build_complete_system_prompt(prompt, style)
            logger.info(f"AI续写请求 - 上下文长度: {len(context)}, 风格: {style or '默认'}")
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": context}
        ]
        
        async for chunk in self._stream_chat(messages, max_tokens, temperature):
            yield chunk
    
    async def stream_polish(
        self,
        text: str,
        max_tokens: int = 1000,
        temperature: float = 0.5
    ) -> AsyncGenerator[str, None]:
        """AI Polish (streaming response)"""
        system_prompt, user_prefix = self.prompts.get_polish_prompt()
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"{user_prefix}{text}"}
        ]
        
        logger.info(f"AI Polish request - text length: {len(text)}")
        
        async for chunk in self._stream_chat(messages, max_tokens, temperature):
            yield chunk
    
    async def stream_translate(
        self,
        text: str,
        target_lang: str = "auto",
        max_tokens: int = 1000
    ) -> AsyncGenerator[str, None]:
        """AI Translate (streaming response)"""
        system_prompt = self.prompts.get_translate_prompt(target_lang)
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": text}
        ]
        
        logger.info(f"AI Translate request - text length: {len(text)}, target: {target_lang}")
        
        async for chunk in self._stream_chat(messages, max_tokens, temperature=0.3):
            yield chunk
    
    async def stream_expand(
        self,
        text: str,
        max_tokens: int = 1000,
        temperature: float = 0.7
    ) -> AsyncGenerator[str, None]:
        """AI Expand (streaming response)"""
        system_prompt, user_prefix = self.prompts.get_expand_prompt()
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"{user_prefix}{text}"}
        ]
        
        logger.info(f"AI Expand request - text length: {len(text)}")
        
        async for chunk in self._stream_chat(messages, max_tokens, temperature):
            yield chunk
    
    async def stream_summarize(
        self,
        text: str,
        max_tokens: int = 500,
        temperature: float = 0.3
    ) -> AsyncGenerator[str, None]:
        """AI Summarize (streaming response)"""
        system_prompt, user_prefix = self.prompts.get_summarize_prompt()
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"{user_prefix}{text}"}
        ]
        
        logger.info(f"AI Summarize request - text length: {len(text)}")
        
        async for chunk in self._stream_chat(messages, max_tokens, temperature):
            yield chunk
    
    def _build_autocomplete_system_prompt(self) -> str:
        """Build autocomplete system prompt from config"""
        return self.prompts.get_autocomplete_prompt()
    
    def _build_complete_system_prompt(self, prompt: str, style: str) -> str:
        """Build complete (continuation) system prompt from config"""
        return self.prompts.get_complete_prompt(prompt, style)
    
    def _should_filter(self, content: str) -> bool:
        """判断内容是否应该被过滤"""
        if not content:
            return True
        
        # 检查思考标签
        filter_patterns = ['<think>', '</think>', '<thinking>', '</thinking>']
        
        for pattern in filter_patterns:
            if pattern in content.lower():
                return True
        
        return False
