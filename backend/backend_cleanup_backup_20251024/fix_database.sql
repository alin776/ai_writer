-- 手动修复数据库迁移
-- 添加缺失的字段和表

-- 步骤 1: 添加 notification_settings 和 preferences 字段到 users 表
ALTER TABLE users
ADD COLUMN IF NOT EXISTS notification_settings JSONB NOT NULL DEFAULT '{}'::jsonb,
ADD COLUMN IF NOT EXISTS preferences JSONB NOT NULL DEFAULT '{}'::jsonb;

-- 步骤 2: 创建 user_sessions 表（如果不存在）
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

-- 步骤 3: 创建索引
CREATE INDEX IF NOT EXISTS ix_user_sessions_id ON user_sessions(id);
CREATE INDEX IF NOT EXISTS ix_user_sessions_user_id ON user_sessions(user_id);

-- 验证
SELECT column_name, data_type
FROM information_schema.columns
WHERE table_name = 'users'
AND column_name IN ('notification_settings', 'preferences');

SELECT EXISTS (
    SELECT FROM information_schema.tables
    WHERE table_name = 'user_sessions'
) AS user_sessions_exists;
