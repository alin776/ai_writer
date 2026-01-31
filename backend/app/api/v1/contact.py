"""
联系表单 API

提供联系表单提交和邮件发送功能
"""
import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

from fastapi import APIRouter, HTTPException

from app.schemas.contact import ContactMessageRequest, ContactMessageResponse
from app.core.config import settings

logger = logging.getLogger(__name__)

router = APIRouter()

# 目标邮箱地址
CONTACT_EMAIL = "2072855200@qq.com"


def send_contact_email(data: ContactMessageRequest) -> bool:
    """
    发送联系表单邮件

    Args:
        data: 联系表单数据

    Returns:
        是否发送成功
    """
    smtp_host = getattr(settings, 'SMTP_HOST', None)
    smtp_port = getattr(settings, 'SMTP_PORT', 587)
    smtp_user = getattr(settings, 'SMTP_USER', None)
    smtp_password = getattr(settings, 'SMTP_PASSWORD', None)

    if not all([smtp_host, smtp_user, smtp_password]):
        logger.warning("SMTP 未配置，跳过邮件发送")
        return False

    # 创建邮件
    msg = MIMEMultipart('alternative')
    msg['Subject'] = '【文枢AI】用户反馈'
    msg['From'] = smtp_user
    msg['To'] = CONTACT_EMAIL
    msg['Reply-To'] = data.email  # 设置回复地址为用户邮箱

    # 当前时间
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # HTML 邮件内容
    html = f"""
    <div style="max-width: 600px; margin: 0 auto; padding: 20px; font-family: Arial, sans-serif; background: #f9fafb;">
        <div style="background: white; border-radius: 12px; padding: 30px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
            <h2 style="color: #1f2937; margin-bottom: 24px; border-bottom: 2px solid #3b82f6; padding-bottom: 12px;">
                📬 新的用户反馈
            </h2>

            <div style="margin-bottom: 20px;">
                <p style="color: #6b7280; font-size: 14px; margin-bottom: 4px;">发送者</p>
                <p style="color: #1f2937; font-size: 16px; font-weight: 500; margin: 0;">
                    {data.name}
                </p>
            </div>

            <div style="margin-bottom: 20px;">
                <p style="color: #6b7280; font-size: 14px; margin-bottom: 4px;">邮箱</p>
                <p style="color: #3b82f6; font-size: 16px; margin: 0;">
                    <a href="mailto:{data.email}" style="color: #3b82f6; text-decoration: none;">
                        {data.email}
                    </a>
                </p>
            </div>

            <div style="margin-bottom: 20px;">
                <p style="color: #6b7280; font-size: 14px; margin-bottom: 4px;">主题</p>
                <p style="color: #1f2937; font-size: 16px; font-weight: 500; margin: 0;">
                    {data.subject}
                </p>
            </div>

            <div style="margin-bottom: 20px;">
                <p style="color: #6b7280; font-size: 14px; margin-bottom: 8px;">消息内容</p>
                <div style="background: #f3f4f6; border-radius: 8px; padding: 16px; color: #374151; line-height: 1.6; white-space: pre-wrap;">
{data.message}
                </div>
            </div>

            <hr style="border: none; border-top: 1px solid #e5e7eb; margin: 24px 0;">

            <p style="color: #9ca3af; font-size: 12px; margin: 0;">
                发送时间: {now}<br>
                来源: 文枢AI 联系表单
            </p>
        </div>
    </div>
    """

    msg.attach(MIMEText(html, 'html', 'utf-8'))

    try:
        # QQ邮箱使用 SSL 端口 465
        if smtp_port == 465:
            server = smtplib.SMTP_SSL(smtp_host, smtp_port)
            try:
                server.login(smtp_user, smtp_password)
                server.send_message(msg)
                logger.info(f"联系表单邮件已发送: {data.email} -> {CONTACT_EMAIL}")
            finally:
                try:
                    server.quit()
                except Exception:
                    pass  # 忽略关闭连接时的错误
        else:
            # 其他邮箱使用 STARTTLS 端口 587
            with smtplib.SMTP(smtp_host, smtp_port, timeout=30) as server:
                server.starttls()
                server.login(smtp_user, smtp_password)
                server.send_message(msg)
            logger.info(f"联系表单邮件已发送: {data.email} -> {CONTACT_EMAIL}")
        return True
    except Exception as e:
        logger.error(f"联系表单邮件发送失败: {e}")
        raise


@router.post(
    "/send-message",
    response_model=ContactMessageResponse,
    summary="发送联系消息",
    description="提交联系表单，发送邮件通知管理员"
)
async def send_contact_message(data: ContactMessageRequest) -> ContactMessageResponse:
    """
    发送联系消息

    接收用户的联系表单数据，发送邮件到管理员邮箱
    """
    try:
        success = send_contact_email(data)

        if not success:
            # SMTP 未配置时，仍然返回成功（可以在日志中查看）
            logger.info(f"联系表单已接收（SMTP未配置）: {data.name} <{data.email}> - {data.subject}")
            return ContactMessageResponse(
                success=True,
                detail="消息已接收，我们会尽快回复您"
            )

        return ContactMessageResponse(
            success=True,
            detail="消息已发送，我们会尽快回复您"
        )

    except Exception as e:
        logger.error(f"联系表单处理失败: {e}")
        raise HTTPException(
            status_code=500,
            detail="消息发送失败，请稍后重试或直接发送邮件联系我们"
        )
