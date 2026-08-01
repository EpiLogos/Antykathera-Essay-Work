#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""okf-scan — read-only orientation over an OKF bundle.

Inventories every Markdown node by type / coordinate / status, reports index.md
and log.md presence, and flags dangling links — so an agent can orient on a large
or index-less bundle in one pass, without reading every file. Reads nothing but
the bundle; writes nothing. Standard library only.

Usage:
    okf-scan.py [ROOT ...]              # scan one or more bundle roots (default: cwd)
    okf-scan.py ROOT --type reference   # only nodes of this type
    okf-scan.py ROOT --coord P4         # only nodes whose coordinates include P4
    okf-scan.py ROOT --status Offered   # only nodes with this claim_status
    okf-scan.py ROOT --unverified       # reference nodes whose verification_status != verified
    okf-scan.py ROOT --dangling         # only the dangling-link report

For the Return-of-Zero essay bundle, point it at both roots:
    okf-scan.py resources/essay-okf
"""
import os, re, sys
from collections import defaultdict, Counter

LINK_WIKI = re.compile(r'\[\[([^\]]+)\]\]')
LINK_MD = re.compile(r'(?<!\!)\[[^\]]*\]\(([^)]+)\)')

def norm(s):
    return re.sub(r'[^a-z0-9]+', '', s.lower())

def unquote(s):
    """Strip only a matched surrounding quote pair — preserves a trailing prime
    mark (L5', P2', L0') that a greedy .strip('\"\\'') would eat."""
    s = s.strip()
    if len(s) >= 2 and s[0] == s[-1] and s[0] in '"\'':
        return s[1:-1]
    return s

def parse_frontmatter(text):
    """Return (dict-ish) frontmatter values we care about + raw block."""
    m = re.match(r'^---\n(.*?)\n---', text, re.S)
    fm = {}
    if not m:
        return fm
    block = m.group(1)
    def scalar(key):
        r = re.search(rf'^{key}:\s*(.+?)\s*$', block, re.M)
        return unquote(r.group(1)) if r else None
    def listvals(key):
        # inline [a, b] or block list
        inl = re.search(rf'^{key}:\s*\[(.*?)\]', block, re.M)
        if inl:
            return [unquote(x) for x in inl.group(1).split(',') if x.strip()]
        blk = re.search(rf'^{key}:\s*\n((?:[ \t]*-\s*.+\n?)+)', block, re.M)
        if blk:
            return [unquote(re.sub(r'^[ \t]*-\s*', '', l))
                    for l in blk.group(1).splitlines() if l.strip()]
        return []
    fm['type'] = scalar('type') or scalar('node_type') or scalar('page_type') or '?'
    fm['title'] = scalar('title')
    fm['coordinates'] = listvals('coordinates')
    fm['aliases'] = listvals('aliases')
    fm['claim_status'] = scalar('claim_status')
    fm['verification_status'] = scalar('verification_status')
    fm['source_status'] = scalar('source_status')
    fm['tier'] = scalar('tier')
    fm['has_aperture'] = bool(re.search(r'^aperture:', block, re.M))
    fm['has_analogia'] = bool(re.search(r'^analogia:', block, re.M))
    return fm

def links_in(text):
    out = []
    for m in LINK_WIKI.finditer(text):
        tgt = m.group(1).split('|', 1)[0].split('#', 1)[0].strip()
        if tgt:
            out.append(tgt)
    for m in LINK_MD.finditer(text):
        tgt = m.group(1).split('#', 1)[0].strip()
        if tgt and not tgt.startswith(('http://', 'https://', 'mailto:')):
            out.append(os.path.splitext(os.path.basename(tgt))[0])
    return out

def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    flags = [a for a in sys.argv[1:] if a.startswith('--')]
    roots = args or ['.']

    def flagval(name):
        for i, f in enumerate(flags):
            if f == '--' + name:
                # value is the next positional-ish token; support --name value and --name=value
                if '=' in f:
                    return f.split('=', 1)[1]
        for f in flags:
            if f.startswith('--' + name + '='):
                return f.split('=', 1)[1]
        return None
    # support "--type reference" where value landed in args
    def flagval2(name):
        v = flagval(name)
        if v:
            return v
        if '--' + name in flags:
            idx = sys.argv.index('--' + name)
            if idx + 1 < len(sys.argv) and not sys.argv[idx + 1].startswith('--'):
                return sys.argv[idx + 1]
        return None

    f_type = flagval2('type')
    f_coord = flagval2('coord')
    f_status = flagval2('status')
    only_unverified = '--unverified' in flags
    only_dangling = '--dangling' in flags
    # a value consumed by --type/--coord/--status is not a root
    consumed = {v for v in (f_type, f_coord, f_status) if v}
    roots = [r for r in roots if r not in consumed] or ['.']

    nodes = []            # (relpath, fm, [links])
    resolve = defaultdict(set)   # norm(name) -> set(relpath)
    has_index = has_log = None

    for root in roots:
        if not os.path.isdir(root):
            print(f"! not a directory: {root}", file=sys.stderr); continue
        for dirpath, dirs, files in os.walk(root):
            dirs[:] = [d for d in dirs if d not in ('.git', 'node_modules', '.obsidian')]
            for fn in sorted(files):
                if not fn.endswith('.md'):
                    continue
                path = os.path.join(dirpath, fn)
                rel = os.path.relpath(path)
                try:
                    text = open(path, encoding='utf-8', errors='replace').read()
                except Exception:
                    continue
                fm = parse_frontmatter(text)
                lk = links_in(text)
                nodes.append((rel, fm, lk))
                stem = fn[:-3]
                resolve[norm(stem)].add(rel)
                for nm in ([fm.get('title')] if fm.get('title') else []) + fm.get('aliases', []):
                    resolve[norm(nm)].add(rel)
                if fn == 'index.md':
                    has_index = rel
                if fn == 'log.md':
                    has_log = rel

    def keep(fm):
        if f_type and norm(fm.get('type') or '') != norm(f_type):
            return False
        if f_coord and norm(f_coord) not in {norm(c) for c in fm.get('coordinates', [])}:
            return False
        if f_status and norm(fm.get('claim_status') or '') != norm(f_status):
            return False
        if only_unverified:
            if norm(fm.get('type') or '') != norm('reference'):
                return False
            vs = fm.get('verification_status') or fm.get('source_status') or ''
            if 'verified' in vs.lower() and 'pending' not in vs.lower() and 'internal' not in vs.lower():
                return False
        return True

    # ---- dangling links ----
    dangling = defaultdict(list)
    for rel, fm, lk in nodes:
        for tgt in lk:
            if norm(tgt) and norm(tgt) not in resolve:
                dangling[tgt].append(rel)

    if only_dangling:
        print(f"# okf-scan — dangling links  ({len(dangling)} distinct)\n")
        for t in sorted(dangling, key=str.lower):
            print(f"- [[{t}]]  ← {len(dangling[t])}x  ({os.path.basename(dangling[t][0])} …)")
        return

    shown = [(rel, fm, lk) for rel, fm, lk in nodes if keep(fm)]

    print(f"# okf-scan  ·  roots: {', '.join(roots)}")
    print(f"nodes: {len(nodes)} total, {len(shown)} shown"
          + (f"  ·  index.md: {has_index}" if has_index else "  ·  index.md: (none — orient via scan)")
          + (f"  ·  log.md: {has_log}" if has_log else ""))
    print()

    by_type = Counter(fm.get('type') or '?' for _, fm, _ in shown)
    print("## by type")
    for t, n in by_type.most_common():
        print(f"  {n:>4}  {t}")
    print()

    print("## nodes  (id · type · coordinates · status)")
    for rel, fm, lk in sorted(shown, key=lambda x: x[0]):
        ident = os.path.splitext(os.path.basename(rel))[0]
        coords = ",".join(fm.get('coordinates', [])) or "—"
        status = fm.get('claim_status') or fm.get('verification_status') or fm.get('source_status') or "—"
        extra = []
        if fm.get('tier'): extra.append(f"tier {fm['tier']}")
        if fm.get('has_aperture'): extra.append("aperture")
        if fm.get('has_analogia'): extra.append("analogia")
        tail = ("  [" + " · ".join(extra) + "]") if extra else ""
        print(f"  {ident:<40} {str(fm.get('type') or '?'):<10} {coords:<22} {status}{tail}")
    print()

    if dangling and not (f_type or f_coord or f_status or only_unverified):
        print(f"## dangling links  ({len(dangling)} distinct — run --dangling for detail)")
        for t in sorted(dangling, key=str.lower)[:12]:
            print(f"  [[{t}]]  ({len(dangling[t])}x)")
        if len(dangling) > 12:
            print(f"  … +{len(dangling) - 12} more")

if __name__ == '__main__':
    main()
