# pin c5=1 (the physical branch) and complete SP-1: physicality, traces, decomposition
exec(open('sp1_bl.py').read().split("# ---------- SP-1")[0])
g,y,bL=phys_assign[0]
import sympy as sp
rows=[]
for i,lam in enumerate(weights):
    t3l=sp.Rational(wt_ip(lam,bL),2); yy=sp.Rational(y_eig(y,lam),6)
    rows.append((i,lam,i in colored,t3l,yy,t3l+yy))
c=[0,-1,0,sp.Rational(1,3),0,1]   # c5=1 branch of the solved family
BL=[sum(sp.Rational(c[j])*sp.Rational(lam[j]) for j in range(6)) for i,lam,col,t3l,yy,q in rows]
ok=all((b in (sp.Rational(1,3),sp.Rational(-1,3),sp.Rational(2,3),sp.Rational(-2,3))) if col
       else (b in (sp.Rational(1),sp.Rational(-1),sp.Rational(0)))
       for (i,lam,col,t3l,yy,q),b in zip(rows,BL))
print("SP-1 (c5=1): B-L physical on ALL 27:", ok)
print("Tr(B-L) =", sum(BL), "  Tr(B-L)^3 =", sum(b**3 for b in BL))
# decomposition vs (Y, T3R)
zs=[r for r in list(G1c)+list(G2c) if sum(y[i]*iprr(cor[i],r) for i in range(4))==0]
bR=[r for r in zs if (r in G1c)!=(bL in G1c)][0]
t3r=[sp.Rational(wt_ip(lam,bR),2) for i,lam,col,t3l,yy,q in rows]
yv=[yy for i,lam,col,t3l,yy,q in rows]
import itertools as it
solved=None
for i1,i2 in it.combinations(range(27),2):
    M=sp.Matrix([[yv[i1],t3r[i1]],[yv[i2],t3r[i2]]])
    if M.det()!=0:
        ab=M.solve(sp.Matrix([BL[i1],BL[i2]]))
        if all(sp.simplify(ab[0]*yv[k]+ab[1]*t3r[k]-BL[k])==0 for k in range(27)): solved=ab; break
print("B-L = a*Y + b*T3R exactly?", f"YES (a,b)=({solved[0]},{solved[1]})" if solved else "NO — independent third Cartan direction")
# is B-L in the span of {Y, T3L, T3R}?
av,bv,cvv=sp.symbols('av bv cvv')
t3lv=[t3l for i,lam,col,t3l,yy,q in rows]
s3=None
for i1,i2,i3 in it.combinations(range(27),3):
    M=sp.Matrix([[yv[i1],t3r[i1],t3lv[i1]],[yv[i2],t3r[i2],t3lv[i2]],[yv[i3],t3r[i3],t3lv[i3]]])
    if M.det()!=0:
        ab=M.solve(sp.Matrix([BL[i1],BL[i2],BL[i3]]))
        if all(sp.simplify(ab[0]*yv[k]+ab[1]*t3r[k]+ab[2]*t3lv[k]-BL[k])==0 for k in range(27)): s3=ab; break
print("B-L in span{Y,T3R,T3L}?", f"YES {tuple(s3)}" if s3 else "NO — genuinely fourth direction")
