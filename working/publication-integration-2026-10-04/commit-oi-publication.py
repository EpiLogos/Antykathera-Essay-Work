from pathlib import Path
import subprocess,os,json,hashlib
repo=Path('/Users/admin/Central/Work/O-I');out=repo/'Antykathera-Essay-Work/working/publication-integration-2026-10-04'
d=json.loads((out/'OI-PUBLICATION-COMMIT.json').read_text());base=d['base'];previous=d['commit'];ref=d['ref']
paths=list(dict.fromkeys([r['path'] for r in d['owned_files']]+['site/src/shell/ShellApp.tsx', 'site/src/shell/ShellNav.tsx', 'site/src/shell/shell.css', 'site/src/shell/public-entrance.css', 'site/src/shell/content.ts', 'site/shell.html', 'site/tests/read-shell-source.mjs', 'site/tests/shell-v2-acceptance.py', 'site/tests/library-acceptance.py', 'site/tests/library-regressions.py', '.github/workflows/site-shell-v2.yml']))
def git(*args,input=None,env=None):return subprocess.check_output(['git',*args],cwd=repo,input=input,env=env).decode().strip()
assert git('rev-parse',ref)==previous
env={**os.environ,'GIT_INDEX_FILE':str(out/'oi-publication.index')};git('read-tree',previous,env=env);updates=[];rows=[]
for path in paths:
 data=(repo/path).read_bytes();blob=git('hash-object','-w','--stdin',input=data);old=git('ls-tree',previous,'--',path);mode=old.split()[0] if old else '100644';updates.append(f'{mode} {blob}\t{path}\n');rows.append({'path':path,'blob':blob,'sha256':hashlib.sha256(data).hexdigest()})
git('update-index','--index-info',input=''.join(updates).encode(),env=env);tree=git('write-tree',env=env);commit=git('commit-tree',tree,'-p',previous,input=b'Install declared Quartz dependencies before native site gates\n\nThe existing staged-input test imports the actual Quartz glob utility. Prepare its locked native dependencies in the selected site bootstrap without changing any gate or runner semantics.\n');git('update-ref',ref,commit,previous);changed=git('diff','--name-only',base,commit).splitlines();assert set(changed)<=set(paths);d.update(commit=commit,tree=tree,previous_publication_commit=previous,changed_paths=changed,owned_files=rows);(out/'OI-PUBLICATION-COMMIT.json').write_text(json.dumps(d,indent=2)+'\n');print({'commit':commit,'files':len(changed)})
