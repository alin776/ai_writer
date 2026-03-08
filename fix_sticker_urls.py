"""
Fix existing sticker messages in database by proxying Tenor URLs to COS.
Run inside the backend container:
  docker exec wenshu_backend python /app/fix_sticker_urls.py
"""
import asyncio
import re
import httpx
import os
import sys

# Add app to path
sys.path.insert(0, os.path.dirname(__file__))


async def main():
    from app.core.database import engine as async_engine
    from app.services.cos_service import get_cos_service
    from sqlalchemy import text

    cos_service = get_cos_service()
    cos_host = cos_service.host or ""
    cos_bucket_host = f"{cos_service.bucket}.cos."

    # Find all sticker messages with Tenor URLs
    async with async_engine.connect() as conn:
        result = await conn.execute(text(
            "SELECT id, content FROM channel_messages "
            "WHERE content LIKE '%![sticker](%tenor.com%' "
            "ORDER BY created_at DESC"
        ))
        rows = result.fetchall()

    print(f"Found {len(rows)} sticker messages with Tenor URLs")

    if not rows:
        print("Nothing to fix!")
        return

    fixed = 0
    failed = 0

    for row in rows:
        msg_id, content = row[0], row[1]
        # Extract sticker URL
        match = re.search(r'!\[sticker\]\(([^)]+)\)', content)
        if not match:
            continue

        original_url = match.group(1)

        # Skip if already on COS
        if cos_host and original_url.startswith(cos_host):
            continue
        if cos_bucket_host and cos_bucket_host in original_url:
            continue

        print(f"\nProcessing: {original_url[:80]}...")

        try:
            async with httpx.AsyncClient(timeout=30.0, follow_redirects=True) as client:
                resp = await client.get(original_url)
                resp.raise_for_status()
                image_data = resp.content
                content_type = resp.headers.get("content-type", "image/gif")

            print(f"  Downloaded: {len(image_data)/1024/1024:.1f}MB")

            ct = content_type.split(";")[0].strip()
            ext_map = {
                "image/gif": ".gif", "image/png": ".png",
                "image/jpeg": ".jpg", "image/webp": ".webp", "video/mp4": ".mp4",
            }
            ext = ext_map.get(ct, ".gif")

            cos_url = await cos_service.upload_sticker(
                user_id="proxy",
                filename=f"sticker{ext}",
                content=image_data,
                content_type=ct,
            )

            # Update the message content
            new_content = content.replace(original_url, cos_url)

            async with async_engine.begin() as conn:
                await conn.execute(text(
                    "UPDATE channel_messages SET content = :content WHERE id = :id"
                ), {"content": new_content, "id": msg_id})

            print(f"  Fixed -> {cos_url[:80]}...")
            fixed += 1

        except Exception as e:
            print(f"  FAILED: {e}")
            failed += 1

    print(f"\nDone! Fixed: {fixed}, Failed: {failed}")


if __name__ == "__main__":
    asyncio.run(main())
