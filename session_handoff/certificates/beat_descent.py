#!/usr/bin/env python3
"""THE DESCENT — the Gieseking beat on the e6 layer (B1127's bridge, completed).

1. 2x2 level (exact over Q(q)): the beat g -> W conj(g) W^-1 with W=[[1,q],[0,1]]
   fixes A and sends B to an explicit parabolic; on sl2: e->e, h->h-2q e,
   f->f+q h-q^2 e — precisely the unipotent exp(ad(q e)) composed with Galois.
2. e6 level: Sigma := exp(ad(q E)) o gal (E = the paper's principal e6e, gal =
   coefficientwise q -> 1-q) is an antilinear automorphism of e6 extending the
   beat through the principal dictionary.  VERIFY exactly:
     - exp(ad(qE)) e6h = e6h - 2q e6e ;  exp(ad(qE)) e6f = e6f + q e6h - q^2 e6e
     - Sigma^2 = exp(ad(E)) = Ad(meridian)  on ALL 78 basis vectors
     - Sigma is a bracket-automorphism (spot check over Q(q))
3. THE OBSTRUCTION: Sigma^2 = Ad(tick) != 1 — the object's antilinear element is
   NOT a real structure (those need sigma^2=1).  And the beat does not fix the
   color slot: dim( exp(ad qE)(I2) n I2 ).
"""
import importlib.util, itertools, random
from fractions import Fraction as F

SCR="/tmp/claude-0/-home-user-golden-gate/7aec077f-59a6-5129-b1a7-361cc5dcb800/scratchpad"
src=open(SCR+"/twisted_double.py").read()
cut=src.index("# ---------------- stage 1")
exec(src[:cut])          # field Q(q) ops + e6 (br, ROOTS, IDX, N, DIM) + e6e,e6h,e6f

# ---------- part 1: the 2x2 beat ----------
W=[[ONE,QQ],[ZERO,ONE]]
def mm2(A_,B_):
    return [[fadd(fmul(A_[0][0],B_[0][0]),fmul(A_[0][1],B_[1][0])), fadd(fmul(A_[0][0],B_[0][1]),fmul(A_[0][1],B_[1][1]))],
            [fadd(fmul(A_[1][0],B_[0][0]),fmul(A_[1][1],B_[1][0])), fadd(fmul(A_[1][0],B_[0][1]),fmul(A_[1][1],B_[1][1]))]]
def minv2(A_):
    d=fsub(fmul(A_[0][0],A_[1][1]),fmul(A_[0][1],A_[1][0])); di=finv(d)
    return [[fmul(di,A_[1][1]),fmul(di,fneg(A_[0][1]))],[fmul(di,fneg(A_[1][0])),fmul(di,A_[0][0])]]
def fbar(u): return (u[0]+u[1], -u[1])
def mbar2(A_): return [[fbar(x) for x in r] for r in A_]
def beat2(g): return mm2(mm2(W,mbar2(g)),minv2(W))
A2m=[[ONE,ONE],[ZERO,ONE]]; B2m=[[ONE,ZERO],[QQ,ONE]]
e2=[[ZERO,ONE],[ZERO,ZERO]]; f2=[[ZERO,ZERO],[ONE,ZERO]]; h2=[[ONE,ZERO],[ZERO,fneg(ONE)]]
def beat_lie(x): return mm2(mm2(W,mbar2(x)),minv2(W))
be=beat_lie(e2); bh=beat_lie(h2); bf=beat_lie(f2)
exp_h=[[ONE,fneg(fadd(QQ,QQ))],[ZERO,fneg(ONE)]]     # h - 2q e
q2=fmul(QQ,QQ)
exp_f=[[QQ,fneg(q2)],[ONE,fneg(QQ)]]                  # f + q h - q^2 e
print("2x2: beat(e)=e:", be==e2, "  beat(h)=h-2q e:", bh==exp_h, "  beat(f)=f+q h-q^2 e:", bf==exp_f)
print("2x2: beat(A)=A:", beat2(A2m)==A2m)

# ---------- part 2: e6 with Q(q) coefficients ----------
# represent X = X0 + q X1 as (X0, X1), X0/X1 rational DIM-vectors; brackets bilinear:
def br_pair(X,Y):
    X0,X1=X; Y0,Y1=Y
    a=br(X0,Y0); b=br(X0,Y1); c=br(X1,Y0); d=br(X1,Y1)
    # (X0+qX1)(Y0+qY1): q^2 = q-1  => rational part a - d ; q part b + c + d
    return ([ai-di for ai,di in zip(a,d)], [bi+ci+di for bi,ci,di in zip(b,c,d)])
def pair(v): return (v,[F(0)]*DIM)
def gal_pair(X):
    X0,X1=X
    return ([a+b for a,b in zip(X0,X1)], [-b for b in X1])
