"""清理 Prompt 缓存脚本

用途：清理所有 prompt 相关的 Redis 缓存，确保代码修改后使用新的 prompt

使用方法：
    python clear_prompt_cache.py
"""

import redis
import sys

def clear_prompt_cache():
    """清理所有 prompt 相关缓存"""
    try:
        # 连接 Redis
        r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

        # 测试连接
        r.ping()
        print("[OK] Redis 连接成功")

        # 查找所有 prompt 相关的 key
        patterns = [
            "prompt:*",
            "cache:prompt:*",
        ]

        total_deleted = 0
        for pattern in patterns:
            keys = r.keys(pattern)
            if keys:
                print(f"\n[INFO] 找到 {len(keys)} 个匹配 '{pattern}' 的缓存:")
                for key in keys[:10]:  # 只显示前10个
                    print(f"   - {key}")
                if len(keys) > 10:
                    print(f"   ... 还有 {len(keys) - 10} 个")

                # 删除这些 key
                deleted = r.delete(*keys)
                total_deleted += deleted
                print(f"[OK] 删除了 {deleted} 个缓存")

        if total_deleted == 0:
            print("\n[INFO] 没有找到需要清理的缓存")
        else:
            print(f"\n[SUCCESS] 总计删除 {total_deleted} 个缓存")
            print("\n[WARNING] 请重启后端服务以使新的 prompt 生效")

        return True

    except redis.ConnectionError as e:
        print(f"[ERROR] Redis 连接失败: {e}")
        print("\n[TIP] 提示：")
        print("   1. 检查 Redis 是否运行: wsl docker ps | grep redis")
        print("   2. 如果在 WSL Docker 中，确保端口映射正确")
        return False
    except Exception as e:
        print(f"[ERROR] 错误: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("  清理 Prompt 缓存工具")
    print("=" * 60)

    success = clear_prompt_cache()
    sys.exit(0 if success else 1)
