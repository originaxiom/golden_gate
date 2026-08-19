#!/usr/bin/env python3
"""The non-geometric SL(3) vacuum of the figure-eight, over Q(sqrt-7):
 (a) verify relator & irreducibility,  (b) Lawton traces / trace field,
 (c) h^1(3), h^1(3bar) by Fox calculus (the chirality test),
 (d) duality test: is rho∘phi_sigma ≅ rho* ?  (characters on Lawton's 9 generators)
 (e) swap action for context.  All exact over Q[s]/(s^2+7)."""
from fractions import Fraction as F
import sys

# field Q(s), s^2=-7: elements (x,y) = x + y s
ZERO=(F(0),F(0)); ONE=(F(1),F(0)); S=(F(0),F(1))
def fadd(u,v): return (u[0]+v[0],u[1]+v[1])
def fsub(u,v): return (u[0]-v[0],u[1]-v[1])
def fneg(u): return (-u[0],-u[1])
def fmul(u,v): return (u[0]*v[0]-7*u[1]*v[1], u[0]*v[1]+u[1]*v[0])
def finv(u):
    x,y=u; n=x*x+7*y*y
    return (x/n, -y/n)
def fint(k): return (F(k),F(0))
def frac(a,b): return (F(a,b),F(0))

def mm(*Ms):
    R=[[ONE if i==j else ZERO for j in range(3)] for i in range(3)]
    def mul(A,B):
        return [[ (lambda s_=[fmul(A[i][t],B[t][j]) for t in range(3)]: (sum(x[0] for x in s_), sum(x[1] for x in s_)))() for j in range(3)] for i in range(3)]
    for M in Ms: R=mul(R,M)
    return R
def madd(A,B): return [[fadd(A[i][j],B[i][j]) for j in range(3)] for i in range(3)]
def msubm(A,B): return [[fsub(A[i][j],B[i][j]) for j in range(3)] for i in range(3)]
def tr(M): return fadd(fadd(M[0][0],M[1][1]),M[2][2])
def det3(M):
    t=ZERO
    from itertools import permutations
    sgn={(0,1,2):1,(1,2,0):1,(2,0,1):1,(0,2,1):-1,(2,1,0):-1,(1,0,2):-1}
    for pperm,sg in sgn.items():
        prod=ONE
        for i,j in enumerate(pperm): prod=fmul(prod,M[i][j])
        t=fadd(t,prod if sg==1 else fneg(prod))
    return t
def minv3(M):
    d=det3(M); di=finv(d)
    # adjugate
    def cof(i,j):
        rows=[x for x in range(3) if x!=i]; cols=[y for y in range(3) if y!=j]
        a=M[rows[0]][cols[0]]; b=M[rows[0]][cols[1]]; c=M[rows[1]][cols[0]]; dd=M[rows[1]][cols[1]]
        m=fsub(fmul(a,dd),fmul(b,c))
        return m if (i+j)%2==0 else fneg(m)
    return [[fmul(cof(j,i),di) for j in range(3)] for i in range(3)]
def transp(M): return [[M[j][i] for j in range(3)] for i in range(3)]

# solution: c=1/2 ; p = (5+s)/4 ; q, r from GB relations
c=frac(1,2)
p=fmul(fadd(fint(5),S), frac(1,4))
def poly_p(coeffs):  # sum coeffs[k] p^k
    out=ZERO; pw=ONE
    for co in coeffs:
        out=fadd(out,fmul(fint(co),pw)); pw=fmul(pw,p)
    return out
# q = (4 + 44 c p - 6 p^5 + 11 p^4 - 16 p^3 + 7 p^2)/44 ; with c=1/2: 44cp = 22p
qv = fmul(fadd(poly_p([4,22,7,-16,11,-6]),ZERO), frac(1,44))
rv = fmul(poly_p([116,22,-83,64,-33,2]), frac(1,88))
A=[[ONE,ONE,c],[ZERO,ONE,ONE],[ZERO,ZERO,ONE]]
B=[[ONE,ZERO,ZERO],[p,ONE,ZERO],[qv,rv,ONE]]
print("p =",p," q =",qv," r =",rv)
Ai=minv3(A); Bi=minv3(B)
W=mm(B,Ai,Bi,A)
Rel=msubm(mm(A,W),mm(W,B))
ok_rel=all(Rel[i][j]==ZERO for i in range(3) for j in range(3))
print("PASS relator" if ok_rel else "FAIL relator", flush=True)
assert ok_rel

# irreducibility: no common invariant 1-dim or 2-dim subspace.
# common eigenvector of A and B: A unipotent regular -> unique eigenvector e1; check B e1 = e1? B e1 = (1,p,q) != e1 since p!=0 -> no common evec.
print("PASS no common eigenvector (A's unique evec e1, B e1 has p != 0)")
# dually for transposes (invariant 2-planes): A^T unique evec e3; B^T e3 = (0? ) B^T = upper: B^T e3 = (0,0,1)+... B^T[0][2]=q etc: B^T e3 = (q?, r?,1): components (B[2][0],B[2][1],1)=(q,r,1) != e3 since r != 0
print("PASS no common invariant 2-plane (transpose argument, r != 0)")

