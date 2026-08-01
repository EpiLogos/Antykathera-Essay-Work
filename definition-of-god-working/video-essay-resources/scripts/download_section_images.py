#!/usr/bin/env python3
"""Download section-organised image candidates from Wikimedia Commons.

The script is intentionally provenance-first: it records source URL, author,
license, dimensions, MIME type, and the query that found each image beside the
downloaded files. It uses the Commons API rather than scraping web pages.
"""

from __future__ import annotations

import argparse
import json
import re
import ssl
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MANIFEST = ROOT / "image-manifest.json"
DEFAULT_OUTPUT = ROOT / "sections"
DEFAULT_TIMEOUT = 30
DEFAULT_RETRIES = 3


class DownloadError(RuntimeError):
    """Raised when Commons returns unusable data or a download fails."""


@dataclass(frozen=True)
class Section:
    slug: str
    title: str
    visual_intent: str
    symbols: list[str]
    queries: list[str]


def slugify(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = re.sub(r"-{2,}", "-", value).strip("-")
    return value or "untitled"


def load_manifest(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        manifest = json.load(handle)
    validate_manifest(manifest)
    return manifest


def validate_manifest(manifest: dict[str, Any]) -> None:
    if not isinstance(manifest.get("sections"), list) or not manifest["sections"]:
        raise ValueError("Manifest must contain a non-empty 'sections' list.")
    seen: set[str] = set()
    for index, raw_section in enumerate(manifest["sections"], start=1):
        for key in ("slug", "title", "visual_intent", "symbols", "queries"):
            if key not in raw_section:
                raise ValueError(f"Section #{index} is missing required key: {key}")
        slug = raw_section["slug"]
        if slug in seen:
            raise ValueError(f"Duplicate section slug: {slug}")
        if slugify(slug) != slug:
            raise ValueError(f"Section slug must be slugified already: {slug}")
        seen.add(slug)
        if not raw_section["queries"]:
            raise ValueError(f"Section {slug} must define at least one query.")


def iter_sections(manifest: dict[str, Any]) -> Iterable[Section]:
    for raw in manifest["sections"]:
        yield Section(
            slug=raw["slug"],
            title=raw["title"],
            visual_intent=raw["visual_intent"],
            symbols=list(raw["symbols"]),
            queries=list(raw["queries"]),
        )


def api_get(
    endpoint: str,
    params: dict[str, Any],
    user_agent: str,
    timeout: int,
    retries: int = DEFAULT_RETRIES,
) -> dict[str, Any]:
    encoded = urllib.parse.urlencode(params)
    request = urllib.request.Request(
        f"{endpoint}?{encoded}",
        headers={"User-Agent": user_agent, "Accept": "application/json"},
    )
    for attempt in range(retries + 1):
        try:
            with urllib.request.urlopen(request, timeout=timeout, context=ssl_context()) as response:
                return json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            if exc.code == 429 and attempt < retries:
                time.sleep(retry_after_seconds(exc, attempt))
                continue
            raise DownloadError(f"Commons API request failed: {exc}") from exc
        except urllib.error.URLError as exc:
            raise DownloadError(f"Commons API request failed: {exc}") from exc
        except json.JSONDecodeError as exc:
            raise DownloadError("Commons API returned invalid JSON.") from exc
    raise DownloadError("Commons API request failed after retries.")


def search_commons(
    endpoint: str,
    query: str,
    user_agent: str,
    limit: int,
    timeout: int,
    retries: int,
) -> list[str]:
    data = api_get(
        endpoint,
        {
            "action": "query",
            "format": "json",
            "generator": "search",
            "gsrsearch": f"{query} filetype:bitmap|drawing",
            "gsrnamespace": 6,
            "gsrlimit": max(limit * 4, limit),
            "prop": "imageinfo",
            "iiprop": "url|mime|size|extmetadata",
            "iiurlwidth": 1600,
        },
        user_agent,
        timeout,
        retries,
    )
    pages = data.get("query", {}).get("pages", {})
    titles: list[str] = []
    for page in pages.values():
        title = page.get("title", "")
        imageinfo = page.get("imageinfo") or []
        if title.startswith("File:") and imageinfo:
            titles.append(title)
    return titles


def fetch_imageinfo(
    endpoint: str,
    titles: list[str],
    user_agent: str,
    timeout: int,
    retries: int,
) -> list[dict[str, Any]]:
    if not titles:
        return []
    data = api_get(
        endpoint,
        {
            "action": "query",
            "format": "json",
            "titles": "|".join(titles),
            "prop": "imageinfo",
            "iiprop": "url|mime|size|extmetadata",
            "iiurlwidth": 1600,
        },
        user_agent,
        timeout,
        retries,
    )
    records: list[dict[str, Any]] = []
    for page in data.get("query", {}).get("pages", {}).values():
        imageinfo = (page.get("imageinfo") or [{}])[0]
        records.append({"title": page.get("title", ""), "imageinfo": imageinfo})
    return records


def metadata_value(extmetadata: dict[str, Any], key: str) -> str:
    value = extmetadata.get(key, {})
    if isinstance(value, dict):
        return str(value.get("value", "")).strip()
    return str(value).strip()


def strip_html(value: str) -> str:
    value = re.sub(r"<[^>]+>", " ", value)
    return re.sub(r"\s+", " ", value).strip()


def license_allowed(record: dict[str, Any], reject_fragments: list[str]) -> bool:
    extmetadata = record.get("imageinfo", {}).get("extmetadata", {})
    fields = [
        metadata_value(extmetadata, "LicenseShortName"),
        metadata_value(extmetadata, "UsageTerms"),
        metadata_value(extmetadata, "Restrictions"),
        metadata_value(extmetadata, "Copyrighted"),
    ]
    joined = " ".join(strip_html(field).lower() for field in fields)
    return not any(fragment.lower() in joined for fragment in reject_fragments)


def relevance_score(record: dict[str, Any], query: str, section: Section) -> int:
    title = record.get("title", "")
    extmetadata = record.get("imageinfo", {}).get("extmetadata", {})
    description = strip_html(metadata_value(extmetadata, "ImageDescription"))
    categories = strip_html(metadata_value(extmetadata, "Categories"))
    haystack = f"{title} {description} {categories}".lower()
    query_tokens = meaningful_tokens(query)
    symbol_tokens = [token for symbol in section.symbols for token in meaningful_tokens(symbol)]
    score = 0
    score += sum(3 for token in query_tokens if token in haystack)
    score += sum(2 for token in symbol_tokens if token in haystack)
    imageinfo = record.get("imageinfo", {})
    if imageinfo.get("width", 0) >= 1000:
        score += 1
    if imageinfo.get("mime", "").startswith("image/"):
        score += 2
    return score


def meaningful_tokens(value: str) -> list[str]:
    stopwords = {"and", "the", "with", "from", "public", "domain", "diagram"}
    return [
        token
        for token in re.findall(r"[a-z0-9]+", value.lower())
        if len(token) > 2 and token not in stopwords
    ]


def choose_download_url(imageinfo: dict[str, Any]) -> str:
    thumb = imageinfo.get("thumburl")
    url = imageinfo.get("url")
    if thumb:
        return thumb
    if url:
        return url
    raise DownloadError("Image record has no usable URL.")


def file_extension(url: str, mime: str, fallback_title: str) -> str:
    path_ext = Path(urllib.parse.urlparse(url).path).suffix.lower()
    if path_ext in {".jpg", ".jpeg", ".png", ".webp", ".gif", ".tif", ".tiff"}:
        return ".jpg" if path_ext == ".jpeg" else path_ext
    mime_map = {
        "image/jpeg": ".jpg",
        "image/png": ".png",
        "image/webp": ".webp",
        "image/gif": ".gif",
        "image/tiff": ".tif",
        "image/svg+xml": ".svg",
    }
    if mime in mime_map:
        return mime_map[mime]
    title_ext = Path(fallback_title.replace("File:", "")).suffix.lower()
    return title_ext if title_ext else ".img"


def build_record(
    record: dict[str, Any],
    section: Section,
    query: str,
    score: int,
    filename: str | None = None,
) -> dict[str, Any]:
    imageinfo = record["imageinfo"]
    extmetadata = imageinfo.get("extmetadata", {})
    title = record["title"]
    source_name = title.removeprefix("File:")
    source_url = "https://commons.wikimedia.org/wiki/" + urllib.parse.quote(title.replace(" ", "_"), safe="/:_")
    output = {
        "section_slug": section.slug,
        "section_title": section.title,
        "query": query,
        "score": score,
        "title": title,
        "source_url": source_url,
        "description": strip_html(metadata_value(extmetadata, "ImageDescription")),
        "author": strip_html(metadata_value(extmetadata, "Artist")),
        "license": strip_html(metadata_value(extmetadata, "LicenseShortName")),
        "usage_terms": strip_html(metadata_value(extmetadata, "UsageTerms")),
        "mime": imageinfo.get("mime", ""),
        "width": imageinfo.get("width"),
        "height": imageinfo.get("height"),
        "download_url": choose_download_url(imageinfo),
    }
    if filename:
        output["filename"] = filename
    if not output["description"]:
        output["description"] = source_name
    return output


def download_binary(url: str, target: Path, user_agent: str, timeout: int, retries: int) -> None:
    request = urllib.request.Request(url, headers={"User-Agent": user_agent})
    for attempt in range(retries + 1):
        try:
            with urllib.request.urlopen(request, timeout=timeout, context=ssl_context()) as response:
                target.write_bytes(response.read())
                return
        except urllib.error.HTTPError as exc:
            if exc.code == 429 and attempt < retries:
                time.sleep(retry_after_seconds(exc, attempt))
                continue
            raise DownloadError(f"Download failed for {url}: {exc}") from exc
        except urllib.error.URLError as exc:
            raise DownloadError(f"Download failed for {url}: {exc}") from exc
    raise DownloadError(f"Download failed for {url} after retries.")


def ssl_context() -> ssl.SSLContext:
    try:
        import certifi  # type: ignore

        return ssl.create_default_context(cafile=certifi.where())
    except ImportError:
        return ssl.create_default_context()


def retry_after_seconds(exc: urllib.error.HTTPError, attempt: int) -> float:
    header = exc.headers.get("Retry-After")
    if header:
        try:
            return min(float(header), 60.0)
        except ValueError:
            pass
    return min(2.0 ** attempt, 30.0)


def append_jsonl(path: Path, record: dict[str, Any]) -> None:
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")


def write_report(path: Path, rows: list[dict[str, Any]], dry_run: bool) -> None:
    lines = ["# Download Report", ""]
    lines.append("Mode: dry run" if dry_run else "Mode: downloaded")
    lines.append("")
    for row in rows:
        filename = row.get("filename", "(not downloaded)")
        lines.append(f"- `{filename}` — score {row['score']} — {row['title']}")
        lines.append(f"  - Query: {row['query']}")
        lines.append(f"  - License: {row.get('license') or row.get('usage_terms') or 'unknown'}")
        lines.append(f"  - Source: {row['source_url']}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def process_section(
    section: Section,
    manifest: dict[str, Any],
    output_dir: Path,
    per_query: int,
    dry_run: bool,
    overwrite: bool,
    timeout: int,
    sleep_seconds: float,
    min_score: int,
    retries: int,
    fail_fast: bool,
) -> list[dict[str, Any]]:
    endpoint = manifest["api"]["endpoint"]
    user_agent = manifest["api"]["user_agent"]
    reject_fragments = manifest["license_policy"].get("reject_license_fragments", [])
    section_dir = output_dir / section.slug
    image_dir = section_dir / "images"
    metadata_path = section_dir / "metadata.jsonl"
    existing_titles = set() if overwrite else read_existing_titles(metadata_path)
    if not dry_run:
        image_dir.mkdir(parents=True, exist_ok=True)

    chosen_rows: list[dict[str, Any]] = []
    seen_titles: set[str] = set()
    for query in section.queries:
        titles = search_commons(endpoint, query, user_agent, per_query, timeout, retries)
        time.sleep(sleep_seconds)
        records = fetch_imageinfo(endpoint, titles, user_agent, timeout, retries)
        candidates = []
        for record in records:
            if record["title"] in seen_titles:
                continue
            imageinfo = record.get("imageinfo", {})
            if not imageinfo.get("mime", "").startswith("image/"):
                continue
            if not license_allowed(record, reject_fragments):
                continue
            score = relevance_score(record, query, section)
            if score < min_score:
                continue
            candidates.append((score, record))
        candidates.sort(key=lambda item: item[0], reverse=True)
        for score, record in candidates[:per_query]:
            if record["title"] in existing_titles:
                continue
            seen_titles.add(record["title"])
            imageinfo = record["imageinfo"]
            url = choose_download_url(imageinfo)
            stem = slugify(record["title"].removeprefix("File:"))[:90]
            ext = file_extension(url, imageinfo.get("mime", ""), record["title"])
            filename = f"{slugify(query)[:40]}__{stem}{ext}"
            row = build_record(record, section, query, score, filename)
            if not dry_run:
                target = image_dir / filename
                if target.exists() and not overwrite:
                    row["skipped"] = "file exists"
                else:
                    try:
                        download_binary(url, target, user_agent, timeout, retries)
                    except DownloadError as exc:
                        row["download_error"] = str(exc)
                        print(f"  warning: {exc}", file=sys.stderr, flush=True)
                        if fail_fast:
                            raise
                    time.sleep(sleep_seconds)
                append_jsonl(metadata_path, row)
                existing_titles.add(record["title"])
            chosen_rows.append(row)
    if not dry_run:
        write_report(section_dir / "download-report.md", chosen_rows, dry_run=False)
    return chosen_rows


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--section", help="Only process one section slug.")
    parser.add_argument("--exclude-section", action="append", default=[], help="Skip a section slug. Can be repeated.")
    parser.add_argument("--per-query", type=int, default=2, help="Candidates to keep per query.")
    parser.add_argument("--dry-run", action="store_true", help="Query and rank without downloading files.")
    parser.add_argument("--overwrite", action="store_true", help="Replace existing downloaded files.")
    parser.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT)
    parser.add_argument("--sleep", type=float, default=0.2, help="Pause between Commons requests.")
    parser.add_argument("--min-score", type=int, default=7, help="Minimum relevance score to keep.")
    parser.add_argument("--retries", type=int, default=DEFAULT_RETRIES, help="Retries for 429 rate limits.")
    parser.add_argument("--fail-fast", action="store_true", help="Stop at the first failed media download.")
    return parser.parse_args(argv)


def read_existing_titles(path: Path) -> set[str]:
    if not path.exists():
        return set()
    titles: set[str] = set()
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            try:
                row = json.loads(line)
            except json.JSONDecodeError:
                continue
            title = row.get("title")
            if isinstance(title, str):
                titles.add(title)
    return titles


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    manifest = load_manifest(args.manifest)
    sections = list(iter_sections(manifest))
    if args.section:
        sections = [section for section in sections if section.slug == args.section]
        if not sections:
            print(f"Unknown section slug: {args.section}", file=sys.stderr)
            return 2
    if args.exclude_section:
        excluded = set(args.exclude_section)
        sections = [section for section in sections if section.slug not in excluded]

    all_rows: list[dict[str, Any]] = []
    for section in sections:
        print(f"Processing {section.slug}...", flush=True)
        rows = process_section(
            section=section,
            manifest=manifest,
            output_dir=args.output,
            per_query=args.per_query,
            dry_run=args.dry_run,
            overwrite=args.overwrite,
            timeout=args.timeout,
            sleep_seconds=args.sleep,
            min_score=args.min_score,
            retries=args.retries,
            fail_fast=args.fail_fast,
        )
        all_rows.extend(rows)
        if args.dry_run:
            for row in rows:
                print(f"  score={row['score']:02d} {row['title']} [{row['license'] or row['usage_terms']}]", flush=True)

    if args.dry_run:
        report_path = ROOT / "dry-run-report.md"
        write_report(report_path, all_rows, dry_run=True)
        print(f"Dry-run report written to {report_path}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
