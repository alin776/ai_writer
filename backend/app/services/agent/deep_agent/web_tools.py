"""Web search and URL fetching tools for DeepAgent.

Expose web search (Tavily) and URL fetching (Jina Reader) capabilities.
Both tools are optional — only created when their respective API keys are configured.
"""

from __future__ import annotations

import logging
import re
from typing import Annotated

import httpx
from langchain_core.tools import BaseTool, StructuredTool

logger = logging.getLogger(__name__)

# Jina Reader 输出上限——防止长网页撑爆 LLM 上下文窗口
_DEFAULT_MAX_LENGTH = 20_000


def create_web_tools(
    *,
    tavily_api_key: str | None = None,
    jina_api_key: str | None = None,
) -> list[BaseTool]:
    """Create web tools backed by external APIs.

    Only tools whose API keys are provided will be included in the returned list.
    If neither key is provided, returns an empty list.
    """
    tools: list[BaseTool] = []

    # ── web_search (Tavily) ────────────────────────────────────────────
    if tavily_api_key:

        def web_search(
            query: Annotated[str, "Search query in natural language"],
            max_results: Annotated[int, "Maximum number of results to return (1-10)"] = 5,
        ) -> str:
            """Search the web for current information.

            Use this tool when you need up-to-date facts, real-world references,
            genre conventions, historical details, or any information not already
            in the project files.
            """
            try:
                from tavily import TavilyClient

                client = TavilyClient(api_key=tavily_api_key)
                response = client.search(
                    query=query,
                    search_depth="basic",
                    max_results=min(max(max_results, 1), 10),
                    include_answer=True,
                )
                return _format_search_results(response)
            except ImportError:
                return "Error: tavily-python package is not installed. Run: pip install tavily-python"
            except Exception as e:
                logger.warning("web_search failed for query=%r: %s", query, e)
                return f"Error: Web search failed — {e}"

        tools.append(
            StructuredTool.from_function(
                name="web_search",
                description=(
                    "Search the web for current information. Use when you need real-world facts, "
                    "genre conventions, historical details, cultural references, or any knowledge "
                    "not found in the project files. Input a natural language query."
                ),
                func=web_search,
            )
        )

    # ── fetch_url (Jina Reader) ────────────────────────────────────────
    if jina_api_key:

        def fetch_url(
            url: Annotated[str, "The URL to fetch content from"],
            max_length: Annotated[int, "Maximum character length of returned content"] = _DEFAULT_MAX_LENGTH,
        ) -> str:
            """Fetch and extract the main content from a web page as clean Markdown.

            Use this tool to read a specific web page (article, wiki, documentation, etc.)
            when you have its URL. Returns the page content converted to readable Markdown.
            """
            try:
                with httpx.Client(timeout=30.0) as http_client:
                    resp = http_client.get(
                        f"https://r.jina.ai/{url}",
                        headers={
                            "Authorization": f"Bearer {jina_api_key}",
                            "Accept": "text/plain",
                        },
                    )
                    resp.raise_for_status()

                content = resp.text
                effective_max = max(max_length, 1000)
                if len(content) > effective_max:
                    content = content[:effective_max] + f"\n\n[... truncated at {effective_max} characters]"

                return content
            except httpx.HTTPStatusError as e:
                logger.warning("fetch_url HTTP error for url=%r: %s", url, e)
                return f"Error: HTTP {e.response.status_code} when fetching {url}"
            except httpx.TimeoutException:
                logger.warning("fetch_url timeout for url=%r", url)
                return f"Error: Request timed out when fetching {url}"
            except Exception as e:
                logger.warning("fetch_url failed for url=%r: %s", url, e)
                return f"Error: Failed to fetch URL — {e}"

        tools.append(
            StructuredTool.from_function(
                name="fetch_url",
                description=(
                    "Fetch and extract clean content from a web page URL. Use when you have a specific "
                    "URL to read (article, wiki page, documentation, reference material). "
                    "Returns Markdown text of the page content."
                ),
                func=fetch_url,
            )
        )

    return tools


# ── 内部辅助函数 ───────────────────────────────────────────────────────


def _format_search_results(response: dict) -> str:
    """Format Tavily search response as readable Markdown for LLM consumption."""
    parts: list[str] = []

    answer = response.get("answer")
    if answer:
        parts.append(f"**Summary:** {answer}")
        parts.append("")

    results = response.get("results", [])
    if results:
        parts.append("**Sources:**")
        parts.append("")
        for i, r in enumerate(results, 1):
            title = r.get("title", "Untitled")
            url = r.get("url", "")
            content = r.get("content", "")
            parts.append(f"{i}. **{title}**")
            if url:
                parts.append(f"   URL: {url}")
            if content:
                snippet = content[:500]
                if len(content) > 500:
                    snippet += "..."
                parts.append(f"   {snippet}")
            parts.append("")

    if not parts:
        return "No results found."

    return "\n".join(parts)
