#!/usr/bin/env python3
"""G-1: THE Y-SELECTION — which of B1102's 18 hypercharge directions survive the
gauge closing as COMPACT u(1) generators?

A rational Cartan direction Y enters the real form g^sigma as a compact u(1)
iff theta(Y) = -Y (then iY in g^sigma with negative form).  theta's Cartan action
depends only on the root involution g (sign lifts act trivially on the Cartan).

Frame: B1102's — color = S0 (the landing A2, closed compact), EW pair = {S1,S2};
the 18 Y's live in Cartan(S1) + Cartan(S2), coords [p1(0),p1(1),p2(0),p2(1)].
Gauge row = slot signatures (S0,S1,S2) = ((0,8),(4,4),(4,4)) [global E6(-14)].

Compute: (a) the 18 Y's (recomputed, must match B1102/B1118: 18, orbits 9+9);
(b) for every factor-preserving involution g: the subset {Y : gY = -Y} and
whether g admits a gauge-row sign lift; (c) the selection statistics, and for
selected Y's the roots beta with beta(Y)=0 (the surviving su(2) candidates).
"""
import importlib.util, itertools, random
from fractions import Fraction as F
from collections import Counter

SCR=__import__('os').path.dirname(__import__('os').path.abspath(__file__))+""
spec = importlib.util.spec_from_file_location("ccb", SCR+"/paper/verify/check_charge_bracket.py")
ccb = importlib.util.module_from_spec(spec); spec.loader.exec_module(ccb)
br, add_, smul_, is_zero = ccb.br, ccb.add, ccb.smul, ccb.is_zero
evec, hvec, eps, ip = ccb.evec, ccb.hvec, ccb.eps, ccb.ip
ROOTS, IDX, N, DIM = ccb.ROOTS, ccb.IDX, ccb.N, ccb.DIM
A = [[ip(tuple(1 if k==i else 0 for k in range(N)), tuple(1 if k==j else 0 for k in range(N)))
      for j in range(N)] for i in range(N)]

# ---------- the 27's weights (crystal of omega_1), minimal rebuild ----------
import sympy as sp
Cart=sp.Matrix(6,6, lambda i,j: A[i][j])
simple=[tuple(1 if k==i else 0 for k in range(N)) for i in range(N)]
# omega_1: ip(omega1, alpha_j) = delta_{1j} in the paper's node order — recompute the
# crystal instead directly: weights of the 27 = orbit closure under f_i from omega_1.
# Solve omega_1 from <omega1, alpha_j> = delta_{0j}? twisted_double used node index 1
# of the paper's ordering (its stage-1 built 27 weights and VERIFIED 3003 brackets).
# We only need the WEIGHTS; rebuild by minuscule-orbit: 27 weights = W-orbit of omega
# for the minuscule node. Try each fundamental weight; the minuscule ones give orbit 27.
def fund(k):
    b=sp.Matrix([1 if j==k else 0 for j in range(6)])
    return Cart.solve(b)      # coords in simple-root basis; pairing via ip
def wt_ip(lamvec, r):  # <lam, r> with lam in simple-root coords
    return sum(lamvec[i]*A[i][j]*r[j] for i in range(6) for j in range(6))
weights=None
for k in range(6):
    lam0=tuple(fund(k))
    orb={lam0}; frontier=[lam0]
    while frontier and len(orb)<=27:
        nf=[]
        for lam in frontier:
            for i in range(6):
                c=wt_ip(lam, simple[i])
                if c>0:
                    nl=tuple(lam[j]-c*sp.Rational(simple[i][j]) for j in range(6))
                    if nl not in orb: orb.add(nl); nf.append(nl)
        frontier=nf
    if len(orb)==27: weights=sorted(orb); break
assert weights is not None and len(weights)==27
print("27 minuscule weights rebuilt:", len(weights))

# ---------- slots ----------
a0=simple[0]; a2=simple[2]
def iprr(a,b): return sum(a[i]*A[i][j]*b[j] for i in range(6) for j in range(6))
S0={r for r in ROOTS if r in {tuple(c1*a0[k]+c2*a2[k] for k in range(N)) for c1 in (-1,0,1) for c2 in (-1,0,1)}}
orth=[r for r in ROOTS if iprr(r,a0)==0 and iprr(r,a2)==0]
comps=[]; left=set(orth)
while left:
    seed=next(iter(left)); comp={seed}; grew=True
    while grew:
        grew=False
        for r in list(left-comp):
            if any(iprr(r,s)!=0 for s in comp): comp.add(r); grew=True
    comps.append(comp); left-=comp
G1c,G2c=comps
def simple_pair(Gc):
    for r1,r2 in itertools.permutations(Gc,2):
        if iprr(r1,r2)==-1 and tuple(a+b for a,b in zip(r1,r2)) in Gc: return r1,r2
p1=simple_pair(G1c); p2=simple_pair(G2c)
cor=[p1[0],p1[1],p2[0],p2[1]]
print("slots: S0 (landing), S1, S2 orthogonal; cor basis fixed")

