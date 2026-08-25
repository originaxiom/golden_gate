#!/usr/bin/env python3
"""FULL verification of the simultaneous-closing hits.

For each hit (swapper g, sign solution c) with color (0,8):
  - theta^2 = I exactly (78x78)
  - automorphism on ALL 3003 basis bracket pairs (first hit; 300 random for the rest)
  - global signature & character of sigma = tau.theta   (which real form?)
  - double signature (expect (3,3) = so(3,1))
  - color signature (expect (0,8) = compact su(3))
  - locate g: in W or in deltaW; order of action on S2
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
i0=frozenset(IDX[r] for r in S0); i1=frozenset(IDX[r] for r in S1); i2=frozenset(IDX[r] for r in S2)
def image(p,fs): return frozenset(p[i] for i in fs)
G_swap=[g for g in AUT if image(g,i0)==i1 and image(g,i1)==i0 and image(g,i2)==i2
        and compose(g,g)==ident]
print(f"involutive swappers: {len(G_swap)}")

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

def a2_base(S):
    for r,s in itertools.permutations(S,2):
        t=tuple(r[k]+s[k] for k in range(N))
        if ip(r,s)==-1 and t in S: return r,s
    raise RuntimeError
r2,s2=a2_base(S2)
cb=[evec(r) for r in sorted(S2)]+[[F(x) for x in list(r2)+[0]*72],[F(x) for x in list(s2)+[0]*72]]
cols=[[cb[j][i] for j in range(8)] for i in range(DIM)]
def coords(v):
    Mm=[cols[i]+[v[i]] for i in range(DIM)]
    R,piv=frac_rref(Mm)
    assert 8 not in piv
    out=[F(0)]*8
    for irow,cc in enumerate(piv): out[cc]=R[irow][8]
    return out
def theta_matrix(phi,c):
    T=[[F(0)]*DIM for _ in range(DIM)]
    for i in range(N):
        pr=root_list[phi[IDX[tuple(1 if k==i else 0 for k in range(N))]]]
        for j in range(N): T[j][i]=F(pr[j])
    for ir in range(nR): T[N+phi[ir]][N+ir]=F(c[ir])
    return T
def apply(T,v): return [sum(T[i][j]*v[j] for j in range(DIM) if v[j]) for i in range(DIM)]
def color_sig(phi,c):
    Tc=[[F(0)]*8 for _ in range(8)]
    T=theta_matrix(phi,c)
    for j in range(8):
        cj=coords(apply(T,cb[j]))
        for i in range(8): Tc[i][j]=cj[i]
    Fx=[[Tc[i][j]-(F(1) if i==j else F(0)) for j in range(8)] for i in range(8)]
    Ax=[[Tc[i][j]+(F(1) if i==j else F(0)) for j in range(8)] for i in range(8)]
    fb=frac_nullspace(Fx); ab=frac_nullspace(Ax)
    tofull=lambda coef: [sum(cb[j][i]*coef[j] for j in range(8)) for i in range(DIM)]
    fbv=[tofull(v) for v in fb]; abv=[tofull(v) for v in ab]
    p1,n1,_=sig_of_sym([[gform(u,v) for v in fbv] for u in fbv])
    p2,n2,_=sig_of_sym([[-gform(u,v) for v in abv] for u in abv])
    return (p1+p2, n1+n2)

# principal triple of S0
def principal_triple(S):
    r,s=a2_base(S)
    e=add_(evec(r),evec(s))
    h=add_(smul_(2,[F(x) for x in list(r)+[0]*72]), smul_(2,[F(x) for x in list(s)+[0]*72]))
    f=add_(smul_(-2,evec(tuple(-x for x in r))), smul_(-2,evec(tuple(-x for x in s))))
    assert br(e,f)==h
    return [e,h,f]
T1=principal_triple(S0)

basis=[hvec(i) for i in range(N)]+[evec(r) for r in ROOTS]
random.seed(23)
FORM={-78:"E6 compact",-26:"E6(-26)=M(O,C)",-14:"E6(-14)",2:"E6(2)",6:"E6(6) split"}

hitno=0; summary={}
for gi,g in enumerate(G_swap):
    for c in solve_lift(g):
        if color_sig(g,c)!=(0,8): continue
        hitno+=1
        T=theta_matrix(g,c)
        # theta^2 = I exact
        TT=[[sum(T[i][k]*T[k][j] for k in range(DIM) if T[k][j]) for j in range(DIM)] for i in range(DIM)]
        assert all(TT[i][j]==(F(1) if i==j else F(0)) for i in range(DIM) for j in range(DIM))
        # automorphism: full 3003 for hit #1, else 300 random
        if hitno==1:
            pairs=[(x,y) for xi,x in enumerate(basis) for y in basis[xi+1:]]
        else:
            pairs=[(random.choice(basis),random.choice(basis)) for _ in range(300)]
        for x,y in pairs:
            assert apply(T,br(x,y))==br(apply(T,x),apply(T,y)), "automorphism FAIL"
        # global signature
        Mfix=[[T[i][j]-(F(1) if i==j else F(0)) for j in range(DIM)] for i in range(DIM)]
        Manti=[[T[i][j]+(F(1) if i==j else F(0)) for j in range(DIM)] for i in range(DIM)]
        fixb=frac_nullspace(Mfix); antib=frac_nullspace(Manti)
        pf,nf,_=sig_of_sym([[gform(u,v) for v in fixb] for u in fixb])
        pa,na,_=sig_of_sym([[-gform(u,v) for v in antib] for u in antib])
        char=(pf+pa)-(nf+na)
        # double signature
        th_t1=[apply(T,v) for v in T1]
        fD=[add_(T1[k],th_t1[k]) for k in range(3)]
        aD=[[x-y for x,y in zip(T1[k],th_t1[k])] for k in range(3)]
        p1,n1,z1=sig_of_sym([[gform(u,v) for v in fD] for u in fD])
        p2,n2,z2=sig_of_sym([[-gform(u,v) for v in aD] for u in aD])
        dbl=(p1+p2,n1+n2,z1+z2)
        coset = "W" if g in seen else "deltaW"
        s2act = "id" if all(g[i]==i for i in i2) else "nontrivial"
        key=(char,dbl,coset,s2act)
        summary[key]=summary.get(key,0)+1
        if summary[key]==1:
            full="FULL-3003" if hitno==1 else "300-random"
            print(f"hit: swapper#{gi} [{coset}] S2-action={s2act}  theta^2=I OK  "
                  f"automorphism {full} OK  global sig ({pf+pa},{nf+na}) char {char:+d} "
                  f"[{FORM.get(char,'?')}]  double {dbl}  color (0,8)")
print(f"\ntotal hits verified: {hitno}")
print("summary {(char, double_sig, coset, S2-action): count}:")
for k,v in sorted(summary.items()): print("  ", k, ":", v)
