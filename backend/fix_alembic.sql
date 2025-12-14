-- 删除错误的迁移记录
DELETE FROM alembic_version WHERE version_num = '16144b2711da';

-- 如果需要，可以手动删除tasks表
-- DROP TABLE IF EXISTS tasks CASCADE;
