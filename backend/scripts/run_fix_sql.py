"""
自动修复数据库脚本
添加缺失的字段和表
"""
import sys
import os
import asyncio

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine, text
from app.core.config import settings


async def main():
    """执行数据库修复"""
    print("=" * 60)
    print("数据库修复脚本")
    print("=" * 60)

    # 创建同步引擎（用于执行 DDL）
    engine = create_engine(settings.DATABASE_URL.replace('+asyncpg', ''))

    try:
        with engine.connect() as conn:
            print("\n步骤 1: 添加 notification_settings 和 preferences 字段...")

            # 添加字段
            conn.execute(text("""
                ALTER TABLE users
                ADD COLUMN IF NOT EXISTS notification_settings JSONB NOT NULL DEFAULT '{}'::jsonb,
                ADD COLUMN IF NOT EXISTS preferences JSONB NOT NULL DEFAULT '{}'::jsonb;
            """))
            conn.commit()
            print("✅ 字段添加成功")

            print("\n步骤 2: 创建 user_sessions 表...")

            # 创建表
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS user_sessions (
                    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                    session_token VARCHAR(255) NOT NULL UNIQUE,
                    refresh_token VARCHAR(255),
                    device_type VARCHAR(50),
                    device_name VARCHAR(100),
                    browser VARCHAR(100),
                    browser_version VARCHAR(50),
                    operating_system VARCHAR(100),
                    ip_address VARCHAR(45),
                    location VARCHAR(255),
                    user_agent VARCHAR(500),
                    is_active BOOLEAN NOT NULL DEFAULT true,
                    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),
                    last_active_at TIMESTAMP WITH TIME ZONE,
                    expires_at TIMESTAMP WITH TIME ZONE,
                    logged_out_at TIMESTAMP WITH TIME ZONE
                );
            """))
            conn.commit()
            print("✅ user_sessions 表创建成功")

            print("\n步骤 3: 创建索引...")

            # 创建索引
            conn.execute(text("""
                CREATE INDEX IF NOT EXISTS ix_user_sessions_id ON user_sessions(id);
            """))
            conn.execute(text("""
                CREATE INDEX IF NOT EXISTS ix_user_sessions_user_id ON user_sessions(user_id);
            """))
            conn.commit()
            print("✅ 索引创建成功")

            print("\n步骤 4: 验证修复...")

            # 验证字段
            result = conn.execute(text("""
                SELECT column_name, data_type
                FROM information_schema.columns
                WHERE table_name = 'users'
                AND column_name IN ('notification_settings', 'preferences');
            """))
            columns = result.fetchall()

            print(f"\n找到的字段:")
            for col in columns:
                print(f"  - {col[0]}: {col[1]}")

            # 验证表
            result = conn.execute(text("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables
                    WHERE table_name = 'user_sessions'
                );
            """))
            table_exists = result.scalar()

            print(f"\nuser_sessions 表存在: {'✅ 是' if table_exists else '❌ 否'}")

            print("\n" + "=" * 60)
            print("✅ 数据库修复完成!")
            print("=" * 60)
            print("\n请重启后端服务:")
            print("  python -m uvicorn app.main:app --reload --port 8000")

    except Exception as e:
        print(f"\n❌ 修复失败: {e}")
        print("\n请检查:")
        print("1. 数据库连接是否正确")
        print("2. 用户是否有修改表结构的权限")
        print("3. 数据库是否正在运行")
        return 1
    finally:
        engine.dispose()

    return 0


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
