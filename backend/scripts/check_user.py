# -*- coding: utf-8 -*-
"""
用户诊断和密码重置脚本

用法:
    # 查询所有用户
    python scripts/check_user.py list

    # 查询特定用户
    python scripts/check_user.py check Drew

    # 重置用户密码
    python scripts/check_user.py reset Drew NewPassword123!

    # 创建新用户（跳过邀请码验证）
    python scripts/check_user.py create username email@example.com Password123!
"""

import sys
import os
import asyncio
import io

# 设置标准输出编码为 UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import re
from sqlalchemy import select, text
from app.core.database import AsyncSessionLocal, engine
from app.models.user import User
from app.core.security import get_password_hash, verify_password


def validate_password_strength(password: str) -> tuple[bool, str]:
    """
    验证密码强度
    - 长度8-20位
    - 必须包含字母、数字、特殊符号三种字符

    返回: (是否通过, 错误信息)
    """
    if len(password) < 8:
        return False, "密码长度至少为8位"
    if len(password) > 20:
        return False, "密码长度不能超过20位"

    has_letter = bool(re.search(r'[a-zA-Z]', password))
    has_number = bool(re.search(r'\d', password))
    has_special = bool(re.search(r'[!@#$%^&*()_+\-=\[\]{};\':"\\|,.<>\/?]', password))

    if not (has_letter and has_number and has_special):
        return False, "密码必须包含字母、数字、特殊符号三种字符"

    return True, ""


async def list_users():
    """列出所有用户"""
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(User.id, User.username, User.email, User.is_active, User.is_admin, User.created_at)
            .order_by(User.created_at.desc())
        )
        users = result.all()

        if not users:
            print("\n[ERROR] 数据库中没有任何用户！")
            print("   请先通过网页注册用户，或使用 'create' 命令创建用户。")
            return

        print(f"\n[INFO] 共找到 {len(users)} 个用户:\n")
        print("-" * 100)
        print(f"{'ID':<36} | {'用户名':<15} | {'邮箱':<25} | {'激活':<4} | {'管理员':<6} | {'创建时间'}")
        print("-" * 100)

        for user in users:
            user_id, username, email, is_active, is_admin, created_at = user
            active_str = "[Y]" if is_active else "[N]"
            admin_str = "[Y]" if is_admin else "[N]"
            created_str = created_at.strftime("%Y-%m-%d %H:%M") if created_at else "N/A"
            print(f"{str(user_id):<36} | {username:<15} | {email:<25} | {active_str:<4} | {admin_str:<6} | {created_str}")

        print("-" * 100)


async def check_user(username: str):
    """检查用户是否存在"""
    async with AsyncSessionLocal() as session:
        # 按用户名查找
        result = await session.execute(
            select(User).where(User.username == username)
        )
        user = result.scalar_one_or_none()

        if not user:
            # 按邮箱查找
            result = await session.execute(
                select(User).where(User.email == username)
            )
            user = result.scalar_one_or_none()

        if not user:
            print(f"\n[ERROR] 用户 '{username}' 不存在！")
            print("\n可能的解决方案:")
            print("  1. 检查用户名拼写是否正确（区分大小写）")
            print("  2. 使用 'list' 命令查看所有用户")
            print("  3. 前往 /register 页面注册新用户")
            print("  4. 使用 'create' 命令创建用户")
            return None

        print(f"\n[OK] 找到用户:")
        print(f"   ID: {user.id}")
        print(f"   用户名: {user.username}")
        print(f"   邮箱: {user.email}")
        print(f"   激活状态: {'已激活' if user.is_active else '未激活'}")
        print(f"   管理员: {'是' if user.is_admin else '否'}")
        print(f"   创建时间: {user.created_at}")
        print(f"   最后登录: {user.last_login_at or '从未登录'}")

        return user


async def reset_password(username: str, new_password: str):
    """重置用户密码"""
    async with AsyncSessionLocal() as session:
        # 查找用户
        result = await session.execute(
            select(User).where(User.username == username)
        )
        user = result.scalar_one_or_none()

        if not user:
            result = await session.execute(
                select(User).where(User.email == username)
            )
            user = result.scalar_one_or_none()

        if not user:
            print(f"\n[ERROR] 用户 '{username}' 不存在！")
            return False

        # 验证密码强度
        is_valid, error_msg = validate_password_strength(new_password)
        if not is_valid:
            print(f"\n[ERROR] {error_msg}")
            print("   密码要求: 8-20位，必须包含字母、数字、特殊符号")
            return False

        # 重置密码
        user.hashed_password = get_password_hash(new_password)
        await session.commit()

        print(f"\n[OK] 用户 '{user.username}' 的密码已重置！")
        print(f"   新密码: {new_password}")
        print(f"\n   现在可以使用新密码登录了。")
        return True


