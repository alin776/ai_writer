"""
小说微观分析服务
负责对单个章节进行细节提取和结构化分析
"""
import json
import logging
import asyncio
import time
from typing import Dict, Any, Optional
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.ai.http_ai_service import HTTPAIService
from app.services.agent.model_selector import TaskType  # ✅ 新增：用于成本追踪

logger = logging.getLogger(__name__)


class NovelMicroAnalysisService:
    """小说微观分析服务"""

    def __init__(
        self,
        user_id: Optional[str] = None,
        db: Optional[AsyncSession] = None,
        work_id: Optional[str] = None
    ):
        """初始化服务

        Args:
            user_id: 用户ID（用于token记录）
            db: 数据库会话（用于token记录）
            work_id: 作品ID（用于token记录）
        """
        # ❌ DEPRECATED - 2025-12-01
        # self.ai_service = HTTPAIService()
        # ✅ 新增：传递db和user_id给HTTPAIService
        self.user_id = user_id
        self.db = db
        self.work_id = work_id
        self.ai_service = HTTPAIService(db=db, user_id=str(user_id) if user_id else None)
        self.cache_service = None  # 延迟初始化
        self._load_prompts()

    async def _ensure_cache_service(self):
        """确保缓存服务已初始化"""
        if self.cache_service is None:
            from app.services.redis_cache_service import get_cache_service
            try:
                self.cache_service = await get_cache_service()
            except Exception as e:
                logger.warning(f"初始化缓存服务失败: {e}")
                self.cache_service = None
    
    def _load_prompts(self):
        """加载微观分析提示词"""
        try:
            import os
            prompts_path = os.path.join(
                os.path.dirname(__file__), 
                'prompts', 
                'novel_analysis.json'
            )
            with open(prompts_path, 'r', encoding='utf-8') as f:
                prompts_data = json.load(f)
                self.micro_prompt = prompts_data['micro_analysis']
                logger.info("微观分析提示词加载成功")
        except Exception as e:
            logger.error(f"加载提示词失败: {e}", exc_info=True)
            raise
    
    async def analyze_chapter(
        self,
        chapter_text: str,
        chapter_id: str,
        chapter_title: str = "",
        chapter_number: int = 0,
        max_retries: int = None
    ) -> Dict[str, Any]:
        """
        分析单个章节(带缓存)

        Args:
            chapter_text: 章节文本内容
            chapter_id: 章节ID
            chapter_title: 章节标题
            chapter_number: 章节序号
            max_retries: 最大重试次数

        Returns:
            Dict[str, Any]: 微观分析结果（JSON格式）

        Raises:
            Exception: 分析失败或JSON解析失败
        """
        from app.core.config import settings

        # 确保缓存服务已初始化
        await self._ensure_cache_service()

        # 1. 尝试从缓存获取结果
        if self.cache_service:
            cached_result = await self.cache_service.get_cached_analysis(
                chapter_content=chapter_text,
                analysis_type="micro"
            )
            if cached_result:
                logger.info(f"⚡ 使用缓存结果: {chapter_id} - {chapter_title}")
                # 更新chapter_id为当前章节
                cached_result['chapter_id'] = chapter_id
                return cached_result

        # 2. 缓存未命中,执行AI分析
        logger.info(f"开始AI分析章节: {chapter_id} - {chapter_title}")

        # ✅ 修复：检查内容是否为空或过短
        from app.core.config import settings
        MIN_CONTENT_LENGTH = settings.ANALYSIS_MIN_MICRO_CONTENT_LENGTH
        if not chapter_text or len(chapter_text.strip()) < MIN_CONTENT_LENGTH:
            content_length = len(chapter_text.strip()) if chapter_text else 0
            logger.warning(
                f"章节 {chapter_id} 内容过短（{content_length}字符 < {MIN_CONTENT_LENGTH}字符），"
                f"返回空分析结果"
            )
            # 返回空结构而不是调用AI
            return {
                "chapter_id": chapter_id,
                "analysis_type": "Micro_Detail_Extraction",
                "detailed_events": [],
                "chapter_theme": "内容待填写",
                "warning": f"章节内容过短（{content_length}字符），建议至少填写{MIN_CONTENT_LENGTH}字符"
            }

        # 使用配置的重试次数，如果未指定则使用配置值
        if max_retries is None:
            max_retries = settings.ANALYSIS_MAX_RETRIES - 1  # 减1因为第一次不算重试

        # 构建用户消息
        user_prompt = self.micro_prompt['user_prefix'].format(
            chapter_title=chapter_title or "未命名章节",
            chapter_number=chapter_number or "未知"
        )
        user_prompt += chapter_text

        # 构建消息列表
        messages = [
            {"role": "system", "content": self.micro_prompt['system']},
            {"role": "user", "content": user_prompt}
        ]

        # 尝试调用AI并解析结果
        for attempt in range(max_retries + 1):
            try:
                logger.info(f"第 {attempt + 1}/{max_retries + 1} 次尝试调用AI分析")

                # 调用AI（非流式，直接获取完整响应）
                response_text = await self._call_ai_non_stream(messages, chapter_id=chapter_id)

                logger.debug(f"AI返回原始文本: {response_text[:200]}...")

                # 解析JSON
                result = self._parse_json_response(response_text)

                # 验证JSON格式
                self._validate_micro_result(result)

                # 确保chapter_id正确
                result['chapter_id'] = chapter_id

                # 3. 写入缓存
                if self.cache_service:
                    await self.cache_service.cache_analysis_result(
                        chapter_content=chapter_text,
                        result=result,
                        analysis_type="micro",
                        ttl=60 * 60 * 24 * 7  # 7天
                    )

                logger.info(f"章节 {chapter_id} 分析成功，提取事件数: {len(result.get('detailed_events', []))}")
                return result
                
            except json.JSONDecodeError as e:
                logger.warning(f"第 {attempt + 1} 次尝试JSON解析失败: {e}")
                if attempt == max_retries:
                    logger.error(f"章节 {chapter_id} 分析失败：JSON解析失败（已重试{max_retries}次）")
                    raise Exception(f"AI返回的数据不是有效的JSON格式: {e}")
                # 等待后重试
                from app.core.config import settings
                await asyncio.sleep(settings.ANALYSIS_RETRY_DELAY)
            
            except Exception as e:
                logger.warning(f"第 {attempt + 1} 次尝试失败: {e}")
                if attempt == max_retries:
                    logger.error(f"章节 {chapter_id} 分析失败: {e}", exc_info=True)
                    raise
                # 等待后重试
                from app.core.config import settings
                await asyncio.sleep(settings.ANALYSIS_RETRY_DELAY)
    
    async def _call_ai_non_stream(
        self,
        messages: list,
        chapter_id: Optional[str] = None
    ) -> str:
        """
        调用AI（非流式）

        Args:
            messages: 消息列表
            chapter_id: 章节ID（用于token记录）

        Returns:
            str: AI返回的完整文本

        Raises:
            Exception: 如果AI返回空响应
        """
        full_response = ""
        final_usage = None
        start_time = time.time()

        # ✅ HTTPAIService会自动追踪成本，传递task_type即可
        async for chunk in self.ai_service._stream_chat(
            messages=messages,
            max_tokens=4000,  # 微观分析可能需要较多token
            temperature=0.3,  # 降低温度以获得更稳定的JSON输出
            task_type=TaskType.SUMMARIZATION  # ✅ 新增：微观分析是总结类任务
        ):
            # chunk 是 tuple (文本片段, usage统计)
            text_chunk, usage = chunk
            full_response += text_chunk
            if usage:  # 最后一个chunk包含usage
                final_usage = usage

        full_response = full_response.strip()

        # 检查是否为空响应
        if not full_response:
            logger.error("AI返回空响应")
            raise Exception("AI返回空响应，可能是超时或API限流")

        # ❌ DEPRECATED - 2025-12-02: 删除重复的成本追踪逻辑
        # HTTPAIService._track_api_cost()已经自动记录成本到数据库

        return full_response
    
    def _parse_json_response(self, text: str) -> Dict[str, Any]:
        """
        解析AI返回的JSON响应

        Args:
            text: AI返回的文本

        Returns:
            Dict[str, Any]: 解析后的JSON对象

        Raises:
            json.JSONDecodeError: JSON解析失败
        """
        # 尝试提取JSON（可能包含在```json```代码块中）
        text = text.strip()

        # 移除可能的代码块标记
        if text.startswith("```json"):
            text = text[7:]
        if text.startswith("```"):
            text = text[3:]
        if text.endswith("```"):
            text = text[:-3]

        text = text.strip()

        # 尝试解析JSON
        try:
            return json.loads(text)
        except json.JSONDecodeError as e:
            logger.warning(f"直接解析JSON失败: {e}, 尝试提取JSON对象...")

            # 尝试查找JSON对象的开始和结束
            start_idx = text.find('{')
            end_idx = text.rfind('}')

            if start_idx != -1 and end_idx != -1:
                json_text = text[start_idx:end_idx + 1]
                try:
                    return json.loads(json_text)
                except json.JSONDecodeError as e2:
                    logger.error(f"提取后仍无法解析JSON: {e2}")
                    logger.error(f"JSON文本片段: {json_text[:500]}...")
                    raise
            else:
                logger.error("无法找到JSON对象的开始和结束标记")
                logger.error(f"响应文本: {text[:500]}...")
                raise
    
    def _validate_micro_result(self, result: Dict[str, Any]) -> None:
        """
        验证微观分析结果的格式
        
        Args:
            result: 分析结果
            
        Raises:
            ValueError: 如果格式不正确
        """
        required_fields = ['chapter_id', 'analysis_type', 'detailed_events']
        
        for field in required_fields:
            if field not in result:
                raise ValueError(f"缺少必需字段: {field}")
        
        # 验证detailed_events是列表
        if not isinstance(result['detailed_events'], list):
            raise ValueError("detailed_events 必须是列表")
        
        # 验证每个事件的结构
        for idx, event in enumerate(result['detailed_events']):
            if not isinstance(event, dict):
                raise ValueError(f"事件 {idx} 必须是对象")
            
            event_required = ['time_context', 'action_summary', 'entities_involved']
            for field in event_required:
                if field not in event:
                    raise ValueError(f"事件 {idx} 缺少字段: {field}")
            
            # 验证entities_involved
            if not isinstance(event['entities_involved'], list):
                raise ValueError(f"事件 {idx} 的 entities_involved 必须是列表")
        
        logger.debug(f"微观分析结果验证通过: {len(result['detailed_events'])} 个事件")
    
    async def close(self):
        """关闭AI服务"""
        await self.ai_service.close()
