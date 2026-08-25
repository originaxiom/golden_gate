#!/usr/bin/env python3
"""AW STABILIZER TYPING — B1111's residue (ii), executed on the stored 96.

Full census (B1111 sampled 25 pairs; here ALL transversal pairs):
 1. reproduce the per-element census {1:42, 3:53} (B1084) and the joint-dim census
    {0:1656, 1:2556, 3:253} (B1111) — two-bench cross-check;
 2. for ALL 1656 transversal pairs: the generated subgroup's order (full table);
 3. TYPE every order-24 subgroup that arises:
    - element-order histogram: 2T = SL(2,3) iff {1:1, 2:1, 3:8, 4:6, 6:8};
    - the ADE check: does it act on the H = R^4 block by LEFT quaternion
      multiplications (i.e. inside Sp(1) = SU(2))?  [that is the E6 McKay condition]
    - the R^3 action (through which rotation group) and H-fixed vectors on R^7.
All exact over Q(sqrt2) (fast pair arithmetic, converted once from the sympy build).
"""
import sympy as sp, itertools
from fractions import Fraction as F
exec(open(__import__('os').path.dirname(__import__('os').path.abspath(__file__))+'/g2strata.py').read().split("# ---------- S1/S2")[0])
# els: 96 sympy 7x7 matrices. Convert to Q(sqrt2) pairs (a, b) = a + b*sqrt2.
s2sym=sp.sqrt(2)
def conv_entry(x):
    x=sp.nsimplify(sp.expand(x))
    a=x.subs(s2sym,0)
    b=sp.expand((x-a)/s2sym)
    a=sp.Rational(a); b=sp.Rational(b)
    return (F(a.p,a.q), F(b.p,b.q))
def conv(M): return tuple(tuple(conv_entry(M[i,j]) for j in range(7)) for i in range(7))
G=[conv(M) for M in els]
def emul(u,v): return (u[0]*v[0]+2*u[1]*v[1], u[0]*v[1]+u[1]*v[0])
def eadd(u,v): return (u[0]+v[0], u[1]+v[1])
def mmul7(A,B):
    return tuple(tuple(
        (sum(A[i][k][0]*B[k][j][0]+2*A[i][k][1]*B[k][j][1] for k in range(7)),
         sum(A[i][k][0]*B[k][j][1]+A[i][k][1]*B[k][j][0] for k in range(7)))
        for j in range(7)) for i in range(7))
GI={g:i for i,g in enumerate(G)}
assert len(GI)==96
print("96 converted to exact Q(sqrt2); building multiplication table...")
MT=[[GI[mmul7(G[i],G[j])] for j in range(96)] for i in range(96)]
ident=G.index(tuple(tuple(((F(1) if i==j else F(0)),F(0)) for j in range(7)) for i in range(7)))
# element orders
def el_order(i):
    o=1; x=i
    while x!=ident:
        x=MT[x][i]; o+=1
    return o
orders=[el_order(i) for i in range(96)]
# fixed-space dims over Q(sqrt2)
def erref_rank(rows):
    M=[r[:] for r in rows]; nr=len(M); r=0
    for c in range(7):
        pr=next((i for i in range(r,nr) if M[i][c]!=(F(0),F(0))), None)
        if pr is None: continue
        M[r],M[pr]=M[pr],M[r]
        a,b=M[r][c]; n=a*a-2*b*b
        inv=(a/n, -b/n)
        M[r]=[emul(inv,x) for x in M[r]]
        for i in range(nr):
            if i!=r and M[i][c]!=(F(0),F(0)):
                f_=M[i][c]
                M[i]=[(x[0]-(f_[0]*y[0]+2*f_[1]*y[1]), x[1]-(f_[0]*y[1]+f_[1]*y[0])) for x,y in zip(M[i],M[r])]
        r+=1
    return r
def fixdim(idxs):
    rows=[]
    for gi in idxs:
        Mg=G[gi]
        for i in range(7):
            row=[(Mg[i][j][0]-(F(1) if i==j else F(0)), Mg[i][j][1]) for j in range(7)]
            if any(x!=(F(0),F(0)) for x in row): rows.append(row)
    return 7-erref_rank(rows)
from collections import Counter
nontrivial=[i for i in range(96) if i!=ident]
census=Counter(fixdim([i]) for i in nontrivial)
print("per-element fixed dims:", dict(census), "(B1084: {1:42, 3:53})")
pairs=list(itertools.combinations(nontrivial,2))
jd={}
for p in pairs: jd[p]=fixdim(list(p))
jc=Counter(jd.values())
print("joint fixed dims over all pairs:", dict(jc), "(B1111: {0:1656, 1:2556, 3:253})")
trans=[p for p in pairs if jd[p]==0]
# generated subgroups (full census, not a sample)
def gen_sub(p):
    S={ident, p[0], p[1]}
    frontier=[p[0],p[1]]
    while frontier:
        nf=[]
        for x in frontier:
            for g in (p[0],p[1]):
                for y in (MT[x][g], MT[g][x]):
                    if y not in S: S.add(y); nf.append(y)
        frontier=nf
    return frozenset(S)
subs=Counter(); sub24=set()
for p in trans:
    Sg=gen_sub(p)
    subs[len(Sg)]+=1
    if len(Sg)==24: sub24.add(Sg)
print(f"generated-subgroup orders over ALL {len(trans)} transversal pairs:", dict(subs))
print(f"distinct order-24 subgroups arising: {len(sub24)}")
# type each order-24 subgroup
def is_left_quat(Mg):
    """4x4 lower block commutes with all right-multiplications <=> left multiplication."""
    blk=[[Mg[i][j] for j in range(3,7)] for i in range(3,7)]
    for q in ((0,1,0,0),(0,0,1,0),(0,0,0,1)):
        R=qmat_right(q)
        Rc=[[conv_entry(R[i,j]) for j in range(4)] for i in range(4)]
        for i in range(4):
            for j in range(4):
                lhs=(sum(blk[i][k][0]*Rc[k][j][0]+2*blk[i][k][1]*Rc[k][j][1] for k in range(4)),
                     sum(blk[i][k][0]*Rc[k][j][1]+blk[i][k][1]*Rc[k][j][0] for k in range(4)))
                rhs=(sum(Rc[i][k][0]*blk[k][j][0]+2*Rc[i][k][1]*blk[k][j][1] for k in range(4)),
                     sum(Rc[i][k][0]*blk[k][j][1]+Rc[i][k][1]*blk[k][j][0] for k in range(4)))
                if lhs!=rhs: return False
    return True
for si,Sg in enumerate(sorted(sub24, key=lambda s: sorted(s))):
    hist=Counter(orders[i] for i in Sg)
    is2T = dict(hist)=={1:1,2:1,3:8,4:6,6:8}
    left=all(is_left_quat(G[i]) for i in Sg)
    fdH=fixdim([i for i in Sg if i!=ident])
    # R3 action: kernel of the R3 block
    r3triv=sum(1 for i in Sg if all(G[i][a][b]==((F(1) if a==b else F(0)),F(0)) for a in range(3) for b in range(3)))
    print(f"order-24 subgroup #{si+1}: element orders {dict(hist)}  2T=SL(2,3): {is2T}  "
          f"acts on H by LEFT unit quaternions (SU(2)/McKay-E6 condition): {left}  "
          f"H-fixed vectors on R^7: {fdH}  |kernel of R^3 action|: {r3triv}")
