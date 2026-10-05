#!/usr/bin/env python3
"""Preserve the local authoring layout while receiving published recovery bodies."""
from pathlib import Path
import hashlib, json, os, posixpath, re, subprocess, sys, tempfile

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent

def git(*args, data=None, env=None):
    return subprocess.run(['git', *args], cwd=ROOT, input=data, capture_output=True, check=True, env=env).stdout

def tree(ref):
    result = {}
    for row in git('ls-tree', '-rz', ref).split(b'\0'):
        if row:
            meta, path = row.split(b'\t', 1)
            mode, kind, sha = meta.decode().split()
            if kind == 'blob': result[path.decode()] = (mode, sha)
    return result

def digest(data): return hashlib.sha256(data).hexdigest() if data is not None else None

def mapped(path):
    prefix = 'submission-package/essay/'
    for old, new in [('arguments/', 'arguments/'), ('conjugate/', 'arguments/conjugate/'),
                     ('concepts/', 'arguments/concepts/'), ('products/', 'arguments/products/')]:
        before = prefix + 'symbolon/episteme/' + old
        if path.startswith(before): return prefix + 'section-rooms/' + new + path[len(before):]
    p = Path(path)
    if path.startswith(prefix + 'symbolon/episteme/sources/'):
        if p.name == 'SOURCE.md': return str(p.with_name(p.parent.name + '.md'))
        if p.name == 'SOURCE': return str(p.with_name(p.parent.name))
        if p.name == 'NOTES.md': return str(p.with_name(p.parent.name + '-NOTES.md'))
    if path.startswith(prefix + 'section-rooms/') and p.name in ('ROOM.md', 'READING.md'):
        return str(p.with_name(p.stem + '-' + p.parent.name + '.md'))
    if path.startswith(prefix + 'symbolon/episteme/') and p.name in ('HISTORY.md', 'DEVELOPMENT.md', 'WHOLE-FIELD.md', 'HISTORICAL-BRANCHES.md'):
        return str(p.with_name(p.stem + '-' + p.parent.name + '.md'))
    if path.startswith(prefix + 'section-rooms/arguments/') and re.match(r'^\d\d-', p.name):
        return 'working/legacy/section-rooms-arguments/' + p.name
    return path

def relocate(data, oldpath, newpath):
    try: text = data.decode('utf-8')
    except UnicodeDecodeError: return data
    if not oldpath.endswith('.md'): return data
    def target(value):
        if not value or value.startswith(('#', '/', 'http:', 'https:', 'mailto:', 'data:', 'app:', 'resource:')): return value
        bare, sep, anchor = value.partition('#')
        if ' ' in bare or '\n' in bare: return value
        resolved = posixpath.normpath(posixpath.join(posixpath.dirname(oldpath), bare))
        destination = mapped(resolved)
        if destination != resolved or oldpath != newpath:
            return posixpath.relpath(destination, posixpath.dirname(newpath)) + (sep + anchor if sep else '')
        return value
    text = re.sub(r'(?<=\]\()([^()\n]+)(?=\))', lambda m: target(m.group()), text)
    def wiki(m):
        inner = m.group(1)
        value, sep, label = inner.partition('|')
        bare, mark, anchor = value.partition('#')
        if bare.startswith(('symbolon/', 'section-rooms/')):
            replacement = mapped('submission-package/essay/' + bare)[len('submission-package/essay/'):]
            return '[[' + replacement + (mark + anchor if mark else '') + (sep + label if sep else '') + ']]'
        return m.group()
    return re.sub(r'\[\[([^\]\n]+)\]\]', wiki, text).encode()

def main():
    old = git('rev-parse', 'HEAD').decode().strip()
    new = git('rev-parse', 'origin/main').decode().strip()
    base, incoming = tree(old), tree(new)
    shas = sorted({v[1] for p,v in incoming.items() if base.get(p) != v} | {base[p][1] for p,v in incoming.items() if p in base and base[p] != v})
    raw = git('cat-file', '--batch', data=('\n'.join(shas)+'\n').encode())
    blobs = {}; offset = 0
    for sha in shas:
        end = raw.index(b'\n', offset); header = raw[offset:end].decode().split(); size = int(header[2]); offset = end+1
        blobs[sha] = raw[offset:offset+size]; offset += size+1
    rows = []; candidate = OUT/'.legacy-candidates'; candidate.mkdir(parents=True, exist_ok=True)
    for path, item in incoming.items():
        if base.get(path) == item: continue
        destination = mapped(path); f = ROOT/destination
        local = f.read_bytes() if f.is_file() and not f.is_symlink() else None
        received = relocate(blobs[item[1]], path, destination)
        previous = relocate(blobs[base[path][1]], path, destination) if path in base else None
        decision = 'receive'; result = received
        if path == 'submission-package/essay/THE-RETURN-OF-ZERO.md' or path.endswith('NOTES.md'):
            decision = 'preserve-authorial'; result = local
        elif local == received: decision = 'already-received'; result = local
        elif local is not None and previous is None: decision = 'addition-collision'; result = local
        elif local is not None and local != previous:
            with tempfile.TemporaryDirectory(dir=OUT) as temp:
                a,b,c = [Path(temp)/x for x in ('local','base','received')]
                a.write_bytes(local);b.write_bytes(previous);c.write_bytes(received)
                r = subprocess.run(['git','merge-file','-p',str(a),str(b),str(c)],capture_output=True)
                decision = 'merged' if r.returncode == 0 else 'conflict'; result = r.stdout
        if decision not in ('preserve-authorial','already-received'):
            c = candidate/destination;c.parent.mkdir(parents=True,exist_ok=True);c.write_bytes(result)
        rows.append(dict(published_path=path,local_path=destination,mode=item[0],published_blob=item[1],preimage_sha256=digest(local),postimage_sha256=digest(result),decision=decision))
    report=dict(schema='essay.local-recovery-reconciliation/v1',old_head=old,incoming_main=new,rows=rows,deleted_upstream_preserved=[p for p in base if p not in incoming])
    (OUT/'RECONCILIATION-PLAN.json').write_text(json.dumps(report,indent=2)+'\n')
    from collections import Counter
    print(json.dumps(dict(old_head=old,incoming_main=new,dispositions=Counter(x['decision'] for x in rows),conflict_count=sum(x['decision'] in ('conflict','addition-collision') for x in rows)),indent=2))

if __name__ == '__main__': main()
