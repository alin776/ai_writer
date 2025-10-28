"""
HTTP-based AI Service (Bypass Cloudflare blocking)

Direct httpx calls to OpenAI API, not using openai-python SDK
"""

import httpx
import json
import logging
import asyncio
from typing import AsyncGenerator
from app.core.config import settings
from app.services.ai.prompts import get_prompts_manager

logger = logging.getLogger(__name__)


class HTTPAIService:
    """基于 HTTP 的 AI 服务 - 直接调用 API 绕过 Cloudflare"""

    def __init__(self, model: str = None, timeout: int = None):
        """Initialize HTTP client and prompts manager

        Args:
            model: 指定模型名称,如果不提供则使用默认配置
            timeout: 超时时间(秒),如果不提供则使用默认配置
        """
        self.api_key = settings.OPENAI_API_KEY
        self.base_url = settings.OPENAI_BASE_URL
        self.model = model or settings.OPENAI_MODEL  # 支持自定义模型
        timeout_value = timeout or settings.OPENAI_TIMEOUT  # 支持自定义超时
        self.prompts = get_prompts_manager()

        # 创建持久化客户端，模拟普通浏览器/应用
        self.client = httpx.AsyncClient(
            headers={
                "User-Agent": "okhttp/4.12.0",
                "Accept": "application/json",
                "Accept-Encoding": "gzip, deflate",
                "Connection": "keep-alive",
            },
            timeout=httpx.Timeout(
                timeout_value,  # 使用可配置的超时
                connect=10.0
            ),
            follow_redirects=True,
            http2=False,  # 使用 HTTP/1.1
        )

        logger.info(
            f"HTTP AI Service 初始化成功，Base URL: {self.base_url}, "
            f"Model: {self.model}, Timeout: {timeout_value}s"
        )
    
    async def close(self):
        """关闭 HTTP 客户端"""
        await self.client.aclose()
    
    async def _stream_chat(
        self,
        messages: list,
        max_tokens: int = 1000,
        temperature: float = 0.7
    ) -> AsyncGenerator[tuple[str, dict | None], None]:
        """
        通用流式聊天方法

        Args:
            messages: 消息列表
            max_tokens: 最大token数
            temperature: 温度参数

        Yields:
            tuple: (文本片段, usage统计或None)
                - 文本片段: str
                - usage: 仅在最后一个块返回完整usage,其他为None
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
                total_content = ""
                usage_info = None  # 用于存储最终的usage信息

                async for line in response.aiter_lines():
                    line = line.strip()

                    # SSE 格式: data: {...}
                    if not line or not line.startswith("data: "):
                        continue

                    # 移除 "data: " 前缀
                    data_str = line[6:]

                    # 结束标记
                    if data_str == "[DONE]":
                        logger.info(
                            f"API 响应完成，共接收 {chunk_count} 个数据块，总长度: {len(total_content)}"
                        )
                        # 记录usage统计
                        if usage_info:
                            logger.info(
                                f"流式响应Token统计: {usage_info.get('total_tokens', 0)} "
                                f"(prompt={usage_info.get('prompt_tokens', 0)}, "
                                f"completion={usage_info.get('completion_tokens', 0)})"
                            )
                        break

                    try:
                        data = json.loads(data_str)

                        # 提取usage信息(通常在最后一个块)
                        if "usage" in data:
                            usage_info = data["usage"]

                        # 提取内容
                        if "choices" in data and len(data["choices"]) > 0:
                            choice = data["choices"][0]

                            if "delta" in choice and "content" in choice["delta"]:
                                content = choice["delta"]["content"]

                                # 修复: Gemini API 第一个块的 content 可能是 null
                                if content is not None and content and not self._should_filter(content):
                                    chunk_count += 1
                                    total_content += content
                                    yield content, None  # 中间块不返回usage

                    except json.JSONDecodeError as e:
                        logger.warning(f"JSON 解析错误: {e}, 数据: {data_str[:100]}")
                        continue

                # 循环结束后,yield最终的usage信息
                if usage_info:
                    yield "", usage_info  # 空内容块 + 完整usage统计
                else:
                    logger.warning("流式响应未返回usage信息")

                # 如果没有接收到任何内容，记录警告
                if chunk_count == 0:
                    logger.error(f"警告: AI 响应为空！未接收到任何内容块。")
        
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
    ) -> AsyncGenerator[tuple[str, dict | None], None]:
        """AI 续写（流式响应）

        Yields:
            tuple: (文本片段, usage统计或None)
        """
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

        async for chunk, usage in self._stream_chat(messages, max_tokens, temperature):
            yield chunk, usage
    
    async def stream_polish(
        self,
        text: str,
        max_tokens: int = 1000,
        temperature: float = 0.5
    ) -> AsyncGenerator[tuple[str, dict | None], None]:
        """AI Polish (streaming response)

        Yields:
            tuple: (文本片段, usage统计或None)
        """
        system_prompt, user_prefix = self.prompts.get_polish_prompt()
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"{user_prefix}{text}"}
        ]
        
        logger.info(f"AI Polish request - text length: {len(text)}")

        async for chunk, usage in self._stream_chat(messages, max_tokens, temperature):
            yield chunk, usage
    
    async def stream_translate(
        self,
        text: str,
        target_lang: str = "auto",
        max_tokens: int = 1000
    ) -> AsyncGenerator[tuple[str, dict | None], None]:
        """AI Translate (streaming response)

        Yields:
            tuple: (文本片段, usage统计或None)
        """
        system_prompt = self.prompts.get_translate_prompt(target_lang)
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": text}
        ]
        
        logger.info(f"AI Translate request - text length: {len(text)}, target: {target_lang}")

        async for chunk, usage in self._stream_chat(messages, max_tokens, temperature=0.3):
            yield chunk, usage
    
    async def stream_expand(
        self,
        text: str,
        max_tokens: int = 1000,
        temperature: float = 0.7
    ) -> AsyncGenerator[tuple[str, dict | None], None]:
        """AI Expand (streaming response)

        Yields:
            tuple: (文本片段, usage统计或None)
        """
        system_prompt, user_prefix = self.prompts.get_expand_prompt()
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"{user_prefix}{text}"}
        ]
        
        logger.info(f"AI Expand request - text length: {len(text)}")

        async for chunk, usage in self._stream_chat(messages, max_tokens, temperature):
            yield chunk, usage
    
    async def stream_summarize(
        self,
        text: str,
        max_tokens: int = 500,
        temperature: float = 0.3
    ) -> AsyncGenerator[tuple[str, dict | None], None]:
        """AI Summarize (streaming response)

        Yields:
            tuple: (文本片段, usage统计或None)
        """
        system_prompt, user_prefix = self.prompts.get_summarize_prompt()
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"{user_prefix}{text}"}
        ]
        
        logger.info(f"AI Summarize request - text length: {len(text)}")

        async for chunk, usage in self._stream_chat(messages, max_tokens, temperature):
            yield chunk, usage
    
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

    async def call_ai(
        self,
        system_prompt: str,
        user_prompt: str,
        max_tokens: int = 2000,
        temperature: float = 0.7,
        max_retries: int = 3
    ) -> str:
        """
        非流式AI调用 (用于评审等需要完整响应的场景,带重试机制)

        Args:
            system_prompt: 系统提示词
            user_prompt: 用户提示词
            max_tokens: 最大token数
            temperature: 温度参数
            max_retries: 最大重试次数(默认3次)

        Returns:
            完整的AI响应文本
        """
        url = f"{self.base_url}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": False  # 非流式
        }

        # 重试机制
        for attempt in range(max_retries):
            try:
                if attempt > 0:
                    # 指数退避: 2秒, 4秒, 8秒
                    wait_time = 2 ** attempt
                    logger.warning(
                        f"AI调用失败,进行第{attempt}次重试 (共{max_retries - 1}次重试机会), "
                        f"等待 {wait_time}秒后重试..."
                    )
                    await asyncio.sleep(wait_time)

                logger.info(
                    f"开始非流式AI调用: max_tokens={max_tokens}, temp={temperature}, "
                    f"尝试={attempt + 1}/{max_retries}"
                )

                response = await self.client.post(url, json=payload, headers=headers)

                if response.status_code != 200:
                    error_text = response.text
                    logger.error(f"API错误: {response.status_code}, {error_text[:500]}")

                    # 如果是服务器错误(5xx)或超时(429),可以重试
                    if response.status_code >= 500 or response.status_code == 429:
                        if attempt < max_retries - 1:
                            continue  # 重试

                    raise Exception(f"API请求失败: {response.status_code}")

                data = response.json()
                content = data['choices'][0]['message']['content']

                logger.info(
                    f"AI响应成功, 长度={len(content)}, "
                    f"尝试次数={attempt + 1}"
                )
                return content

            except httpx.ReadTimeout as e:
                logger.error(
                    f"AI调用超时 (尝试 {attempt + 1}/{max_retries}): {str(e)}"
                )
                if attempt < max_retries - 1:
                    continue  # 重试
                else:
                    logger.error(f"AI调用超时,已重试{max_retries}次,全部失败")
                    raise Exception(f"网络请求超时,已重试{max_retries}次")

            except httpx.HTTPError as e:
                logger.error(
                    f"HTTP请求错误 (尝试 {attempt + 1}/{max_retries}): "
                    f"{type(e).__name__}: {str(e)}"
                )
                if attempt < max_retries - 1:
                    continue  # 重试
                else:
                    logger.error(f"HTTP请求失败,已重试{max_retries}次,全部失败")
                    raise Exception(f"网络请求失败: {str(e)}")

            except Exception as e:
                logger.error(
                    f"AI调用错误 (尝试 {attempt + 1}/{max_retries}): "
                    f"{type(e).__name__}: {str(e)}"
                )
                # 其他异常不重试
                raise

        # 理论上不会到这里
        raise Exception(f"AI调用失败,已重试{max_retries}次")
