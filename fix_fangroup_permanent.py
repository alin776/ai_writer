"""
直接通过requests调用API执行SQL修复
"""
import requests

# 直接用curl执行SQL
import subprocess

sql = """
UPDATE channels
SET is_permanent = false
WHERE type = 'fangroup';
"""

# 使用psql命令
cmd = [
    'psql',
    '-h', 'localhost',
    '-U', 'postgres',
    '-d', 'ai_writer',
    '-c', sql
]

try:
    result = subprocess.run(cmd, capture_output=True, text=True, env={'PGPASSWORD': 'postgres'})
    print("STDOUT:", result.stdout)
    print("STDERR:", result.stderr)
    print("Return code:", result.returncode)

    if result.returncode == 0:
        print("\n✓ 成功将所有粉丝群设置为非永久状态")
        print("请刷新页面查看效果")
    else:
        print("\n✗ 执行失败")
except Exception as e:
    print(f"错误: {e}")
