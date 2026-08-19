#!/usr/bin/env python3
"""Equivariant Z2xZ2 signs on H^1(Q; Sym^n) — fast exact arithmetic over Q[q]/(q^2-q+1).
Field elements: (Fraction x, Fraction y) = x + y q,  q^2 = q - 1,  q^{-1} = 1 - q."""
from fractions import Fraction as F
import sys

ZERO=(F(0),F(0)); ONE=(F(1),F(0)); QQ=(F(0),F(1))
def fadd(u,v): return (u[0]+v[0], u[1]+v[1])
def fsub(u,v): return (u[0]-v[0], u[1]-v[1])
def fneg(u): return (-u[0],-u[1])
def fmul(u,v):
    a=u[0]*v[0]; b=u[0]*v[1]+u[1]*v[0]; c=u[1]*v[1]
    return (a-c, b+c)
def finv(u):
    x,y=u; n=x*x+x*y+y*y
    return ((x+y)/n, -y/n)
def fint(k): return (F(k),F(0))

# --- generic matrix ops (lists of lists of field elements) ---
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
            Bt=B[t]
            Ci=C[i]
            for j in range(m):
                if Bt[j]!=ZERO: Ci[j]=fadd(Ci[j], fmul(a,Bt[j]))
    return C
def madd(A,B): return [[fadd(x,y) for x,y in zip(r,s)] for r,s in zip(A,B)]
def msub(A,B): return [[fsub(x,y) for x,y in zip(r,s)] for r,s in zip(A,B)]
def msc(c,A): return [[fmul(c,x) for x in r] for r in A]

def rref(M):
    """Return (rref matrix, pivot columns). M: list of rows (copies made)."""
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
                f=M[i][c]
                M[i]=[fsub(x,fmul(f,y)) for x,y in zip(M[i],M[r])]
        piv.append(c); r+=1
        if r==rows: break
    return M,piv

def nullspace(M):
    R,piv=rref(M)
    cols=len(M[0])
    free=[c for c in range(cols) if c not in piv]
    basis=[]
    for fc in free:
        v=[ZERO]*cols; v[fc]=ONE
        for i,c in enumerate(piv):
            v[c]=fneg(R[i][fc])
    # careful: need R row i entries at fc
        basis.append(v)
    return basis
def rank(M):
    _,piv=rref(M)
    return len(piv)
def colstack(*mats):
    # horizontal stack of column-lists? here mats are lists of column vectors -> matrix with those columns
    cols=[]
    for m in mats: cols.extend(m)
    n=len(cols[0])
    return [[cols[j][i] for j in range(len(cols))] for i in range(n)]

# --- 2x2 base matrices ---
def m2mul(A,B):
    return ((fadd(fmul(A[0],B[0]),fmul(A[1],B[2])), fadd(fmul(A[0],B[1]),fmul(A[1],B[3]))),
            (fadd(fmul(A[2],B[0]),fmul(A[3],B[2])), fadd(fmul(A[2],B[1]),fmul(A[3],B[3]))))[0]+\
           ((fadd(fmul(A[2],B[0]),fmul(A[3],B[2])), fadd(fmul(A[2],B[1]),fmul(A[3],B[3]))))
def m2(A,B):
    return (fadd(fmul(A[0],B[0]),fmul(A[1],B[2])), fadd(fmul(A[0],B[1]),fmul(A[1],B[3])),
            fadd(fmul(A[2],B[0]),fmul(A[3],B[2])), fadd(fmul(A[2],B[1]),fmul(A[3],B[3])))
def m2inv(A):
    d=fsub(fmul(A[0],A[3]),fmul(A[1],A[2])); di=finv(d)
    return (fmul(A[3],di),fmul(fneg(A[1]),di),fmul(fneg(A[2]),di),fmul(A[0],di))
Am=(ONE,ONE,ZERO,ONE); Bm=(ONE,ZERO,QQ,ONE)
NT=(ZERO,ONE,QQ,ZERO); NS=(ONE,ZERO,ZERO,fneg(ONE))

# Sym^n of a 2x2 (a,b,c,d) acting on x^{n-k}y^k: need polynomial expansion; do with integer conv over field
from math import comb
def symrep(M,n):
    if n==0: return [[ONE]]
    a,b,c,d = M
    # column k: coeffs of (a x + c y)^{n-k} (b x + d y)^k in basis x^{n-j} y^j
    S=mat(n+1,n+1)
    # precompute powers
    def powlist(u,mx):
        out=[ONE]
        for _ in range(mx): out.append(fmul(out[-1],u))
        return out
    pa=powlist(a,n); pb=powlist(b,n); pc=powlist(c,n); pd=powlist(d,n)
    for k in range(n+1):
        # (a x + c y)^{n-k} = sum_i C(n-k,i) a^{n-k-i} c^i x^{n-k-i} y^i
        # (b x + d y)^k     = sum_l C(k,l)   b^{k-l}   d^l x^{k-l}   y^l
        for i in range(n-k+1):
            ci=fmul(fint(comb(n-k,i)), fmul(pa[n-k-i],pc[i]))
            if ci==ZERO: continue
            for l in range(k+1):
                cl=fmul(fint(comb(k,l)), fmul(pb[k-l],pd[l]))
                if cl==ZERO: continue
                j=i+l  # power of y
                S[j][k]=fadd(S[j][k], fmul(ci,cl))
    return S

