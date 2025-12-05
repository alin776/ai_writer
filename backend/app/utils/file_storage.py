"""临时文件存储管理"""
import tempfile
import uuid
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional
import logging
from app.utils.datetime_utils import get_utc_now

logger = logging.getLogger(__name__)


class TempFileStorage:
    """临时文件存储管理器
    
    用于存储导出的文件，提供临时下载链接
    文件默认保存24小时后自动清理
    """
    
    def __init__(self, temp_dir: Optional[Path] = None):
        """初始化临时存储目录"""
        if temp_dir is None:
            self.temp_dir = Path(tempfile.gettempdir()) / "novelaide_exports"
        else:
            self.temp_dir = Path(temp_dir)
        
        # 确保目录存在
        self.temp_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"临时文件存储目录: {self.temp_dir}")
    
    def save_file(self, content: bytes, filename: str) -> tuple[str, str, int]:
        """保存文件到临时目录
        
        Args:
            content: 文件内容（字节）
            filename: 原始文件名
        
        Returns:
            (file_id, full_path, file_size)
        """
        # 生成唯一ID
        file_id = uuid.uuid4().hex
        
        # 构建文件路径（保留原始文件名用于下载）
        safe_filename = self._sanitize_filename(filename)
        file_path = self.temp_dir / f"{file_id}_{safe_filename}"
        
        # 写入文件
        file_path.write_bytes(content)
        file_size = len(content)
        
        logger.info(f"保存临时文件: {file_path} ({file_size} bytes)")
        
        return file_id, str(file_path), file_size
    
    def get_file_path(self, file_id: str) -> Optional[Path]:
        """根据file_id获取文件路径"""
        # 查找匹配的文件（文件名格式: {file_id}_{original_name}）
        for file_path in self.temp_dir.glob(f"{file_id}_*"):
            return file_path
        return None
    
    def get_original_filename(self, file_id: str) -> Optional[str]:
        """根据file_id获取原始文件名"""
        file_path = self.get_file_path(file_id)
        if file_path:
            # 提取原始文件名（去除file_id前缀）
            filename = file_path.name
            parts = filename.split('_', 1)
            if len(parts) == 2:
                return parts[1]
        return None
    
    def delete_file(self, file_id: str) -> bool:
        """删除文件"""
        file_path = self.get_file_path(file_id)
        if file_path and file_path.exists():
            file_path.unlink()
            logger.info(f"删除临时文件: {file_path}")
            return True
        return False
    
    def cleanup_expired_files(self, hours: int = 24) -> int:
        """清理过期文件
        
        Args:
            hours: 文件保留时间（小时）
        
        Returns:
            删除的文件数量
        """
        cutoff_time = get_utc_now().timestamp() - (hours * 3600)
        deleted_count = 0
        
        for file_path in self.temp_dir.glob("*"):
            if file_path.is_file():
                # 检查文件修改时间
                file_mtime = file_path.stat().st_mtime
                if file_mtime < cutoff_time:
                    try:
                        file_path.unlink()
                        deleted_count += 1
                        logger.info(f"清理过期文件: {file_path}")
                    except Exception as e:
                        logger.error(f"删除文件失败: {file_path}, 错误: {e}")
        
        logger.info(f"清理完成，删除 {deleted_count} 个过期文件")
        return deleted_count
    
    def get_expiry_time(self, hours: int = 24) -> datetime:
        """获取过期时间"""
        return get_utc_now() + timedelta(hours=hours)
    
    @staticmethod
    def _sanitize_filename(filename: str) -> str:
        """清理文件名，移除不安全字符"""
        import re
        # 只保留字母、数字、中文、下划线、点号、连字符
        safe_name = re.sub(r'[^\w\u4e00-\u9fff.\-]', '_', filename)
        # 限制长度
        if len(safe_name) > 200:
            # 保留扩展名
            name_parts = safe_name.rsplit('.', 1)
            if len(name_parts) == 2:
                safe_name = name_parts[0][:190] + '.' + name_parts[1]
            else:
                safe_name = safe_name[:200]
        return safe_name


# 全局实例
temp_storage = TempFileStorage()
