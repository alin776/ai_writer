# -*- coding: utf-8 -*-
"""测试Chapter API是否返回work_id"""
import requests
import json
import sys
import io

# 设置输出编码为UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# API配置
BASE_URL = "http://localhost:8000"
CHAPTER_ID = "07ede618-df82-425a-b0bb-427d686679e5"

print("=" * 60)
print("步骤0: 注册测试用户")
print("=" * 60)

# 注册新用户
register_url = f"{BASE_URL}/api/v1/auth/register"
register_data = {
    "email": "test_chapter@test.com",
    "username": "test_chapter_user",
    "password": "test123456"
}

try:
    register_response = requests.post(register_url, json=register_data)
    print(f"注册状态码: {register_response.status_code}")
    if register_response.status_code in [200, 201]:
        print("✅ 注册成功")
    elif register_response.status_code == 409:
        print("ℹ️ 用户已存在，继续登录")
    else:
        print(f"⚠️ 注册响应: {register_response.text}")
except Exception as e:
    print(f"⚠️ 注册异常: {e}")

# 先登录获取token
login_url = f"{BASE_URL}/api/v1/auth/login"
# OAuth2PasswordRequestForm需要使用form-data格式
login_data = {
    "username": "test_chapter_user",
    "password": "test123456"
}

print("=" * 60)
print("步骤1: 登录获取Token")
print("=" * 60)

try:
    # 使用form-data格式
    login_response = requests.post(login_url, data=login_data)
    print(f"登录状态码: {login_response.status_code}")

    if login_response.status_code == 200:
        token_data = login_response.json()
        access_token = token_data.get("access_token")
        print(f"✅ 登录成功，获取到token: {access_token[:50]}...")

        # 设置请求头
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
    else:
        print(f"❌ 登录失败: {login_response.text}")
        exit(1)
except Exception as e:
    print(f"❌ 登录异常: {e}")
    exit(1)

print("\n" + "=" * 60)
print("步骤2: 创建测试作品")
print("=" * 60)

# 创建作品
work_url = f"{BASE_URL}/api/v1/works"
work_data = {
    "title": "测试作品 - Chapter Work ID",
    "genre": "fantasy",
    "description": "用于测试work_id字段"
}

try:
    work_response = requests.post(work_url, json=work_data, headers=headers)
    print(f"创建作品状态码: {work_response.status_code}")

    if work_response.status_code in [200, 201]:
        work_result = work_response.json()
        work_id = work_result.get("id")
        print(f"✅ 作品创建成功，work_id: {work_id}")
    else:
        print(f"❌ 创建作品失败: {work_response.text}")
        exit(1)
except Exception as e:
    print(f"❌ 创建作品异常: {e}")
    exit(1)

print("\n" + "=" * 60)
print("步骤3: 创建测试章节")
print("=" * 60)

# 创建章节
chapter_url = f"{BASE_URL}/api/v1/chapters"
chapter_data = {
    "work_id": work_id,
    "title": "第一章 测试章节",
    "content": "这是测试内容，用于验证work_id字段是否正确返回。",
    "order": 1
}

try:
    chapter_response = requests.post(chapter_url, json=chapter_data, headers=headers)
    print(f"创建章节状态码: {chapter_response.status_code}")

    if chapter_response.status_code in [200, 201]:
        chapter_result = chapter_response.json()
        chapter_id = chapter_result.get("id")
        print(f"✅ 章节创建成功，chapter_id: {chapter_id}")
        CHAPTER_ID = chapter_id
    else:
        print(f"❌ 创建章节失败: {chapter_response.text}")
        exit(1)
except Exception as e:
    print(f"❌ 创建章节异常: {e}")
    exit(1)

print("\n" + "=" * 60)
print("步骤4: 获取Chapter数据")
print("=" * 60)

# 获取Chapter数据
chapter_url = f"{BASE_URL}/api/v1/chapters/{CHAPTER_ID}"

try:
    chapter_response = requests.get(chapter_url, headers=headers)
    print(f"请求URL: {chapter_url}")
    print(f"响应状态码: {chapter_response.status_code}")

    if chapter_response.status_code == 200:
        chapter_data = chapter_response.json()

        print("\n" + "=" * 60)
        print("步骤5: 验证work_id字段")
        print("=" * 60)

        # 美化输出
        print("\n📄 完整响应数据:")
        print(json.dumps(chapter_data, indent=2, ensure_ascii=False))

        # 检查work_id
        print("\n" + "=" * 60)
        print("✅ 验证结果")
        print("=" * 60)

        has_work_id = "work_id" in chapter_data
        work_id_value = chapter_data.get("work_id")
        work_id_type = type(work_id_value).__name__

        print(f"1. work_id字段存在: {'✅ 是' if has_work_id else '❌ 否'}")
        if has_work_id:
            print(f"2. work_id值: {work_id_value}")
            print(f"3. work_id类型: {work_id_type}")
            print(f"4. work_id是否为有效UUID: {'✅ 是' if len(str(work_id_value)) == 36 else '❌ 否'}")

        # 显示所有字段
        print(f"\n📋 所有字段列表:")
        for key in chapter_data.keys():
            print(f"   - {key}: {type(chapter_data[key]).__name__}")

    else:
        print(f"❌ 获取章节失败: {chapter_response.text}")

except Exception as e:
    print(f"❌ 请求异常: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
