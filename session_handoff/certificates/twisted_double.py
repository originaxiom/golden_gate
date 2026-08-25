#!/usr/bin/env python3
"""L79: the theta-odd twisted mirror-double — INTERFACE SPECTRUM + GENERICITY SWEEP.
Stages (each gated):
  0. import the paper's e6 (Chevalley basis, 78-dim, exact); principal sl2; x8, x16.
  1. build the 27: weights = crystal of omega_1; module action via the shift-cocycle
     e_r . v_lam = eps(r, q_lam) v_{lam+r}  (q_lam = lam - omega_1 in the root lattice).
     VERIFY: rho([u,v]) = [rho(u),rho(v)] over the full Chevalley basis.
  2. principal grading on the 27: strings Sym^16 + Sym^8 + Sym^0 (matches physics1).
  3. group rep on the 27 with NO basis mismatch: A27 = exp(rho(E)), B27 = exp(q rho(F))
     (Riley A=[[1,1],[0,1]] = exp(e), B=[[1,0],[q,1]] = exp(q f)); relator check.
  4. Fox H^1(M; 27) = 3 (control: matches the session's per-block run and B662's grammar).
  5. the longitude: search for the peripheral partner of the meridian a.
  6. H^*(T^2; 27), restriction maps, Mayer-Vietoris for the double
     D_t = M cup_{T^2} M with the right copy dial-twisted by D(t)=exp(t rho(x8)),
     for t in {0, 1, 2, omega=q-1}, and gluing sign variants.
     CONTROL: t=0 identity-gluing must give h^1(D;27)=5 (B662/B1036).
  7. same for the DUAL 27-bar: chirality-at-count test (PD predicts equality).
  8. Part 1 of L79: adjoint genericity sweep — bracket closure of the dial-twisted
     sl2-pair at t in {1,2,omega}, slots x8 and x16 (expect 78 = e6; either answer banks).
Field: Q(q)/(q^2-q+1) as Fraction pairs (x+yq); omega = q-1.
"""
import importlib.util, sys, itertools
from fractions import Fraction as F
import sympy as sp

# ---------------- field Q(q), q^2 = q-1 ----------------
ZERO=(F(0),F(0)); ONE=(F(1),F(0)); QQ=(F(0),F(1)); OMEGA=(F(-1),F(1))
def fadd(u,v): return (u[0]+v[0], u[1]+v[1])
def fsub(u,v): return (u[0]-v[0], u[1]-v[1])
def fneg(u): return (-u[0],-u[1])
def fmul(u,v):
    a=u[0]*v[0]; b=u[0]*v[1]+u[1]*v[0]; c=u[1]*v[1]
    return (a-c, b+c)
def finv(u):
    x,y=u; n=x*x+x*y+y*y
    return ((x+y)/n, -y/n)
def frat(r): return (F(r),F(0))

def mat(n,m): return [[ZERO]*m for _ in range(n)]
def eye(n):
    M=mat(n,n)
    for i in range(n): M[i][i]=ONE
    return M
def mmul(A,B):
    n=len(A); k=len(B); m=len(B[0])
    C=mat(n,m)
    for i in range(n):
        Ai=A[i]
        for t in range(k):
            a=Ai[t]
            if a==ZERO: continue
            Bt=B[t]; Ci=C[i]
            for j in range(m):
                if Bt[j]!=ZERO: Ci[j]=fadd(Ci[j], fmul(a,Bt[j]))
    return C
def madd(A,B): return [[fadd(x,y) for x,y in zip(r,s)] for r,s in zip(A,B)]
def msub(A,B): return [[fsub(x,y) for x,y in zip(r,s)] for r,s in zip(A,B)]
def msc(c,A): return [[fmul(c,x) for x in r] for r in A]
def mvec(A,v): return [ (lambda s: s)( _dot(A[i],v) ) for i in range(len(A)) ]
def _dot(row,v):
    s=ZERO
    for x,y in zip(row,v):
        if x!=ZERO and y!=ZERO: s=fadd(s,fmul(x,y))
    return s
def rref(M):
    M=[row[:] for row in M]
    rows=len(M); cols=len(M[0]) if rows else 0
    piv=[]; r=0
    for c in range(cols):
        pr=None
        for i in range(r,rows):
            if M[i][c]!=ZERO: pr=i; break
        if pr is None: continue
        M[r],M[pr]=M[pr],M[r]
        inv=finv(M[r][c])
        M[r]=[fmul(inv,x) for x in M[r]]
        for i in range(rows):
            if i!=r and M[i][c]!=ZERO:
                f_=M[i][c]
                M[i]=[fsub(x,fmul(f_,y)) for x,y in zip(M[i],M[r])]
        piv.append(c); r+=1
        if r==rows: break
    return M,piv
