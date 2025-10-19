"""
小说微观分析服务
负责对单个章节进行细节提取和结构化分析
"""
import json
import logging
from typing import Dict, Any, Optional
from app.services.ai.http_ai_service import HTTPAIService

logger = logging.getLogger(__name__)


class NovelMicroAnalysisService:
    """小说微观分析服务"""
    
    def __init__(self):
        """初始化服务"""
        self.ai_service = HTTPAIService()
        self._load_prompts()
    
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
        max_retries: int = 2
    ) -> Dict[str, Any]:
        """
        分析单个章节
        
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
        logger.info(f"开始分析章节: {chapter_id} - {chapter_title}")
        
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
                response_text = await self._call_ai_non_stream(messages)
                
                logger.debug(f"AI返回原始文本: {response_text[:200]}...")
                
                # 解析JSON
                result = self._parse_json_response(response_text)
                
                # 验证JSON格式
                self._validate_micro_result(result)
                
                # 确保chapter_id正确
                result['chapter_id'] = chapter_id
                
                logger.info(f"章节 {chapter_id} 分析成功，提取事件数: {len(result.get('detailed_events', []))}")
                return result
                
            except json.JSONDecodeError as e:
                logger.warning(f"第 {attempt + 1} 次尝试JSON解析失败: {e}")
                if attempt == max_retries:
                    logger.error(f"章节 {chapter_id} 分析失败：JSON解析失败（已重试{max_retries}次）")
                    raise Exception(f"AI返回的数据不是有效的JSON格式: {e}")
            
            except Exception as e:
                logger.warning(f"第 {attempt + 1} 次尝试失败: {e}")
                if attempt == max_retries:
                    logger.error(f"章节 {chapter_id} 分析失败: {e}", exc_info=True)
                    raise
    
    async def _call_ai_non_stream(self, messages: list) -> str:
        """
        调用AI（非流式）
        
        Args:
            messages: 消息列表
            
        Returns:
            str: AI返回的完整文本
        """
        full_response = ""
        
        async for chunk in self.ai_service._stream_chat(
            messages=messages,
            max_tokens=4000,  # 微观分析可能需要较多token
            temperature=0.3   # 降低温度以获得更稳定的JSON输出
        ):
            full_response += chunk
        
        return full_response.strip()
    
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
        except json.JSONDecodeError:
            # 尝试查找JSON对象的开始和结束
            start_idx = text.find('{')
            end_idx = text.rfind('}')
            
            if start_idx != -1 and end_idx != -1:
                json_text = text[start_idx:end_idx + 1]
                return json.loads(json_text)
            else:
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
