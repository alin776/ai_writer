"""检查第28章的数据库内容"""
import asyncio
import asyncpg
import json


async def check_chapter_content():
    """查询第28章的实际内容"""
    # 连接数据库
    conn = await asyncpg.connect(
        user='novelaide',
        password='novelaide_password',
        database='novelaide',
        host='localhost',
        port=5432
    )

    try:
        # 查询所有作品
        works = await conn.fetch("SELECT id, title FROM works ORDER BY created_at DESC LIMIT 5")
        print("=" * 80)
        print("最近的5部作品：")
        print("=" * 80)
        for work in works:
            print(f"作品ID: {work['id']}, 标题: {work['title']}")

        if works:
            work_id = works[0]['id']
            print(f"\n将查询作品 {works[0]['title']} (ID: {work_id}) 的第28章")

            # 查询第28章
            chapter = await conn.fetchrow(
                """
                SELECT id, title, "order", content, word_count, status
                FROM chapters
                WHERE work_id = $1 AND "order" = 28
                """,
                work_id
            )

            if chapter:
                print("\n" + "=" * 80)
                print(f"第28章信息：")
                print("=" * 80)
                print(f"章节ID: {chapter['id']}")
                print(f"标题: {chapter['title']}")
                print(f"序号: {chapter['order']}")
                print(f"字数: {chapter['word_count']}")
                print(f"状态: {chapter['status']}")
                print(f"内容长度: {len(chapter['content']) if chapter['content'] else 0} 字符")

                if chapter['content']:
                    content = chapter['content']

                    # 将内容写入文件
                    with open("chapter_28_from_db.txt", "w", encoding="utf-8") as f:
                        f.write("=" * 80 + "\n")
                        f.write("第28章完整内容（从数据库）\n")
                        f.write("=" * 80 + "\n\n")
                        f.write(content)

                    print("\n内容已写入 chapter_28_from_db.txt")

                    print("\n" + "=" * 80)
                    print("内容前500字：")
                    print("=" * 80)
                    with open("chapter_28_preview.txt", "w", encoding="utf-8") as f:
                        f.write(content[:500])
                    print("已写入 chapter_28_preview.txt")

                    print("\n" + "=" * 80)
                    print("内容特征检查：")
                    print("=" * 80)

                    # 检查关键词
                    keywords_check = {
                        "段融": "段融" in content,
                        "林寻": "林寻" in content,
                        "宁蒙": "宁蒙" in content,
                        "血鹿茸": "血鹿茸" in content,
                        "灵海境": "灵海境" in content,
                        "内息": "内息" in content,
                        "宁家": "宁家" in content,
                        "九州八宗": "九州八宗" in content,
                        "青阳门": "青阳门" in content
                    }

                    for keyword, exists in keywords_check.items():
                        status = "FOUND" if exists else "NOT_FOUND"
                        print(f"{keyword}: {status}")
                else:
                    print("\n⚠️ 章节内容为空！")
            else:
                print(f"\n⚠️ 未找到第28章")

                # 查看该作品有多少章
                chapter_count = await conn.fetchval(
                    "SELECT COUNT(*) FROM chapters WHERE work_id = $1",
                    work_id
                )
                print(f"该作品共有 {chapter_count} 章")

                # 列出前30章
                chapters = await conn.fetch(
                    """
                    SELECT "order", title
                    FROM chapters
                    WHERE work_id = $1
                    ORDER BY "order"
                    LIMIT 30
                    """,
                    work_id
                )
                print("\n前30章列表：")
                for ch in chapters:
                    print(f"第{ch['order']}章: {ch['title']}")

    finally:
        await conn.close()


if __name__ == "__main__":
    asyncio.run(check_chapter_content())