def rank(M): return len(rref(M)[1])
def nullity(M): return (len(M[0]) if M else 0) - rank(M) if M else 0
def nullspace(M):
    R,piv=rref(M); cols=len(M[0])
    free=[c for c in range(cols) if c not in piv]
    out=[]
    for fc in free:
        v=[ZERO]*cols; v[fc]=ONE
        for i,c in enumerate(piv): v[c]=fneg(R[i][fc])
        out.append(v)
    return out
def minv(A):
    n=len(A)
    aug=[A[i][:]+eye(n)[i] for i in range(n)]
    R,piv=rref(aug)
    assert piv==list(range(n)), "singular"
    return [R[i][n:] for i in range(n)]

# ---------------- stage 0: the paper's e6 ----------------
spec = importlib.util.spec_from_file_location("ccb",
  __import__('os').path.dirname(__import__('os').path.abspath(__file__))+"/paper/verify/check_charge_bracket.py")
ccb = importlib.util.module_from_spec(spec); spec.loader.exec_module(ccb)
br, add_, smul_, is_zero = ccb.br, ccb.add, ccb.smul, ccb.is_zero
evec, hvec, eps, ip = ccb.evec, ccb.hvec, ccb.eps, ccb.ip
ROOTS, IDX, N, DIM = ccb.ROOTS, ccb.IDX, ccb.N, ccb.DIM
print(f"stage 0: e6 loaded, {len(ROOTS)} roots, dim {DIM}")

# principal sl2 (as in allbrackets.py)
e6e=[F(0)]*DIM
for i in range(N):
    pos=tuple(1 if k==i else 0 for k in range(N))
    e6e[N+IDX[pos]]=F(1)
Cart=sp.Matrix(6,6, lambda i,j: ccb.ip(tuple(1 if k==i else 0 for k in range(6)), tuple(1 if k==j else 0 for k in range(6))))
hcoef=Cart.solve(sp.Matrix([2]*6))
e6h=[F(0)]*DIM
for j in range(N): e6h[j]=F(int(hcoef[j]))
e6f=[F(0)]*DIM
for j in range(N):
    neg=tuple(-1 if i2==j else 0 for i2 in range(N))
    e6f[N+IDX[neg]] = e6h[j]/F(eps(tuple(1 if k==j else 0 for k in range(N)), neg))
assert br(e6e,e6f)==e6h
x,y=sp.symbols('x y')
Wp=x**8+14*x**4*y**4+y**8
def highest_vector(n):
    cands=[r for r in ROOTS if br(e6h,evec(r))[N+IDX[r]]==n]
    for r in cands:
        v=evec(r)
        if is_zero(br(e6e,v)): return v
    cols=[evec(r) for r in cands]
    Mx=sp.zeros(DIM,len(cols))
    for j,c in enumerate(cols):
        img=br(e6e,c)
        for i2,val in enumerate(img): Mx[i2,j]=sp.Rational(val.numerator,val.denominator)
    ns=Mx.nullspace()
    if not ns: return None
    vec=ns[0]; out=[F(0)]*DIM
    for j,c in enumerate(cols):
        coef=sp.Rational(vec[j])
        if coef: out=add_(out, smul_(F(coef.p,coef.q), c))
    return out
def embed(poly,n):
    v=highest_vector(n); P=sp.Poly(poly,x,y); out=[F(0)]*DIM; cur=v
    for k in range(n+1):
        c=P.coeff_monomial(x**(n-k)*y**k)
        if c:
            rat=sp.Rational(c)*sp.factorial(n-k)/sp.factorial(n)
            out=add_(out, smul_(F(sp.Rational(rat).p,sp.Rational(rat).q), cur))
        cur=br(e6f,cur)
    return out
X8=highest_vector(8); X16=highest_vector(16)   # the DIAL SLOTS: e-centralizing tops of the
assert not is_zero(X8) and not is_zero(X16)     # Sym^8 / Sym^16 adjoint blocks (exponents 4, 8)
assert is_zero(br(e6e,X8)) and is_zero(br(e6e,X16)), "slots must centralize the principal e"
print("stage 0: principal sl2 + dial slots hv(8), hv(16) embedded")

