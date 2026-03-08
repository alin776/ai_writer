"""
Shared sticker proxy utility.

Downloads external sticker/image URLs (e.g. Tenor) and re-uploads to COS
so they never expire. Used by channels, comments, and sticker APIs.
"""
import logging
import re

import httpx

logger = logging.getLogger(__name__)

# Match sticker markdown: ![sticker](url) — may appear in mixed content
_STICKER_INLINE_RE = re.compile(r'!\[sticker\]\(([^)]+)\)')

# Max download size for proxied stickers (20 MB)
_MAX_PROXY_SIZE = 20 * 1024 * 1024

_EXT_MAP = {
    "image/gif": ".gif",
    "image/png": ".png",
    "image/jpeg": ".jpg",
    "image/webp": ".webp",
    "video/mp4": ".mp4",
}


async def proxy_url_to_cos(url: str) -> str:
    """Download an external image URL and re-upload to COS.

    Returns the COS URL on success, or the original URL on failure.
    """
    try:
        from app.services.cos_service import get_cos_service
        cos_service = get_cos_service()
        cos_host = cos_service.host
        cos_bucket_host = f"{cos_service.bucket}.cos."
    except Exception:
        return url

    # Skip if already hosted on our COS
    if cos_host and url.startswith(cos_host):
        return url
    if cos_bucket_host and cos_bucket_host in url:
        return url

    try:
        async with httpx.AsyncClient(timeout=15.0, follow_redirects=True) as client:
            resp = await client.get(url)
            resp.raise_for_status()
            image_data = resp.content
            content_type = resp.headers.get("content-type", "image/gif")

        if len(image_data) > _MAX_PROXY_SIZE:
            logger.warning(f"Sticker too large ({len(image_data)} bytes), keeping original URL")
            return url

        ct = content_type.split(";")[0].strip()
        ext = _EXT_MAP.get(ct, ".gif")

        cos_url = await cos_service.upload_sticker(
            user_id="proxy",
            filename=f"sticker{ext}",
            content=image_data,
            content_type=ct,
        )

        logger.info(f"Proxied sticker to COS: {url[:80]}... -> {cos_url[:80]}...")
        return cos_url

    except Exception as e:
        logger.warning(f"Failed to proxy sticker URL, keeping original: {e}")
        return url


async def proxy_sticker_urls_in_content(content: str) -> str:
    """Find all ![sticker](url) patterns in message content and proxy
    external URLs to COS so they never expire.
    """
    matches = list(_STICKER_INLINE_RE.finditer(content))
    if not matches:
        return content

    result = content
    for m in reversed(matches):
        original_url = m.group(1)
        cos_url = await proxy_url_to_cos(original_url)
        if cos_url != original_url:
            result = result[:m.start(1)] + cos_url + result[m.end(1):]

    return result
