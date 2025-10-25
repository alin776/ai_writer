"""
文本智能分析服务

使用 LangChain PydanticOutputParser 进行结构化输出解析
分析文本质量，检测问题，给出改写建议
"""

import httpx
import json
import logging
from typing import Optional
from langchain_core.output_parsers import PydanticOutputParser

from app.core.config import settings
from app.schemas.text_analysis import (
    TextAnalysisResult,
    RewriteMode,
    TextIssue,
    IssueSeverity,
    IssueType
)

logger = logging.getLogger(__name__)


class TextAnalyzer:
    """文本智能分析器 - 使用 LangChain 结构化输出"""

    def __init__(self):
        """初始化分析器"""
        self.api_key = settings.OPENAI_API_KEY
        self.base_url = settings.OPENAI_BASE_URL
        self.model = settings.OPENAI_MODEL

        # 创建 HTTP 客户端
        self.client = httpx.AsyncClient(
            headers={
                "User-Agent": "okhttp/4.12.0",
                "Accept": "application/json",
                "Accept-Encoding": "gzip, deflate",
                "Connection": "keep-alive",
            },
            timeout=httpx.Timeout(30.0, connect=10.0),
            follow_redirects=True,
            http2=False,
        )

        # 创建 Pydantic 输出解析器
        self.parser = PydanticOutputParser(pydantic_object=TextAnalysisResult)

        logger.info(
            f"TextAnalyzer 初始化成功，Base URL: {self.base_url}, "
            f"Model: {self.model}"
        )

    async def close(self):
        """关闭 HTTP 客户端"""
        await self.client.aclose()

    def _build_analysis_prompt(
        self,
        text: str,
        context_before: Optional[str] = None,
        context_after: Optional[str] = None
    ) -> str:
        """
        构建文本分析提示词

        Args:
            text: 待分析的文本
            context_before: 前文上下文
            context_after: 后文上下文

        Returns:
            str: 完整的提示词
        """
        # 获取格式说明
        format_instructions = self.parser.get_format_instructions()

        # 构建上下文部分
        context_info = ""
        if context_before:
            context_info += f"\n【前文上下文】\n{context_before}\n"
        if context_after:
            context_info += f"\n【后文上下文】\n{context_after}\n"

        # 构建完整提示词
        prompt = f"""你是一位专业的小说编辑，擅长分析文本质量并给出改进建议。

请仔细分析以下文本，从多个维度评估其质量：

【待分析文本】
{text}
{context_info}

请按照以下维度进行分析：
1. **描写质量** - 是否生动具体，有画面感
2. **情感渲染** - 是否有情感深度和感染力
3. **细节丰富度** - 是否有足够的细节支撑
4. **逻辑连贯性** - 前后是否连贯合理
5. **节奏感** - 叙述节奏是否合适
6. **语言表达** - 遣词造句是否准确优美

基于分析结果：
1. 给出质量评分（0-100分）
2. 列出主要问题（每个问题包含类型、严重程度、描述）
3. 推荐最合适的改写模式：
   - optimize: 优化提升（让文字更优美生动）
   - expand: 扩写丰富（增加细节和情感渲染）
   - compress: 精简压缩（保留核心删除冗余）
4. 说明推荐理由

{format_instructions}

请严格按照上述 JSON 格式输出，确保是有效的 JSON。
"""
        return prompt

    async def analyze_text(
        self,
        text: str,
        context_before: Optional[str] = None,
        context_after: Optional[str] = None
    ) -> TextAnalysisResult:
        """
        分析文本质量

        Args:
            text: 待分析的文本
            context_before: 前文上下文
            context_after: 后文上下文

        Returns:
            TextAnalysisResult: 分析结果

        Raises:
            Exception: API 调用失败或解析失败
        """
        prompt = self._build_analysis_prompt(text, context_before, context_after)

        messages = [
            {
                "role": "system",
                "content": "你是一位专业的小说编辑，擅长分析文本质量。请始终返回有效的 JSON 格式数据。"
            },
            {
                "role": "user",
                "content": prompt
            }
        ]

        logger.info(f"开始分析文本，长度: {len(text)} 字")

        try:
            # 调用 AI API（非流式）
            response_text = await self._call_api(messages)

            # 使用 LangChain 解析器解析响应
            result = self.parser.parse(response_text)

            logger.info(
                f"文本分析完成，评分: {result.quality_score}, "
                f"问题数: {len(result.issues)}, "
                f"推荐模式: {result.recommended_mode}"
            )

            return result

        except Exception as e:
            logger.error(f"文本分析失败: {type(e).__name__}: {str(e)}")
            # 返回默认分析结果
            return self._get_fallback_result(text)

    async def _call_api(
        self,
        messages: list,
        temperature: float = 0.3,
        max_tokens: int = 1000
    ) -> str:
        """
        调用 AI API 获取完整响应

        Args:
            messages: 消息列表
            temperature: 温度参数（分析任务用较低温度）
            max_tokens: 最大token数

        Returns:
            str: API 响应的完整文本

        Raises:
            Exception: API 调用失败
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
            "stream": False  # 非流式
        }

        try:
            response = await self.client.post(url, json=payload, headers=headers)

            if response.status_code != 200:
                error_text = response.text[:500]
                logger.error(f"API 错误: {response.status_code}, {error_text}")
                raise Exception(f"API 请求失败: {response.status_code}")

            data = response.json()

            # 提取内容
            if "choices" in data and len(data["choices"]) > 0:
                content = data["choices"][0]["message"]["content"]
                return content
            else:
                raise Exception("API 响应格式错误")

        except httpx.HTTPError as e:
            logger.error(f"HTTP 请求错误: {type(e).__name__}: {str(e)}")
            raise Exception(f"网络请求失败: {str(e)}")

    def _get_fallback_result(self, text: str) -> TextAnalysisResult:
        """
        获取降级分析结果（当 AI 调用失败时）

        Args:
            text: 原文本

        Returns:
            TextAnalysisResult: 简单的分析结果
        """
        # 简单的启发式分析
        text_length = len(text)

        # 根据长度判断问题
        issues = []
        recommended_mode = RewriteMode.OPTIMIZE

        if text_length < 30:
            issues.append(TextIssue(
                type=IssueType.TOO_SIMPLE,
                severity=IssueSeverity.HIGH,
                description="文本过短，描写过于简单"
            ))
            recommended_mode = RewriteMode.EXPAND
        elif text_length > 300:
            issues.append(TextIssue(
                type=IssueType.REPETITIVE,
                severity=IssueSeverity.MEDIUM,
                description="文本较长，可能存在冗余"
            ))
            recommended_mode = RewriteMode.COMPRESS

        # 默认添加通用问题
        if not issues:
            issues.append(TextIssue(
                type=IssueType.LACK_EMOTION,
                severity=IssueSeverity.MEDIUM,
                description="可以增加更多情感渲染"
            ))

        # 计算评分（简单规则）
        quality_score = max(30, min(70, 50 + (text_length - 50) // 10))

        return TextAnalysisResult(
            quality_score=quality_score,
            issues=issues,
            recommended_mode=recommended_mode,
            reason=f"建议使用{recommended_mode.value}模式改善文本质量"
        )
