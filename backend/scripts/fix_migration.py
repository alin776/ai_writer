"""
数据库迁移修复脚本

问题：Alembic 迁移版本与数据库实际状态不一致
解决：手动标记已存在的迁移为完成
"""
import sys
import os

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine, text
from app.core.config import settings

def main():
    """修复迁移版本"""
    print("=" * 60)
    print("数据库迁移修复工具")
    print("=" * 60)

    # 创建数据库连接
    engine = create_engine(settings.DATABASE_URL)

    print("\n步骤 1: 检查当前迁移版本...")
    with engine.connect() as conn:
        # 检查 alembic_version 表是否存在
        result = conn.execute(text("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables
                WHERE table_name = 'alembic_version'
            );
        """))
        table_exists = result.scalar()

        if not table_exists:
            print("❌ alembic_version 表不存在，需要先初始化数据库")
            return

        # 获取当前版本
        result = conn.execute(text("SELECT version_num FROM alembic_version;"))
        current_version = result.scalar()
        print(f"✅ 当前数据库版本: {current_version}")

    print("\n步骤 2: 检查需要运行的迁移...")
    # 我们新增的会话管理迁移版本
    target_version = "d1e2f3g4h5i6"  # 20251024_1015_add_user_settings_and_sessions.py

    print(f"目标版本: {target_version}")

    print("\n步骤 3: 检查 user_sessions 表是否已存在...")
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables
                WHERE table_name = 'user_sessions'
            );
        """))
        user_sessions_exists = result.scalar()

        if user_sessions_exists:
            print("✅ user_sessions 表已存在，迁移可能已完成")
        else:
            print("⚠️  user_sessions 表不存在，需要运行迁移")

    print("\n步骤 4: 检查 notification_settings 和 preferences 字段...")
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT column_name
            FROM information_schema.columns
            WHERE table_name = 'users'
            AND column_name IN ('notification_settings', 'preferences');
        """))
        existing_columns = [row[0] for row in result]
        print(f"已存在的字段: {existing_columns}")

    print("\n" + "=" * 60)
    print("修复建议:")
    print("=" * 60)

    if user_sessions_exists and len(existing_columns) == 2:
        print("✅ 数据库结构已完整，无需运行迁移")
        print("\n请直接启动应用：")
        print("  python -m uvicorn app.main:app --reload")
    else:
        print("⚠️  需要手动修复迁移")
        print("\n请执行以下步骤：")
        print("1. 运行以下 SQL 标记迁移为完成：")
        print(f"   UPDATE alembic_version SET version_num = '{target_version}';")
        print("\n2. 或者使用 Alembic 命令：")
        print(f"   alembic stamp {target_version}")

    engine.dispose()

if __name__ == "__main__":
    main()
