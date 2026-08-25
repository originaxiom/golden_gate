#!/usr/bin/env python3
"""THE SIMULTANEOUS CLOSING (V-4 candidate).

B1114: so(3,1) on the Lorentz double <=> the antilinear map SWAPS the two sl2 triples.
B1127: compact color (0,8) reached only in the ANTIPODAL (factor-preserving) class;
       permute class gives (5,3)/(4,4).  Read jointly: within the swept torsor the two
       closings are mutually exclusive.  But the MIXED root-map  phi = -w  (w = Weyl
       involution swapping S0<->S1, fixing color S2 setwise) swaps the Lorentz factors
       AND acts antipodally on color simultaneously.  Question: does a signed involutive
       lift theta of phi exist, and does some sign solution give BOTH
         - sigma = tau.theta swaps the triples  => fixed algebra on the double = sl(2,C)_R = so(3,1)
         - color signature (0,8) compact
       and inside WHICH global real form?

Conventions (paper's e6): [e_r,e_{-r}] = -h_r; corrected invariant form
G(h_i,h_j)=A_ij, G(e_r,e_{-r})=-1; split real span => char +6; compact conj
tau.(e_r->e_{-r}, h->-h) => char -78.  Real form of sigma=tau.theta:
g^sigma = Fix(theta)_R (+) i.AntiFix(theta)_R ; signature = sig(G|Fix) + sig(-G|AntiFix);
character = (#pos) - (#neg):  -78 compact, -26 E6(-26), -14 E6(-14), +2 E6(2), +6 E6(6).
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
print(f"e6 loaded: {len(ROOTS)} roots, dim {DIM}")

# ---------- pure-Fraction linear algebra ----------
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
    """Signature of a rational symmetric matrix by congruence diagonalization."""
    M=[row[:] for row in M]; n=len(M); p=neg=z=0; idx=list(range(n))
    i=0
    while i<n:
        if M[i][i]==0:
            j=next((j for j in range(i+1,n) if M[j][i]!=0 or M[i][j]!=0), None)
            if j is None:
                jj=next((jj for jj in range(i+1,n) if M[i][jj]!=0), None)
                if jj is None: z+=1; i+=1; continue
                j=jj
            # row/col add: v_i += v_j
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

# ---------- the corrected invariant form ----------
G=[[F(0)]*DIM for _ in range(DIM)]
for i in range(N):
    for j in range(N): G[i][j]=F(A[i][j])
for k,r in enumerate(ROOTS):
    nr=tuple(-x for x in r)
    G[N+k][N+IDX[nr]]=F(-1)
# ad-invariance spot check: G([x,y],z) + G(y,[x,z]) = 0
def gform(u,v):
    s=F(0)
    for i,ui in enumerate(u):
        if ui:
            Gi=G[i]
            for j,vj in enumerate(v):
                if vj and Gi[j]: s+=ui*vj*Gi[j]
    return s
random.seed(7); ok=True
basis=[hvec(i) for i in range(N)]+[evec(r) for r in ROOTS]
for _ in range(300):
    x,y,z=(random.choice(basis) for _ in range(3))
    if gform(br(x,y),z)+gform(y,br(x,z))!=0: ok=False; break
print("corrected form ad-invariance (300 triples):", "PASS" if ok else "FAIL")
assert ok

# ---------- the A2 landing: S0 (nodes 0,2), orthogonal A2+A2 = S1, S2 ----------
a0=tuple(1 if k==0 else 0 for k in range(N)); a2=tuple(1 if k==2 else 0 for k in range(N))
assert ip(a0,a2)==-1, "nodes (0,2) must be adjacent (A2)"
S0=set()
for c1 in (-1,0,1):
    for c2 in (-1,0,1):
        r=tuple(c1*a0[k]+c2*a2[k] for k in range(N))
        if r in IDX: S0.add(r)
assert len(S0)==6
Rperp=[r for r in ROOTS if ip(r,a0)==0 and ip(r,a2)==0]
assert len(Rperp)==12
# split into components by adjacency
comps=[]; left=set(Rperp)
while left:
    seed=next(iter(left)); comp={seed}; grew=True
    while grew:
        grew=False
        for r in list(left-comp):
            if any(ip(r,s)!=0 for s in comp): comp.add(r); grew=True
    comps.append(comp); left-=comp
assert len(comps)==2 and all(len(c)==6 for c in comps)
S1,S2=comps
print(f"S0 (Levi 0,2), orthogonal components S1,S2 of sizes {len(S1)},{len(S2)}: OK")

def a2_base(S):
    """two 'simple' roots of an A2 subsystem: r,s with (r,s)=-1 and r+s in S"""
    for r,s in itertools.permutations(S,2):
        t=tuple(r[k]+s[k] for k in range(N))
        if ip(r,s)==-1 and t in S: return r,s
    raise RuntimeError
def principal_triple(S):
    r,s=a2_base(S)
    e=add_(evec(r),evec(s))
    h=add_(smul_(2,[F(x) for x in list(r)+[0]*72]), smul_(2,[F(x) for x in list(s)+[0]*72]))
    f=add_(smul_(-2,evec(tuple(-x for x in r))), smul_(-2,evec(tuple(-x for x in s))))
    assert br(e,f)==h and br(h,e)==smul_(2,e) and br(h,f)==smul_(-2,f)
    return e,h,f
T1=principal_triple(S0)
print("triple1 (regular of S0) verified")

# ---------- full W(E6) enumeration on root permutations ----------
root_list=ROOTS; nR=len(root_list)
def srefl(i):
    ai=tuple(1 if k==i else 0 for k in range(N))
    perm=[]
    for r in root_list:
        c=ip(r,ai)
        rr=tuple(r[k]-c*ai[k] for k in range(N))
        perm.append(IDX[rr])
    return tuple(perm)
gens=[srefl(i) for i in range(N)]
ident=tuple(range(nR))
seen={ident}; frontier=[ident]; elements=[ident]
while frontier:
    nf=[]
    for p in frontier:
        for g in gens:
            q=tuple(p[g[i]] for i in range(nR))
            if q not in seen:
                seen.add(q); nf.append(q); elements.append(q)
    frontier=nf
print(f"|W(E6)| enumerated: {len(elements)} (expect 51840)")
assert len(elements)==51840

i0=frozenset(IDX[r] for r in S0); i1=frozenset(IDX[r] for r in S1); i2=frozenset(IDX[r] for r in S2)
def image(p,fs): return frozenset(p[i] for i in fs)
swappers=[p for p in elements
          if image(p,i0)==i1 and image(p,i1)==i0 and image(p,i2)==i2]
invol=[p for p in swappers if tuple(p[p[i]] for i in range(nR))==ident]
pointwise=[p for p in invol if all(p[i]==i for i in i2)]
print(f"swap elements (S0<->S1, S2 setwise): {len(swappers)}; involutions: {len(invol)}; "
      f"involutions pointwise-id on S2: {len(pointwise)}")
assert invol, "no involutive swap in W — would kill the construction"
W_INV = pointwise[0] if pointwise else invol[0]
w_pointwise = bool(pointwise)

# ---------- root maps for the three classes ----------
NEG=tuple(IDX[tuple(-x for x in r)] for r in root_list)
def compose(p,q): return tuple(p[q[i]] for i in range(nR))
phi_anti = NEG                        # control: pure antipodal
phi_perm = W_INV                      # control: pure permute (B1114's linear swap class)
phi_mix  = compose(NEG, W_INV)        # THE MIXED CLASS: -w
for name,phi in (("antipodal",phi_anti),("permute",phi_perm),("mixed",phi_mix)):
    assert compose(phi,phi)==ident, name

# ---------- F2 signed-lift solver ----------
def solve_lift(phi):
    """theta(e_r)=c_r e_{phi r}, theta(h_a)=h_{phi a}; involution. Returns list of sign
    vectors c (each: root-idx -> +-1), [] if inconsistent."""
    rows=[]  # each row: (bitmask over 72 vars, rhs bit) as (frozenset, int) -> use int mask
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
                pa,pb=root_list[phi[ia]],root_list[phi[ib]]
                ratio=eps(ra,rb)*eps(pa,pb)
                addrow([ia,ib,IDX[s]],0 if ratio==1 else 1)
    # gaussian elim over GF(2)
    pivots={}
    for m,rhs in rows:
        while m:
            hb=m.bit_length()-1
            if hb in pivots:
                pm,pr=pivots[hb]; m^=pm; rhs^=pr
            else:
                pivots[hb]=(m,rhs); break
        else:
            if rhs: return []   # inconsistent
    # particular solution — pivot rows have their pivot as HIGHEST bit, so all other
    # bits are lower: evaluate pivots in ASCENDING order so dependencies are assigned
    sol=0
    for hb in sorted(pivots):
        pm,pr=pivots[hb]
        v=pr ^ (bin((pm ^ (1<<hb)) & sol).count('1')%2)
        if v: sol|=(1<<hb)
    # kernel basis (same ascending order)
    freev=[i for i in range(nR) if i not in pivots]
    kern=[]
    for fv in freev:
        k=1<<fv
        for hb in sorted(pivots):
            pm,_=pivots[hb]
            v=bin((pm ^ (1<<hb)) & k).count('1')%2
            if v: k|=(1<<hb)
        kern.append(k)
    sols=[]
    assert len(kern)<=13, f"kernel too big to enumerate: {len(kern)}"
    for bits in range(1<<len(kern)):
        x=sol
        for j in range(len(kern)):
            if bits>>j & 1: x^=kern[j]
        # sanity: x must satisfy EVERY original row
        for m,rhs in rows:
            assert bin(m & x).count('1')%2 == rhs, "GF(2) solver corrupt"
        sols.append([1-2*((x>>i)&1) for i in range(nR)])
    return sols

# ---------- build & verify theta; compute the three diagnostics ----------
def theta_matrix(phi,c):
    T=[[F(0)]*DIM for _ in range(DIM)]
    for i in range(N):
        pr=root_list[phi[IDX[tuple(1 if k==i else 0 for k in range(N))]]]
        for j in range(N): T[j][i]=F(pr[j])
    for ir in range(nR):
        T[N+phi[ir]][N+ir]=F(c[ir])
    return T
def apply(T,v): return [sum(T[i][j]*v[j] for j in range(DIM) if v[j]) for i in range(DIM)]
def verify_aut(T,ntrials=250):
    for _ in range(ntrials):
        x,y=random.choice(basis),random.choice(basis)
        if apply(T,br(x,y))!=br(apply(T,x),apply(T,y)): return False
    return True

def real_form_data(phi,c,label):
    T=theta_matrix(phi,c)
    # involution + automorphism
    TT=[[sum(T[i][k]*T[k][j] for k in range(DIM) if T[k][j]) for j in range(DIM)] for i in range(DIM)]
    if any(TT[i][j]!=(F(1) if i==j else F(0)) for i in range(DIM) for j in range(DIM)):
        return None
    if not verify_aut(T): return None
    # Fix / AntiFix
    Mfix=[[T[i][j]-(F(1) if i==j else F(0)) for j in range(DIM)] for i in range(DIM)]
    Manti=[[T[i][j]+(F(1) if i==j else F(0)) for j in range(DIM)] for i in range(DIM)]
    fixb=frac_nullspace(Mfix); antib=frac_nullspace(Manti)
    assert len(fixb)+len(antib)==DIM
    def gram(bas,sgn):
        return [[sgn*gform(u,v) for v in bas] for u in bas]
    pf,nf,zf=sig_of_sym(gram(fixb,1)); pa,na,za=sig_of_sym(gram(antib,-1))
    assert zf==0 and za==0
    char=(pf+pa)-(nf+na)
    # color slot
    cb=[evec(r) for r in S2]
    r1,s1=a2_base(S2)
    cb+= [ [F(x) for x in list(r1)+[0]*72], [F(x) for x in list(s1)+[0]*72] ]
    # theta preserves color span? project theta(cb) onto span cb
    span=[v[:] for v in cb]
    def in_span(v,span):
        Mm=[ [span[j][i] for j in range(len(span))]+[v[i]] for i in range(DIM)]
        R,piv=frac_rref(Mm)
        return len(span) not in piv
    col_pres=all(in_span(apply(T,v),span) for v in cb)
    # signature on color: Fix/AntiFix within the slot
    col_sig=None
    if col_pres:
        # restrict theta to slot: solve coefficients
        cols=[[cb[j][i] for j in range(8)] for i in range(DIM)]
        def coords(v):
            Mm=[cols[i]+[v[i]] for i in range(DIM)]
            R,piv=frac_rref(Mm)
            out=[F(0)]*8
            for irow,cc in enumerate(piv):
                if cc<8: out[cc]=R[irow][8]
            return out
        Tc=[[F(0)]*8 for _ in range(8)]
        for j in range(8):
            cj=coords(apply(T,cb[j]))
            for i in range(8): Tc[i][j]=cj[i]
        Fx=[[Tc[i][j]-(F(1) if i==j else F(0)) for j in range(8)] for i in range(8)]
        Ax=[[Tc[i][j]+(F(1) if i==j else F(0)) for j in range(8)] for i in range(8)]
        fb=frac_nullspace(Fx); ab=frac_nullspace(Ax)
        tofull=lambda coef: [sum(cb[j][i]*coef[j] for j in range(8)) for i in range(DIM)]
        fbv=[tofull(v) for v in fb]; abv=[tofull(v) for v in ab]
        p1,n1,z1=sig_of_sym([[gform(u,v) for v in fbv] for u in fbv])
        p2,n2,z2=sig_of_sym([[-gform(u,v) for v in abv] for u in abv])
        assert z1==0 and z2==0
        col_sig=(p1+p2, n1+n2)
    # double: D = span(T1) + theta(span T1); swap?
    t1=[T1[0],T1[1],T1[2]]
    th_t1=[apply(T,v) for v in t1]
    # does theta map span(T1) OFF itself (into sl(S1))? check first component supports
    sup=lambda v: {i for i,x in enumerate(v) if x}
    swap = not any( in_span(v,[t1[0],t1[1],t1[2]]) for v in th_t1 )
    dbl_sig=None
    if swap:
        Dbas=t1+th_t1
        # Fix on D: v + theta v ; AntiFix: v - theta v
        fD=[add_(t1[k],th_t1[k]) for k in range(3)]
        aD=[[x-y for x,y in zip(t1[k],th_t1[k])] for k in range(3)]
        p1,n1,z1=sig_of_sym([[gform(u,v) for v in fD] for u in fD])
        p2,n2,z2=sig_of_sym([[-gform(u,v) for v in aD] for u in aD])
        dbl_sig=(p1+p2,n1+n2,z1+z2)
    return dict(label=label,char=char,gsig=((pf+pa),(nf+na)),col_pres=col_pres,
                col_sig=col_sig,swap=swap,dbl_sig=dbl_sig)

FORM={-78:"E6 compact",-26:"E6(-26)=M(O,C)",-14:"E6(-14)",2:"E6(2)",6:"E6(6) split"}
def run_class(name,phi):
    sols=solve_lift(phi)
    print(f"\n=== class {name}: {len(sols)} involutive sign solutions ===")
    if not sols:
        print("   F2 SYSTEM INCONSISTENT — no involutive lift (order-4 obstruction)")
        return []
    out=[]
    seenkinds=set()
    for c in sols:
        d=real_form_data(phi,c,name)
        if d is None: continue
        key=(d['char'],d['col_sig'],d['swap'],d['dbl_sig'])
        out.append(d)
        if key in seenkinds: continue
        seenkinds.add(key)
        print(f"  char {d['char']:+d} [{FORM.get(d['char'],'?')}]  global sig {d['gsig']}  "
              f"color_preserved={d['col_pres']} color_sig={d['col_sig']}  "
              f"swaps_triples={d['swap']} double_sig={d['dbl_sig']}")
    return out

print(f"\nw involution: pointwise-id on S2 = {w_pointwise}")
res_a=run_class("antipodal (control)",phi_anti)
res_p=run_class("permute (control, B1114 class)",phi_perm)
res_m=run_class("MIXED -w (the unswept class)",phi_mix)

# verdict
def compact_col(d): return d['col_sig']==(0,8)
def lorentz(d): return d['swap'] and d['dbl_sig'] and (d['dbl_sig'][0],d['dbl_sig'][1])==(3,3)
print("\n================ VERDICT ================")
for name,res in (("antipodal",res_a),("permute",res_p),("mixed",res_m)):
    both=[d for d in res if compact_col(d) and lorentz(d)]
    print(f"{name}: solutions={len(res)}, compact-color={sum(map(compact_col,res))}, "
          f"so(3,1)-double={sum(map(lorentz,res))}, BOTH={len(both)}")
    for d in both:
        print(f"   >>> SIMULTANEOUS CLOSING: char {d['char']:+d} = {FORM.get(d['char'],'?')}")
