-- NovelAIde 数据库初始化脚本

-- 创建数据库
CREATE DATABASE novelaide
    WITH 
    OWNER = postgres
    ENCODING = 'UTF8'
    LC_COLLATE = 'Chinese (Simplified)_China.936'
    LC_CTYPE = 'Chinese (Simplified)_China.936'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1;

-- 切换到 novelaide 数据库
\c novelaide

-- 创建用户
CREATE USER novelaide WITH PASSWORD 'novelaide_password';

-- 授予权限
GRANT ALL PRIVILEGES ON DATABASE novelaide TO novelaide;
GRANT ALL PRIVILEGES ON SCHEMA public TO novelaide;

-- 安装 UUID 扩展（用于生成 UUID）
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ============================================
-- 安装 pgvector 扩展（小说分析功能需要）
-- 注意：需要先在PostgreSQL服务器上编译安装pgvector
-- 详见：INSTALL_PGVECTOR_EXTENSION.md
-- ============================================
CREATE EXTENSION IF NOT EXISTS vector;

-- 验证安装
SELECT version();
SELECT extname, extversion FROM pg_extension WHERE extname IN ('uuid-ossp', 'vector');