# ---------- the 18 hypercharge directions (B1102 recomputation) ----------
def wt4(lam): return tuple(int(wt_ip(lam, r)) for r in cor)
W4=[wt4(w) for w in weights]
classes=Counter(W4)
assert sorted(classes.values(),reverse=True)==[3]*6+[1]*9, sorted(classes.values(),reverse=True)
target={6:1, 3:2, 2:6, 1:6, 0:2, -2:3, -3:4, -4:3}
cls=list(classes.items())
big=[c for c in cls if c[1]==3]
vals3=[v for v,m in target.items() if m>=3]
sols=set()
for assign in itertools.product(vals3, repeat=6):
    used=Counter()
    for v in assign: used[v]+=3
    if any(used[v]>target.get(v,0) for v in used): continue
    Am=sp.Matrix([list(w) for w,_ in big]); bvec=sp.Matrix(list(assign))
    if Am.rank()!=Am.row_join(bvec).rank() or Am.rank()<4: continue
    y=(Am.T*Am).solve(Am.T*bvec)
    got=Counter(); ok=True
    for w,sz in cls:
        val=sum(y[i]*w[i] for i in range(4))
        if val!=int(val): ok=False; break
        got[int(val)]+=sz
    if ok and dict(got)==target:
        sols.add(tuple(sp.Rational(y[i]) for i in range(4)))
sols=sorted(sols)
print(f"hypercharge directions recomputed: {len(sols)} (B1102/B1118 banked: 18)")
assert len(sols)==18

# ---------- FP involutions of Aut(Phi) + their Cartan action on cor-coords ----------
root_list=ROOTS; nR=len(root_list)
def srefl(i):
    ai=simple[i]
    return tuple(IDX[tuple(r[k]-iprr(r,ai)*ai[k] for k in range(N))] for r in root_list)
gens=[srefl(i) for i in range(N)]
ident=tuple(range(nR))
seen={ident}; frontier=[ident]; Wg=[ident]
while frontier:
    nf=[]
    for p in frontier:
        for g in gens:
            q=tuple(p[g[i]] for i in range(nR))
            if q not in seen: seen.add(q); nf.append(q); Wg.append(q)
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
AUT = Wg + [compose(delta,w) for w in Wg]
iS=[frozenset(IDX[r] for r in S) for S in (S0,G1c,G2c)]
def image(p,fs): return frozenset(p[i] for i in fs)
FP=[g for g in AUT if all(image(g,fs)==fs for fs in iS) and compose(g,g)==ident]
print(f"factor-preserving involutions: {len(FP)}")

# Cartan action of g on cor-coords: Y = sum y_i h_{cor_i}; g(h_r)=h_{g(r)}.
# Need images h_{g(cor_i)} in the cor-basis: g preserves S1,S2 so g(cor_i) is a root of
# the same pair-slot; its coroot = integer combo of that slot's two base coroots.
def coroot_coords(r):
    # express h_r in cor basis: r in S1: r = a*p1[0]+b*p1[1] etc.
    for (base,off) in ((p1,0),(p2,2)):
        # try integer combo
        M2=sp.Matrix([[base[0][k] for k in range(6)],[base[1][k] for k in range(6)]]).T
        v=sp.Matrix([r[k] for k in range(6)])
        solset=M2.solve_least_squares(v)
        if M2*solset==v:
            out=[sp.Rational(0)]*4
            out[off]=solset[0]; out[off+1]=solset[1]
            return out
    raise RuntimeError("root not in S1 u S2 span")
def cartan_mat4(g):
    cols=[]
    for i in range(4):
        gi=root_list[g[IDX[cor[i]]]]
        cols.append(coroot_coords(gi))
    return sp.Matrix(4,4, lambda r,c: cols[c][r])

# gauge-row test: reuse sign-lift + fast slot signatures
NEG=tuple(IDX[tuple(-x for x in r)] for r in root_list)
def solve_lift(phi):
    rows=[]
    def addrow(idxs,rhs):
        m=0
        for i in idxs: m^=(1<<i)
        rows.append((m,rhs))
    for ia,ra in enumerate(root_list):
        addrow([ia,NEG[ia]],0); addrow([ia,phi[ia]],0)
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
    freev=[i for i in range(nR) if i not in pivots]; kern=[]
    for fv in freev:
        k=1<<fv
        for hb in sorted(pivots):
            pm,_=pivots[hb]
            if bin((pm ^ (1<<hb)) & k).count('1')%2: k|=(1<<hb)
        kern.append(k)
    out=[]
    for bits in range(1<<len(kern)):
        x=sol
        for j in range(len(kern)):
            if bits>>j & 1: x^=kern[j]
        for m,rhs in rows: assert bin(m & x).count('1')%2 == rhs
        out.append([1-2*((x>>i)&1) for i in range(nR)])
    return out
Gm=[[F(0)]*DIM for _ in range(DIM)]
for i in range(N):
    for j in range(N): Gm[i][j]=F(A[i][j])
