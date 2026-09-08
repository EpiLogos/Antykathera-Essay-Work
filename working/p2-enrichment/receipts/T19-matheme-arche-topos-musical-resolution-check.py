from pathlib import Path
from fractions import Fraction as F
import json,re,hashlib
root=Path(__file__).resolve().parents[3]
p=root/'submission-package/essay/symbolon/matheme/harmonics/arche-topos-musical-resolution.md'
s=p.read_text();checks={}
checks['six_sections']=len(re.findall(r'^## #',s,re.M))==6
name=['C','C♯','D','D♯','E','F','F♯','G','G♯','A','A♯','B']
rows=[line.split('|')[1:-1] for line in s.splitlines() if re.match(r'^\| [0-5] \|',line)]
assert len(rows)==6
for k,cols in enumerate(rows):
 assert int(cols[0])==k
 assert cols[2].strip()==' / '.join(name[(2*k+e)%12] for e in [0,1])
 assert cols[3].strip()==' / '.join(name[(7*k+6*e)%12] for e in [0,1])
checks['printed_pitch_maps']=True
for label,fn in [('Chromatic',lambda k,e:(2*k+e)%12),('Fifths',lambda k,e:(7*k+6*e)%12)]:
 row=next(line for line in s.splitlines() if line.startswith('| '+label+' `'))
 printed=[int(x.strip()) for x in row.split('|')[2:-1]]
 expected=[(fn(5-k,1)-fn(k,0))%12 for k in range(6)]
 assert printed==expected
checks['printed_D2_arrays']=True
checks['mirror_involution']=all((5-(5-k),1-(1-e))==(k,e) for k in range(6) for e in range(2))
checks['ratio_path']=F(288)*F(4,3)==384 and F(384)*F(9,8)==432 and F(432)*F(4,3)==576
checks['totality_then_return']=F(288)*F(16,9)==512 and F(512)*F(9,8)==576
checks['equal_remainders']=F(3,2)/F(4,3)==F(2)/F(16,9)==F(9,8)
checks['comma']=F(3,2)**12/F(2)**7==F(9,8)**6/F(2)==F(531441,524288)
selection=[(0,0),(1,0),(2,0),(2,1),(3,1),(4,1),(5,1)]
pcs=[(2*k+e)%12 for k,e in selection]
checks['major_selection']=pcs==[0,2,4,5,7,9,11]
checks['inner_outer']=sum(k in [1,2,3,4] for k,e in selection)==5
checks['dorian']=[(p-2)%12 for p in pcs[1:]+pcs[:1]]==[0,2,3,5,7,9,10]
checks['distinct_indexed_modal_field']=len({(a,m) for a in range(12) for m in range(7)})==84
checks['parallel_minor_moves']=((2*2+0)%12,(2*1+1)%12)==(4,3)
checks['full_chain']='0/1 = 4+2 = 5→0 = 1/0 = 4′+2′ = 5′→0′ = 0/1' in s
links=[]
for dest in re.findall(r'\]\(([^)]+)\)',s):
 if '://' not in dest and not dest.startswith('#'):
  links.append({'destination':dest,'exists':(p.parent/dest.split('#')[0]).exists()})
checks['relative_links']=all(x['exists'] for x in links)
assert all(checks.values()),checks
out={'page':str(p.relative_to(root)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'checks':checks,'links':links,'standing':'Exact candidate mathematical constructions; no audio capture or deployed runtime observation'}
(root/'working/p2-enrichment/receipts/T19-matheme-arche-topos-musical-resolution-checks.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'checks':checks,'links':len(links),'sha256':out['sha256']},indent=2))
