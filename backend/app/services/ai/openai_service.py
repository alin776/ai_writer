"""
OpenAI 服务封装

提供对 OpenAI API 的封装，支持：
- 流式响应（Server-Sent Events）
- 多种 AI 功能（续写、润色、翻译、扩写、总结）
- 自动过滤思考标签
- 错误处理和日志记录
"""

from openai import AsyncOpenAI
from typing import AsyncGenerator, Optional
import logging
from app.core.config import settings

logger = logging.getLogger(__name__)


class OpenAIService:
    """OpenAI 服务类 - 支持流式响应"""
    
    def __init__(self):
        """初始化 OpenAI 客户端"""
        import httpx
        
        # 创建自定义 HTTP 客户端，模拟 Java/OkHttp 请求特征绕过 Cloudflare
        http_client = httpx.AsyncClient(
            timeout=60.0,
            follow_redirects=True,
            # 使用 HTTP/1.1（更像传统客户端）
            http2=False,
        )
        
        self.client = AsyncOpenAI(
            api_key=settings.OPENAI_API_KEY,
            base_url=settings.OPENAI_BASE_URL,
            http_client=http_client,
            # 关键：在 SDK 级别设置自定义 headers
            default_headers={
                "User-Agent": "okhttp/4.12.0",
                "Accept": "*/*",
                "Accept-Encoding": "gzip, deflate",
                "Connection": "keep-alive",
            }
        )
        self.default_model = settings.OPENAI_MODEL
        logger.info(
            f"OpenAI Service 初始化成功（模拟 Java 客户端），Base URL: {settings.OPENAI_BASE_URL}, "
            f"Model: {self.default_model}"
        )
    
    async def stream_complete(
        self,
        context: str,
        prompt: str = "续写",
        style: str = "",
        max_tokens: int = 500,
        temperature: float = 0.7
    ) -> AsyncGenerator[str, None]:
        """
        AI 续写（流式响应）
        
        Args:
            context: 上下文内容（用户已写的内容）
            prompt: 续写指令（如"续写"、"继续写"等）
            style: 写作风格（如"玄幻小说"、"现代都市"等）
            max_tokens: 最大生成token数
            temperature: 温度参数，控制创意度（0.0-2.0）
            
        Yields:
            str: 流式输出的文本片段
        """
        system_prompt = self._build_complete_system_prompt(prompt, style)
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": context}
        ]
        
        logger.info(f"AI续写请求 - 上下文长度: {len(context)}, 风格: {style or '默认'}")
        
        try:
            async for chunk in self._stream_chat(messages, max_tokens, temperature):
                yield chunk
                
        except Exception as e:
            logger.error(f"AI续写错误: {e}")
            raise
    
    async def stream_polish(
        self,
        text: str,
        max_tokens: int = 1000,
        temperature: float = 0.5
    ) -> AsyncGenerator[str, None]:
        """
        AI 润色（流式响应）
        
        Args:
            text: 待润色的文本
            max_tokens: 最大生成token数
            temperature: 温度参数
            
        Yields:
            str: 润色后的文本片段
        """
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
        
        try:
            async for chunk in self._stream_chat(messages, max_tokens, temperature):
                yield chunk
                
        except Exception as e:
            logger.error(f"AI润色错误: {e}")
            raise
    
    async def stream_translate(
        self,
        text: str,
        target_lang: str = "auto",
        max_tokens: int = 1000
    ) -> AsyncGenerator[str, None]:
        """
        AI 翻译（流式响应）
        
        Args:
            text: 待翻译的文本
            target_lang: 目标语言（auto/english/chinese）
            max_tokens: 最大生成token数
            
        Yields:
            str: 翻译结果片段
        """
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
        
        try:
            async for chunk in self._stream_chat(messages, max_tokens, temperature=0.3):
                yield chunk
                
        except Exception as e:
            logger.error(f"AI翻译错误: {e}")
            raise
    
    async def stream_expand(
        self,
        text: str,
        max_tokens: int = 1000,
        temperature: float = 0.7
    ) -> AsyncGenerator[str, None]:
        """
        AI 扩写（流式响应）
        
        Args:
            text: 待扩写的文本
            max_tokens: 最大生成token数
            temperature: 温度参数
            
        Yields:
            str: 扩写后的文本片段
        """
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
        
        try:
            async for chunk in self._stream_chat(messages, max_tokens, temperature):
                yield chunk
                
        except Exception as e:
            logger.error(f"AI扩写错误: {e}")
            raise
    
    async def stream_summarize(
        self,
        text: str,
        max_tokens: int = 500,
        temperature: float = 0.3
    ) -> AsyncGenerator[str, None]:
        """
        AI 总结（流式响应）
        
        Args:
            text: 待总结的文本
            max_tokens: 最大生成token数
            temperature: 温度参数
            
        Yields:
            str: 总结后的文本片段
        """
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
        
        try:
            async for chunk in self._stream_chat(messages, max_tokens, temperature):
                yield chunk
                
        except Exception as e:
            logger.error(f"AI总结错误: {e}")
            raise
    
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
        try:
            logger.info(f"开始调用 OpenAI API: model={self.default_model}, max_tokens={max_tokens}, temp={temperature}")
            
            stream = await self.client.chat.completions.create(
                model=self.default_model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                stream=True
            )
            
            logger.info("OpenAI API 流式响应已建立，开始接收数据...")
            chunk_count = 0
            
            async for chunk in stream:
                chunk_count += 1
                if chunk.choices and chunk.choices[0].delta.content:
                    content = chunk.choices[0].delta.content
                    
                    # 过滤思考标签和推理内容
                    if not self._should_filter(content):
                        yield content
            
            logger.info(f"OpenAI API 响应完成，共接收 {chunk_count} 个数据块")
                        
        except Exception as e:
            logger.error(f"OpenAI API 调用错误: {type(e).__name__}: {str(e)}")
            logger.error(f"错误详情: {repr(e)}", exc_info=True)
            raise
    
    def _build_complete_system_prompt(self, prompt: str, style: str) -> str:
        """
        构建续写的系统提示词
        
        Args:
            prompt: 续写指令
            style: 写作风格
            
        Returns:
            str: 系统提示词
        """
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
        """
        判断内容是否应该被过滤
        
        过滤规则：
        - 包含 <think> 标签
        - 包含 </think> 标签
        - 包含 "reasoning" 关键词（某些模型的思考内容）
        
        Args:
            content: 待检查的内容
            
        Returns:
            bool: True 表示应该过滤，False 表示保留
        """
        if not content:
            return True
        
        # 检查思考标签
        filter_patterns = ['<think>', '</think>', '<thinking>', '</thinking>']
        
        for pattern in filter_patterns:
            if pattern in content.lower():
                return True
        
        return False
