from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from datetime import datetime, timedelta

from app.core.database import get_db
from app.core.security import create_access_token, create_refresh_token
from app.core.config import settings
from app.schemas.user import UserCreate, UserResponse, Token, AuthResponse
from app.services.user_service import UserService
from app.utils.device_parser import parse_user_agent, get_client_ip
from app.utils.datetime_utils import get_utc_now

router = APIRouter()


class LoginRequest(BaseModel):
    """登录请求"""
    username: str
    password: str
    remember_me: bool = False  # 记住我选项


class RefreshTokenRequest(BaseModel):
    """刷新Token请求"""
    refresh_token: str


class ForgotPasswordRequest(BaseModel):
    """忘记密码请求"""
    email: str


class ResetPasswordRequest(BaseModel):
    """重置密码请求"""
    email: str
    code: str
    new_password: str


class SendEmailVerificationRequest(BaseModel):
    """发送邮箱验证码请求"""
    email: str


class VerifyEmailRequest(BaseModel):
    """验证邮箱请求"""
    email: str
    code: str


def _parse_bool(value) -> bool:
    """Best-effort bool parsing for login payloads."""
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return bool(value)
    if isinstance(value, str):
        normalized = value.strip().lower()
        return normalized in {"1", "true", "yes", "on", "y"}
    return False


@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
async def register(
    user_data: UserCreate,
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    """
    用户注册（需要邀请码和邮箱验证码）

    - **email**: 邮箱地址
    - **username**: 用户名（3-50字符）
    - **password**: 密码（8-20字符，必须包含字母、数字、特殊符号）
    - **invitation_code**: 8位邀请码（必填）
    - **email_verification_code**: 6位邮箱验证码（必填）
    - **device_fingerprint**: 设备指纹（可选，用于防刷）

    注册成功后请前往登录页面登录
    """
    import logging
    logger = logging.getLogger(__name__)

    from app.services.invitations.invitation_service import InvitationService
    from app.services.credits.credit_service import CreditService
    from app.services.credits.credit_exceptions import InvitationCodeInvalidError
    from app.services.email_verification_service import get_email_verification_service

    user_service = UserService(db)
    invitation_service = InvitationService(db)
    credit_service = CreditService(db)

    try:
        # 获取IP地址
        ip_address = get_client_ip(request)

        # ✅ 安全检查：验证邮箱验证码
        logger.info(f"Verifying email verification code for: {user_data.email}")
        email_verification_service = await get_email_verification_service()

        try:
            is_verified = await email_verification_service.verify_code(
                user_data.email,
                user_data.email_verification_code
            )
            if not is_verified:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="邮箱验证码错误或已过期"
                )
        except ValueError as e:
            # 验证码错误、锁定等
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )

        # ✅ Critical修复1: 使用数据库事务确保原子性
        # 开始嵌套事务，确保所有操作要么全部成功，要么全部回滚
        async with db.begin_nested():
            # 1. 验证邀请码（只读操作，不修改数据）
            logger.info(f"Validating invitation code: {user_data.invitation_code}")
            is_valid, error_msg, invitation = await invitation_service.validate_invitation_code(
                code=user_data.invitation_code,
                ip_address=ip_address,
                device_fingerprint=user_data.device_fingerprint
            )

            if not is_valid:
                logger.warning(f"Invalid invitation code: {user_data.invitation_code} - {error_msg}")
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=error_msg
                )

            # 2. 创建用户
            logger.info(f"Creating user: {user_data.username}")
            user = await user_service.create_user(user_data)
            logger.info(f"User created successfully: {user.id}")

            # 3. 创建用户积分记录（优先创建，避免后续扣费时竞态）
            logger.info(f"Creating credits for new user: {user.id}")
            await credit_service.get_or_create_credits(user.id, commit=False)

            # 4. 使用邀请码（最后执行，避免前面步骤失败导致邀请码被消耗）
            logger.info(f"Using invitation code for user: {user.id}")
            await invitation_service.use_invitation_code(
                code=user_data.invitation_code,
                invitee_id=user.id,
                ip_address=ip_address,
                device_fingerprint=user_data.device_fingerprint
            )

            # 5. 立即激活邀请奖励（注册即奖励模式）
            logger.info(f"Activating invitation reward for user: {user.id}")
            reward_info = await invitation_service.activate_invitation(
                invitee_id=user.id,
                force=True,
                commit=False
            )
            if reward_info:
                logger.info(f"Invitation reward activated: {reward_info}")

        # 提交外层事务
        await db.commit()
        logger.info(f"Registration completed successfully for user: {user.id}")

        # 只返回用户信息，不返回 token
        # 用户需要手动登录
        return user
    except InvitationCodeInvalidError as e:
        logger.error(f"InvitationCodeInvalidError: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except ValueError as e:
        logger.error(f"ValueError: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except IntegrityError as e:
        # 数据库层面的唯一约束冲突（如并发下的重复用户名/邮箱）
        logger.error(f"IntegrityError: {e}")
        # 使用 409 更符合语义（资源冲突）
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username or email already exists")
    except Exception as e:
        logger.error(f"Unexpected error: {type(e).__name__}: {e}")
        import traceback
        logger.error(traceback.format_exc())
        raise


@router.post("/login", response_model=Token)
async def login(
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    """
    用户登录

    - **username**: 用户名或邮箱
    - **password**: 密码
    - **remember_me**: 记住我（可选，默认 false）
      - true: refreshToken 有效期 30 天
      - false: refreshToken 有效期 7 天

    返回 JWT Token

    注意：连续登录失败5次后将被锁定15分钟
    """
    import logging
    logger = logging.getLogger(__name__)

    from app.services.login_rate_limit_service import get_login_rate_limit_service

    raw_username = None
    raw_password = None
    raw_remember_me = False
    content_type = (request.headers.get("content-type") or "").lower()

    try:
        if "application/x-www-form-urlencoded" in content_type or "multipart/form-data" in content_type:
            form_data = await request.form()
            raw_username = form_data.get("username")
            raw_password = form_data.get("password")
            raw_remember_me = form_data.get("remember_me", False)
        else:
            payload = await request.json()
            if isinstance(payload, dict):
                raw_username = payload.get("username")
                raw_password = payload.get("password")
                raw_remember_me = payload.get("remember_me", False)
    except Exception:
        # 交给下方统一参数校验
        pass

    username = str(raw_username or "").strip()
    password = str(raw_password or "")
    remember_me = _parse_bool(raw_remember_me)

    if not username or not password:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="username and password are required"
        )

    login_data = LoginRequest(
        username=username,
        password=password,
        remember_me=remember_me
    )

    logger.info(f"[LOGIN] 尝试登录: {login_data.username} (记住我: {login_data.remember_me})")

    # 获取客户端 IP
    ip_address = get_client_ip(request)

    # 检查是否被限流
    rate_limit_service = await get_login_rate_limit_service()
    allowed, error_msg = await rate_limit_service.check_rate_limit(
        login_data.username, ip_address
    )
    if not allowed:
        logger.warning(f"[LOGIN] 登录被限流: {login_data.username} ({ip_address}) - {error_msg}")
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=error_msg
        )

    user_service = UserService(db)

    user = await user_service.authenticate_user(
        login_data.username,
        login_data.password
    )

    if not user:
        # 记录失败尝试
        remaining, locked = await rate_limit_service.record_failed_attempt(
            login_data.username, ip_address
        )
        if locked:
            logger.warning(f"[LOGIN] 账户已被锁定: {login_data.username} ({ip_address})")
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="登录失败次数过多，账户已被锁定15分钟"
            )
        logger.warning(f"[LOGIN] 登录失败: {login_data.username} - 用户名或密码错误，剩余 {remaining} 次尝试")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"用户名或密码错误，还剩 {remaining} 次尝试机会",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        logger.warning(f"[LOGIN] 登录失败: {login_data.username} - 账户已禁用")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive"
        )

    # 登录成功，清除失败记录
    await rate_limit_service.clear_failed_attempts(login_data.username, ip_address)

    # 创建访问令牌和刷新令牌
    access_token = create_access_token(data={"sub": str(user.id)})

    # 根据 remember_me 参数设置不同的 refreshToken 有效期
    refresh_token_days = 30 if login_data.remember_me else 7
    refresh_token = create_refresh_token(
        data={"sub": str(user.id), "remember_me": login_data.remember_me},
        expires_days=refresh_token_days
    )

    logger.info(f"[LOGIN] 登录成功: {login_data.username} (refreshToken 有效期: {refresh_token_days}天)")

    # 解析设备信息
    user_agent = request.headers.get("user-agent", "")
    device_info = parse_user_agent(user_agent)
    device_info['user_agent'] = user_agent  # 保存完整的 User-Agent

    # 获取客户端 IP
    ip_address = get_client_ip(request)

    # 创建会话记录
    try:
        await user_service.create_session(
            user_id=str(user.id),
            session_token=access_token,
            device_info=device_info,
            ip_address=ip_address
        )
        logger.info(f"[LOGIN] 会话创建成功: {user.id} ({ip_address})")
    except Exception as e:
        # 会话创建失败不影响登录，但记录错误
        logger.error(f"[LOGIN] 会话创建失败: {user.id} - {e}")

    logger.info(f"[LOGIN] 登录成功: {user.username} ({user.id}) from {ip_address}")

    await db.commit()

    # 计算过期时间戳（Unix 时间戳，秒）
    now = get_utc_now()
    token_expires_at = int((now + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)).timestamp())
    refresh_token_expires_at = int((now + timedelta(days=refresh_token_days)).timestamp())

    return Token(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        expires_at=token_expires_at,
        refresh_expires_at=refresh_token_expires_at
    )


