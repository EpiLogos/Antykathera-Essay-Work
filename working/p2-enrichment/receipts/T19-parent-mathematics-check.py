from fractions import Fraction as F
from itertools import product
import math,sympy as s
assert F(4,3)**2*F(9,8)==2 and F(3,2)/F(4,3)==F(9,8)
C=F(3,2)**12/2**7;assert C==F(531441,524288)==F(9,8)**6/2==F(19683,16384)/F(32,27)
assert abs(1200*math.log2(C)-23.46)<.01
assert [sum(d for d in range(1,n) if n%d==0) for n in range(1,7)]==[0,1,1,3,1,6]
assert sum([1,2,4,7,14])==28 and math.prod([1,2,4,7,14])==784
assert sum(range(1,5))==10 and 3**2+4**2==5**2 and 3*4/2==6 and 3+4+5==12
assert 12*12+7*13==235 and 19*12==228
assert len({(2*n)%12 for n in range(6)})==6 and len({(7*n)%12 for n in range(12)})==12
x,t,c,L,A=s.symbols('x t c L A',positive=True);u=2*A*s.sin(3*s.pi*x/L)*s.cos(3*s.pi*c*t/L)
assert s.simplify(s.diff(u,t,2)-c*c*s.diff(u,x,2))==0
for j in range(4):assert s.simplify(u.subs(x,j*L/3))==0
x,y=s.symbols('x y',real=True);r=x*x+y*y;X=2*x/(r+1);Y=2*y/(r+1);Z=(r-1)/(r+1)
assert s.simplify(X*X+Y*Y+Z*Z-1)==0
assert s.simplify(X/(1-Z)-x)==0 and s.simplify(Y/(1-Z)-y)==0
assert s.solve([s.Symbol('v')-2*s.Symbol('u')-s.Symbol('w'),s.Symbol('v')-2*s.Symbol('u')+3*s.Symbol('w')],[s.Symbol('v'),s.Symbol('w')])=={s.Symbol('v'):2*s.Symbol('u'),s.Symbol('w'):0}
a=lambda p:(p[0]+1,-p[1]);ai=lambda p:(p[0]-1,-p[1]);b=lambda p:(p[0],p[1]+1)
assert a(b(ai((x,y))))==(x,y-1) and a(a((x,y)))==(x+2,y)
for n in range(6):assert (3*(n%2)+4*(n%3))%6==n
for a0,b0 in product(range(6),repeat=2):
 assert ((a0+b0)%2,(a0+b0)%3)==((a0%2+b0%2)%2,(a0%3+b0%3)%3)
 assert ((a0*b0)%2,(a0*b0)%3)==((a0%2*b0%2)%2,(a0%3*b0%3)%3)
# All formal pairs in the idempotent monoid collapse under stabilisation.
for a0,b0,c0,d0 in product((0,1),repeat=4):assert any(max(a0,d0,t0)==max(c0,b0,t0) for t0 in (0,1))
assert s.diff(x*x+3,x)==2*x and (x*x+3).subs(x,1)==4
cr=lambda a,b,c,d:F((a-c)*(b-d),(a-d)*(b-c))
assert cr(0,1,2,3)==F(4,3) and cr(1,0,2,3)==F(3,4) and cr(0,1,4,9)==F(32,27)
for a0,b0,c0,d0 in [(1,2,1,4),(2,3,1,1),(3,-2,2,7)]:
 if a0*d0-b0*c0:
  z=[F(a0*n+b0,c0*n+d0) for n in (0,1,2,3)]
  assert cr(*z)==F(4,3)
i=s.I;I=s.eye(2);Qi=s.diag(i,-i);Qj=s.Matrix([[0,1],[-1,0]]);Qk=s.Matrix([[0,i],[i,0]])
assert Qi*Qj==Qk and Qj*Qi==-Qk and Qi*Qi==-I
Q=[sgn*m for m in [I,Qi,Qj,Qk] for sgn in [1,-1]]
for a0,b0 in product(Q,repeat=2):assert a0*b0 in Q
assert Qi*Qj*(-Qi)==-Qj and Qi*Qk*(-Qi)==-Qk
plus=s.Matrix([1,1])/s.sqrt(2);minus=s.Matrix([1,-1])/s.sqrt(2)
assert (plus.T*minus)[0]==0 and plus*plus.T==s.Matrix([[1,1],[1,1]])/2
rx,ry,rz,lam=s.symbols('rx ry rz lam',real=True)
rho=(I+rx*s.Matrix([[0,1],[1,0]])+ry*s.Matrix([[0,-i],[i,0]])+rz*s.diag(1,-1))/2
assert s.expand((rho-lam*I).det()-(lam**2-lam+(1-rx*rx-ry*ry-rz*rz)/4))==0
mu=s.symbols('mu',real=True);V=x**4/4-mu*x*x/2;v=mu*x-x**3
assert s.expand(s.diff(V,x)*v+v*v)==0
assert s.diff(v,x).subs(x,s.sqrt(mu))==-2*mu
x0=s.symbols('x0',positive=True);tt=s.symbols('tt',nonnegative=True)
sol=x0/s.sqrt(x0*x0+(1-x0*x0)*s.exp(-2*tt))
assert s.simplify(s.diff(sol,tt)-(sol-sol**3))==0 and s.limit(sol,tt,s.oo)==1
print('PASS all 19 coverage families: exact ratio/cycle/divisor/calendar arithmetic; wave/sphere/projective/Klein identities; CRT operations and monoid collapse; derivative; cross-ratio; Q8 closure/conjugation; qubit state/density algebra; pitchfork gradient/stability and explicit basin solution.')
