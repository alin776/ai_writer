"""
基于素材文本验证 OpenSearch 检索行为（any/all/phrase、limit、分页拿全）。

用法：
    python scripts/verify_opensearch_material_search.py
    python scripts/verify_opensearch_material_search.py --strict
    python scripts/verify_opensearch_material_search.py --material-path "../../docs/Agent/real-book/一夕千悟，从杂役弟子开始.txt"
"""

import argparse
import os
import re
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


def _env_bool(name: str, default: bool = False) -> bool:
    value = (os.getenv(name, "") or "").strip().lower()
    if not value:
        return default
    return value in ("1", "true", "yes", "on")


def _normalize_line(text: str) -> str:
    # 去掉中文全角空格，保留正文
    return text.replace("\u3000", " ").strip()


def _parse_chapter_order(line: str, fallback_order: int) -> int:
    m = re.match(r"^第\s*([0-9]+)\s*章", line)
    if m:
        try:
            return int(m.group(1))
        except Exception:
            return fallback_order
    return fallback_order


def parse_material_to_docs(material_path: Path, work_id: str) -> List[Dict[str, Any]]:
    if not material_path.exists():
        raise FileNotFoundError(f"素材文件不存在: {material_path}")

    content = material_path.read_text(encoding="utf-8")
    lines = content.splitlines()

    chapter_pattern = re.compile(r"^第\s*[0-9]+\s*章")
    docs: List[Dict[str, Any]] = []
    chapter_order = 0
    chapter_title = "前言"
    paragraph_index = 0

    for raw_line in lines:
        line = _normalize_line(raw_line)
        if not line:
            continue

        if chapter_pattern.match(line):
            chapter_order = _parse_chapter_order(line, chapter_order + 1)
            chapter_title = line
            paragraph_index = 0
            continue

        doc_id = f"{work_id}:{chapter_order}:{paragraph_index}"
        docs.append(
            {
                "doc_id": doc_id,
                "work_id": work_id,
                "chapter_id": f"chapter-{chapter_order}",
                "chapter_order": chapter_order,
                "chapter_title": chapter_title,
                "paragraph_index": paragraph_index,
                "chunk_text": line,
                "node_id": "",
            }
        )
        paragraph_index += 1

    return docs


def build_query(
    work_id: str,
    keywords: List[str],
    match_mode: str,
    chapter_range: Optional[Tuple[Optional[int], Optional[int]]] = None,
) -> Dict[str, Any]:
    must: List[Dict[str, Any]] = [{"term": {"work_id": work_id}}]

    if chapter_range:
        min_order, max_order = chapter_range
        range_body: Dict[str, Any] = {}
        if min_order is not None:
            range_body["gte"] = int(min_order)
        if max_order is not None:
            range_body["lte"] = int(max_order)
        if range_body:
            must.append({"range": {"chapter_order": range_body}})

    if match_mode == "phrase":
        must.append({"match_phrase": {"chunk_text": keywords[0]}})
        return {"bool": {"must": must}}

    if match_mode == "all":
        for kw in keywords:
            must.append({"match_phrase": {"chunk_text": kw}})
        return {"bool": {"must": must}}

    should = [{"match_phrase": {"chunk_text": kw}} for kw in keywords]
    must.append({"bool": {"should": should, "minimum_should_match": 1}})
    return {"bool": {"must": must}}


def local_match_count(
    docs: List[Dict[str, Any]],
    keywords: List[str],
    match_mode: str,
    chapter_range: Optional[Tuple[Optional[int], Optional[int]]] = None,
) -> Tuple[int, List[str]]:
    kw_list = [kw.strip().lower() for kw in keywords if kw.strip()]
    matched_ids: List[str] = []

    for doc in docs:
        chapter_order = int(doc.get("chapter_order") or 0)
        if chapter_range:
            min_order, max_order = chapter_range
            if min_order is not None and chapter_order < min_order:
                continue
            if max_order is not None and chapter_order > max_order:
                continue

        text_lower = (doc.get("chunk_text") or "").lower()
        ok = False
        if match_mode == "phrase":
            ok = bool(kw_list) and kw_list[0] in text_lower
        elif match_mode == "all":
            ok = bool(kw_list) and all(kw in text_lower for kw in kw_list)
        else:
            ok = any(kw in text_lower for kw in kw_list)

        if ok:
            matched_ids.append(doc["doc_id"])

    return len(matched_ids), matched_ids


def create_client(args: argparse.Namespace):
    from opensearchpy import OpenSearch

    hosts = [h.strip() for h in args.hosts.split(",") if h.strip()]
    kwargs: Dict[str, Any] = {
        "hosts": hosts,
        "timeout": args.timeout,
        "use_ssl": args.use_ssl,
        "verify_certs": args.verify_certs,
    }
    if args.username:
        kwargs["http_auth"] = (args.username, args.password or "")
    return OpenSearch(**kwargs)


