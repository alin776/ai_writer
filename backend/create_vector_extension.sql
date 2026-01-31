-- 创建 pgvector 扩展
CREATE EXTENSION IF NOT EXISTS vector;

-- 验证扩展是否已创建
SELECT * FROM pg_extension WHERE extname = 'vector';
