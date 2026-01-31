"""
联系表单 Schema
"""
from pydantic import BaseModel, EmailStr, Field


class ContactMessageRequest(BaseModel):
    """联系表单请求"""
    name: str = Field(..., min_length=1, max_length=50, description="姓名")
    email: EmailStr = Field(..., description="邮箱地址")
    subject: str = Field(..., min_length=1, max_length=200, description="主题")
    message: str = Field(..., min_length=1, max_length=5000, description="消息内容")


class ContactMessageResponse(BaseModel):
    """联系表单响应"""
    success: bool = True
    detail: str = "消息已发送，我们会尽快回复您"
