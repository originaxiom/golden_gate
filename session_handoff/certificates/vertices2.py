#!/usr/bin/env python3
"""Verify the vertex structure of m004/(Z2xZ2) exactly."""
from fractions import Fraction as F
import itertools, cmath, sys

def fadd(u,v): return (u[0]+v[0], u[1]+v[1])
def fneg(u): return (-u[0], -u[1])
def fmul(u,v):
    x1,y1=u; x2,y2=v
    a=x1*x2; b=x1*y2+y1*x2; c=y1*y2
    return (a-c, b+c)
def finv(u):
    x,y=u; n=x*x+x*y+y*y
    return ((x+y)/n, -y/n)
ZERO=(F(0),F(0)); ONE=(F(1),F(0)); Q=(F(0),F(1))
def mmul(A,B):
    return (fadd(fmul(A[0],B[0]),fmul(A[1],B[2])), fadd(fmul(A[0],B[1]),fmul(A[1],B[3])),
            fadd(fmul(A[2],B[0]),fmul(A[3],B[2])), fadd(fmul(A[2],B[1]),fmul(A[3],B[3])))
def det(A): return fadd(fmul(A[0],A[3]),fneg(fmul(A[1],A[2])))
def tr(A): return fadd(A[0],A[3])
def minv2(A):
    d=det(A); di=finv(d)
    return (fmul(A[3],di),fmul(fneg(A[1]),di),fmul(fneg(A[2]),di),fmul(A[0],di))
def msc(c,A): return tuple(fmul(c,x) for x in A)
def proj_eq(A,B):
    # equal in PGL: A = c B
    for i in range(4):
        if B[i]!=ZERO:
            c = fmul(A[i], finv(B[i]))
            return all(A[j]==fmul(c,B[j]) for j in range(4))
    return False

Am=(ONE,ONE,ZERO,ONE); Bm=(ONE,ZERO,Q,ONE)
nt=(ZERO,ONE,Q,ZERO)           # swap
ns=(ONE,ZERO,ZERO,(F(-1),F(0))) # inversion
ok=True
def check(s,c):
    global ok
    print(("PASS " if c else "FAIL ")+s)
    ok = ok and c

check("n_tau A n_tau^-1 = B", proj_eq(mmul(mmul(nt,Am),minv2(nt)), Bm))
check("n_tau B n_tau^-1 = A", proj_eq(mmul(mmul(nt,Bm),minv2(nt)), Am))
check("n_sig A n_sig^-1 = A^-1", proj_eq(mmul(mmul(ns,Am),minv2(ns)), minv2(Am)))
check("n_sig B n_sig^-1 = B^-1", proj_eq(mmul(mmul(ns,Bm),minv2(ns)), minv2(Bm)))
check("n_tau^2 = 1 in PGL", proj_eq(mmul(nt,nt),(ONE,ZERO,ZERO,ONE)))
check("n_sig^2 = 1 in PGL", proj_eq(mmul(ns,ns),(ONE,ZERO,ZERO,ONE)))
check("[n_tau, n_sig] = 1 in PGL", proj_eq(mmul(nt,ns), msc((F(-1),F(0)), mmul(ns,nt)) ) or proj_eq(mmul(nt,ns),mmul(ns,nt)))
p = mmul(ns,nt)
check("tr(n_sig n_tau) = 0  (third involution)", tr(p)==ZERO)
# common fixed point: axis of ns = vertical over 0; axis of nt = semicircle over +-q^{-1/2}, apex over 0 height |q|^{-1/2}=1
qc = complex(0.5, 3**0.5/2)
print("|q| =", abs(qc), " -> apex of n_tau axis at (z=0, height 1) which lies on n_sig axis: intersection point p0=(0,1)")

# find the axis-holonomy of the closed geodesic: primitive W in Gamma with n_tau W n_tau^{-1} = W (same axis)
# search words in A,B up to length 8
gens={'a':Am,'A':minv2(Am),'b':Bm,'B':minv2(Bm)}
def wval(w):
    M=(ONE,ZERO,ZERO,ONE)
    for ch in w: M=mmul(M,gens[ch])
    return M
best=[]
import itertools as it
alph='aAbB'
found=[]
for L in range(1,7):
    for wt in it.product(alph,repeat=L):
        w=''.join(wt)
        # skip words with immediate cancellation
        bad=False
        for i in range(L-1):
            if (w[i].lower()==w[i+1].lower()) and (w[i]!=w[i+1]): bad=True; break
        if bad: continue
        W=wval(w)
        C=mmul(mmul(nt,W),minv2(nt))
        if proj_eq(C,W):
            t=tr(W)
            tc = t[0]+t[1]*complex(0.5,3**0.5/2)
            if abs(tc.real)>2 or abs(tc.imag)>1e-12:  # loxodromic (non-identity)
                if W!=(ONE,ZERO,ZERO,ONE):
                    found.append((L,w,t,tc))
    if found: break
for L,w,t,tc in found[:6]:
    # complex length: tr = 2 cosh(Lc/2)
    Lc = 2*cmath.acosh(tc/2)
    print(f"gamma candidate '{w}' tr = {t[0]}+{t[1]}q = {tc:.6f}, complex length = {Lc.real:.6f} + {Lc.imag:.6f} i")
# compare with m004 shortest geodesic
try:
    import snappy
    Msn=snappy.Manifold("m004")
    sp_=Msn.length_spectrum(1.5)
    print("m004 length spectrum below 1.5:", [(s.length, s.multiplicity) for s in sp_] if sp_ else sp_)
except Exception as e:
    print("snappy check skipped:",e)

# second vertex: sigma reverses the closed geodesic; on its circle the reversal has 2 fixed pts:
# p0 and the half-translation point, fixed by sigma*gamma; verify sigma*gamma is an involution for the found gamma
if found:
    L,w,t,tc=found[0]
    W=wval(w)
    h=mmul(ns,W)
    print("tr(n_sig * gamma) =", tr(h), " -> involution iff 0:", tr(h)==ZERO)
    h2=mmul(nt if False else mmul(ns,W),(ONE,ZERO,ZERO,ONE))
    # also check sigma' = ns*nt version
    h3=mmul(mmul(ns,nt),W)
    print("tr(n_sig n_tau * gamma) =", tr(h3), " -> involution iff 0:", tr(h3)==ZERO)
print("OVERALL:", "PASS" if ok else "ISSUES")
