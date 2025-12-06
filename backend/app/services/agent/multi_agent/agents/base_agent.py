"""Agent 基类

提供所有 Multi-Agent 角色的通用功能。
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import json
import re
import logging

logger = logging.getLogger(__name__)


class BaseAgent(ABC):
    """Multi-Agent 基类

    所有角色 Agent 都继承自此类，提供：
    - LLM 调用封装
    - JSON 响应解析
    - 日志记录
    """

    def __init__(self, ai_service):
        """初始化 Agent

        Args:
            ai_service: HTTPAIService 实例
        """
        self.ai_service = ai_service

    @property
    @abstractmethod
    def name(self) -> str:
        """Agent 名称"""
        pass

    @property
    @abstractmethod
    def role_description(self) -> str:
        """Agent 角色描述"""
        pass

    @abstractmethod
    async def execute(
        self,
        input_data: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """执行 Agent 任务

        Args:
            input_data: 输入数据
            context: 上下文信息

        Returns:
            执行结果
        """
        pass

    async def _call_llm(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.7,
        max_tokens: int = 2000
    ) -> str:
        """调用 LLM

        Args:
            system_prompt: 系统提示
            user_prompt: 用户提示
            temperature: 温度参数
            max_tokens: 最大 token 数

        Returns:
            LLM 响应文本
        """
        try:
            result = await self.ai_service.call_ai(
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                temperature=temperature,
                max_tokens=max_tokens
            )
            return result
        except Exception as e:
            logger.error(f"[{self.name}] LLM 调用失败: {e}")
            raise

    def _parse_json_response(self, text: str) -> Dict[str, Any]:
        """解析 JSON 响应

        支持：
        - ```json ... ``` 格式
        - 直接 JSON 对象

        Args:
            text: LLM 返回的文本

        Returns:
            解析后的字典
        """
        # 尝试提取 ```json ... ``` 块
        json_match = re.search(r'```json\s*([\s\S]*?)\s*```', text)
        if json_match:
            try:
                return json.loads(json_match.group(1))
            except json.JSONDecodeError:
                pass

        # 尝试直接解析 JSON 对象
        json_match = re.search(r'\{[\s\S]*\}', text)
        if json_match:
            try:
                return json.loads(json_match.group())
            except json.JSONDecodeError:
                pass

        logger.warning(f"[{self.name}] 无法解析 JSON 响应: {text[:200]}...")
        return {}

    def _log_execution(self, action: str, details: Optional[Dict] = None):
        """记录执行日志

        Args:
            action: 动作描述
            details: 额外细节
        """
        log_msg = f"[{self.name}] {action}"
        if details:
            log_msg += f" | {json.dumps(details, ensure_ascii=False)[:200]}"
        logger.info(log_msg)
