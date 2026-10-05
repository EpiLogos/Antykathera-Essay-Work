#!/usr/bin/env python3
"""Reproducible bounded checks for s3; not a proof of its ontological argument."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import hashlib, json, math, re
import sympy as S

checks=[]
def check(name, condition):
    if not bool(condition):
        raise AssertionError(name)
    checks.append(name)

def area(points):
    return abs(sum(x*v-u*y for (x,y),(u,v) in zip(points,points[1:]+points[:1])))/2
N,E,W,South=(0,1),(1,0),(-1,0),(0,-1)
check('triangle area',area([N,E,W])==1)
check('square area',area([N,E,South,W])==2)
check('complementary triangles',area([N,E,W])+area([South,E,W])==2)
def expand(a,b,c,d):
    return ((a,c),(a,d),(b,c),(b,d))
P=expand(0,1,1,0);Q=expand(1,0,0,1)
check('forward parent',P==((0,1),(0,0),(1,1),(1,0)))
check('inverse parent',Q==((1,0),(1,1),(0,0),(0,1)))
check('phase reversal',Q==P[::-1])
check('outer pure positions become mixed',all(P[i][0]!=P[i][1] for i in (0,3)))
check('outer mixed positions become pure',all(P[i][0]==P[i][1] for i in (1,2)))
B=tuple(product((0,1),repeat=2))
check('singles and ordered pairs',2+len(B)==6)
X=S.Matrix([[0,1],[1,0]]);D=S.diag(1,-1);I=S.eye(2);J=X*D
check('swap order two',X*X==I)
check('polarity order two',D*D==I)
check('anticommutation',X*D==-D*X)
check('quarter turn squared',J*J==-I)
check('quarter turn fourth power',J**4==I)
b=S.Matrix([0,1]);p=S.Matrix([1,0]);u=b+p;d=p-b
check('invariant',X*u==u)
check('anti-invariant',X*d==-d)
check('phase reconstruction',(u-d)/2==b and (u+d)/2==p)
check('Boolean coverage',tuple(x|y for x,y in zip((0,1),(1,0)))==(1,1))
check('Boolean fixed point absent',all(n!=1-n for n in (0,1)))
check('second typed count',len(tuple(product((0,1),repeat=6)))+6*6==100)
check('third typed count',1+2**6+2*6**2==137)
check('alternative partition',2**7+3**2==137)
check('four triad blocks',4*3**2==6**2)
check('sector ratio',F(64,36)==F(16,9))
check('harmonic transfer',36*F(16,9)==64 and 64*F(9,8)==72)
check('fourth plus fifth',F(4,3)*F(3,2)==2)
check('two fourths plus tone',F(4,3)**2*F(9,8)==2)
check('ratio comparison not scalar division',(F(4,2)/F(3,3))==2)
check('Pythagorean comma',F(3,2)**12/F(2)**7==F(531441,524288))
check('six just whole tones comma',F(9,8)**6/F(2)==F(531441,524288))

def cr(z):
    a,b,c,d=z;return (c-a)*(d-b)/((c-b)*(d-a))
f=lambda z:(2*z+1)/(z+1)
z=tuple(map(F,(0,1,2,3)))
check('cross ratio',cr(z)==F(4,3))
check('transformed cross ratio',cr(tuple(map(f,z)))==F(4,3))
a,b,c,d,x,y=S.symbols('a b c d x y')
f=lambda t:(a*t+b)/(c*t+d)
check('Mobius difference identity',S.factor(f(x)-f(y)-(a*d-b*c)*(x-y)/((c*x+d)*(c*y+d)))==0)
u,v=S.symbols('u v',real=True)
yu=(u*u-1)/(u*u+1);yv=(1-v*v)/(1+v*v)
check('chart agreement',S.simplify(yu-yv.subs(v,1/u))==0)
check('chart velocity',S.diff(yu,u).subs(u,3)*2==S.Rational(6,25))
check('inverse chart velocity',S.diff(yv,v).subs(v,S.Rational(1,3))*S.Rational(-2,9)==S.Rational(6,25))
check('torus cell Euler characteristic',1-2+1==0)
check('lift endpoint has same quotient',(2%1,(-1)%1)==(0,0))
neg=lambda value: frozenset('F' if bit=='T' else 'T' for bit in value)
pv=frozenset(('T','F'));qv=frozenset()
check('four value countermodel','T' in pv and 'T' in neg(pv) and 'T' not in qv)
Nv,n=S.symbols('N n')
check('Phone independent variables correction',S.expand((Nv+1)*(n-1)-(Nv*n-1))==n-Nv)
check('Phone same variable identity',S.expand((n+1)*(n-1)-(n*n-1))==0)
check('Phone slope not fifteen degrees',abs(math.degrees(math.atan(1/4))-15)>0.9)
check('Phone 24 sectors',360/15==24)

path=Path(__file__).with_name('SECTION.md');text=path.read_text();body=text.split('\n## Source notes\n')[0]
check('six unique movement anchors',re.findall(r'<a id="s3-m(\d+)"></a>',body)==[str(i) for i in range(25,31)])
refs=set(re.findall(r'\[\^(s3-[^]]+)\]',body));defs=re.findall(r'^\[\^(s3-[^]]+)\]:',text,re.M)
check('notes resolve',refs==set(defs))
check('note definitions unique',len(defs)==len(set(defs)))
check('dollar display delimiters balanced',len(re.findall(r'^\$\$$',text,re.M))%2==0)
check('retired display delimiters removed','\\[' not in text and '\\]' not in text)
check('no TODO prose',not re.search(r'\b(TODO|TBD|PLACEHOLDER)\b',body))
# Report both transparent counts; the baseline receipt supplies its own historical count.
stripped=re.sub(r'<[^>]+>','',body)
stripped=re.sub(r'^#{1,6} .*$', '',stripped,flags=re.M)
stripped=re.sub(r'\[\^[^]]+\]','',stripped)
raw=path.read_bytes()
result={'checks_passed':len(checks),'checks':checks,'body_whitespace_words':len(body.split()),'body_words_without_headings_anchors_note_calls':len(stripped.split()),'total_whitespace_words':len(text.split()),'bytes':len(raw),'git_blob_sha1':hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest(),'sha256':hashlib.sha256(raw).hexdigest(),'claim_boundary':'Finite calculations and editorial integrity only; no claim to prove the native metaphysics or independently review the manuscript.'}
Path(__file__).with_name('CHECKS.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='checks'},indent=2))
