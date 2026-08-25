#!/usr/bin/env python3
"""THE PRICE OF SPACETIME — the D5 fork as a centralizer theorem, and the S3 frame torsor.

Claims to verify (all exact over Q):
 1. THE LADDER 16 -> 8 -> 0:
    dim z(T1)                     = 16   (one triple spent: sl(S1)+sl(S2) room)
    dim z(T1 u sl(S2))            = 8    (color also spent: sl(S1) room — the EW branch,
                                          rank-2 Cartan = exactly where B1102's 18 live)
    dim z(T1, T2)                 = 8    (both triples spent, color free — B1114's number)
    dim z(T1, T2, sl(S2))         = 0    (Lorentz glued AND color: NOTHING LEFT —
                                          no hypercharge direction exists in all of e6)
 2. THE S3 FRAME TORSOR: W(E6) contains involutions realizing ALL THREE transpositions
    of {S0,S1,S2} (each fixing the third setwise) and a 3-cycle — the object does not
    distinguish the three A2's; 'which is color' is a frame choice.
 3. B1118's hypercharge-fusing swap (3,2,1,0) on coords [p1(S1'),p2(S2')] is the
    transposition S1'<->S2' of the two orthogonal A2's — i.e. P is a transposition of
    the same S3 (structural, by construction of the coordinates; asserted here).
"""
import importlib.util, itertools
from fractions import Fraction as F

spec = importlib.util.spec_from_file_location("ccb",
  __import__('os').path.dirname(__import__('os').path.abspath(__file__))+"/paper/verify/check_charge_bracket.py")
ccb = importlib.util.module_from_spec(spec); spec.loader.exec_module(ccb)
br, add_, smul_, is_zero = ccb.br, ccb.add, ccb.smul, ccb.is_zero
evec, hvec, eps, ip = ccb.evec, ccb.hvec, ccb.eps, ccb.ip
ROOTS, IDX, N, DIM = ccb.ROOTS, ccb.IDX, ccb.N, ccb.DIM

def frac_rref(M):
    M=[row[:] for row in M]; rows=len(M); cols=len(M[0]) if rows else 0
    piv=[]; r=0
    for c in range(cols):
        pr=next((i for i in range(r,rows) if M[i][c]!=0), None)
        if pr is None: continue
        M[r],M[pr]=M[pr],M[r]
        inv=F(1)/M[r][c]; M[r]=[inv*x for x in M[r]]
        for i in range(rows):
            if i!=r and M[i][c]!=0:
                f_=M[i][c]; M[i]=[x-f_*y for x,y in zip(M[i],M[r])]
        piv.append(c); r+=1
        if r==rows: break
    return M,piv
def rank(M): return len(frac_rref(M)[1])

a0=tuple(1 if k==0 else 0 for k in range(N)); a2=tuple(1 if k==2 else 0 for k in range(N))
S0={r for r in ROOTS if r in {tuple(c1*a0[k]+c2*a2[k] for k in range(N)) for c1 in (-1,0,1) for c2 in (-1,0,1)}}
Rperp=[r for r in ROOTS if ip(r,a0)==0 and ip(r,a2)==0]
comps=[]; left=set(Rperp)
while left:
    seed=next(iter(left)); comp={seed}; grew=True
    while grew:
        grew=False
        for r in list(left-comp):
            if any(ip(r,s)!=0 for s in comp): comp.add(r); grew=True
    comps.append(comp); left-=comp
S1,S2=comps

def a2_base(S):
    for r,s in itertools.permutations(S,2):
        t=tuple(r[k]+s[k] for k in range(N))
        if ip(r,s)==-1 and t in S: return r,s
    raise RuntimeError
def principal_triple(S):
    r,s=a2_base(S)
    e=add_(evec(r),evec(s))
    h=add_(smul_(2,[F(x) for x in list(r)+[0]*72]), smul_(2,[F(x) for x in list(s)+[0]*72]))
    f=add_(smul_(-2,evec(tuple(-x for x in r))), smul_(-2,evec(tuple(-x for x in s))))
    assert br(e,f)==h
    return [e,h,f]