def compute(n):
    An=symrep(Am,n); Bn=symrep(Bm,n)
    Ai=symrep(m2inv(Am),n); Bi=symrep(m2inv(Bm),n)
    N=n+1; I=eye(N)
    W2=m2(m2(m2(Bm,m2inv(Am)),m2inv(Bm)),Am)
    Wn=symrep(W2,n); Wninv=symrep(m2inv(W2),n)
    dw_da=msub(mmul(Bn,mmul(Ai,Bi)), mmul(Bn,Ai))
    dw_db=msub(I, mmul(Bn,mmul(Ai,Bi)))
    AW=mmul(An,Wn); AWBi=mmul(AW,Bi); AWBiWi=mmul(AWBi,Wninv)
    dr_da=madd(I, msub(mmul(An,dw_da), mmul(AWBiWi,dw_da)))
    dr_db=msub(mmul(An,dw_db), madd(AWBi, mmul(AWBiWi,dw_db)))
    # sanity: relator acts as I
    Rn=mmul(AWBi,Wninv)
    Rn=mmul(mmul(An,Wn),mmul(Bi,Wninv))
    assert Rn==I, f"relator not I at n={n}"
    # Z = nullspace of [dr_da | dr_db]  (N x 2N)
    D1=[dr_da[i]+dr_db[i] for i in range(N)]
    Z=nullspace(D1)
    # coboundary columns: (An - I)e_j stacked over (Bn - I)e_j
    Bcols=[]
    AnI=msub(An,I); BnI=msub(Bn,I)
    for j in range(N):
        col=[AnI[i][j] for i in range(N)]+[BnI[i][j] for i in range(N)]
        Bcols.append(col)
    Bmat=[[Bcols[j][i] for j in range(N)] for i in range(2*N)]
    rB=rank(Bmat)
    h1=len(Z)-rB
    # generator z0 of H1: z in Z with rank([B z]) > rank(B)
    z0=None
    for z in Z:
        aug=[[Bcols[j][i] for j in range(N)]+[z[i]] for i in range(2*N)]
        if rank(aug)>rB: z0=z; break
    assert z0 is not None
    va=z0[:N]; vb=z0[N:]
    def colvec(v): return [[x] for x in v]
    def flat(Mcol): return [r[0] for r in Mcol]
    results={}
    for which in ('tau','sigma','sigmatau'):
        if which=='tau':
            T=symrep(NT,n); Ti=None
            # T^{-1} via symrep of inverse
            Ti=symrep(m2inv(NT),n)
            wa=flat(mmul(Ti,colvec(vb))); wb=flat(mmul(Ti,colvec(va)))
            # normalization: det NT = -q ; divide lambda by (-q)^{n/2}
            det=fneg(QQ)
        elif which=='sigma':
            Ti=symrep(m2inv(NS),n)
            wa=flat(mmul(Ti,mmul(msc(fneg(ONE),Ai),colvec(va))))
            wb=flat(mmul(Ti,mmul(msc(fneg(ONE),Bi),colvec(vb))))
            det=fneg(ONE)
        else:
            NST=m2(NS,NT)   # sigma*tau: a->b^-1, b->a^-1
            Ti=symrep(m2inv(NST),n)
            wa=flat(mmul(Ti,mmul(msc(fneg(ONE),Bi),colvec(vb))))
            wb=flat(mmul(Ti,mmul(msc(fneg(ONE),Ai),colvec(va))))
            det=QQ
        img=wa+wb
        # solve img = lam*z0 + B*u : unknowns lam, u (N+1); equations 2N
        # build augmented system columns: [z0, Bcols...] ; solve linear system
        Acols=[z0]+Bcols
        Am_=[[Acols[j][i] for j in range(len(Acols))] for i in range(2*N)]
        # solve Am_ * (lam,u) = img via rref of [Am_ | img]
        aug=[Am_[i]+[img[i]] for i in range(2*N)]
        R,piv=rref(aug)
        # check consistency and extract lam (variable 0)
        ncols=len(Acols)
        lam=None
        for i,c in enumerate(piv):
            if c==0: lam=R[i][ncols]; break
        if lam is None:
            lam=ZERO
        # normalize: T_hat^{-1} = det^{n/2} * Sym^n(N^{-1}), so lam_norm = lam_raw * det^{n/2}
        p=ONE
        for _ in range(n//2): p=fmul(p,det)
        lamn=fmul(lam,p)
        results[which]=lamn
    return h1, results

print(f"{'block':8}{'h1':>4}{'tau':>12}{'sigma':>12}{'sigma*tau':>12}{'consistent':>12}")
table={}
for n in (2,8,10,14,16,22):
    h1,res=compute(n)
    def show(v):
        return "+1" if v==ONE else ("-1" if v==fneg(ONE) else str(v))
    table[n]=(res['tau'],res['sigma'])
    prod=fmul(res['tau'],res['sigma'])
    cons = "OK" if prod==res['sigmatau'] else "MISMATCH"
    print(f"Sym^{n:<4}{h1:>4}{show(res['tau']):>12}{show(res['sigma']):>12}{show(res['sigmatau']):>12}{cons:>12}")
    sys.stdout.flush()
table[0]=(ONE,fneg(ONE))
print(f"Sym^0   {1:>4}{'+1':>12}{'-1':>12}   (trivial block: sigma reverses the meridian)")
adj=[2,8,10,14,16,22]; gen=[16,8,0]
sa=[n for n in adj if table[n]==(ONE,ONE)]
sg=[n for n in gen if table[n]==(ONE,ONE)]
print("\nsurviving adjoint moduli:", len(sa), "of 6 ", sa)
print("surviving 27-generation modes:", len(sg), "of 3 ", sg)