for k,r in enumerate(ROOTS): Gm[N+k][N+IDX[tuple(-x for x in r)]]=F(-1)
def gform(u,v):
    s=F(0)
    for i,ui in enumerate(u):
        if ui:
            Gi=Gm[i]
            for j,vj in enumerate(v):
                if vj and Gi[j]: s+=ui*vj*Gi[j]
    return s
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
def eig_split_roots(phi,c,ridx_set):
    fix=[]; anti=[]; done=set()
    for irt in ridx_set:
        if irt in done: continue
        j=phi[irt]
        if j==irt:
            (fix if c[irt]==1 else anti).append(evec(root_list[irt])); done.add(irt)
        else:
            v1=evec(root_list[irt]); v2=evec(root_list[j])
            fix.append([a+F(c[irt])*b for a,b in zip(v1,v2)])
            anti.append([a-F(c[irt])*b for a,b in zip(v1,v2)])
            done.add(irt); done.add(j)
    return fix,anti
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
def slot_sig(phi,c,slot,base):
    ridx=[IDX[r] for r in slot]
    fx,ax=eig_split_roots(phi,c,set(ridx))
    # slot Cartan 2-dim: phi acts on coroot span
    cb=[[F(x) for x in base[0]],[F(x) for x in base[1]]]
    P6=[[F(0)]*N for _ in range(N)]
    for i in range(N):
        pr=root_list[phi[IDX[simple[i]]]]
        for j in range(N): P6[j][i]=F(pr[j])
    imgs=[[sum(P6[i][j]*v[j] for j in range(N)) for i in range(N)] for v in cb]
    Mm=[[cb[j][i] for j in range(2)] for i in range(N)]
    def coords2(v):
        R,piv=frac_rref([Mm[i]+[v[i]] for i in range(N)])
        out=[F(0)]*2
        for irow,cc in enumerate(piv):
            assert cc<2
            out[cc]=R[irow][2]
        return out
    T=[[F(0)]*2 for _ in range(2)]
    for j in range(2):
        cj=coords2(imgs[j])
        for i in range(2): T[i][j]=cj[i]
    fc=frac_nullspace([[T[i][j]-(F(1) if i==j else F(0)) for j in range(2)] for i in range(2)])
    ac=frac_nullspace([[T[i][j]+(F(1) if i==j else F(0)) for j in range(2)] for i in range(2)])
    pad=lambda h2: [sum(cb[j][i]*h2[j] for j in range(2)) for i in range(N)]+[F(0)]*(DIM-N)
    fx=fx+[pad(v) for v in fc]; ax=ax+[pad(v) for v in ac]
    p1_,n1_,z1=sig_of_sym([[gform(u,v) for v in fx] for u in fx]) if fx else (0,0,0)
    p2_,n2_,z2=sig_of_sym([[-gform(u,v) for v in ax] for u in ax]) if ax else (0,0,0)
    assert z1==0 and z2==0
    return (p1_+n1_ and (p1_+p2_, n1_+n2_)) or (p1_+p2_, n1_+n2_)

solset=set(sols)
gauge_g=0; stats=Counter(); sel_report={}
for g in FP:
    # does g admit a gauge-row lift: (S0,S1,S2) sigs = ((0,8),(4,4),(4,4))?
    has_gauge=False
    for c in solve_lift(g):
        s0=slot_sig(g,c,sorted(S0),( (a0,a2) ))
        if s0!=(0,8): continue
        s1=slot_sig(g,c,sorted(G1c),p1)
        s2=slot_sig(g,c,sorted(G2c),p2)
        if s1==(4,4) and s2==(4,4): has_gauge=True; break
    if not has_gauge: continue
    gauge_g+=1
    M4=cartan_mat4(g)
    anti=[y for y in sols if tuple(-x for x in y)==tuple(sum(M4[i,j]*y[j] for j in range(4)) for i in range(4))]
    fixed=[y for y in sols if tuple(y)==tuple(sum(M4[i,j]*y[j] for j in range(4)) for i in range(4))]
    stats[(len(anti),len(fixed))]+=1
    key=(len(anti),len(fixed))
    if key not in sel_report and anti:
        sel_report[key]=(g,anti)
print(f"\ninvolutions admitting a GAUGE-ROW lift (S0 compact, S1=S2=su(2,1)): {gauge_g}")
print("distribution over them of (#Y with gY=-Y [compact u(1)], #Y with gY=+Y [split u(1)]):")
for k,v in sorted(stats.items()): print(f"   anti={k[0]}, fixed={k[1]} : {v} involutions")
for key,(g,anti) in sorted(sel_report.items()):
    print(f"\nexample with {key[0]} selected compact Y's:")
    for y in anti:
        zeros=[r for r in list(G1c)+list(G2c) if sum(sp.Rational(y[i])*coroot_coords(r)[i]*0 for i in range(4))==0]
        # beta(Y) = <Y, beta> = sum_i y_i <cor_i, beta>
        zs=[r for r in list(G1c)+list(G2c) if sum(y[i]*iprr(cor[i],r) for i in range(4))==0]
        print(f"   Y={tuple(str(x) for x in y)}  annihilated roots (surviving su(2) candidates): {len(zs)}")
