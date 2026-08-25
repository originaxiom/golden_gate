#!/usr/bin/env python3
"""EXHAUSTIVE sweep for the simultaneous closing.

Fact (verified in simul_closing.py): for ANY root-map g swapping S0<->S1 (fixing S2
setwise), sigma = tau.theta_g swaps the two commuting sl2 triples, so the double's
fixed real algebra is sl(2,C)_R = so(3,1) — automatically.  The only question left,
per involutive swapper g and per involutive sign solution, is the COLOR signature.

Sweep: ALL involutions g in Aut(Phi(E6)) = W union deltaW with g(S0)=S1, g(S1)=S0,
g(S2)=S2; all involutive sign lifts of each; compute the color-slot signature of
sigma = tau.theta.  A (0,8) anywhere = SIMULTANEOUS CLOSING EXISTS.  None = NO-GO.
"""
import importlib.util, itertools, random
from fractions import Fraction as F

spec = importlib.util.spec_from_file_location("ccb",
  __import__('os').path.dirname(__import__('os').path.abspath(__file__))+"/paper/verify/check_charge_bracket.py")
ccb = importlib.util.module_from_spec(spec); spec.loader.exec_module(ccb)
br, add_, smul_, is_zero = ccb.br, ccb.add, ccb.smul, ccb.is_zero
evec, hvec, eps, ip = ccb.evec, ccb.hvec, ccb.eps, ccb.ip
ROOTS, IDX, N, DIM = ccb.ROOTS, ccb.IDX, ccb.N, ccb.DIM
A = [[ip(tuple(1 if k==i else 0 for k in range(N)), tuple(1 if k==j else 0 for k in range(N)))
      for j in range(N)] for i in range(N)]

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
def frac_nullspace(M):
    R,piv=frac_rref(M); cols=len(M[0])
    free=[c for c in range(cols) if c not in piv]; out=[]
    for fc in free:
        v=[F(0)]*cols; v[fc]=F(1)
        for i,c in enumerate(piv): v[c]=-R[i][fc]
        out.append(v)
    return out
def sig_of_sym(M):
    M=[row[:] for row in M]; n=len(M); p=neg=z=0
    i=0
    while i<n:
        if M[i][i]==0:
            j=next((j for j in range(i+1,n) if M[j][i]!=0), None)
            if j is None: z+=1; i+=1; continue
            for k in range(n): M[i][k]+=M[j][k]
            for k in range(n): M[k][i]+=M[k][j]
        d=M[i][i]
        if d>0: p+=1
        else: neg+=1
        for j in range(i+1,n):
            if M[j][i]!=0:
                f_=M[j][i]/d
                for k in range(n): M[j][k]-=f_*M[i][k]
                for k in range(n): M[k][j]-=f_*M[k][i]
        i+=1
    return p,neg,z

G=[[F(0)]*DIM for _ in range(DIM)]
for i in range(N):
    for j in range(N): G[i][j]=F(A[i][j])
for k,r in enumerate(ROOTS):
    G[N+k][N+IDX[tuple(-x for x in r)]]=F(-1)
def gform(u,v):
    s=F(0)
    for i,ui in enumerate(u):
        if ui:
            Gi=G[i]
            for j,vj in enumerate(v):
                if vj and Gi[j]: s+=ui*vj*Gi[j]
    return s

# slots
a0=tuple(1 if k==0 else 0 for k in range(N)); a2=tuple(1 if k==2 else 0 for k in range(N))
S0={r for r in ROOTS if all(any(r==tuple(c1*a0[k]+c2*a2[k] for k in range(N)) for c1 in (-1,0,1) for c2 in (-1,0,1)) for _ in [0])}
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
assert len(S0)==6 and len(S1)==6 and len(S2)==6

# Aut(Phi) = W union delta.W
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
            if q not in seen:
                seen.add(q); nf.append(q); W.append(q)
    frontier=nf
assert len(W)==51840
# diagram flip
pi=None
for perm in itertools.permutations(range(N)):
    if perm!=tuple(range(N)) and all(A[perm[i]][perm[j]]==A[i][j] for i in range(N) for j in range(N)):
        pi=perm; break
assert pi is not None
def flip_root(r):
    out=[0]*N
    for i in range(N): out[pi[i]]+=r[i]
    return tuple(out)
delta=tuple(IDX[flip_root(r)] for r in root_list)
assert delta not in seen, "delta must be outer"
def compose(p,q): return tuple(p[q[i]] for i in range(nR))
AUT = W + [compose(delta,w) for w in W]

i0=frozenset(IDX[r] for r in S0); i1=frozenset(IDX[r] for r in S1); i2=frozenset(IDX[r] for r in S2)
def image(p,fs): return frozenset(p[i] for i in fs)
G_swap=[g for g in AUT if image(g,i0)==i1 and image(g,i1)==i0 and image(g,i2)==i2
        and compose(g,g)==ident]
inW=sum(1 for g in G_swap if g in seen)
print(f"involutive swappers: {len(G_swap)} total ({inW} in W, {len(G_swap)-inW} in deltaW)")

