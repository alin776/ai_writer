"""
设置用户为管理员角色

运行此脚本可以将指定用户设置为管理员
"""
import asyncio
import sys
import io
from pathlib import Path

# Windows 编码兼容
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

sys.path.insert(0, str(Path(__file__).parent))

from sqlalchemy import select, update
from app.core.database import AsyncSessionLocal
from app.models.user import User


async def list_users():
    """列出所有用户"""
    async with AsyncSessionLocal() as db:
        result = await db.execute(select(User))
        users = result.scalars().all()
        
        if not users:
            print("❌ 数据库中没有用户")
            return None
        
        print("\n📋 当前用户列表：")
        print("=" * 60)
        for i, user in enumerate(users, 1):
            role_str = "管理员" if user.is_admin else "普通用户"
            print(f"{i}. {user.username} ({user.email}) - {role_str}")
        print("=" * 60)
        
        return users


async def set_admin(user_id: str):
    """设置用户为管理员"""
    async with AsyncSessionLocal() as db:
        # 更新用户为管理员
        await db.execute(
            update(User)
            .where(User.id == user_id)
            .values(is_admin=True)
        )
        await db.commit()
        
        # 验证更新
        result = await db.execute(
            select(User).where(User.id == user_id)
        )
        user = result.scalar_one()
        return user


async def main():
    print("🔧 设置管理员角色工具")
    print("=" * 60)
    
    # 列出所有用户
    users = await list_users()
    if not users:
        return
    
    # 选择用户
    try:
        choice = input("\n请选择要设置为管理员的用户编号（输入 q 退出）: ").strip()
        
        if choice.lower() == 'q':
            print("👋 已取消")
            return
        
        index = int(choice) - 1
        if index < 0 or index >= len(users):
            print("❌ 无效的编号")
            return
        
        selected_user = users[index]
        
        # 确认
        confirm = input(f"\n确认将 {selected_user.username} 设置为管理员？(y/n): ").strip().lower()
        
        if confirm != 'y':
            print("👋 已取消")
            return
        
        # 设置管理员
        updated_user = await set_admin(selected_user.id)
        
        print(f"\n✅ 成功！用户 {updated_user.username} 已设置为管理员")
        print(f"   邮箱: {updated_user.email}")
        print(f"   管理员: {updated_user.is_admin}")
        
    except ValueError:
        print("❌ 请输入有效的数字")
    except Exception as e:
        print(f"❌ 错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