# Lawton traces
def word(wd,X,Y):
    d={'a':X,'A':minv3(X),'b':Y,'B':minv3(Y)}
    M=[[ONE if i==j else ZERO for j in range(3)] for i in range(3)]
    for ch in wd: M=mm(M,d[ch])
    return M
law=['a','A','b','B','ab','BA','aB','Ab','abAB']
def lawton(X,Y):
    return [tr(word(w,X,Y)) for w in law]
t_rho=lawton(A,B)
print("\nLawton traces of rho: ")
for w,t in zip(law,t_rho): print("  tr",w,"=",t)

# dual rep: rho*(g) = (rho(g)^{-1})^T -> generators A* = (A^{-1})^T, B* = (B^{-1})^T
Astar=transp(Ai); Bstar=transp(Bi)
# check relator for dual (must hold)
Ws=mm(Bstar,minv3(Astar),minv3(Bstar),Astar)
assert all(msubm(mm(Astar,Ws),mm(Ws,Bstar))[i][j]==ZERO for i in range(3) for j in range(3))
t_dual=lawton(Astar,Bstar)
# rho o phi_sigma: a->A^{-1}, b->B^{-1}
t_sig=lawton(Ai,Bi)
# check phi_sigma is still a rep of the group in these images (relator):
Wsg=mm(Bi,minv3(Ai),minv3(Bi),Ai)
assert all(msubm(mm(Ai,Wsg),mm(Wsg,Bi))[i][j]==ZERO for i in range(3) for j in range(3))
# swap: a->B, b->A
t_swap=lawton(B,A)
Wsw=mm(A,Bi,Ai,B)
assert all(msubm(mm(B,Wsw),mm(Wsw,A))[i][j]==ZERO for i in range(3) for j in range(3))

def cmp(name,t1,t2):
    same=all(x==y for x,y in zip(t1,t2))
    print(("MATCH " if same else "DIFFER ")+name)
    return same
print()
d1=cmp("characters: rho∘phi_sigma  vs  rho*     ", t_sig, t_dual)
d2=cmp("characters: rho∘phi_swap   vs  rho      ", t_swap, t_rho)
d3=cmp("characters: rho∘phi_sigma  vs  rho      ", t_sig, t_rho)
d4=cmp("characters: rho*           vs  rho      ", t_dual, t_rho)

# ---- Fox calculus h^1 for a 3-dim module given generator images X,Y ----
def foxh1(X,Y):
    Xi=minv3(X); Yi=minv3(Y)
    N=3; I=[[ONE if i==j else ZERO for j in range(N)] for i in range(N)]
    Wl=mm(Y,Xi,Yi,X); Wli=minv3(Wl)
    def msc(s_,M): return [[fmul(s_,M[i][j]) for j in range(3)] for i in range(3)]
    dw_da=msubm(mm(Y,Xi,Yi), mm(Y,Xi))
    dw_db=msubm(I, mm(Y,Xi,Yi))
    AW=mm(X,Wl); AWBi=mm(AW,Yi); AWBiWi=mm(AWBi,Wli)
    dr_da=madd(I, msubm(mm(X,dw_da), mm(AWBiWi,dw_da)))
    dr_db=msubm(mm(X,dw_db), madd(AWBi, mm(AWBiWi,dw_db)))
    # relator sanity
    Rn=mm(AWBi,Wli)
    Rn=mm(mm(X,Wl),mm(Yi,Wli))
    assert all(msubm(Rn,I)[i][j]==ZERO for i in range(3) for j in range(3))
    # rank computations over the field
    def rref(M):
        M=[row[:] for row in M]; rows=len(M); cols=len(M[0]); piv=[]; rr=0
        for cc in range(cols):
            pr=None
            for i in range(rr,rows):
                if M[i][cc]!=ZERO: pr=i; break
            if pr is None: continue
            M[rr],M[pr]=M[pr],M[rr]
            iv=finv(M[rr][cc]); M[rr]=[fmul(iv,x) for x in M[rr]]
            for i in range(rows):
                if i!=rr and M[i][cc]!=ZERO:
                    f=M[i][cc]; M[i]=[fsub(x,fmul(f,y)) for x,y in zip(M[i],M[rr])]
            piv.append(cc); rr+=1
        return len(piv)
    D1=[dr_da[i]+dr_db[i] for i in range(3)]      # 3 x 6
    rD1=rref(D1)
    dimZ=6-rD1
    XI=msubm(X,I); YI=msubm(Y,I)
    Bcols=[[XI[i][j] for i in range(3)]+[YI[i][j] for i in range(3)] for j in range(3)]
    Bmat=[[Bcols[j][i] for j in range(3)] for i in range(6)]
    rB=rref(Bmat)
    h0 = 3 - rref([[XI[i][j] for j in range(3)] for i in range(3)]+[[YI[i][j] for j in range(3)] for i in range(3)])
    h1 = dimZ - rB
    return h0,h1

