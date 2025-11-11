"""
小说宏观分析服务
负责整合所有微观分析结果，生成全局分析报告
"""
import json
import logging
from typing import List, Dict, Any
from app.services.ai.http_ai_service import HTTPAIService

logger = logging.getLogger(__name__)


class NovelMacroAnalysisService:
    """小说宏观分析服务"""
    
    def __init__(self):
        """初始化服务"""
        self.ai_service = HTTPAIService()
        self._load_prompts()
    
    def _load_prompts(self):
        """加载宏观分析提示词"""
        try:
            import os
            prompts_path = os.path.join(
                os.path.dirname(__file__), 
                'prompts', 
                'novel_analysis.json'
            )
            with open(prompts_path, 'r', encoding='utf-8') as f:
                prompts_data = json.load(f)
                self.macro_prompt = prompts_data['macro_analysis']
                logger.info("宏观分析提示词加载成功")
        except Exception as e:
            logger.error(f"加载提示词失败: {e}", exc_info=True)
            raise
    
    async def analyze_novel_macro(
        self,
        micro_results: List[Dict[str, Any]],
        max_retries: int = 2
    ) -> str:
        """
        执行宏观分析（生成三大报告）
        
        Args:
            micro_results: 所有章节的微观分析结果列表
            max_retries: 最大重试次数
            
        Returns:
            str: 宏观分析报告文本
            
        Raises:
            Exception: 分析失败
        """
        if not micro_results:
            raise ValueError("微观分析结果列表不能为空")
        
        logger.info(f"开始宏观分析，共 {len(micro_results)} 个章节的数据")
        
        # 构建用户消息
        user_prompt = self._build_macro_prompt(micro_results)
        
        # 构建消息列表
        messages = [
            {"role": "system", "content": self.macro_prompt['system']},
            {"role": "user", "content": user_prompt}
        ]
        
        # 尝试调用AI
        for attempt in range(max_retries + 1):
            try:
                logger.info(f"第 {attempt + 1}/{max_retries + 1} 次尝试调用AI宏观分析")
                
                # 调用AI（非流式）
                response_text = await self._call_ai_non_stream(messages)
                
                logger.info(f"宏观分析完成，报告长度: {len(response_text)} 字符")
                
                # 简单验证报告格式
                if self._validate_macro_report(response_text):
                    return response_text
                else:
                    logger.warning(f"第 {attempt + 1} 次尝试：报告格式验证失败")
                    if attempt == max_retries:
                        # 即使验证失败，也返回结果（避免丢失数据）
                        logger.warning("宏观分析报告格式不完全符合预期，但仍然返回")
                        return response_text
                
            except Exception as e:
                logger.warning(f"第 {attempt + 1} 次尝试失败: {e}")
                if attempt == max_retries:
                    logger.error(f"宏观分析失败: {e}", exc_info=True)
                    raise
        
        raise Exception("宏观分析失败：超过最大重试次数")
    
    def _build_macro_prompt(self, micro_results: List[Dict[str, Any]]) -> str:
        """
        构建宏观分析的用户提示词
        
        Args:
            micro_results: 微观分析结果列表
            
        Returns:
            str: 用户提示词
        """
        # 构建前缀
        prompt = self.macro_prompt['user_prefix'].format(
            total_chapters=len(micro_results)
        )
        
        # 添加所有章节的微观分析数据
        # 为了避免超出token限制，可能需要压缩数据
        compressed_results = self._compress_micro_results(micro_results)
        
        prompt += json.dumps(compressed_results, ensure_ascii=False, indent=2)
        
        return prompt
    
    def _compress_micro_results(self, micro_results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        压缩微观分析结果（减少token消耗）
        
        Args:
            micro_results: 原始微观分析结果
            
        Returns:
            List[Dict[str, Any]]: 压缩后的结果
        """
        compressed = []
        
        for idx, result in enumerate(micro_results):
            # 保留关键信息
            compressed_result = {
                'chapter_id': result.get('chapter_id', f'chapter_{idx + 1}'),
                'chapter_theme': result.get('chapter_theme', ''),
                'events_summary': []
            }
            
            # 压缩事件信息
            for event in result.get('detailed_events', []):
                event_summary = {
                    'time': event.get('time_context', ''),
                    'action': event.get('action_summary', ''),
                    'entities': [
                        {
                            'type': entity.get('type', ''),
                            'name': entity.get('name', ''),
                            'desc': entity.get('description', '')[:100]  # 限制描述长度
                        }
                        for entity in event.get('entities_involved', [])
                    ]
                }
                compressed_result['events_summary'].append(event_summary)
            
            compressed.append(compressed_result)
        
        logger.debug(f"微观数据压缩完成: {len(micro_results)} 章 -> {len(compressed)} 章摘要")
        return compressed
    
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
            max_tokens=6000,  # 宏观分析需要更多token生成报告
            temperature=0.5   # 适中的温度，保持创造性和稳定性
        ):
            # chunk 是 tuple (文本片段, usage统计)
            text_chunk, usage = chunk
            full_response += text_chunk

        return full_response.strip()
    
    def _validate_macro_report(self, report: str) -> bool:
        """
        验证宏观分析报告的基本格式
        
        Args:
            report: 报告文本
            
        Returns:
            bool: 是否验证通过
        """
        # 检查是否包含三大报告的关键标题
        required_sections = [
            "人物成长轨迹报告",
            "世界观图谱与时间线报告",
            "核心矛盾演变报告"
        ]
        
        for section in required_sections:
            if section not in report:
                logger.warning(f"报告缺少章节: {section}")
                return False
        
        # 检查报告长度（至少应该有一定内容）
        if len(report) < 500:
            logger.warning(f"报告长度过短: {len(report)} 字符")
            return False
        
        logger.debug("宏观分析报告格式验证通过")
        return True
    
    async def close(self):
        """关闭AI服务"""
        await self.ai_service.close()
