from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel

from app.core.database import get_db
from app.core.security import create_access_token, create_refresh_token, get_current_active_user
from app.schemas.user import UserCreate, UserResponse, Token, TokenWithUser
from app.services.user_service import UserService

router = APIRouter()


class RefreshTokenRequest(BaseModel):
    """刷新Token请求"""
    refresh_token: str


@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=TokenWithUser)
async def register(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    用户注册

    - **email**: 邮箱地址
    - **username**: 用户名（3-50字符）
    - **password**: 密码（至少6字符）

    返回 JWT Token 和用户信息
    """
    import logging
    logger = logging.getLogger(__name__)

    user_service = UserService(db)

    try:
        logger.info(f"Attempting to register user - username: {user_data.username}, email: {user_data.email}")

        # 先检查用户名是否存在
        existing_user = await user_service.get_user_by_username(user_data.username)
        if existing_user:
            logger.error(f"Username '{user_data.username}' already exists (ID: {existing_user.id})")

        # 检查邮箱是否存在
        if user_data.email:
            existing_email = await user_service.get_user_by_email(user_data.email)
            if existing_email:
                logger.error(f"Email '{user_data.email}' already exists (ID: {existing_email.id}, username: {existing_email.username})")

        user = await user_service.create_user(user_data)
        logger.info(f"User created successfully: {user.id}")

        # 创建访问令牌和刷新令牌
        access_token = create_access_token(data={"sub": str(user.id)})
        refresh_token = create_refresh_token(data={"sub": str(user.id)})

        # 构建响应对象
        response = TokenWithUser(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
            user=user
        )

        # 只有在所有操作都成功后才提交事务
        await db.commit()

        return response
    except ValueError as e:
        await db.rollback()  # 回滚事务
        logger.error(f"ValueError: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except IntegrityError as e:
        await db.rollback()  # 回滚事务
        # 数据库层面的唯一约束冲突（如并发下的重复用户名/邮箱）
        logger.error(f"IntegrityError: {e}")
        # 使用 409 更符合语义（资源冲突）
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username or email already exists")
    except Exception as e:
        await db.rollback()  # 回滚事务
        logger.error(f"Unexpected error: {type(e).__name__}: {e}")
        import traceback
        logger.error(traceback.format_exc())
        raise


@router.post("/login", response_model=TokenWithUser)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    """
    用户登录

    - **username**: 用户名或邮箱
    - **password**: 密码

    返回 JWT Token 和用户信息
    """
    user_service = UserService(db)

    user = await user_service.authenticate_user(
        form_data.username,
        form_data.password
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive"
        )

    # 创建访问令牌和刷新令牌
    access_token = create_access_token(data={"sub": str(user.id)})
    refresh_token = create_refresh_token(data={"sub": str(user.id)})

    # 构建响应对象
    response = TokenWithUser(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        user=user
    )

    # 提交事务（保存最后登录时间）
    await db.commit()

    return response


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


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user = Depends(get_current_active_user)
):
    """
    获取当前登录用户信息

    需要在请求头中携带 Bearer Token
    """
    return current_user
