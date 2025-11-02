from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel

from app.core.database import get_db
from app.core.security import create_access_token, create_refresh_token
from app.schemas.user import UserCreate, UserResponse, Token, AuthResponse
from app.services.user_service import UserService
from app.utils.device_parser import parse_user_agent, get_client_ip

router = APIRouter()


class RefreshTokenRequest(BaseModel):
    """刷新Token请求"""
    refresh_token: str


@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
async def register(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    用户注册
    
    - **email**: 邮箱地址
    - **username**: 用户名（3-50字符）
    - **password**: 密码（至少6字符）
    
    注册成功后请前往登录页面登录
    """
    import logging
    logger = logging.getLogger(__name__)
    
    user_service = UserService(db)
    
    try:
        logger.info(f"Creating user: {user_data.username}")
        user = await user_service.create_user(user_data)
        logger.info(f"User created successfully: {user.id}")
        
        # 只返回用户信息，不返回 token
        # 用户需要手动登录
        return user
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
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    """
    用户登录

    - **username**: 用户名或邮箱
    - **password**: 密码

    返回 JWT Token
    """
    import logging
    logger = logging.getLogger(__name__)

    logger.info(f"[LOGIN] 尝试登录: {form_data.username}")

    user_service = UserService(db)

    user = await user_service.authenticate_user(
        form_data.username,
        form_data.password
    )

    if not user:
        logger.warning(f"[LOGIN] 登录失败: {form_data.username} - 用户名或密码错误")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        logger.warning(f"[LOGIN] 登录失败: {form_data.username} - 账户已禁用")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive"
        )

    # 创建访问令牌和刷新令牌
    access_token = create_access_token(data={"sub": str(user.id)})
    refresh_token = create_refresh_token(data={"sub": str(user.id)})

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

    return Token(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer"
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
        
        # 创建新的访问令牌
        access_token = create_access_token(data={"sub": user_id})
        new_refresh_token = create_refresh_token(data={"sub": user_id})
        
        return Token(
            access_token=access_token,
            refresh_token=new_refresh_token,
            token_type="bearer"
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )
