#!/usr/bin/env python3
"""F-1: THE EW REAL FORM — the complete slot-signature menu of the trinification frame.

Sweep ALL factor-preserving involutions g in Aut(Phi(E6)) = W u deltaW
(g(S_i) = S_i setwise for i = 0,1,2; g^2 = id) x ALL involutive sign lifts.
For each sigma = tau.theta record (sig S0, sig S1, sig S2, global char).
Answers: which real forms can the EW room sl(S1) take, correlated with compact
color on sl(S2) and with the global form.  Key readings of an 8-dim slot sig:
(0,8) su(3) compact · (4,4) su(2,1) [max compact u(2); coset = complex doublet]
· (5,3) sl(3,R) [max compact so(3): CANNOT host su(2)+u(1)] · (8,0) impossible-compact.
"""
import importlib.util, itertools, random
from fractions import Fraction as F
from collections import Counter

spec = importlib.util.spec_from_file_location("ccb",
  "/tmp/claude-0/-home-user-golden-gate/7aec077f-59a6-5129-b1a7-361cc5dcb800/scratchpad/paper/verify/check_charge_bracket.py")
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
SLOTS=[sorted(S0),sorted(S1),sorted(S2)]

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
pi=None
for perm in itertools.permutations(range(N)):
    if perm!=tuple(range(N)) and all(A[perm[i]][perm[j]]==A[i][j] for i in range(N) for j in range(N)):
        pi=perm; break
def flip_root(r):
    out=[0]*N
    for i in range(N): out[pi[i]]+=r[i]
    return tuple(out)
delta=tuple(IDX[flip_root(r)] for r in root_list)
def compose(p,q): return tuple(p[q[i]] for i in range(nR))
AUT = W + [compose(delta,w) for w in W]
iS=[frozenset(IDX[r] for r in S) for S in (S0,S1,S2)]
def image(p,fs): return frozenset(p[i] for i in fs)
FP=[g for g in AUT if all(image(g,fs)==fs for fs in iS) and compose(g,g)==ident]
print(f"factor-preserving involutions in Aut(Phi): {len(FP)} "
      f"({sum(1 for g in FP if g in seen)} in W, {sum(1 for g in FP if g not in seen)} in deltaW)")

NEG=tuple(IDX[tuple(-x for x in r)] for r in root_list)
def solve_lift(phi):
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

# fast eigen-split of theta on any set of root indices + a Cartan subspace
def cartan_map(phi):
    P6=[[F(0)]*N for _ in range(N)]
    for i in range(N):
        pr=root_list[phi[IDX[tuple(1 if k==i else 0 for k in range(N))]]]
        for j in range(N): P6[j][i]=F(pr[j])
    return P6
def eig_split_roots(phi,c,ridx_set):
    """Fix/AntiFix bases (as DIM-vectors) of theta on span{e_r : r in set}."""
    fix=[]; anti=[]; done=set()
    for irt in ridx_set:
        if irt in done: continue
        j=phi[irt]
        if j==irt:
            (fix if c[irt]==1 else anti).append(evec(root_list[irt]))
            done.add(irt)
        else:
            assert j in ridx_set
            v1=evec(root_list[irt]); v2=evec(root_list[j])
            fp=[a+F(c[irt])*b for a,b in zip(v1,v2)]
            ap=[a-F(c[irt])*b for a,b in zip(v1,v2)]
            fix.append(fp); anti.append(ap); done.add(irt); done.add(j)
    return fix,anti
def eig_split_cartan(phi,coords_basis):
    """coords_basis: list of 6-coord Cartan vectors spanning a phi-stable subspace."""
    P6=cartan_map(phi)
    imgs=[[sum(P6[i][j]*v[j] for j in range(N)) for i in range(N)] for v in coords_basis]
    # express images in the given basis: solve small system
    k=len(coords_basis)
    Mm=[[coords_basis[j][i] for j in range(k)] for i in range(N)]
    def coords(v):
        R,piv=frac_rref([Mm[i]+[v[i]] for i in range(N)])
        out=[F(0)]*k
        for irow,cc in enumerate(piv):
            assert cc<k
            out[cc]=R[irow][k]
        return out
    T=[[F(0)]*k for _ in range(k)]
    for j in range(k):
        cj=coords(imgs[j])
        for i in range(k): T[i][j]=cj[i]
    fixc=frac_nullspace([[T[i][j]-(F(1) if i==j else F(0)) for j in range(k)] for i in range(k)])
    antic=frac_nullspace([[T[i][j]+(F(1) if i==j else F(0)) for j in range(k)] for i in range(k)])
    tofull=lambda coef: [F(0)]*0 or [sum(coords_basis[j][i]*coef[j] for j in range(k)) for i in range(N)]
    pad=lambda h6: [x for x in h6]+[F(0)]*(DIM-N)
    return [pad(tofull(v)) for v in fixc],[pad(tofull(v)) for v in antic]