# ---------------- stage 1: the 27 ----------------
simple=[tuple(1 if k==i else 0 for k in range(N)) for i in range(N)]
# omega_1: solve ip(omega1, alpha_j) = delta_{1j} (simply-laced: <,alpha^v> = ip)
Msys=sp.Matrix(6,6, lambda i,j: ccb.ip(simple[i], simple[j]))
w1=Msys.solve(sp.Matrix([1,0,0,0,0,0]))
omega1=tuple(sp.Rational(w1[k]) for k in range(6))
def tadd(a,b): return tuple(x+y for x,y in zip(a,b))
def tsub(a,b): return tuple(x-y for x,y in zip(a,b))
def ipr(a,b):  # ip extended to rational tuples
    return sum(a[i]*b[j]*Msys[i,j] for i in range(6) for j in range(6))
# crystal
weights=[omega1]; seen={omega1}
queue=[omega1]
while queue:
    lam=queue.pop()
    for al in simple:
        if ipr(lam,al)==1:
            mu=tsub(lam,al)
            if mu not in seen:
                seen.add(mu); weights.append(mu); queue.append(mu)
assert len(weights)==27, f"27 weights expected, got {len(weights)}"
WIDX={w:i for i,w in enumerate(weights)}
qlat={w: tuple(int(x) for x in tsub(w,omega1)) for w in weights}
for w in weights:
    assert all(sp.Rational(a)==int(a) for a in tsub(w,omega1)), "shift not integral"
print("stage 1: 27 weights built (crystal of omega_1)")

# module action of basis elements on the 27 (sparse: dict col->(row, coeff over Q))
def act_root(r):
    out={}
    for w in weights:
        tgt=tadd(w, r)
        if tgt in WIDX:
            out[WIDX[w]] = (WIDX[tgt], F(eps(r, qlat[w])))
    return out
ROOTACT={r: act_root(r) for r in ROOTS}
# Cartan pairing: c(j, r) from adjoint br(hvec(j), evec(r)); it is linear in root coords
CJ=[]
for j in range(6):
    vals=sp.Matrix([ [br(hvec(j), evec(al))[N+IDX[al]] for al in simple] ])
    CJ.append([sp.Rational(vals[0,k]) for k in range(6)])
def cartan_eig(j, lam):  # eigenvalue of hvec(j) on v_lam
    return sum(sp.Rational(CJ[j][k])*sp.Rational(lam[k]) for k in range(6))
# rho27 of a general adjoint vector (list of 78 Fractions) -> dense 27x27 over Q as Fractions
def rho27_Q(vec):
    Mq=[[F(0)]*27 for _ in range(27)]
    for j in range(6):
        if vec[j]:
            for w in weights:
                ev=cartan_eig(j,w)
                if ev:
                    i2=WIDX[w]; Mq[i2][i2]+= vec[j]*F(sp.Rational(ev).p, sp.Rational(ev).q)
    for r in ROOTS:
        c=vec[N+IDX[r]]
        if c:
            for col,(row,s) in ROOTACT[r].items():
                Mq[row][col]+= c*s
    return Mq
# verification: rho([u,v]) = [rho(u),rho(v)] for all Chevalley pairs
def matQ_mul(A,B):
    n=len(A); C=[[F(0)]*n for _ in range(n)]
    for i in range(n):
        for t in range(n):
            a=A[i][t]
            if a:
                Bt=B[t]; Ci=C[i]
                for j in range(n):
                    if Bt[j]: Ci[j]+=a*Bt[j]
    return C
def matQ_sub(A,B): return [[x-y for x,y in zip(r,s)] for r,s in zip(A,B)]
basis_ad=[]
for j in range(6):
    v=[F(0)]*DIM; v[j]=F(1); basis_ad.append(v)
for r in ROOTS:
    basis_ad.append(evec(r))
RHO=[rho27_Q(v) for v in basis_ad]
import random
random.seed(1)
pairs=list(itertools.combinations(range(len(basis_ad)),2))
fails=0
for (i2,j2) in pairs:
    lhs=rho27_Q(br(basis_ad[i2],basis_ad[j2]))
    rhs=matQ_sub(matQ_mul(RHO[i2],RHO[j2]), matQ_mul(RHO[j2],RHO[i2]))
    if lhs!=rhs: fails+=1
print(f"stage 1 VERIFY: rho27 respects ALL {len(pairs)} Chevalley brackets: {'PASS' if fails==0 else f'FAIL ({fails})'}")
if fails: sys.exit(1)

# ---------------- stage 2: principal strings ----------------
E27=rho27_Q(e6e); F27=rho27_Q(e6f); H27=rho27_Q(e6h)
grades={}
for w in weights:
    g=sum(sp.Rational(e6h[j])*cartan_eig(j,w) for j in range(6))
    grades[WIDX[w]]=int(g)
tops=sorted([g for i2,g in grades.items()], reverse=True)
from collections import Counter
gc=Counter(grades.values())
# string content: multiplicity of top n = count(n) - count(n+2)
strings=[n for n in range(0,40,2) if gc.get(n,0)-gc.get(n+2,0)>0 for _ in range(gc.get(n,0)-gc.get(n+2,0))]
print("stage 2: principal strings:", sorted(strings, reverse=True), "(expect [16,8,0])")
assert sorted(strings,reverse=True)==[16,8,0]

# ---------------- stage 3: group rep on the 27 ----------------
def toF(Mq): return [[ (v,F(0)) for v in row] for row in Mq]
def nilexp(Mp, scale):
    n=len(Mp)
    out=eye(n); P=eye(n); fact=F(1); sc=ONE
    for k in range(1,40):
        P=mmul(P,Mp); fact*=k; sc=fmul(sc,scale)
        if all(x==ZERO for row in P for x in row): break
        coef=fmul(sc, finv((fact,F(0))))
        out=madd(out, [[fmul(coef,xx) for xx in row] for row in P])
    return out
E27p=toF(E27); F27p=toF(F27); X8_27p=toF(rho27_Q(X8))
A27=nilexp(E27p, ONE)          # A=[[1,1],[0,1]] = exp(e)
B27=nilexp(F27p, QQ)           # B=[[1,0],[q,1]] = exp(q f)
A27i=nilexp(E27p, fneg(ONE)); B27i=nilexp(F27p, fneg(QQ))
assert mmul(A27,A27i)==eye(27)
# relator check: a w b^-1 w^-1 with w = b a^-1 b^-1 a
def wordmat(word, d):
    Mp=eye(len(d['a']))
    for ch in word: Mp=mmul(Mp, d[ch])
    return Mp
d27={'a':A27,'A':A27i,'b':B27,'B':B27i}
Rel=wordmat('a'+'bABa'+'B'+ 'AbaB', d27)   # a w b^{-1} w^{-1}, w=bABa -> w^{-1}=AbaB
print("stage 3: relator acts as identity on the 27:", "PASS" if Rel==eye(27) else "FAIL")
if Rel!=eye(27): sys.exit(1)

# ---------------- stage 4: Fox H^1(M;27) ----------------
def fox_h1(dd, nn):
    I=eye(nn)
    Ai,Bi=dd['A'],dd['B']; An,Bn=dd['a'],dd['b']
    dw_da=msub(mmul(Bn,mmul(Ai,Bi)), mmul(Bn,Ai))
    dw_db=msub(I, mmul(Bn,mmul(Ai,Bi)))
    W=wordmat('bABa',dd); Wi=wordmat('AbaB',dd)
    AW=mmul(An,W); AWBi=mmul(AW,Bi); AWBiWi=mmul(AWBi,Wi)
    dr_da=madd(I, msub(mmul(An,dw_da), mmul(AWBiWi,dw_da)))
    dr_db=msub(mmul(An,dw_db), madd(AWBi, mmul(AWBiWi,dw_db)))
    D1=[dr_da[i]+dr_db[i] for i in range(nn)]
    Z=nullspace(D1)
    Bcols=[]
    AnI=msub(An,I); BnI=msub(Bn,I)
    for j in range(nn):
        Bcols.append([AnI[i][j] for i in range(nn)]+[BnI[i][j] for i in range(nn)])
    Bmat=[[Bcols[j][i] for j in range(nn)] for i in range(2*nn)]
    rB=rank(Bmat)
    return Z, Bcols, rB
Z27, Bcols27, rB27 = fox_h1(d27, 27)
h1M=len(Z27)-rB27
print(f"stage 4: h^1(M;27) = {h1M} (expect 3; B662 grammar)")
assert h1M==3