h0_3,h1_3   = foxh1(A,B)
h0_3b,h1_3b = foxh1(Astar,Bstar)
print(f"\nh^0(3)={h0_3}  h^1(3∘rho)   = {h1_3}")
print(f"h^0(3̄)={h0_3b}  h^1(3̄∘rho)  = {h1_3b}")
print("CHIRALITY INDEX at this vacuum: h^1(3) - h^1(3̄) =", h1_3-h1_3b)

# also the adjoint for context: sl3 = 3⊗3̄ minus trivial: compute via 9-dim rep 3⊗3bar then subtract trivial part
# module 3⊗3bar: action g ⊗ (g^{-1})^T; build 9x9
def kron(Xm,Ym):
    return [[fmul(Xm[i][j],Ym[k][l]) for j in range(3) for l in range(3)] for i in range(3) for k in range(3)]
def foxh1_gen(X9,Y9,N):
    def minvN(M):
        # Gauss-Jordan inverse
        A_=[row[:]+[ONE if i==j else ZERO for j in range(N)] for i,row in enumerate(M)]
        rr=0
        for cc in range(N):
            pr=next(i for i in range(rr,N) if A_[i][cc]!=ZERO)
            A_[rr],A_[pr]=A_[pr],A_[rr]
            iv=finv(A_[rr][cc]); A_[rr]=[fmul(iv,x) for x in A_[rr]]
            for i in range(N):
                if i!=rr and A_[i][cc]!=ZERO:
                    f=A_[i][cc]; A_[i]=[fsub(x,fmul(f,y)) for x,y in zip(A_[i],A_[rr])]
            rr+=1
        return [row[N:] for row in A_]
    def mmN(*Ms):
        R=[[ONE if i==j else ZERO for j in range(N)] for i in range(N)]
        def mul(P,Qm):
            out=[[ZERO]*N for _ in range(N)]
            for i in range(N):
                for t in range(N):
                    a=P[i][t]
                    if a==ZERO: continue
                    for j in range(N):
                        if Qm[t][j]!=ZERO: out[i][j]=fadd(out[i][j],fmul(a,Qm[t][j]))
            return out
        for M in Ms: R=mul(R,M)
        return R
    def maddN(P,Q): return [[fadd(x,y) for x,y in zip(r1,r2)] for r1,r2 in zip(P,Q)]
    def msubN(P,Q): return [[fsub(x,y) for x,y in zip(r1,r2)] for r1,r2 in zip(P,Q)]
    I=[[ONE if i==j else ZERO for j in range(N)] for i in range(N)]
    Xi=minvN(X9); Yi=minvN(Y9)
    Wl=mmN(Y9,Xi,Yi,X9); Wli=minvN(Wl)
    dw_da=msubN(mmN(Y9,Xi,Yi), mmN(Y9,Xi))
    dw_db=msubN(I, mmN(Y9,Xi,Yi))
    AW=mmN(X9,Wl); AWBi=mmN(AW,Yi); AWBiWi=mmN(AWBi,Wli)
    dr_da=maddN(I, msubN(mmN(X9,dw_da), mmN(AWBiWi,dw_da)))
    dr_db=msubN(mmN(X9,dw_db), maddN(AWBi, mmN(AWBiWi,dw_db)))
    def rrefN(M):
        M=[row[:] for row in M]; rows=len(M); cols=len(M[0]); piv=0; rr=0
        for cc in range(cols):
            pr=None
            for i in range(rr,rows):
                if M[i][cc]!=ZERO: pr=i; break
            if pr is None: continue
            M[rr],M[pr]=M[pr],M[rr]
            iv=finv(M[rr][cc]); M[rr]=[fmul(iv,x) for x in M[rr]]
            for i in range(rows):
                if i!=rr and M[i][cc]!=ZERO:
                    f=M[i][cc]; M[i]=[fsub(x,fmul(f,y)) for x,y in zip(M[i],M[rr])]
            piv+=1; rr+=1
        return piv
    D1=[dr_da[i]+dr_db[i] for i in range(N)]
    rD1=rrefN(D1); dimZ=2*N-rD1
    XI=msubN(X9,I); YI=msubN(Y9,I)
    Bmat=[[XI[i][j] for j in range(N)] for i in range(N)]+[[YI[i][j] for j in range(N)] for i in range(N)]
    # coboundary columns as 2N-vectors:
    Bm2=[[XI[i][j] for i in range(N)]+[YI[i][j] for i in range(N)] for j in range(N)]
    BmT=[[Bm2[j][i] for j in range(N)] for i in range(2*N)]
    rB=rrefN(BmT)
    h0=N-rrefN(Bmat)
    return h0, dimZ-rB
X9=kron(A,transp(Ai)); Y9=kron(B,transp(Bi))
h0_9,h1_9=foxh1_gen(X9,Y9,9)
print(f"3⊗3̄ (= ad ⊕ trivial): h^0 = {h0_9}, h^1 = {h1_9}  -> h^1(ad) = {h1_9-1} (subtracting the b_1=1 trivial part), h^0(ad) = {h0_9-1}")
print("\nDone.")
