"""测试活动通知 API"""
import requests
import json

# 配置
API_BASE = "http://localhost:8000/api/v1"
# 请替换为你的实际 token
TOKEN = "your_admin_token_here"

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

# 测试数据
test_notification = {
    "title": "测试活动-API直接测试",
    "content": "这是通过 API 直接创建的测试活动",
    "category": "announcement",
    "type": "event",
    "priority": "normal",
    "displayType": ["notification", "modal"],
    "targetUsers": "all",
    "validFrom": "2025-12-12T00:00:00Z",
    "validUntil": "2025-12-20T23:59:59Z",
    "activityType": "invitation",
    "activityRules": {
        "type": "invitation",
        "inviterRewards": [
            {
                "type": "points",
                "name": "邀请者奖励",
                "amount": 500
            }
        ],
        "inviteeRewards": [
            {
                "type": "points",
                "name": "被邀请者奖励",
                "amount": 300
            }
        ],
        "requirementForInvitee": "完成首次任务"
    },
    "publishType": "immediate"
}

print("=" * 80)
print("发送创建通知请求...")
print("=" * 80)
print(json.dumps(test_notification, indent=2, ensure_ascii=False))
print("=" * 80)

# 发送请求
response = requests.post(
    f"{API_BASE}/admin/notifications",
    headers=headers,
    json=test_notification
)

print(f"\n响应状态码: {response.status_code}")
print(f"响应内容:")
print(json.dumps(response.json(), indent=2, ensure_ascii=False))

if response.status_code == 200:
    notification_id = response.json()["id"]
    print(f"\n✅ 通知创建成功! ID: {notification_id}")

    # 立即查询刚创建的通知
    print("\n" + "=" * 80)
    print("查询刚创建的通知...")
    print("=" * 80)

    get_response = requests.get(
        f"{API_BASE}/admin/notifications/{notification_id}",
        headers=headers
    )

    if get_response.status_code == 200:
        notification_data = get_response.json()
        print(json.dumps(notification_data, indent=2, ensure_ascii=False))

        print("\n" + "=" * 80)
        print("检查关键字段:")
        print("=" * 80)
        print(f"activityType: {notification_data.get('activityType')}")
        print(f"activityRules: {notification_data.get('activityRules')}")

        if notification_data.get('activityType') and notification_data.get('activityRules'):
            print("\n✅ 活动数据保存成功！")
        else:
            print("\n❌ 活动数据未保存！")
    else:
        print(f"❌ 查询失败: {get_response.status_code}")
else:
    print(f"❌ 创建失败: {response.text}")
