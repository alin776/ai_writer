"""Markdown文件生成器"""
from typing import List, Optional
from html import unescape
from bs4 import BeautifulSoup


class MarkdownGenerator:
    """Markdown文件生成器"""
    
    def __init__(self):
        self.content: List[str] = []
    
    def add_title(self, title: str) -> None:
        """添加标题"""
        self.content.append(f"# {title}\n\n")
    
    def add_metadata(self, work: dict) -> None:
        """添加元数据"""
        self.content.append(f"**作者**: {work.get('author', '未知')}  \n")
        self.content.append(f"**类型**: {work.get('genre', '未知')}  \n")
        self.content.append(f"**状态**: {work.get('status', '未知')}  \n")
        self.content.append(f"**总字数**: {work.get('total_words', 0):,}  \n")
        
        updated_at = work.get('updated_at', '')
        if updated_at:
            if isinstance(updated_at, str):
                # 如果是ISO格式字符串，只取日期部分
                updated_at = updated_at.split('T')[0]
            self.content.append(f"**更新时间**: {updated_at}\n\n")
        else:
            self.content.append("**更新时间**: 未知\n\n")
    
    def add_description(self, description: Optional[str]) -> None:
        """添加简介"""
        if description:
            self.content.append("## 简介\n\n")
            self.content.append(f"{description}\n\n")
    
    def add_chapter(self, title: str, content: str) -> None:
        """添加章节"""
        # 将HTML转为纯文本
        text = self._html_to_text(content)
        
        self.content.append("---\n\n")
        self.content.append(f"## {title}\n\n")
        self.content.append(f"{text}\n\n")
    
    def add_worldview_appendix(
        self, 
        characters: List[dict], 
        locations: List[dict], 
        settings: List[dict]
    ) -> None:
        """添加世界观附录"""
        self.content.append("---\n\n")
        self.content.append("## 附录：世界观设定\n\n")
        
        # 人物设定
        if characters:
            self.content.append("### 人物设定\n\n")
            for char in characters:
                name = char.get('name', '未命名')
                role = char.get('role', '')
                desc = char.get('description', '')
                tags = char.get('tags', [])
                
                self.content.append(f"#### {name}")
                if role:
                    self.content.append(f"（{role}）")
                self.content.append("\n")
                
                if tags:
                    self.content.append(f"- **标签**: {', '.join(tags)}\n")
                if desc:
                    self.content.append(f"- **描述**: {desc}\n")
                self.content.append("\n")
        
        # 地点设定
        if locations:
            self.content.append("### 地点设定\n\n")
            for loc in locations:
                name = loc.get('name', '未命名')
                loc_type = loc.get('type', '')
                desc = loc.get('description', '')
                tags = loc.get('tags', [])
                
                self.content.append(f"#### {name}")
                if loc_type:
                    self.content.append(f"（{loc_type}）")
                self.content.append("\n")
                
                if tags:
                    self.content.append(f"- **标签**: {', '.join(tags)}\n")
                if desc:
                    self.content.append(f"- **描述**: {desc}\n")
                self.content.append("\n")
        
        # 设定资料
        if settings:
            self.content.append("### 设定资料\n\n")
            for setting in settings:
                title = setting.get('title', '未命名')
                category = setting.get('category', '')
                content = setting.get('content', '')
                
                self.content.append(f"#### {title}")
                if category:
                    self.content.append(f"（{category}）")
                self.content.append("\n\n")
                
                if content:
                    self.content.append(f"{content}\n\n")
    
    def generate(self) -> str:
        """生成完整的Markdown文本"""
        return ''.join(self.content)
    
    def _html_to_text(self, html: str) -> str:
        """将HTML转换为纯文本
        
        保留段落结构，移除HTML标签
        """
        if not html:
            return ""
        
        try:
            soup = BeautifulSoup(html, 'html.parser')
            
            # 处理段落标签
            for p in soup.find_all('p'):
                p.insert_after('\n\n')
            
            # 处理换行标签
            for br in soup.find_all('br'):
                br.replace_with('\n')
            
            # 获取纯文本
            text = soup.get_text()
            
            # 清理多余的空行（保留最多2个连续换行）
            lines = []
            prev_empty = False
            for line in text.split('\n'):
                line = line.strip()
                if line:
                    lines.append(line)
                    prev_empty = False
                elif not prev_empty:
                    lines.append('')
                    prev_empty = True
            
            # 解码HTML实体
            text = unescape('\n'.join(lines))
            return text.strip()
            
        except Exception as e:
            # 如果解析失败，返回原始文本（去除HTML标签）
            import re
            text = re.sub(r'<[^>]+>', '', html)
            return unescape(text).strip()
