"""
AI Prompts Manager - Manage AI prompts from JSON configuration
"""

import json
import logging
from pathlib import Path
from typing import Dict, Any

logger = logging.getLogger(__name__)


class PromptsManager:
    """AI prompts configuration manager"""
    
    def __init__(self, config_file: str = "default.json"):
        """
        Initialize prompts manager
        
        Args:
            config_file: Configuration file name (default: default.json)
        """
        self.config_dir = Path(__file__).parent / "prompts"
        self.config_path = self.config_dir / config_file
        self.prompts: Dict[str, Any] = {}
        
        self._load_prompts()
    
    def _load_prompts(self):
        """Load prompts from JSON configuration file"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                self.prompts = json.load(f)
            logger.info(f"Prompts loaded successfully from {self.config_path}")
        except FileNotFoundError:
            logger.error(f"Prompts configuration file not found: {self.config_path}")
            raise
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse prompts JSON: {e}")
            raise
        except Exception as e:
            logger.error(f"Failed to load prompts: {e}")
            raise
    
    def get_autocomplete_prompt(self) -> str:
        """Get autocomplete system prompt"""
        return self.prompts.get("autocomplete", {}).get("system", "")
    
    def get_complete_prompt(self, prompt: str = "续写", style: str = "") -> str:
        """
        Get complete (continuation) system prompt
        
        Args:
            prompt: Task description (e.g., "续写")
            style: Writing style
            
        Returns:
            Complete system prompt
        """
        complete_config = self.prompts.get("complete", {})
        
        base_prompt = complete_config.get("system_base", "")
        
        if style:
            base_prompt += f"\n\n写作风格：{style}"
        
        task = complete_config.get("system_task", "").format(prompt=prompt)
        requirements = complete_config.get("system_requirements", "")
        
        return base_prompt + task + requirements
    
    def get_polish_prompt(self) -> tuple[str, str]:
        """
        Get polish system prompt and user prefix
        
        Returns:
            Tuple of (system_prompt, user_prefix)
        """
        polish_config = self.prompts.get("polish", {})
        system = polish_config.get("system", "")
        user_prefix = polish_config.get("user_prefix", "")
        return system, user_prefix
    
    def get_expand_prompt(self) -> tuple[str, str]:
        """
        Get expand system prompt and user prefix
        
        Returns:
            Tuple of (system_prompt, user_prefix)
        """
        expand_config = self.prompts.get("expand", {})
        system = expand_config.get("system", "")
        user_prefix = expand_config.get("user_prefix", "")
        return system, user_prefix
    
    def get_summarize_prompt(self) -> tuple[str, str]:
        """
        Get summarize system prompt and user prefix
        
        Returns:
            Tuple of (system_prompt, user_prefix)
        """
        summarize_config = self.prompts.get("summarize", {})
        system = summarize_config.get("system", "")
        user_prefix = summarize_config.get("user_prefix", "")
        return system, user_prefix
    
    def get_translate_prompt(self, target_lang: str = "auto") -> str:
        """
        Get translate system prompt
        
        Args:
            target_lang: Target language (auto/english/chinese or custom)
            
        Returns:
            Translate system prompt
        """
        translate_config = self.prompts.get("translate", {})
        instructions = translate_config.get("instructions", {})
        
        # Get instruction based on target language
        if target_lang in instructions:
            instruction = instructions[target_lang]
        else:
            instruction = f"翻译成{target_lang}。"
        
        system_base = translate_config.get("system_base", "")
        return system_base.format(instruction=instruction)
    
    def reload(self):
        """Reload prompts configuration from file"""
        self._load_prompts()
        logger.info("Prompts configuration reloaded")


# Global prompts manager instance
_prompts_manager: PromptsManager = None


def get_prompts_manager() -> PromptsManager:
    """Get global prompts manager instance (singleton)"""
    global _prompts_manager
    if _prompts_manager is None:
        _prompts_manager = PromptsManager()
    return _prompts_manager
