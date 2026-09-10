#!/usr/bin/env python3
"""Audit actual visible links and admitted identities, separately from OKF lookup.

Markdown paths are relative to their file. Wikilinks use vault paths or unique
filenames. Title/alias lookup is retained as a repair lead, never silently used
to certify a link. This intentionally conservative portability audit does not
claim to implement an Obsidian renderer or to judge philosophical coherence.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict, deque
import hashlib
import importlib.util
import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

BODY = Path("submission-package/essay")
NAV = BODY / "symbolon/episteme/maps/navigation"
RECEIPT = Path("working/p2-enrichment/receipts/T20-T21-current-census-acceptance.json")


def workspace(root):
    spec = importlib.util.spec_from_file_location("reader_okf", root / "tools/okf-workspace.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module.Workspace(root)


def visible_text(text):
    """Mask metadata and code without changing source offsets."""
    def mask(m):
        return re.sub(r"[^\n]", " ", m.group())
    text = re.sub(r"\A---\n.*?\n---(?:\n|$)", mask, text, count=1, flags=re.S)
    text = re.sub(r"(?m)^(`{3,}|~{3,})[^\n]*\n.*?^\1[^\n]*(?:\n|$)", mask, text, flags=re.S)
    return re.sub(r"(`+)[^\n]*?\1", mask, text)


def links(text):
    """Yield link spans, including balanced parentheses and angle destinations."""
    masked = visible_text(text)
    pattern = re.compile(r"(?<!\\)(!?\[\[([^\]\n]+)\]\]|!?\[([^\]\n]*)\]\()")
    consumed = 0
    for match in pattern.finditer(masked):
        if match.start() < consumed:
            continue
        if match.group(2) is not None:
            start = match.start(2)
            target = text[start:match.end(2)].split("|", 1)[0]
            end = start + len(target)
            yield {"kind": "wiki", "href": target, "start": start, "end": end,
                   "line": text.count("\n", 0, start) + 1}
            consumed = match.end()
            continue
        start = match.end()
        if masked[start:start + 1] == "<":
            end = masked.find(">", start + 1)
            if end < 0 or masked[end + 1:end + 2] != ")":
                continue
            start += 1
            consumed = end + 2
        else:
            end, depth = start, 1
            while end < len(masked):
                char = masked[end]
                if char == "\\":
                    end += 2
                    continue
                if char == "(":
                    depth += 1
                elif char == ")":
                    depth -= 1
                    if depth == 0:
                        break
                elif char == "\n":
                    break
                end += 1
            if depth != 0:
                continue
            consumed = end + 1
        yield {"kind": "markdown", "href": text[start:end], "start": start,
               "end": end, "line": text.count("\n", 0, start) + 1}


def slug(text):
    text = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"<[^>]+>", "", text)
    return re.sub(r"[^\w\- ]", "", text.lower()).replace(" ", "-")


def fragments(text):
    result = set(re.findall(r'\bid=["\']([^"\']+)["\']', text))
    result.update("^" + value for value in re.findall(r"(?m)\^([\w-]+)\s*$", text))
    counts = Counter()
    # Inline code in headings contributes its text to the heading anchor.
    heading_text = re.sub(r"(?m)^(`{3,}|~{3,})[^\n]*\n.*?^\1[^\n]*(?:\n|$)", "", text, flags=re.S)
    for heading in re.findall(r"(?m)^#{1,6}\s+(.+?)\s*#*\s*$", heading_text):
        result.add(heading)
        result.add(heading.replace("`", ""))
        base = slug(heading)
        result.add(base if counts[base] == 0 else f"{base}-{counts[base]}")
        counts[base] += 1
    return result


class ReaderAudit:
    def __init__(self, root, ws=None):
        self.root = root.resolve()
        self.ws = ws if ws is not None else workspace(self.root)
        self.pages = {str(p.relative_to(self.root)): p for p in (self.root / BODY).rglob("*.md")
                      if not p.is_relative_to(self.root / NAV)}
        self.names = defaultdict(list)
        for name, path in self.pages.items():
            self.names[path.stem.casefold()].append(name)
        self.anchor_cache = {}

    def resolve(self, source, item):
        href = item["href"].strip()
        if item["kind"] == "wiki":
            href = href.removesuffix("\\")  # table's escaped display delimiter
        if re.match(r"^[A-Za-z][A-Za-z0-9+.-]*:", href):
            return None, "external"
        raw, _, fragment = href.partition("#")
        raw, fragment = unquote(raw), unquote(fragment)
        target = None
        status = "ok"
        if not raw:
            target = self.root / source
        elif item["kind"] == "markdown":
            target = ((self.root / source).parent / raw).resolve()
            if not target.exists():
                status = "missing-path"
        elif "/" in raw:
            target = self.root / BODY / raw
            if not target.is_file():
                target = Path(str(target) + ".md")
            if not target.is_file():
                status = "missing-vault-path"
        else:
            candidates = self.names.get(Path(raw).stem.casefold(), [])
            local = [p for p in candidates if Path(p).parent == Path(source).parent]
            if len(local) == 1:
                candidates = local
            if len(candidates) == 1:
                target = self.root / candidates[0]
            else:
                status = "ambiguous-filename" if candidates else "title-or-alias-only"
        if status != "ok":
            art = self.ws.artifacts.get(source)
            lead = self.ws._resolve(raw, source=art) if raw else source
            return lead, status
        if not target.is_relative_to(self.root / BODY):
            return str(target), "outside-body"
        if target.is_dir():
            return str(target.relative_to(self.root)), "directory-link"
        rel = str(target.relative_to(self.root))
        if target.suffix == ".md" and fragment:
            if rel not in self.anchor_cache:
                self.anchor_cache[rel] = fragments(target.read_text())
            if fragment not in self.anchor_cache[rel]:
                return rel, "missing-fragment"
        return rel, "ok"

    def run(self):
        problems, external, edges = [], [], defaultdict(set)
        for source, path in sorted(self.pages.items()):
            for item in links(path.read_text()):
                target, status = self.resolve(source, item)
                row = {"source": source, **item, "target": target, "status": status}
                if status == "ok":
                    if target in self.pages:
                        edges[source].add(target)
                elif status == "external":
                    continue
                elif status == "outside-body":
                    external.append(row)
                else:
                    problems.append(row)
        start = str(BODY / "README.md")
        depth, queue = {start: 0}, deque([start])
        while queue:
            here = queue.popleft()
            for target in edges[here]:
                if target not in depth:
                    depth[target] = depth[here] + 1
                    queue.append(target)
        receipt = json.loads((self.root / RECEIPT).read_text())
        records = []
        for row in receipt["records"]:
            path = self.root / row["canonical_home"]
            actual = hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else None
            records.append({**row, "exists": path.is_file(), "current_sha256": actual,
                            "changed_since_acceptance": actual != row["sha256"],
                            "reader_depth": depth.get(row["canonical_home"])})
        returns = {name for name in self.pages if "/movements/" in name}
        reverse = defaultdict(set)
        for source, targets in edges.items():
            for target in targets:
                reverse[target].add(source)
        queue = deque(returns)
        while queue:
            for source in reverse[queue.popleft()]:
                if source not in returns:
                    returns.add(source)
                    queue.append(source)
        return {
            "scope": "Visible links in publication Markdown; code/frontmatter excluded. Alias-only links are portability debt. No semantic certification.",
            "accepted_census": str(RECEIPT),
            "counts": {"pages": len(self.pages), "reachable": len(depth),
                       "problems": dict(Counter(x["status"] for x in problems)),
                       "admitted": len(records), "missing_admitted": sum(not r["exists"] for r in records),
                       "unreachable_admitted": sum(r["reader_depth"] is None for r in records)},
            "records": records, "problems": problems, "outside_body": external,
            "unreachable": sorted(set(self.pages) - set(depth)),
            "no_visible_path_to_movement": sorted(set(self.pages) - returns),
        }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    report = ReaderAudit(args.project_root).run()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(report["counts"], indent=2))


if __name__ == "__main__":
    main()
