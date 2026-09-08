from pathlib import Path
from fractions import Fraction as F
import json
s=Path('submission-package/essay/symbolon/matheme/music/field.md').read_text()
S=[0,2,4,5,7,9,11];K={0,2,4,5,7}
scales={a:{(a+x)%12 for x in S}for a in range(12)}
clusters={a:{(a+x)%12 for x in K}for a in range(12)}
M={(a,m)for a in range(12)for m in range(7)}
V={(a,b)for a in range(12)for b in range(12)}
Vi={(a,b)for a,b in V if b in scales[a]};Vo=V-Vi
image={(a,(a+S[m])%12)for a,m in M}
assert len(M)==84 and len(V)==144 and len(Vi)==84 and len(Vo)==60
assert image==Vi and len(image)==len(M)
for a,b in image:assert len([m for m in range(7)if(a+S[m])%12==b])==1
fits={(a,b):[c for c in range(12)if clusters[a]|{b}<=scales[c]]for a,b in Vo}
assert sum(bool(v)for v in fits.values())==12
assert sum(not v for v in fits.values())==48
for a in range(12):
 for b in range(12):
  if (a,b)in fits:
   assert fits[a,b]==([(a+5)%12]if b==(a+10)%12 else [])
for note,b in [('C♯',1),('D♯',3),('F♯',6),('G♯',8)]:
 assert f'| {note} | None |'in s and fits[0,b]==[]
assert '| A♯ = B♭ | F |'in s and fits[0,10]==[5]
kappa=F(531441,524288)
assert F(3,2)**12/F(2)**7==kappa
assert F(9,8)**6/F(2)==kappa
assert F(9,8)**5/F(16,9)==kappa
assert kappa!=F(9,8)
Path('working/p2-enrichment/receipts/T19-matheme-music-field-arithmetic.json').write_text(json.dumps({'method':'Exhaust all indexed modal and cluster/bass states, all candidate containing scales, and exact Fraction returns','M':len(M),'V':len(V),'V_in':len(Vi),'V_out':len(Vo),'bijection_verified':image==Vi,'outside_with_alternative_major_parent':12,'outside_without_any_major_parent':48,'C_parent_outside_rows':{str(b):fits[0,b]for b in [1,3,6,8,10]},'comma_three_routes':str(kappa),'passed':True},indent=2)+'\n')
print('84→84 bijection, 144=84+60 partition, all 720 outside-parent containment tests and three comma identities passed.')