# ---------------- stage 5: the longitude ----------------
qc=complex(0.5, 3**0.5/2)
def m2mulc(P,Q):
    return ((P[0][0]*Q[0][0]+P[0][1]*Q[1][0], P[0][0]*Q[0][1]+P[0][1]*Q[1][1]),
            (P[1][0]*Q[0][0]+P[1][1]*Q[1][0], P[1][0]*Q[0][1]+P[1][1]*Q[1][1]))
A2n=((1,1),(0,1)); B2n=((1,0),(qc,1))
A2ni=((1,-1),(0,1)); B2ni=((1,0),(-qc,1))
d2n={'a':A2n,'A':A2ni,'b':B2n,'B':B2ni}
lam_word=None
for L in (8,6,10):
    for combo in itertools.product('aAbB', repeat=L):
        word=''.join(combo)
        bad=False
        for i2 in range(L-1):
            if word[i2].swapcase()==word[i2+1]: bad=True; break
        if bad: continue
        es=word.count('a')-word.count('A')+word.count('b')-word.count('B')
        if es!=0: continue
        if word.count('b')+word.count('B')==0: continue
        Mw=((1,0),(0,1))
        for ch in word: Mw=m2mulc(Mw,d2n[ch])
        if abs(Mw[1][0])>1e-9: continue
        sgn=None
        if abs(Mw[0][0]-1)<1e-9 and abs(Mw[1][1]-1)<1e-9: sgn=1
        if abs(Mw[0][0]+1)<1e-9 and abs(Mw[1][1]+1)<1e-9: sgn=-1
        if sgn is None: continue
        if abs(Mw[0][1])<1e-6: continue
        if abs(Mw[0][1].imag)<1e-6: continue
        lam_word=word; lam_off_num=Mw[0][1]; break
    if lam_word: break
assert lam_word is not None, "no longitude found"
# symbolic verification
q_s=sp.Rational(1,2)+sp.sqrt(-3)/2
A2=sp.Matrix([[1,1],[0,1]]); B2=sp.Matrix([[1,0],[q_s,1]])
d2={'a':A2,'A':sp.Matrix([[1,-1],[0,1]]),'b':B2,'B':sp.Matrix([[1,0],[-q_s,1]])}
Mw=sp.eye(2)
for ch in lam_word: Mw=sp.expand(Mw*d2[ch])
Mw=Mw.applyfunc(lambda z: sp.simplify(sp.expand(z)))
assert Mw[1,0]==0 and (Mw[0,0]==1 or Mw[0,0]==-1) and Mw[1,1]==Mw[0,0], f"longitude not parabolic: {Mw}"
print(f"   (SL2 lift has diagonal {Mw[0,0]} — the fig-8 longitude's famous trace -2 lift)" if Mw[0,0]==-1 else "")
assert sp.simplify(sp.expand(Mw[0,1]))!=0
print(f"stage 5: longitude found and verified symbolically: {lam_word}, off-diag {sp.nsimplify(Mw[0,1])}")

# ---------------- stage 6: T^2 cohomology + Mayer-Vietoris ----------------
Amu=A27
Alam=wordmat(lam_word, d27)
assert mmul(Amu,Alam)==mmul(Alam,Amu), "peripheral images must commute on the 27"
I27=eye(27)
def h_torus(Amu_,Alam_):
    # Z^1 = {(u,v): (Amu-1)v = (Alam-1)u};  B^1 = {((Amu-1)w,(Alam-1)w)}
    Mu=msub(Amu_,I27); Ml=msub(Alam_,I27)
    # equations: Ml*u - Mu*v = 0  (27 eqs, 54 unknowns u,v)
    Sys=[[Ml[i][j] for j in range(27)]+[fneg(Mu[i][j]) for j in range(27)] for i in range(27)]
    Zb=nullspace(Sys)
    Bc=[]
    for j in range(27):
        Bc.append([Mu[i][j] for i in range(27)]+[Ml[i][j] for i in range(27)])
    Bm=[[Bc[j][i] for j in range(len(Bc))] for i in range(54)]
    rB_=rank(Bm)
    h0=nullity([[Mu[i][j] for j in range(27)] for i in range(27)]+[[Ml[i][j] for j in range(27)] for i in range(27)])
    return Zb, Bc, rB_, h0
Zt, Bt, rBt, h0T = h_torus(Amu, Alam)
h1T=len(Zt)-rBt
print(f"stage 6: torus: h^0 = {h0T}, h^1 = {h1T} (expect 3 and 6)")

def cocycle_eval(za, zb, word, dd):
    val=[ZERO]*27; pref=eye(27)
    zmap={'a':za,'b':zb}
    for ch in word:
        if ch in 'ab':
            zv=zmap[ch]
            val=[fadd(val[i], _dot(pref[i], zv)) for i in range(27)]
            pref=mmul(pref, dd[ch])
        else:
            g=dd[ch]  # inverse letter: z(x^{-1}) = -g z(x) with g = rho(x)^{-1}
            zv=zmap[ch.lower()]
            t1=[_dot(g[i], zv) for i in range(27)]
            val=[fsub(val[i], _dot(pref[i], t1)) for i in range(27)]
            pref=mmul(pref, dd[ch])
    return val

# H^1(M) basis as cocycles: pick 3 independent-mod-B elements of Z27
def h1_basis(Z, Bcols, rB, nn):
    out=[]; cur=[c[:] for c in Bcols]
    curm=[[cur[j][i] for j in range(len(cur))] for i in range(2*nn)]
    r0=rB
    for z in Z:
        test=[[cur[j][i] for j in range(len(cur))]+[z[i]] for i in range(2*nn)]
        if rank(test)>r0:
            out.append(z); cur.append(z); r0+=1
    return out
H1M=h1_basis(Z27, Bcols27, rB27, 27)
assert len(H1M)==3

# torus H^1 basis (mod coboundaries) as pairs (u,v):
H1T=h1_basis(Zt, Bt, rBt, 27)
assert len(H1T)==h1T

# restriction of an M-cocycle z=(za,zb) to the torus: (z(mu), z(lambda)) = (z(a), z(lam_word))
def restrict(z, dd):
    za=z[:27]; zb=z[27:]
    return za, cocycle_eval(za,zb,lam_word,dd)

# express a torus cocycle pair in coordinates mod torus-coboundaries:
# build matrix [H1T basis | Bt columns]; solve for coefficients of the H1T part
TB=[hb for hb in H1T]+[c for c in Bt]
TBm=[[TB[j][i] for j in range(len(TB))] for i in range(54)]
def torus_coords(u,v):
    vec=u+v
    aug=[TBm[i][:]+[vec[i]] for i in range(54)]
    R,piv=rref(aug)
    ncol=len(TB)
    coords=[ZERO]*h1T
    for i2,c in enumerate(piv):
        if c<h1T: coords[c]=R[i2][ncol]
        if c==ncol: raise RuntimeError("restriction not a torus cocycle?!")
    return coords

# dial
def dial(tval, Xp):
    return nilexp(Xp, tval)
X16_27p=toF(rho27_Q(X16))
X14v=highest_vector(14); X14_27p=toF(rho27_Q(X14v))   # theta-EVEN control slot (exponent 7)
Dt=dial(ONE, X8_27p)
assert mmul(Dt,Amu)==mmul(Amu,Dt) and mmul(Dt,Alam)==mmul(Alam,Dt), "dial must centralize the cusp"

def gal(c): return (c[0]+c[1], -c[1])          # q -> 1-q (the sqrt(-3) Galois = complex conj)
def galmat(M): return [[gal(x) for x in row] for row in M]
def invword(w): return w[::-1].swapcase()

# the mirror vertex rep: galois of the left rep. Edge compatibility (THE convention check):
d27g={k: galmat(v) for k,v in d27.items()}
assert d27g['a']==Amu, "galois must fix the meridian"
assert wordmat(invword(lam_word), d27g)==Alam, "galois(lam^{-1}) must equal lam: the mirror at the cusp"
print("stage 6: mirror rep = Galois twist VERIFIED at the cusp: gal fixes mu, gal(lam^{-1}) = lam")

def mv_h1(tval, Xp, right_dd, right_H1M, right_w0, right_lam_w):
    Dm=dial(tval, Xp)
    rows=[]
    for z in H1M:
        za=z[:27]; zb=z[27:]
        u=za[:]
        v=cocycle_eval(za,zb,lam_word,d27)
        rows.append(torus_coords(u,v))
    for z in right_H1M:
        za=z[:27]; zb=z[27:]
        u=cocycle_eval(za,zb,'a',right_dd)
        v=cocycle_eval(za,zb,right_lam_w,right_dd)
        u=[_dot(Dm[i],u) for i in range(27)]
        v=[_dot(Dm[i],v) for i in range(27)]
        rows.append([fneg(c) for c in torus_coords(u,v)])
    nL=len(H1M)+len(right_H1M)
    Dmat=[[rows[j][i] for j in range(nL)] for i in range(h1T)]
    ker1=nL-rank(Dmat)
    w0R=[_dot(Dm[i],right_w0) for i in range(27)]
    Mu=msub(Amu,I27); Ml=msub(Alam,I27)
    invT=nullspace([[Mu[i][j] for j in range(27)] for i in range(27)]+[[Ml[i][j] for j in range(27)] for i in range(27)])
    pair=[[w0[i], w0R[i]] for i in range(27)]
    rk=rank(pair)
    cok0=len(invT)-rk
    return ker1+cok0, ker1, cok0

invM=nullspace([[msub(A27,I27)[i][j] for j in range(27)] for i in range(27)]
              +[[msub(B27,I27)[i][j] for j in range(27)] for i in range(27)])
assert len(invM)==1
w0=invM[0]
Z27g, Bcols27g, rB27g = fox_h1(d27g, 27)
H1Mg=h1_basis(Z27g, Bcols27g, rB27g, 27)
assert len(H1Mg)==3
invMg=nullspace([[msub(d27g['a'],I27)[i][j] for j in range(27)] for i in range(27)]
               +[[msub(d27g['b'],I27)[i][j] for j in range(27)] for i in range(27)])
w0g=invMg[0]

tvals={'0':ZERO, '1':ONE, '2':frat(2), 'omega':OMEGA}
print("\nstage 6: MAYER-VIETORIS  h^1(D_t;27) = ker(delta^1)+coker(delta^0)")
print(" IDENTITY double (right = same rep), dial slot hv8 (theta-odd):")
line="   "
for name,tv in tvals.items():
    h1D,k1,c0=mv_h1(tv, X8_27p, d27, H1M, w0, lam_word)
    line+=f" t={name}: {h1D} ({k1}+{c0}) |"
print(line)
print(" MIRROR double (right = Galois twist, lam -> lam^{-1}):")
for slotname,Xp in (("hv8  theta-odd ",X8_27p),("hv16 theta-odd ",X16_27p),("hv14 theta-EVEN",X14_27p)):
    line=f"   dial {slotname}:"
    for name,tv in tvals.items():
        h1D,k1,c0=mv_h1(tv, Xp, d27g, H1Mg, w0g, invword(lam_word))
        line+=f" t={name}: {h1D} ({k1}+{c0}) |"
    print(line)

# ---------------- stage 7: the dual 27-bar ----------------
def dualize(Mp):
    n=len(Mp)
    Mi=minv(Mp)
    return [[Mi[j][i] for j in range(n)] for i in range(n)]
d27b={'a':dualize(A27),'b':dualize(B27),'A':dualize(A27i),'B':dualize(B27i)}
def negT(Mp): return [[fneg(Mp[j][i]) for j in range(27)] for i in range(27)]
X8b=negT(X8_27p); X16b=negT(X16_27p); X14b=negT(X14_27p)
Z27b, Bcols27b, rB27b = fox_h1(d27b, 27)
h1Mb=len(Z27b)-rB27b
print(f"\nstage 7: h^1(M;27bar) = {h1Mb} (expect 3)")
Amu, Alam = d27b['a'], wordmat(lam_word, d27b)
Zt,Bt,rBt,h0Tb = h_torus(Amu, Alam)
h1T=len(Zt)-rBt
H1M=h1_basis(Z27b,Bcols27b,rB27b,27)
H1T=h1_basis(Zt,Bt,rBt,27)
TB=[hb for hb in H1T]+[c for c in Bt]
TBm=[[TB[j][i] for j in range(len(TB))] for i in range(54)]
d27=d27b
invMb=nullspace([[msub(d27b['a'],I27)[i][j] for j in range(27)] for i in range(27)]
               +[[msub(d27b['b'],I27)[i][j] for j in range(27)] for i in range(27)])
w0=invMb[0]
d27bg={k: galmat(v) for k,v in d27b.items()}
assert d27bg['a']==Amu and wordmat(invword(lam_word), d27bg)==Alam, "dual mirror cusp check"
Z27bg,Bcols27bg,rB27bg=fox_h1(d27bg,27)
H1Mbg=h1_basis(Z27bg,Bcols27bg,rB27bg,27)
invMbg=nullspace([[msub(d27bg['a'],I27)[i][j] for j in range(27)] for i in range(27)]
                +[[msub(d27bg['b'],I27)[i][j] for j in range(27)] for i in range(27)])