def recreate_index(client: Any, index_name: str) -> None:
    if client.indices.exists(index=index_name):
        client.indices.delete(index=index_name)

    body = {
        "settings": {
            "index": {
                "number_of_shards": 1,
                "number_of_replicas": 0,
            }
        },
        "mappings": {
            "properties": {
                "work_id": {"type": "keyword"},
                "chapter_id": {"type": "keyword"},
                "chapter_order": {"type": "integer"},
                "chapter_title": {"type": "text"},
                "paragraph_index": {"type": "integer"},
                "chunk_text": {"type": "text"},
                "node_id": {"type": "keyword"},
            }
        },
    }
    client.indices.create(index=index_name, body=body)


def bulk_index_docs(client: Any, index_name: str, docs: List[Dict[str, Any]]) -> int:
    from opensearchpy import helpers

    actions = []
    for doc in docs:
        actions.append(
            {
                "_op_type": "index",
                "_index": index_name,
                "_id": doc["doc_id"],
                "_source": {
                    "work_id": doc["work_id"],
                    "chapter_id": doc["chapter_id"],
                    "chapter_order": doc["chapter_order"],
                    "chapter_title": doc["chapter_title"],
                    "paragraph_index": doc["paragraph_index"],
                    "chunk_text": doc["chunk_text"],
                    "node_id": doc["node_id"],
                },
            }
        )

    success, _errors = helpers.bulk(client, actions, raise_on_error=False, refresh="wait_for")
    return int(success or 0)


def search_page(
    client: Any,
    index_name: str,
    query: Dict[str, Any],
    size: int,
    search_after: Optional[List[Any]] = None,
) -> List[Dict[str, Any]]:
    body: Dict[str, Any] = {
        "size": max(1, int(size)),
        "query": query,
        "sort": [
            {"chapter_order": {"order": "asc"}},
            {"paragraph_index": {"order": "asc"}},
            {"_id": {"order": "asc"}},
        ],
        "_source": [
            "chapter_order",
            "chapter_title",
            "paragraph_index",
            "chunk_text",
            "work_id",
        ],
    }
    if search_after:
        body["search_after"] = search_after
    resp = client.search(index=index_name, body=body)
    return (((resp or {}).get("hits") or {}).get("hits") or [])


def search_all(
    client: Any,
    index_name: str,
    query: Dict[str, Any],
    page_size: int,
) -> List[Dict[str, Any]]:
    all_hits: List[Dict[str, Any]] = []
    search_after: Optional[List[Any]] = None
    while True:
        hits = search_page(client, index_name, query, page_size, search_after=search_after)
        if not hits:
            break
        all_hits.extend(hits)
        search_after = hits[-1].get("sort")
        if not search_after:
            break
    return all_hits


@dataclass
class Case:
    name: str
    keywords: List[str]
    match_mode: str
    chapter_range: Optional[Tuple[Optional[int], Optional[int]]] = None