async def create_user(username: str, email: str, password: str, is_admin: bool = False):
    """创建新用户（跳过邀请码验证）"""
    async with AsyncSessionLocal() as session:
        # 检查用户名是否存在
        result = await session.execute(
            select(User).where(User.username == username)
        )
        if result.scalar_one_or_none():
            print(f"\n[ERROR] 用户名 '{username}' 已存在！")
            return False

        # 检查邮箱是否存在
        result = await session.execute(
            select(User).where(User.email == email)
        )
        if result.scalar_one_or_none():
            print(f"\n[ERROR] 邮箱 '{email}' 已被注册！")
            return False

        # 验证密码强度
        is_valid, error_msg = validate_password_strength(password)
        if not is_valid:
            print(f"\n[ERROR] {error_msg}")
            print("   密码要求: 8-20位，必须包含字母、数字、特殊符号")
            return False

        # 创建用户
        user = User(
            username=username,
            email=email,
            hashed_password=get_password_hash(password),
            is_active=True,
            is_admin=is_admin,
            is_verified=True,  # 直接验证
        )

        session.add(user)
        await session.commit()
        await session.refresh(user)

        print(f"\n[OK] 用户创建成功！")
        print(f"   ID: {user.id}")
        print(f"   用户名: {username}")
        print(f"   邮箱: {email}")
        print(f"   密码: {password}")
        print(f"   管理员: {'是' if is_admin else '否'}")
        print(f"\n   现在可以使用这些凭据登录了。")
        return True


async def test_password(username: str, password: str):
    """测试密码是否正确"""
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(User).where(User.username == username)
        )
        user = result.scalar_one_or_none()

        if not user:
            result = await session.execute(
                select(User).where(User.email == username)
            )
            user = result.scalar_one_or_none()

        if not user:
            print(f"\n[ERROR] 用户 '{username}' 不存在！")
            return False

        if verify_password(password, user.hashed_password):
            print(f"\n[OK] 密码正确！用户 '{user.username}' 可以正常登录。")
            return True
        else:
            print(f"\n[ERROR] 密码错误！")
            print(f"   用户 '{user.username}' 存在，但密码不匹配。")
            print(f"   请使用 'reset' 命令重置密码。")
            return False


async def test_db_connection():
    """测试数据库连接"""
    try:
        async with engine.connect() as conn:
            result = await conn.execute(text("SELECT 1"))
            result.fetchone()
        print("[OK] 数据库连接正常")
        return True
    except Exception as e:
        print(f"[ERROR] 数据库连接失败: {e}")
        return False


def print_help():
    """打印帮助信息"""
    print(__doc__)
    print("\n命令列表:")
    print("  list                           - 列出所有用户")
    print("  check <用户名或邮箱>            - 检查用户是否存在")
    print("  reset <用户名或邮箱> <新密码>   - 重置用户密码")
    print("  create <用户名> <邮箱> <密码>   - 创建新用户")
    print("  create-admin <用户名> <邮箱> <密码> - 创建管理员用户")
    print("  test <用户名或邮箱> <密码>      - 测试密码是否正确")
    print("  db                             - 测试数据库连接")
    print("  help                           - 显示帮助信息")


async def main():
    if len(sys.argv) < 2:
        print_help()
        return

    command = sys.argv[1].lower()

    # 先测试数据库连接
    if command != "help":
        print("正在连接数据库...")
        if not await test_db_connection():
            print("\n请检查:")
            print("  1. PostgreSQL 是否正在运行")
            print("  2. .env 文件中的 DATABASE_URL 是否正确")
            print("  3. 数据库用户名和密码是否正确")
            return

    if command == "list":
        await list_users()

    elif command == "check":
        if len(sys.argv) < 3:
            print("用法: python scripts/check_user.py check <用户名或邮箱>")
            return
        await check_user(sys.argv[2])

    elif command == "reset":
        if len(sys.argv) < 4:
            print("用法: python scripts/check_user.py reset <用户名或邮箱> <新密码>")
            return
        await reset_password(sys.argv[2], sys.argv[3])

    elif command == "create":
        if len(sys.argv) < 5:
            print("用法: python scripts/check_user.py create <用户名> <邮箱> <密码>")
            return
        await create_user(sys.argv[2], sys.argv[3], sys.argv[4])

    elif command == "create-admin":
        if len(sys.argv) < 5:
            print("用法: python scripts/check_user.py create-admin <用户名> <邮箱> <密码>")
            return
        await create_user(sys.argv[2], sys.argv[3], sys.argv[4], is_admin=True)

    elif command == "test":
        if len(sys.argv) < 4:
            print("用法: python scripts/check_user.py test <用户名或邮箱> <密码>")
            return
        await test_password(sys.argv[2], sys.argv[3])

    elif command == "db":
        pass  # 已经测试过了

    elif command == "help":
        print_help()

    else:
        print(f"未知命令: {command}")
        print_help()


if __name__ == "__main__":
    asyncio.run(main())
