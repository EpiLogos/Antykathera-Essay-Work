from pathlib import Path
import re,json
s=Path('submission-package/essay/symbolon/matheme/music/pairing-grammar.md').read_text()
N={'C':0,'C♯':1,'D':2,'D♯':3,'E':4,'F':5,'F♯':6,'G':7,'G♯':8,'A':9,'A♯':10,'B':11}
P={'A':[(0,1),(2,3),(4,5)],'B':[(0,5),(1,4),(2,3)],'C':[(1,2),(3,4),(5,0)]}
rows=re.findall(r'\| ([ABC]) \| `\((\d),(\d)\)` \| ([A-G]♯?)→([A-G]♯?) \| (\d+) \| ([A-G]♯?)→([A-G]♯?) \| (\d+) \|',s)
assert len(rows)==9
for family,i,j,c1,c2,cd,f1,f2,fd in rows:
 i,j=int(i),int(j);assert(i,j)in P[family]
 assert (N[c1],N[c2])==(2*i%12,2*j%12)
 assert (N[f1],N[f2])==(7*i%12,7*j%12)
 assert int(cd)==(N[c2]-N[c1])%12
 assert int(fd)==(N[f2]-N[f1])%12
squares=re.findall(r'\| ([ABC])-sq([123]) \| `[^`]+` \| ([A-G♯, ]+) \|',s)
assert len(squares)==9
sets=[]
for family,idx,notes in squares:
 i,j=P[family][int(idx)-1]
 got=[N[n.strip()]for n in notes.split(',')];expected=[2*i,2*j,2*i+1,2*j+1]
 assert got==expected,(family,idx,got,expected)
 sets.append(frozenset(got))
assert len(set(sets))==7
assert sets[1]==sets[5] and sets[3]==sets[8]
m=lambda t:(5-t[0],t[1]);sig=lambda t:(t[0],1-t[1])
for k in range(6):
 for e in (0,1):
  t=(k,e);assert m(m(t))==t and sig(sig(t))==t and m(sig(t))==sig(m(t))
  assert len({t,m(t),sig(t),m(sig(t))})==4
invariance=0
for pair in set(sum(P.values(),[])):
 i,j=pair
 for f in [lambda k,e:(2*k+e)%12,lambda k,e:(7*k+6*e)%12]:
  delta=(f(j,0)-f(i,0))%12
  assert (f(j,1)-f(i,1))%12==delta
  for a in range(12):
   assert ((f(j,0)+a)-(f(i,0)+a))%12==delta;invariance+=1
assert [(N['D']-N['C♯'])%12,(N['D♯']-N['C'])%12,(N['D♯']-N['C♯'])%12]==[1,3,2]
Path('working/p2-enrichment/receipts/T19-matheme-music-pairing-grammar-arithmetic.json').write_text(json.dumps({'method':'Parse printed interval and square tables; compare modular maps and exact sets','interval_rows_verified':len(rows),'square_rows_verified':len(squares),'ordered_base_pairs':len(set(sum(P.values(),[]))),'unique_tetrads':len(set(sets)),'coincidences':['A-sq2=B-sq3','B-sq1=C-sq3 as unordered tetrads'],'mirror_flip_states_verified':12,'full_inversion_pairs_and_bases':16,'anchor_transpositions_verified':invariance,'D_example_displacements':[1,3,2],'passed':True},indent=2)+'\n')
print('All printed table and algebra checks passed; seven unique tetrads verified.')