def run_validation(args: argparse.Namespace) -> int:
    material_path = Path(args.material_path).resolve()
    docs = parse_material_to_docs(material_path, work_id=args.work_id)
    if not docs:
        print("[ERROR] 素材没有可用段落，无法测试")
        return 2

    index_name = args.index_name or f"tmp_material_search_test_{int(time.time())}"
    client = create_client(args)
    strict = bool(args.strict)
    exit_code = 0

    print("=" * 72)
    print("[INFO] OpenSearch 素材检索验证开始")
    print(f"[INFO] material_path={material_path}")
    print(f"[INFO] paragraphs={len(docs)} index={index_name} work_id={args.work_id}")
    print("=" * 72)

    try:
        recreate_index(client, index_name)
        indexed = bulk_index_docs(client, index_name, docs)
        print(f"[INFO] 已索引段落: {indexed}")

        cases = [
            Case("any_吞噬器灵牛尾刀", ["吞噬", "器灵", "牛尾刀"], "any", None),
            Case("all_牛尾刀器灵", ["牛尾刀", "器灵"], "all", None),
            Case("phrase_五虎群羊刀入门", ["五虎群羊刀入门"], "phrase", None),
            Case("any_浑圆桩赵穆_第2到3章", ["浑圆桩", "赵穆"], "any", (2, 3)),
            Case("all_孔斌李充张征_第2到3章", ["孔斌", "李充", "张征"], "all", (2, 3)),
        ]

        for case in cases:
            query = build_query(
                work_id=args.work_id,
                keywords=case.keywords,
                match_mode=case.match_mode,
                chapter_range=case.chapter_range,
            )

            limited_hits = search_page(client, index_name, query, args.limit)
            all_hits = search_all(client, index_name, query, args.page_size)
            baseline_count, baseline_ids = local_match_count(
                docs=docs,
                keywords=case.keywords,
                match_mode=case.match_mode,
                chapter_range=case.chapter_range,
            )

            search_ids = [h.get("_id", "") for h in all_hits]
            missing_ids = sorted(set(baseline_ids) - set(search_ids))
            extra_ids = sorted(set(search_ids) - set(baseline_ids))

            pass_limit = len(limited_hits) <= args.limit
            pass_paging = len(all_hits) >= len(limited_hits)
            pass_baseline = len(all_hits) == baseline_count and not missing_ids
            case_ok = pass_limit and pass_paging and (pass_baseline or (not strict))

            if not case_ok:
                exit_code = 1

            print("-" * 72)
            print(f"[CASE] {case.name}")
            print(
                f"  mode={case.match_mode} keywords={case.keywords} range={case.chapter_range}"
            )
            print(
                f"  limit_hits={len(limited_hits)} all_hits={len(all_hits)} baseline={baseline_count}"
            )
            print(
                f"  pass_limit={pass_limit} pass_paging={pass_paging} pass_baseline={pass_baseline} strict={strict}"
            )
            if missing_ids:
                print(f"  missing_ids(sample)={missing_ids[:5]}")
            if extra_ids:
                print(f"  extra_ids(sample)={extra_ids[:5]}")

        broad_case_query = build_query(
            work_id=args.work_id,
            keywords=["段融"],
            match_mode="any",
            chapter_range=None,
        )
        one_page = search_page(client, index_name, broad_case_query, args.limit)
        all_pages = search_all(client, index_name, broad_case_query, args.page_size)
        print("-" * 72)
        print("[CASE] pagination_demo_段融")
        print(f"  one_page_hits={len(one_page)} all_pages_hits={len(all_pages)}")
        print("  说明：one_page 表示 limit 截断；all_pages 表示分页拿全。")

        print("=" * 72)
        if exit_code == 0:
            print("[RESULT] 检索验证通过（或 strict=false 下无阻断项）")
        else:
            print("[RESULT] 检索验证失败（存在 strict 阻断项）")
        print("=" * 72)
        return exit_code
    finally:
        if not args.keep_index:
            try:
                if client.indices.exists(index=index_name):
                    client.indices.delete(index=index_name)
                    print(f"[CLEANUP] 已删除临时索引: {index_name}")
            except Exception as cleanup_error:
                print(f"[WARN] 清理索引失败: {cleanup_error}")


def parse_args() -> argparse.Namespace:
    repo_root = Path(__file__).resolve().parents[2]
    default_material = repo_root / "docs/Agent/real-book/一夕千悟，从杂役弟子开始.txt"
    default_hosts = os.getenv("OPENSEARCH_HOSTS", "http://localhost:9200")

    parser = argparse.ArgumentParser(
        description="Test OpenSearch search behavior with local novel material"
    )
    parser.add_argument(
        "--material-path",
        default=str(default_material),
        help="素材 txt 路径",
    )
    parser.add_argument(
        "--work-id",
        default="material-work-test",
        help="写入索引时使用的 work_id",
    )
    parser.add_argument(
        "--index-name",
        default="",
        help="临时索引名（不传则自动生成）",
    )
    parser.add_argument(
        "--hosts",
        default=default_hosts,
        help="OpenSearch hosts，逗号分隔",
    )
    parser.add_argument(
        "--username",
        default=os.getenv("OPENSEARCH_USERNAME", ""),
        help="OpenSearch 用户名",
    )
    parser.add_argument(
        "--password",
        default=os.getenv("OPENSEARCH_PASSWORD", ""),
        help="OpenSearch 密码",
    )
    parser.add_argument(
        "--use-ssl",
        action="store_true",
        default=_env_bool("OPENSEARCH_USE_SSL", False),
        help="启用 SSL",
    )
    parser.add_argument(
        "--verify-certs",
        action="store_true",
        default=_env_bool("OPENSEARCH_VERIFY_CERTS", False),
        help="校验证书",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=int(os.getenv("OPENSEARCH_TIMEOUT_SECONDS", "10") or "10"),
        help="OpenSearch 请求超时（秒）",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=5,
        help="单页 limit（用于验证截断）",
    )
    parser.add_argument(
        "--page-size",
        type=int,
        default=20,
        help="分页读取 size（用于验证拿全）",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="严格模式：基线数量不一致即返回非 0",
    )
    parser.add_argument(
        "--keep-index",
        action="store_true",
        help="保留临时索引，默认结束后删除",
    )
    return parser.parse_args()


if __name__ == "__main__":
    arguments = parse_args()
    try:
        code = run_validation(arguments)
    except KeyboardInterrupt:
        print("[INFO] 手动中断")
        code = 130
    except Exception as exc:
        print(f"[ERROR] 执行失败: {exc}")
        code = 2
    sys.exit(code)