@router.post("/refresh", response_model=Token)
async def refresh_token(
    request: RefreshTokenRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    刷新 Token
    
    - **refresh_token**: 刷新令牌
    """
    from app.core.security import decode_token
    
    try:
        payload = decode_token(request.refresh_token)
        token_type = payload.get("type")
        
        if token_type != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token type"
            )
        
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )

        # 从原 refresh token 中读取 remember_me 状态
        remember_me = payload.get("remember_me", False)
        refresh_token_days = 30 if remember_me else 7

        # 创建新的访问令牌
        access_token = create_access_token(data={"sub": user_id})
        # 创建新的刷新令牌，保持原有的 remember_me 状态
        new_refresh_token = create_refresh_token(
            data={"sub": user_id, "remember_me": remember_me},
            expires_days=refresh_token_days
        )

        # 计算过期时间戳
        now = get_utc_now()
        token_expires_at = int((now + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)).timestamp())
        refresh_token_expires_at = int((now + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)).timestamp())

        return Token(
            access_token=access_token,
            refresh_token=new_refresh_token,
            token_type="bearer",
            expires_at=token_expires_at,
            refresh_expires_at=refresh_token_expires_at
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )


@router.post("/forgot-password")
async def forgot_password(
    request: ForgotPasswordRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    发送密码重置验证码

    - **email**: 邮箱地址

    验证码有效期为 5 分钟，每分钟最多发送一次
    """
    import logging
    logger = logging.getLogger(__name__)

    from app.services.password_reset_service import get_password_reset_service

    user_service = UserService(db)

    # 检查用户是否存在
    user = await user_service.get_user_by_email(request.email)
    if not user:
        # 安全考虑：不暴露用户是否存在，统一返回成功
        logger.warning(f"[FORGOT_PASSWORD] 邮箱不存在: {request.email}")
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"message": "如果邮箱存在，验证码已发送"}
        )

    try:
        # 发送验证码
        password_reset_service = await get_password_reset_service()
        code = await password_reset_service.send_reset_code(request.email)

        logger.info(f"[FORGOT_PASSWORD] 验证码已发送: {request.email}")

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"message": "验证码已发送到您的邮箱"}
        )
    except ValueError as e:
        # 频率限制等错误
        logger.warning(f"[FORGOT_PASSWORD] 发送失败: {request.email} - {e}")
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"[FORGOT_PASSWORD] 未知错误: {request.email} - {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="发送验证码失败，请稍后重试"
        )


