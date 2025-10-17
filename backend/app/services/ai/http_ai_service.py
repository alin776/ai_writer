"""
基于 HTTP 的 AI 服务（绕过 Cloudflare 拦截）

直接使用 httpx 调用 OpenAI API，不使用 openai-python SDK
"""

import httpx
import json
import logging
from typing import AsyncGenerator
from app.core.config import settings

logger = logging.getLogger(__name__)


class HTTPAIService:
    """基于 HTTP 的 AI 服务 - 直接调用 API 绕过 Cloudflare"""
    
    def __init__(self):
        """初始化 HTTP 客户端"""
        self.api_key = settings.OPENAI_API_KEY
        self.base_url = settings.OPENAI_BASE_URL
        self.model = settings.OPENAI_MODEL
        
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
        system_prompt = self._build_complete_system_prompt(prompt, style)
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": context}
        ]
        
        logger.info(f"AI续写请求 - 上下文长度: {len(context)}, 风格: {style or '默认'}")
        
        async for chunk in self._stream_chat(messages, max_tokens, temperature):
            yield chunk
    
    async def stream_polish(
        self,
        text: str,
        max_tokens: int = 1000,
        temperature: float = 0.5
    ) -> AsyncGenerator[str, None]:
        """AI 润色（流式响应）"""
        messages = [
            {
                "role": "system",
                "content": (
                    "你是专业的文本润色助手。你的任务是优化文字表达，使其更加流畅、生动、富有感染力。\n\n"
                    "要求：\n"
                    "- 保持原文的核心意思和情节\n"
                    "- 优化词汇选择，使表达更精准\n"
                    "- 改善句式结构，提升可读性\n"
                    "- 增强情感表达和画面感\n"
                    "- 只返回润色后的文本，不要添加说明"
                )
            },
            {
                "role": "user",
                "content": f"请润色以下文本：\n\n{text}"
            }
        ]
        
        logger.info(f"AI润色请求 - 文本长度: {len(text)}")
        
        async for chunk in self._stream_chat(messages, max_tokens, temperature):
            yield chunk
    
    async def stream_translate(
        self,
        text: str,
        target_lang: str = "auto",
        max_tokens: int = 1000
    ) -> AsyncGenerator[str, None]:
        """AI 翻译（流式响应）"""
        if target_lang == "auto":
            instruction = "智能识别语言并翻译。如果是中文则翻译成英文，如果是英文则翻译成中文。"
        elif target_lang == "english":
            instruction = "翻译成英文。"
        elif target_lang == "chinese":
            instruction = "翻译成中文。"
        else:
            instruction = f"翻译成{target_lang}。"
        
        messages = [
            {
                "role": "system",
                "content": (
                    f"你是专业的翻译助手。{instruction}\n\n"
                    "要求：\n"
                    "- 准确传达原文意思\n"
                    "- 符合目标语言的表达习惯\n"
                    "- 保持原文的语气和风格\n"
                    "- 只返回翻译结果，不要添加说明"
                )
            },
            {
                "role": "user",
                "content": text
            }
        ]
        
        logger.info(f"AI翻译请求 - 文本长度: {len(text)}, 目标语言: {target_lang}")
        
        async for chunk in self._stream_chat(messages, max_tokens, temperature=0.3):
            yield chunk
    
    async def stream_expand(
        self,
        text: str,
        max_tokens: int = 1000,
        temperature: float = 0.7
    ) -> AsyncGenerator[str, None]:
        """AI 扩写（流式响应）"""
        messages = [
            {
                "role": "system",
                "content": (
                    "你是专业的扩写助手。你的任务是在保持原文核心内容的基础上，丰富细节和表达。\n\n"
                    "要求：\n"
                    "- 保持原文的核心情节和主旨\n"
                    "- 增加环境描写、心理描写和动作描写\n"
                    "- 扩展对话和细节，增强代入感\n"
                    "- 使场景更加生动、立体\n"
                    "- 只返回扩写后的文本，不要添加说明"
                )
            },
            {
                "role": "user",
                "content": f"请扩写以下内容：\n\n{text}"
            }
        ]
        
        logger.info(f"AI扩写请求 - 文本长度: {len(text)}")
        
        async for chunk in self._stream_chat(messages, max_tokens, temperature):
            yield chunk
    
    async def stream_summarize(
        self,
        text: str,
        max_tokens: int = 500,
        temperature: float = 0.3
    ) -> AsyncGenerator[str, None]:
        """AI 总结（流式响应）"""
        messages = [
            {
                "role": "system",
                "content": (
                    "你是专业的总结助手。你的任务是提取核心信息，生成简洁的摘要。\n\n"
                    "要求：\n"
                    "- 保留关键情节和重要信息\n"
                    "- 去除冗余和次要细节\n"
                    "- 逻辑清晰，语言简练\n"
                    "- 控制在原文长度的30%以内\n"
                    "- 只返回总结内容，不要添加说明"
                )
            },
            {
                "role": "user",
                "content": f"请总结以下内容：\n\n{text}"
            }
        ]
        
        logger.info(f"AI总结请求 - 文本长度: {len(text)}")
        
        async for chunk in self._stream_chat(messages, max_tokens, temperature):
            yield chunk
    
    def _build_complete_system_prompt(self, prompt: str, style: str) -> str:
        """构建续写的系统提示词"""
        base_prompt = (
            "你是一位专业的小说创作助手，擅长续写、扩写和润色小说内容。"
            "你的写作风格自然流畅，善于刻画人物、描写场景、推动情节发展。"
        )
        
        if style:
            base_prompt += f"\n\n写作风格：{style}"
        
        base_prompt += f"\n\n任务：根据用户提供的上下文，进行{prompt}。"
        
        base_prompt += (
            "\n\n要求：\n"
            "- 保持与上文的叙述风格一致\n"
            "- 情节发展自然合理\n"
            "- 人物性格符合设定\n"
            "- 控制在200-500字之间\n"
            "- 直接开始续写，不要添加说明性文字"
        )
        
        return base_prompt
    
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