w0bg=invMbg[0]
print("stage 7: 27bar sweeps (PD predicts equality with the 27 rows):")
print(" IDENTITY double, dial hv8:")
line="   "
for name,tv in tvals.items():
    h1D,k1,c0=mv_h1(tv, X8b, d27b, H1M, w0, lam_word)
    line+=f" t={name}: {h1D} ({k1}+{c0}) |"
print(line)
print(" MIRROR double:")
for slotname,Xp in (("hv8  theta-odd ",X8b),("hv16 theta-odd ",X16b),("hv14 theta-EVEN",X14b)):
    line=f"   dial {slotname}:"
    for name,tv in tvals.items():
        h1D,k1,c0=mv_h1(tv, Xp, d27bg, H1Mbg, w0bg, invword(lam_word))
        line+=f" t={name}: {h1D} ({k1}+{c0}) |"
    print(line)

# ---------------- stage 8: adjoint genericity sweep (L79 sub-item i) ----------------
print("\nstage 8: ADJOINT SWEEP — bracket closure of <sl2, Ad_{exp(t ad x)}(sl2)>")
# structure constants of e6 in pair-field
def brF(u,v):
    # u,v: 78-vectors over pair-field; use bilinearity over the rational SC via ccb.br on basis
    # build once: SC as dict (i,j)->sparse vector
    pass
SC={}
for i2 in range(DIM):
    for j2 in range(i2+1,DIM):
        w_=br(basis_ad[i2],basis_ad[j2])
        nz={k2: w_[k2] for k2 in range(DIM) if w_[k2]}
        if nz: SC[(i2,j2)]=nz
def brv(u,v):
    out=[ZERO]*DIM
    nu=[(k2,u[k2]) for k2 in range(DIM) if u[k2]!=ZERO]
    nv=[(k2,v[k2]) for k2 in range(DIM) if v[k2]!=ZERO]
    for (i2,ci) in nu:
        for (j2,cj) in nv:
            if i2==j2: continue
            key=(i2,j2) if i2<j2 else (j2,i2)
            s=SC.get(key)
            if not s: continue
            c=fmul(ci,cj)
            if i2>j2: c=fneg(c)
            for k2,val in s.items():
                out[k2]=fadd(out[k2], fmul(c,(val,F(0))))
    return out
def toFv(v): return [(val,F(0)) for val in v]
def adX(xvec):
    # ad(x) as function on pair-field vectors
    xf=toFv(xvec)
    return lambda v: brv(xf,v)
def closure_dim(gens):
    red=[]; piv=[]
    def reduce_add(v):
        v=v[:]
        for (p,row) in zip(piv,red):
            if v[p]!=ZERO:
                c=v[p]
                v=[fsub(xx,fmul(c,yy)) for xx,yy in zip(v,row)]
        for k2 in range(DIM):
            if v[k2]!=ZERO:
                inv=finv(v[k2])
                red.append([fmul(inv,xx) for xx in v]); piv.append(k2)
                return True
        return False
    basis=[]
    for g in gens:
        if reduce_add(g): basis.append(g)
    frontier=basis[:]
    while frontier and len(piv)<DIM:
        newv=[]
        for u in frontier:
            for v in basis[:]:
                w_=brv(u,v)
                if any(c!=ZERO for c in w_) and reduce_add(w_):
                    basis.append(w_); newv.append(w_)
        frontier=newv
    return len(piv)
def _powf(t,k):
    out=ONE
    for _ in range(k): out=fmul(out,t)
    return out
sl2_gens=[toFv(e6e), toFv(e6f), toFv(e6h)]
for slotname, xv in (("x8 (slot 4)",X8), ("x16 (slot 8)",X16)):
    adx=adX(xv)
    for name,tv in (('1',ONE),('2',frat(2)),('omega',OMEGA)):
        tw=[]
        for g in sl2_gens:
            acc=[c for c in g]; term=[c for c in g]; fact=F(1); sc=ONE
            for k in range(1,40):
                term=adx(term); fact*=k; sc=fmul(sc,tv)
                if all(c==ZERO for c in term): break
                coef=fmul(sc, finv((fact,F(0))))
                acc=[fadd(a, fmul(coef,b)) for a,b in zip(acc,term)]
            tw.append(acc)
        dimc=closure_dim(sl2_gens+tw)
        print(f"  dial {slotname}, t={name}: closure dim = {dimc}"+("  = e6, FULL" if dimc==78 else "  -- DEGENERATION"))
