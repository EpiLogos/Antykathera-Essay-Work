from pathlib import Path
import re,json
s=Path('submission-package/essay/symbolon/matheme/music/lens-anchors.md').read_text()
N={'C':0,'C♯':1,'D':2,'D♯':3,'E':4,'F':5,'F♯':6,'G':7,'G♯':8,'A':9,'A♯':10,'B':11}
rows=re.findall(r'\| L([0-5])(′?) \| ([^|]+) \| ([0-5])(′?) \| ([A-G]♯?) \| ([A-G]♯?) \|',s)
assert len(rows)==12
for k,prime,label,j,jprime,c,f in rows:
 k=int(k);e=int(bool(prime));assert k==int(j) and prime==jprime
 assert N[c]==(2*k+e)%12 and N[f]==(7*k+6*e)%12
assert len({N[r[-2]]for r in rows})==12
assert len({N[r[-1]]for r in rows})==12
assert [(p-4)%12 for p in (0,4,7)]==[8,0,3]
assert [(p-2)%12 for p in (0,2,7)]==[10,0,5]
for a in range(12):
 for p in range(12):
  for d in range(12):assert ((p+d)-(a+d))%12==(p-a)%12
I={(k,e)for k in range(1,5)for e in (0,1)}
B={(k,e)for k in (0,5)for e in (0,1)}
assert len(I)==8 and len(B)==4 and not I&B and len(I|B)==12
pc=lambda t:(2*t[0]+t[1])%12
assert {pc(t)for t in I}==set(range(2,10))
assert {pc(t)for t in B}=={0,1,10,11}
major={0,2,4,5,7,9,11}
assert len(major&{pc(t)for t in I})==5
assert len(major&{pc(t)for t in B})==2
R=lambda t:(5-t[0],1-t[1])
for t in I|B:assert R(R(t))==t
assert R((1,0))==(4,1) and R((4,0))==(1,1)
Path('working/p2-enrichment/receipts/T19-matheme-music-lens-anchors-arithmetic.json').write_text(json.dumps({'method':'Parse actual lens table; exact integer maps and finite sets','lens_rows_verified':len(rows),'anchor_bijections':2,'worked_reference_examples':2,'transposition_reference_identities':12**3,'architectural_partition':[8,4],'CF_major_partition':[5,2],'return_involutions':12,'passed':True},indent=2)+'\n')
print('All lens, reference, partition and return checks passed.')
