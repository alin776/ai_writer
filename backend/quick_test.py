"""
快速测试脚本 - AI评价功能

简单快速地测试评价API是否正常工作
"""

import requests
import json

# 配置
BASE_URL = "http://localhost:8000"
USERNAME = "2072855200@qq.com"  # 可以是用户名或邮箱
PASSWORD = "zrt3ljnygz@163.com"

# 测试文本
TEXT = "林风深吸一口气,推开木门。房间里灰尘飞舞,桌上的剑散发着强大气息。他握住剑柄,炽热能量涌入体内,眼前景象扭曲变形。恍惚间看到白发老者站在云端。幻象消失后,林风知道命运将要改变。"

print("登录中...")
# 1. 登录 (使用表单数据)
resp = requests.post(f"{BASE_URL}/api/v1/auth/login", data={
    "username": USERNAME,
    "password": PASSWORD
})
token = resp.json()["access_token"]
print(f"✅ 登录成功! Token: {token[:20]}...\n")

print("调用评价API...")
# 2. 调用评价
resp = requests.post(
    f"{BASE_URL}/api/v1/ai/evaluate",
    headers={"Authorization": f"Bearer {token}"},
    json={
        "text": TEXT,
        "operation_type": "continue",
        "context": {
            "work_title": "测试小说",
            "chapter_title": "第一章"
        }
    },
    timeout=60
)

result = resp.json()
print("✅ 评价成功!\n")

# 3. 显示结果
print(f"总分: {result['overall_score']:.1f}/100")
print(f"\n5维度评分:")
dims = result['dimensions']
print(f"  文学性: {dims['literary_quality']:.1f}")
print(f"  连贯性: {dims['coherence']:.1f}")
print(f"  创意性: {dims['creativity']:.1f}")
print(f"  情感感染力: {dims['emotional_impact']:.1f}")
print(f"  节奏把控: {dims['pacing']:.1f}")

print(f"\n优点: {', '.join(result['highlights'])}")
print(f"问题: {', '.join(result['issues'])}")
print(f"建议: {', '.join(result['suggestions'])}")

print(f"\n评价ID: {result['evaluation_id']}")
print("\n✅ 测试完成!")