def sig_from_bases(fix,anti):
    p1,n1,z1=sig_of_sym([[gform(u,v) for v in fix] for u in fix]) if fix else (0,0,0)
    p2,n2,z2=sig_of_sym([[-gform(u,v) for v in anti] for u in anti]) if anti else (0,0,0)
    assert z1==0 and z2==0
    return (p1+p2, n1+n2)

def slot_bases(phi,c,slot):
    ridx=[IDX[r] for r in slot]
    fx,ax=eig_split_roots(phi,c,set(ridx))
    # slot Cartan: coroot coords of two base roots
    def a2_base(S):
        for r,s in itertools.permutations(S,2):
            t=tuple(r[k]+s[k] for k in range(N))
            if ip(r,s)==-1 and t in S: return r,s
        raise RuntimeError
    r1,s1=a2_base(set(slot))
    fc,ac=eig_split_cartan(phi,[[F(x) for x in r1],[F(x) for x in s1]])
    return fx+fc, ax+ac

random.seed(31)
basis=[hvec(i) for i in range(N)]+[evec(r) for r in ROOTS]
def spot_aut(phi,c,ntrials=30):
    T=[[F(0)]*DIM for _ in range(DIM)]
    P6=cartan_map(phi)
    for i in range(N):
        for j in range(N): T[j][i]=P6[j][i]
    for ir in range(nR): T[N+phi[ir]][N+ir]=F(c[ir])
    def ap(v): return [sum(T[i][j]*v[j] for j in range(DIM) if v[j]) for i in range(DIM)]
    for _ in range(ntrials):
        x,y=random.choice(basis),random.choice(basis)
        if ap(br(x,y))!=br(ap(x),ap(y)): return False
    return True

menu=Counter(); examples={}
tot=0
simple6=[[F(1) if k==i else F(0) for k in range(N)] for i in range(N)]
for gi,g in enumerate(FP):
    sols=solve_lift(g)
    if not sols: continue
    assert spot_aut(g,sols[0]), f"FP #{gi}: bad lift"
    for c in sols:
        tot+=1
        sigs=[]
        allfix=[]; allanti=[]
        for slot in SLOTS:
            fx,ax=slot_bases(g,c,slot)
            sigs.append(sig_from_bases(fx,ax))
        # global: all 72 roots + full Cartan
        fx,ax=eig_split_roots(g,c,set(range(nR)))
        fc,ac=eig_split_cartan(g,simple6)
        gp,gn=sig_from_bases(fx+fc,ax+ac)
        char=gp-gn
        key=(tuple(sigs),char)
        menu[key]+=1
        if key not in examples:
            coset="W" if g in seen else "dW"
            examples[key]=coset
print(f"total (involution, sign-solution) pairs: {tot}")
FORM={-78:"E6c",-26:"E6(-26)",-14:"E6(-14)",2:"E6(2)",6:"E6(6)"}
NAME={(0,8):"su(3)",(4,4):"su(2,1)",(5,3):"sl(3,R)",(8,0):"IMPOSSIBLE"}
print("\nTHE MENU  (sig S0 | sig S1 | sig S2 | global char) : count [coset of first example]")
for (sigs,char),cnt in sorted(menu.items(), key=lambda kv:(-kv[1],kv[0][1])):
    lbl=" | ".join(f"{s}={NAME.get(s,'?')}" for s in sigs)
    print(f"  {lbl} | char {char:+d} [{FORM.get(char,'?')}] : {cnt}  [{examples[(sigs,char)]}]")
print("\nROWS WITH COMPACT COLOR (S2=(0,8)) — the EW options coexisting with compact color:")
ew=Counter()
for (sigs,char),cnt in menu.items():
    if sigs[2]==(0,8): ew[(sigs[0],sigs[1],char)]+=cnt
for (s0,s1,char),cnt in sorted(ew.items()):
    print(f"  S0={s0}={NAME.get(s0,'?')}  EW-slot S1={s1}={NAME.get(s1,'?')}  char {char:+d} [{FORM.get(char,'?')}] : {cnt}")
