#!/usr/bin/env python3
"""THE 64 ORGANIZED — B1134's relayed value target, decomposed exactly.

On a memo-10/B1134 hit sigma (the spacetime closing, E6(-26)): the fixed form holds
so(3,1) [6] + su(3)c [8] + a 64. Decompose the complex 64-complement of
sl2(T1) + sl2(theta T1) + sl3(color) in e6 under (h1, h2, color):
  PREDICTION (declared): 64 = (spin2,0;1) + (0,spin2;1) + (1,1;3) + (1,1;3bar),
  with ZERO color-singlet (0,0)-weight outside the algebra — i.e. NO room where a
  hypercharge u(1) could organize (the rep-side refinement of memo 11's z=0).
Then verify sigma glues the two spin-2 pieces (theta swaps their spans) — the
sigma-real 64 = one COMPLEX spin-2 [10] + the colored bi-vector [54].
"""
import importlib.util, itertools, random
from fractions import Fraction as F
SCR=__import__('os').path.dirname(__import__('os').path.abspath(__file__))+""
exec(open(SCR+'/simul_verify.py').read().split("# principal triple of S0")[0])
# machinery loaded: e6 (ccb), slots S0/S1/S2, G_swap, solve_lift, theta_matrix, apply,
# frac_nullspace, gform...
def a2b(S):
    for r,s in itertools.permutations(S,2):
        t=tuple(r[k]+s[k] for k in range(N))
        if ip(r,s)==-1 and t in S: return r,s
def principal_triple(S):
    r,s=a2b(S)
    e=add_(evec(r),evec(s))
    h=[F(0)]*DIM
    for k in range(N): h[k]=F(2*(r[k]+s[k]))
    f=add_(smul_(-2,evec(tuple(-x for x in r))), smul_(-2,evec(tuple(-x for x in s))))
    assert br(e,f)==h
    return [e,h,f]
T1=principal_triple(S0)
# find the first hit (as in memo 10 verification)
hit=None
for gi,g in enumerate(G_swap):
    for c in solve_lift(g):
        if color_sig(g,c)==(0,8): hit=(g,c); break
    if hit: break
g,c=hit
T=theta_matrix(g,c)
h1=T1[1]; h2=apply(T,h1)
# both in Cartan
assert all(h1[N+i]==0 for i in range(len(ROOTS))) and all(h2[N+i]==0 for i in range(len(ROOTS)))
def pair_with(h, r):  # eigenvalue of ad h on e_r
    v=br(h,evec(r))
    return v[N+IDX[r]]
# color Cartan: the two coroots of S2
r2,s2=a2b(S2)
def col_wt(r): return (ip(r,r2), ip(r,s2))
# weight table over the 78 basis dirs
from collections import Counter
S0i={IDX[r] for r in S0}; S1i={IDX[r] for r in S1}; S2i={IDX[r] for r in S2}
table=Counter()
alg_dims=0
# the algebra part: sl2(T1) in sl3(S0), sl2(thetaT1) in sl3(S1), sl3(S2)
# we work at complex level: complement = e6 minus (sl2 + sl2 + sl3c) = 64
# decompose the FULL 78 by (h1,h2) weights and color content, then subtract algebra content.
full=Counter()
for r in ROOTS:
    a=pair_with(h1,r); b=pair_with(h2,r)
    iscol = IDX[r] in S2i
    colored = (col_wt(r)!=(0,0)) and not iscol
    full[(a,b,'S2root' if iscol else ('col' if colored else 'neutral'))]+=1
full[(0,0,'cartan')]=6
print("hit found: swapper#%d; h2 = theta(h1) in Cartan OK"%gi)
print("full weight table (a,b,type):")
for k,v in sorted(full.items(), key=lambda kv:(str(kv[0]))): print("  ",k,":",v)
# algebra content to subtract: sl2_1: (±2,0)+1 Cartan dir; sl2_2: (0,±2)+1; sl3(S2): 6 roots (0,0)+2 Cartan
# complement = everything else. Identify rep content:
comp=Counter()
for (a,b,t),v in full.items():
    comp[(a,b,t)]=v
comp[(2,0,'neutral')]-=1; comp[(-2,0,'neutral')]-=1
comp[(0,2,'neutral')]-=1; comp[(0,-2,'neutral')]-=1
comp[(0,0,'S2root')]=comp.get((0,0,'S2root'),0)  # S2 roots all have (a,b)=(0,0)? check:
s2ab={(pair_with(h1,r),pair_with(h2,r)) for r in S2}
print("S2 root (h1,h2) weights:", s2ab, "(expect {(0,0)})")
comp[(0,0,'cartan')]-=4   # 1+1+2 Cartan dirs of the algebra... sl2s use h1,h2; sl3c uses 2
# remove S2 roots (color algebra)
for k in list(comp):
    if k[2]=='S2root': del comp[k]
total=sum(v for v in comp.values() if v>0)
print("complement dimension:", total, "(expect 64)")
print("complement weight table:")
sing=0
for k,v in sorted(comp.items(), key=lambda kv:str(kv[0])):
    if v>0:
        print("  ",k,":",v)
        if k[0]==0 and k[1]==0 and k[2] in ('neutral','cartan'): sing+=v
print("color-singlet (0,0) content in the complement:", sing, "(0 = NO hypercharge room; matches memo 11)")
# spin-2 pieces: neutral weights (±4,0),(±2,0),(0,0)? and (0,±4) etc:
# verify theta swaps the two spin-2 spans: the S0-side spin-2 span = weight vectors in sl3(S0) beyond sl2:
# take the 5-dim: root vectors of S0 give 6 roots + 2 cartan = 8 = 3+5; top of 5 = weight (4,0):
top1=[r for r in ROOTS if IDX[r] in S0i and pair_with(h1,r)==4]
top2=[r for r in ROOTS if IDX[r] in S1i and pair_with(h2,r)==4]
print("spin-2 tops: S0-side weight-(4,0) roots:", len(top1), "; S1-side (0,4):", len(top2))
img=apply(T, evec(top1[0]))
in_S1=all(img[i]==0 for i in range(DIM) if not (i>=N and (ROOTS[i-N] in S1)) and not i<N)
print("theta maps S0 spin-2 top into sl3(S1) span:", in_S1, "-> sigma glues the two spin-2s into ONE complex spin-2 (real dim 10)")