@router.post("/reset-password")
async def reset_password(
    request: ResetPasswordRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    重置密码

    - **email**: 邮箱地址
    - **code**: 6位验证码
    - **new_password**: 新密码（8-20字符，必须包含字母、数字、特殊符号）

    验证码错误超过5次将被锁定5分钟
    """
    import logging
    logger = logging.getLogger(__name__)

    from app.services.password_reset_service import get_password_reset_service

    user_service = UserService(db)

    # 检查用户是否存在
    user = await user_service.get_user_by_email(request.email)
    if not user:
        logger.warning(f"[RESET_PASSWORD] 邮箱不存在: {request.email}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="邮箱不存在"
        )

    try:
        # 验证验证码
        password_reset_service = await get_password_reset_service()
        is_valid = await password_reset_service.verify_code(request.email, request.code)

        if not is_valid:
            logger.warning(f"[RESET_PASSWORD] 验证码错误: {request.email}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="验证码错误或已过期"
            )

        # 更新密码
        await user_service.update_user_password(user.id, request.new_password)
        await db.commit()

        logger.info(f"[RESET_PASSWORD] 密码重置成功: {request.email}")

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"message": "密码重置成功"}
        )
    except ValueError as e:
        # 验证码错误、锁定等错误
        logger.warning(f"[RESET_PASSWORD] 验证失败: {request.email} - {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"[RESET_PASSWORD] 未知错误: {request.email} - {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="密码重置失败，请稍后重试"
        )


@router.post("/send-email-verification")
async def send_email_verification(
    request: SendEmailVerificationRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    发送邮箱验证码（注册时使用）

    - **email**: 邮箱地址

    验证码有效期为 5 分钟，每分钟最多发送一次
    """
    import logging
    logger = logging.getLogger(__name__)

    from app.services.email_verification_service import get_email_verification_service

    user_service = UserService(db)

    # 检查邮箱是否已被注册
    existing_user = await user_service.get_user_by_email(request.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="该邮箱已被注册"
        )

    try:
        # 发送验证码
        email_verification_service = await get_email_verification_service()
        code = await email_verification_service.send_verification_code(request.email)

        logger.info(f"[EMAIL_VERIFICATION] 验证码已发送: {request.email}")

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"message": "验证码已发送到您的邮箱"}
        )
    except ValueError as e:
        # 频率限制等错误
        logger.warning(f"[EMAIL_VERIFICATION] 发送失败: {request.email} - {e}")
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"[EMAIL_VERIFICATION] 未知错误: {request.email} - {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="发送验证码失败，请稍后重试"
        )


@router.post("/verify-email")
async def verify_email(
    request: VerifyEmailRequest
):
    """
    验证邮箱验证码

    - **email**: 邮箱地址
    - **code**: 6位验证码

    验证码错误超过5次将被锁定5分钟
    """
    import logging
    logger = logging.getLogger(__name__)

    from app.services.email_verification_service import get_email_verification_service

    try:
        # 验证验证码（不消费，让用户知道验证码是否正确）
        email_verification_service = await get_email_verification_service()
        is_valid = await email_verification_service.verify_code(request.email, request.code, consume=False)

        if not is_valid:
            logger.warning(f"[EMAIL_VERIFICATION] 验证码错误: {request.email}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="验证码错误或已过期"
            )

        logger.info(f"[EMAIL_VERIFICATION] 验证成功: {request.email}")

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"message": "邮箱验证成功"}
        )
    except ValueError as e:
        # 验证码错误、锁定等错误
        logger.warning(f"[EMAIL_VERIFICATION] 验证失败: {request.email} - {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"[EMAIL_VERIFICATION] 未知错误: {request.email} - {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="邮箱验证失败，请稍后重试"
        )