# sign-lift solver (fixed ascending back-substitution + per-solution row check)
def solve_lift(phi):
    NEG=tuple(IDX[tuple(-x for x in r)] for r in root_list)
    rows=[]
    def addrow(idxs,rhs):
        m=0
        for i in idxs: m^=(1<<i)
        rows.append((m,rhs))
    for ia,ra in enumerate(root_list):
        addrow([ia,NEG[ia]],0)
        addrow([ia,phi[ia]],0)
        for ib in range(ia+1,nR):
            rb=root_list[ib]
            s=tuple(ra[k]+rb[k] for k in range(N))
            if s in IDX:
                ratio=eps(ra,rb)*eps(root_list[phi[ia]],root_list[phi[ib]])
                addrow([ia,ib,IDX[s]],0 if ratio==1 else 1)
    pivots={}
    for m,rhs in rows:
        while m:
            hb=m.bit_length()-1
            if hb in pivots:
                pm,pr=pivots[hb]; m^=pm; rhs^=pr
            else:
                pivots[hb]=(m,rhs); break
        else:
            if rhs: return []
    sol=0
    for hb in sorted(pivots):
        pm,pr=pivots[hb]
        if pr ^ (bin((pm ^ (1<<hb)) & sol).count('1')%2): sol|=(1<<hb)
    freev=[i for i in range(nR) if i not in pivots]
    kern=[]
    for fv in freev:
        k=1<<fv
        for hb in sorted(pivots):
            pm,_=pivots[hb]
            if bin((pm ^ (1<<hb)) & k).count('1')%2: k|=(1<<hb)
        kern.append(k)
    sols=[]
    for bits in range(1<<len(kern)):
        x=sol
        for j in range(len(kern)):
            if bits>>j & 1: x^=kern[j]
        for m,rhs in rows:
            assert bin(m & x).count('1')%2 == rhs
        sols.append([1-2*((x>>i)&1) for i in range(nR)])
    return sols

# color-slot machinery (8-dim): basis = 6 root vectors of S2 + 2 coroots
def a2_base(S):
    for r,s in itertools.permutations(S,2):
        t=tuple(r[k]+s[k] for k in range(N))
        if ip(r,s)==-1 and t in S: return r,s
    raise RuntimeError
r2,s2=a2_base(S2)
S2list=sorted(S2)
cb=[evec(r) for r in S2list]+[[F(x) for x in list(r2)+[0]*72],[F(x) for x in list(s2)+[0]*72]]
cols=[[cb[j][i] for j in range(8)] for i in range(DIM)]
def coords(v):
    Mm=[cols[i]+[v[i]] for i in range(DIM)]
    R,piv=frac_rref(Mm)
    assert 8 not in piv, "vector escaped the color slot"
    out=[F(0)]*8
    for irow,cc in enumerate(piv):
        out[cc]=R[irow][8]
    return out
def theta_apply_basisvec(phi,c,bv):
    """theta on a color-basis vector, using theta(e_r)=c_r e_{phi r}, theta(h_r)=h_{phi r}."""
    out=[F(0)]*DIM
    for i,x in enumerate(bv):
        if not x: continue
        if i<N:
            # h_i -> h_{phi(alpha_i)}: phi acts linearly; alpha_i image root coords
            pr=root_list[phi[IDX[tuple(1 if k==i else 0 for k in range(N))]]]
            for j in range(N): out[j]+=x*F(pr[j])
        else:
            out[N+phi[i-N]]+=x*F(c[i-N])
    return out
def color_sig(phi,c):
    Tc=[[F(0)]*8 for _ in range(8)]
    for j in range(8):
        cj=coords(theta_apply_basisvec(phi,c,cb[j]))
        for i in range(8): Tc[i][j]=cj[i]
    Fx=[[Tc[i][j]-(F(1) if i==j else F(0)) for j in range(8)] for i in range(8)]
    Ax=[[Tc[i][j]+(F(1) if i==j else F(0)) for j in range(8)] for i in range(8)]
    fb=frac_nullspace(Fx); ab=frac_nullspace(Ax)
    tofull=lambda coef: [sum(cb[j][i]*coef[j] for j in range(8)) for i in range(DIM)]
    fbv=[tofull(v) for v in fb]; abv=[tofull(v) for v in ab]
    p1,n1,z1=sig_of_sym([[gform(u,v) for v in fbv] for u in fbv])
    p2,n2,z2=sig_of_sym([[-gform(u,v) for v in abv] for u in abv])
    assert z1==0 and z2==0
    return (p1+p2, n1+n2)

# spot automorphism guard per swapper (first solution)
basis=[hvec(i) for i in range(N)]+[evec(r) for r in ROOTS]
random.seed(11)
def spot_aut(phi,c,ntrials=40):
    T=[[F(0)]*DIM for _ in range(DIM)]
    for i in range(N):
        pr=root_list[phi[IDX[tuple(1 if k==i else 0 for k in range(N))]]]
        for j in range(N): T[j][i]=F(pr[j])
    for ir in range(nR): T[N+phi[ir]][N+ir]=F(c[ir])
    def ap(v): return [sum(T[i][j]*v[j] for j in range(DIM) if v[j]) for i in range(DIM)]
    for _ in range(ntrials):
        x,y=random.choice(basis),random.choice(basis)
        if ap(br(x,y))!=br(ap(x),ap(y)): return False
    return True

from collections import Counter
tally=Counter(); hits=[]
nolift=0
for gi,g in enumerate(G_swap):
    sols=solve_lift(g)
    if not sols:
        nolift+=1; continue
    assert spot_aut(g,sols[0]), f"swapper {gi}: lift is not an automorphism"
    for c in sols:
        cs=color_sig(g,c)
        tally[cs]+=1
        if cs==(0,8): hits.append((gi,g,c))
print(f"swappers with no involutive lift: {nolift}/{len(G_swap)}")
print("color signatures over ALL (swapper, sign-solution) pairs:", dict(tally))
print(f"\nSIMULTANEOUS CLOSING (so(3,1) + compact color (0,8)): {len(hits)} hits")
if hits:
    print(">>> EXISTS — first hit at swapper", hits[0][0])
else:
    print(">>> NO-GO: no lattice-compatible conjugation buys Lorentz signature and "
          "compact color simultaneously — exhaustive over all involutive swappers in "
          "Aut(Phi) = W u deltaW and all involutive sign lifts.")