T1=principal_triple(S0); T2=principal_triple(S1)
r2,s2=a2_base(S2)
COLOR=[evec(r) for r in sorted(S2)]+[[F(x) for x in list(r2)+[0]*72],[F(x) for x in list(s2)+[0]*72]]

def centralizer_dim(gens):
    """dim {X in e6 : [X,g]=0 for all g} — stack ad(g) rows, X as unknown column."""
    rows=[]
    basis=[hvec(i) for i in range(N)]+[evec(r) for r in ROOTS]
    for g in gens:
        # [X,g] = 0: for X = sum x_j b_j: sum x_j [b_j, g] = 0 — build matrix cols = j
        colvecs=[br(b,g) for b in basis]
        for comp in range(DIM):
            row=[colvecs[j][comp] for j in range(DIM)]
            if any(x!=0 for x in row): rows.append(row)
    return DIM - rank(rows)

d1=centralizer_dim(T1)
d2=centralizer_dim(T1+COLOR)
d3=centralizer_dim(T1+T2)
d4=centralizer_dim(T1+T2+COLOR)
print(f"dim z(T1)               = {d1}  (expect 16: one triple spent)")
print(f"dim z(T1 u color)       = {d2}  (expect 8: EW branch — sl(S1) room, rank-2 Cartan for Y)")
print(f"dim z(T1,T2)            = {d3}  (expect 8 = B1114: color exactly)")
print(f"dim z(T1,T2 u color)    = {d4}  (expect 0: Lorentz+color leaves NOTHING for hypercharge)")
assert (d1,d2,d3,d4)==(16,8,8,0), "LADDER FAILS"
print("THE LADDER 16 -> 8 -> 0: PASS — the fork is a centralizer theorem\n")

# S3 frame torsor
root_list=ROOTS; nR=len(root_list)
def srefl(i):
    ai=tuple(1 if k==i else 0 for k in range(N))
    return tuple(IDX[tuple(r[k]-ip(r,ai)*ai[k] for k in range(N))] for r in root_list)
gens=[srefl(i) for i in range(N)]
ident=tuple(range(nR))
seen={ident}; frontier=[ident]; W=[ident]
while frontier:
    nf=[]
    for p in frontier:
        for g in gens:
            q=tuple(p[g[i]] for i in range(nR))
            if q not in seen: seen.add(q); nf.append(q); W.append(q)
    frontier=nf
iS=[frozenset(IDX[r] for r in S) for S in (S0,S1,S2)]
def image(p,fs): return frozenset(p[i] for i in fs)
def action(p):
    im=[image(p,fs) for fs in iS]
    if any(x not in iS for x in im): return None
    return tuple(iS.index(x) for x in im)
from collections import Counter
acts=Counter()
for p in W:
    a=action(p)
    if a is not None: acts[a]+=1
print("S3 actions realized by W(E6) on the three A2's {S0,S1,S2}:")
for a,c in sorted(acts.items()): print(f"   {a}: {c} elements")
need={(1,0,2),(2,1,0),(0,2,1),(1,2,0),(2,0,1)}
assert need <= set(acts), "S3 not fully realized"
print("ALL THREE transpositions + both 3-cycles realized inside W(E6): PASS")
print("=> the three A2's are one W-orbit of frames; 'which factor is color' is a frame choice\n")

# B1118's fusing swap is the S1<->S2 transposition (coordinate identity):
# hyper_orbits built coords [p1(0),p1(1),p2(0),p2(1)] from the two orthogonal components
# and found the SOLUTION-PRESERVING swap (3,2,1,0): y -> (y3,y2,y1,y0) — it exchanges the
# p1-block with the p2-block, i.e. exchanges the two orthogonal A2's (with internal
# reversal, an inner Weyl move of each A2). Structural, no computation needed:
print("B1118's fusing swap (3,2,1,0) exchanges the p1-block and p2-block of the")
print("hypercharge Cartan coordinates = the transposition of the two orthogonal A2's.")
print("The simultaneous-closing swap is the S0<->S1 transposition. Same S3 conjugacy class.")