def padd(X,Y): return ([a+b for a,b in zip(X[0],Y[0])],[a+b for a,b in zip(X[1],Y[1])])
def psmul(c,X):  # c = field pair
    c0,c1=c
    return ([c0*a - c1*b for a,b in zip(X[0],X[1])],
            [c0*b + c1*a + c1*b for a,b in zip(X[0],X[1])])
def peq(X,Y): return X[0]==Y[0] and X[1]==Y[1]
qE=psmul(QQ,pair(e6e))
def exp_ad(t_vec,X,maxk=40):
    out=X; term=X; k=1
    while True:
        term=br_pair(t_vec,term)
        if all(x==0 for x in term[0]) and all(x==0 for x in term[1]): break
        term=psmul((F(1,k),F(0)),term)   # divide by k stepwise: term_k = ad^k/k!
        out=padd(out,term); k+=1
        assert k<=maxk
    return out
U =lambda X: exp_ad(qE,X)
E1=pair(e6e)
# checks on the principal sl2
lhs=U(pair(e6h)); rhs=padd(pair(e6h), psmul(fneg(fadd(QQ,QQ)),pair(e6e)))
print("e6: exp(ad qE) H = H - 2q E:", peq(lhs,rhs))
lhs=U(pair(e6f))
rhs=padd(padd(pair(e6f), psmul(QQ,pair(e6h))), psmul(fneg(q2),pair(e6e)))
print("e6: exp(ad qE) F = F + q H - q^2 E:", peq(lhs,rhs))
# Sigma and Sigma^2 = exp(ad E) on all 78 basis vectors
def Sigma(X): return U(gal_pair(X))
def expE(X): return exp_ad(pair(e6e),X)
basis=[pair([F(1) if j==i else F(0) for j in range(DIM)]) for i in range(DIM)]
ok=all(peq(Sigma(Sigma(b)), expE(b)) for b in basis)
print("e6: Sigma^2 = exp(ad E) = Ad(meridian) on ALL 78 basis vectors:", ok)
print("    (and exp(ad E) != identity, so Sigma is NOT an involution:",
      not all(peq(expE(b),b) for b in basis), ")")
# bracket-automorphism spot check (antilinear: Sigma[X,Y] = [Sigma X, Sigma Y])
random.seed(5); ok2=True
for _ in range(120):
    i,j=random.randrange(DIM),random.randrange(DIM)
    X,Y=basis[i],basis[j]
    if not peq(Sigma(br_pair(X,Y)), br_pair(Sigma(X),Sigma(Y))): ok2=False; break
print("e6: Sigma is a bracket-automorphism (120 random pairs):", ok2)

# ---------- part 3: the color slot under the beat ----------
# color I2 from the Levi-(0,2) landing (as in the banked construction)
A6=[[ccb.ip(tuple(1 if k==i else 0 for k in range(N)), tuple(1 if k==j else 0 for k in range(N))) for j in range(N)] for i in range(N)]
a0=tuple(1 if k==0 else 0 for k in range(N)); c2=tuple(1 if k==2 else 0 for k in range(N))
def iprr(a,b): return sum(a[i]*A6[i][j]*b[j] for i in range(N) for j in range(N))
orth=[r for r in ROOTS if iprr(r,a0)==0 and iprr(r,c2)==0]
comps=[]; left=set(orth)
while left:
    seed=next(iter(left)); comp={seed}; grew=True
    while grew:
        grew=False
        for r in list(left-comp):
            if any(iprr(r,s)!=0 for s in comp): comp.add(r); grew=True
    comps.append(comp); left-=comp
S1c,S2c=comps
I2=[pair(evec(r)) for r in sorted(S2c)]
def a2b(S):
    for r,s in itertools.permutations(S,2):
        t=tuple(r[k]+s[k] for k in range(N))
        if iprr(r,s)==-1 and t in S: return r,s
r2,s2=a2b(S2c)
for base in (r2,s2):
    h=[F(0)]*DIM
    for kk in range(N): h[kk]=F(base[kk])
    I2.append(pair(h))
# dim( U(I2) meet I2 ) over Q(q): stack [U(I2) | -I2] and count intersection
UI2=[U(v) for v in I2]
# solve: sum a_i U(v_i) = sum b_j v_j  -> nullspace of [U(I2), -I2] as 78 x 16 over field
cols=[]
for v in UI2: cols.append(v)
for v in I2: cols.append(( [-x for x in v[0]], [-x for x in v[1]] ))
Mfield=[[ (cols[c][0][row], cols[c][1][row]) for c in range(16)] for row in range(DIM)]
R,piv=rref(Mfield)
nullity=16-len(piv)
print(f"color slot: dim( exp(ad qE)(I2) meet I2 ) = {nullity}  (8 = preserved; <8 = the beat MOVES color)")
