import asyncio
from sqlalchemy import text
from app.core.database import AsyncSessionLocal

async def check():
    async with AsyncSessionLocal() as db:
        work_id = '3ad137d3-650a-41c2-acba-8e93fd6232fc'
        
        print('=== 检查作品的所有角色 ===')
        result = await db.execute(text(f"""
            SELECT id, name FROM characters WHERE work_id = '{work_id}' ORDER BY created_at
        """))
        characters = result.fetchall()
        print(f'角色总数: {len(characters)}')
        for i, (char_id, char_name) in enumerate(characters, 1):
            print(f'角色{i}: {char_id} - {char_name}')
        
        print('\n=== 检查关系引用的角色 ===')
        source_id = 'ed26a6dd-13d8-4333-b62a-8e18d29069bd'
        target_id = 'a5ef7481-ac45-40b3-ad84-eaf0dca2f326'
        
        result = await db.execute(text(f"""
            SELECT id, name, work_id FROM characters WHERE id IN ('{source_id}', '{target_id}')
        """))
        rel_chars = result.fetchall()
        print(f'关系引用的角色数: {len(rel_chars)}')
        for char_id, char_name, char_work_id in rel_chars:
            print(f'  {char_id} - {char_name}')
            print(f'  角色work_id: {char_work_id} (类型: {type(char_work_id)})')
            print(f'  查询work_id: {work_id} (类型: {type(work_id)})')
            print(f'  字符串比较: {str(char_work_id) == work_id}')

asyncio.run(check())
