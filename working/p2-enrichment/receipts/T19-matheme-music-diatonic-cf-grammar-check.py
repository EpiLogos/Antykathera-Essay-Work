from pathlib import Path
from fractions import Fraction as F
import re,json
s=Path('submission-package/essay/symbolon/matheme/music/diatonic-cf-grammar.md').read_text()
N={'C':0,'C♯':1,'D':2,'D♯':3,'E':4,'F':5,'F♯':6,'G':7,'G♯':8,'A':9,'A♯':10,'B':11}
S=[0,2,4,5,7,9,11];faces='NNNPPPP'
selection=re.findall(r'\| (\d) / CF(\d) \| (\d)(′?) \| (Name|Power) \| ([A-G]) \|',s)
assert len(selection)==7
for deg,cf,k,prime,face,note in selection:
 assert deg==cf
 assert N[note]==2*int(k)+bool(prime)==S[int(deg)-1]
 assert ('P' if prime else 'N')==faces[int(deg)-1]
 assert face==('Power' if prime else 'Name')
modes=re.findall(r'\| (Ionian|Dorian|Phrygian|Lydian|Mixolydian|Aeolian|Locrian) \| ([A-G]) / CF(\d) \| `([0-9,]+)` \| `([NP]+)` \|',s)
assert len(modes)==7
for name,note,cf,degrees,pattern in modes:
 i=int(cf)-1; assert N[note]==S[i]
 seq=S[i:]+[v+12 for v in S[:i]]
 assert [int(x)for x in degrees.split(',')]==[v-S[i]for v in seq]
 assert pattern==faces[i:]+faces[:i]
scales=re.findall(r'\| L([0-5])(′?) \| ([A-G]♯?) \| ([A-G♯ ]+) \|',s)
assert len(scales)==12
for k,prime,anchor,notes in scales:
 a=N[anchor];assert a==2*int(k)+bool(prime)
 assert [N[v]for v in notes.split()]==[(a+t)%12 for t in S]
r=[F(1),F(9,8),F(81,64),F(4,3),F(3,2),F(27,16),F(243,128),F(2)]
steps=[r[i+1]/r[i]for i in range(7)]
assert steps==[F(9,8),F(9,8),F(256,243),F(9,8),F(9,8),F(9,8),F(256,243)]
prod=F(1)
for step in steps:prod*=step
assert prod==2 and F(4,3)*F(9,8)*F(4,3)==2
minor=[0,2,3,5,7,8,10]
assert ''.join('P'if x%2 else'N'for x in minor)=='NNPPPNN'
cluster={0,2,4,5,7};maj9={0,4,7,11,2}
assert cluster-maj9=={5}and maj9-cluster=={11}
assert sorted((x-2)%12 for x in cluster)==[0,2,3,5,10]
Path('working/p2-enrichment/receipts/T19-matheme-music-diatonic-cf-grammar-arithmetic.json').write_text(json.dumps({'method':'Parse actual selected-note, mode and lens-scale rows; exact Fraction ratio checks','CF_rows':len(selection),'modal_rows_and_face_patterns':len(modes),'lens_scales':len(scales),'pure_step_ratios':[str(x)for x in steps],'pure_product':str(prod),'parallel_minor_faces':'NNPPPNN','cluster_not_major_ninth':True,'passed':True},indent=2)+'\n')
print('Seven CF rows, seven modes, twelve lens scales and exact ratio/chord checks passed.')
