import sympy as s
t=s.symbols('t',real=True);m,k,A,B,w=s.symbols('m k A B w',positive=True)
x=A*s.cos(w*t);y=B*s.sin(w*t)
l=s.simplify(m*(x*s.diff(y,t)-y*s.diff(x,t)));assert l==m*A*B*w
H=m*(s.diff(x,t)**2+s.diff(y,t)**2)/2+k*(x*x+y*y)/2
assert s.simplify(H.subs(k,m*w*w)-m*w*w*(A*A+B*B)/2)==0
X,Y,VX,VY,KT,DK=s.symbols('X Y VX VY KT DK')
L=m*(VX*VX+VY*VY)/2-KT*(X*X+Y*Y)/2
assert s.expand(-Y*s.diff(L,X)+X*s.diff(L,Y)-VY*s.diff(L,VX)+VX*s.diff(L,VY))==0
energy=m*(VX*VX+VY*VY)/2+KT*(X*X+Y*Y)/2
D=lambda f:s.diff(f,X)*VX+s.diff(f,Y)*VY-s.diff(f,VX)*KT*X/m-s.diff(f,VY)*KT*Y/m+s.diff(f,KT)*DK
assert s.simplify(D(energy)-DK*(X*X+Y*Y)/2)==0
assert s.expand(D(m*(X*VY-Y*VX)))==0
q=s.Function('q')(t);a=s.Function('a')(t);e=s.Function('epsilon')(t)
wq=s.diff(q,t)-a
assert s.simplify(-s.diff(wq,t)-s.diff(-wq,t))==0
assert s.expand(s.diff(q+e,t)-(a+s.diff(e,t))-wq)==0
print('PASS exact oscillator charges, rotational variation, driven energy balance, preserved angular momentum, arbitrary-function gauge invariance and off-shell differential identity.')
