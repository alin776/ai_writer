import asyncio
import mimetypes
import os
from functools import lru_cache
from typing import Optional
from uuid import uuid4

from qcloud_cos import CosConfig, CosS3Client

from app.core.config import settings


class CosService:
    """腾讯云 COS 存储服务"""

    def __init__(self) -> None:
        if not all([
            settings.COS_SECRET_ID,
            settings.COS_SECRET_KEY,
            settings.COS_REGION,
            settings.COS_BUCKET,
        ]):
            raise RuntimeError("COS 配置缺失，请检查环境变量")

        config = CosConfig(
            Region=settings.COS_REGION,
            SecretId=settings.COS_SECRET_ID,
            SecretKey=settings.COS_SECRET_KEY,
            Token=None,
            Scheme=settings.COS_SCHEME or "https",
        )
        self.client = CosS3Client(config)
        self.bucket = settings.COS_BUCKET
        self.host = (settings.COS_HOST or "").rstrip("/")
        self.prefix = (settings.COS_PREFIX or "").strip("/")

    def _build_object_key(self, user_id: str, filename: Optional[str], content_type: Optional[str]) -> str:
        """构造 COS 对象 Key"""
        ext = ""
        if filename:
            _, ext = os.path.splitext(filename)
            ext = ext.lower()

        if not ext and content_type:
            guessed = mimetypes.guess_extension(content_type)
            if guessed:
                ext = guessed

        if not ext:
            ext = ".png"

        key = f"avatars/{user_id}/{uuid4().hex}{ext}"
        if self.prefix:
            key = f"{self.prefix}/{key}"
        return key

    def _build_public_url(self, key: str) -> str:
        """构造对外可访问 URL"""
        if self.host:
            return f"{self.host}/{key}"
        return f"https://{self.bucket}.cos.{settings.COS_REGION}.myqcloud.com/{key}"

    async def upload_avatar(self, user_id: str, filename: Optional[str], content: bytes, content_type: Optional[str]) -> str:
        """上传头像至 COS 并返回访问 URL"""
        key = self._build_object_key(user_id, filename, content_type)

        await asyncio.to_thread(
            self.client.put_object,
            Bucket=self.bucket,
            Key=key,
            Body=content,
            ContentType=content_type or "application/octet-stream",
        )

        return self._build_public_url(key)

    async def upload_notification_cover(self, filename: Optional[str], content: bytes, content_type: Optional[str]) -> str:
        """上传通知封面图片至 COS 并返回访问 URL"""
        # 构建对象 Key
        ext = ""
        if filename:
            _, ext = os.path.splitext(filename)
            ext = ext.lower()

        if not ext and content_type:
            guessed = mimetypes.guess_extension(content_type)
            if guessed:
                ext = guessed

        if not ext:
            ext = ".png"

        # 使用 notifications/covers 路径存储封面图片
        key = f"notifications/covers/{uuid4().hex}{ext}"
        if self.prefix:
            key = f"{self.prefix}/{key}"

        # 上传到 COS
        await asyncio.to_thread(
            self.client.put_object,
            Bucket=self.bucket,
            Key=key,
            Body=content,
            ContentType=content_type or "application/octet-stream",
        )

        return self._build_public_url(key)

    async def upload_channel_attachment(
        self,
        channel_id: str,
        filename: Optional[str],
        content: bytes,
        content_type: Optional[str]
    ) -> str:
        """上传频道附件至 COS 并返回访问 URL"""
        ext = ""
        if filename:
            _, ext = os.path.splitext(filename)
            ext = ext.lower()

        if not ext and content_type:
            guessed = mimetypes.guess_extension(content_type)
            if guessed:
                ext = guessed

        if not ext:
            ext = ".bin"

        # 使用 channels/{channel_id}/attachments 路径存储附件
        key = f"channels/{channel_id}/attachments/{uuid4().hex}{ext}"
        if self.prefix:
            key = f"{self.prefix}/{key}"

        # 上传到 COS
        await asyncio.to_thread(
            self.client.put_object,
            Bucket=self.bucket,
            Key=key,
            Body=content,
            ContentType=content_type or "application/octet-stream",
        )

        return self._build_public_url(key)


@lru_cache(maxsize=1)
def get_cos_service() -> CosService:
    """获取 COS 服务单例"""
    return CosService()
