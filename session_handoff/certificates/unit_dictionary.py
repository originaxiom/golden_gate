#!/usr/bin/env python3
"""PR-2: THE UNIT DICTIONARY — geodesics <-> units of (quadratic extensions of) Q(sqrt-3).

For gamma in Gamma with trace t in Z[omega] (automatic: A,B in SL2(Z[q])), the
eigenvalue lam satisfies lam^2 - t lam + 1 = 0, and its Q-minimal polynomial divides
   P_{T,N}(x) = x^4 - T x^3 + (N+2) x^2 - T x + 1,   T = Tr_{K/Q}(t), N = N_{K/Q}(t)
— PALINDROMIC with constant term 1: every loxodromic eigenvalue is an ALGEBRAIC UNIT,
and the geodesic is labeled by TWO RATIONAL INTEGERS (T, N).  Moreover
   length(gamma) = 2 log|lam| = log (Mahler measure of P_{T,N})
— the exact 'log p <-> length' entry of the prime-geodesic dictionary.

Census: all cyclically-reduced words to length 8 (up to rotation/inversion, deduped
by (T,N)); verify the quartic identity EXACTLY per class; verify the Mahler-length
identity numerically; tabulate the splitting data N(t^2-4) and its rational prime
factors (split/inert/ramified in Q(sqrt-3) by p mod 3).
"""
import itertools, cmath
from fractions import Fraction as F
ZERO=(F(0),F(0)); ONE=(F(1),F(0)); QQ=(F(0),F(1))
def fadd(u,v): return (u[0]+v[0], u[1]+v[1])
def fmul(u,v):
    a=u[0]*v[0]; b=u[0]*v[1]+u[1]*v[0]; c=u[1]*v[1]
    return (a-c, b+c)
def fbar(u): return (u[0]+u[1], -u[1])
def mm(A,B):
    return [[fadd(fmul(A[0][0],B[0][0]),fmul(A[0][1],B[1][0])), fadd(fmul(A[0][0],B[0][1]),fmul(A[0][1],B[1][1]))],
            [fadd(fmul(A[1][0],B[0][0]),fmul(A[1][1],B[1][0])), fadd(fmul(A[1][0],B[0][1]),fmul(A[1][1],B[1][1]))]]
Am=[[ONE,ONE],[ZERO,ONE]]; Bm=[[ONE,ZERO],[QQ,ONE]]
def inv2(M):
    # SL2: inverse = adjugate
    return [[M[1][1],(-M[0][1][0],-M[0][1][1])],[(-M[1][0][0],-M[1][0][1]),M[0][0]]]
GEN={'a':Am,'b':Bm,'A':inv2(Am),'B':inv2(Bm)}
def wordmat(w):
    M=[[ONE,ZERO],[ZERO,ONE]]
    for ch in w: M=mm(M,GEN[ch])
    return M
def cyc_reduced(w):
    if any(w[i]+w[(i+1)%len(w)] in ('aA','Aa','bB','Bb') for i in range(len(w))): return False
    return True
def canon(w):
    """canonical form under rotation and inversion"""
    invmap={'a':'A','A':'a','b':'B','B':'b'}
    cands=[]
    for ww in (w, ''.join(invmap[c] for c in reversed(w))):
        for i in range(len(ww)): cands.append(ww[i:]+ww[:i])
    return min(cands)
seen=set(); classes=[]
for L in range(1,9):
    for tup in itertools.product('abAB',repeat=L):
        w=''.join(tup)
        if not cyc_reduced(w): continue
        c=canon(w)
        if c in seen: continue
        seen.add(c); classes.append(c)
print(f"cyclically-reduced classes (rotation+inversion) to length 8: {len(classes)}")
qc=complex(0.5, 3**0.5/2)   # q = e^{i pi/3}
def fnum(u): return u[0]+u[1]*qc
results={}
fails_quartic=0; nlox=0
mahler_err_max=0.0
for w in classes:
    M=wordmat(w)
    t=fadd(M[0][0],M[1][1])
    T2=t[0]*2+t[1]        # Tr(t) = t + tbar : (x+yq)+(x+y(1-q)) = 2x+y
    Nt=t[0]*t[0]+t[0]*t[1]+t[1]*t[1]   # norm
    # loxodromic iff |trace| != 2 as complex and not real-elliptic; skip identity/parabolic
    tc=fnum(t)
    if abs(tc-2)<1e-12 or abs(tc+2)<1e-12 or abs(tc)<1e-12 and False: continue
    if abs(tc.imag)<1e-12 and abs(tc.real)<=2+1e-12: continue   # elliptic/parabolic
    nlox+=1
    # EXACT quartic check: lam^2 = t lam - 1; check P(lam)=0 symbolically via
    # P(x) = (x^2 - t x + 1)(x^2 - tbar x + 1) expansion identity over Z[omega]:
    tb=fbar(t)
    # expand (x^2 - t x + 1)(x^2 - tb x + 1) = x^4 -(t+tb)x^3 + (t*tb + 2)x^2 - (t+tb)x + 1
    s=fadd(t,tb); p=fmul(t,tb)
    okq = (s[1]==0 and p[1]==0 and s[0]==T2 and p[0]==Nt)
    if not okq: fails_quartic+=1
    # Mahler measure of P_{T,N} vs geodesic length: 2 log|lam|
    T=float(T2); N=float(Nt)
    # roots of x^2 - t x + 1 numerically
    lam=(tc+cmath.sqrt(tc*tc-4))/2
    if abs(lam)<1: lam=(tc-cmath.sqrt(tc*tc-4))/2
    ell=2*abs(cmath.log(abs(lam)))
    # Mahler measure of quartic: product of |roots|>1
    import numpy as np
    rts=np.roots([1,-T,N+2,-T,1])
    Mh=1.0
    for r in rts:
        if abs(r)>1: Mh*=abs(r)
    err=abs(ell - abs(cmath.log(Mh)))
    mahler_err_max=max(mahler_err_max,err)
    key=(T2,Nt)
    if key not in results: results[key]=(w, t)
print(f"loxodromic classes: {nlox}; distinct (T,N) labels: {len(results)}")
print(f"EXACT quartic identity x^4 - T x^3 + (N+2) x^2 - T x + 1 (constant term 1 => UNIT): "
      f"{'PASS all' if fails_quartic==0 else f'FAIL {fails_quartic}'}")
print(f"length = log Mahler(P_TN): max |error| over census = {mahler_err_max:.2e}")
# splitting table: disc = t^2-4, N(disc), rational prime factorization, split type mod 3
def factorint(n):
    n=abs(n); out={}
    d=2
    while d*d<=n:
        while n%d==0: out[d]=out.get(d,0)+1; n//=d
        d+=1
    if n>1: out[n]=out.get(n,0)+1
    return out
print("\nfirst entries of the dictionary (shortest word per (T,N) label):")
print(f"{'word':10s} {'T':>4s} {'N':>4s} {'N(t^2-4)':>10s}  prime factors [p mod 3: 1=split, 2=inert, 3=ram]")
shown=0
for (T2,Nt),(w,t) in sorted(results.items(), key=lambda kv:(len(kv[1][0]),kv[0])):
    d=fadd(fmul(t,t),(F(-4),F(0)))
    Nd=d[0]*d[0]+d[0]*d[1]+d[1]*d[1]
    fac=factorint(int(Nd)) if Nd!=0 else {}
    lab=", ".join(f"{p}^{e}[{p%3 if p!=3 else 'ram'}]" for p,e in sorted(fac.items()))
    print(f"{w:10s} {int(T2):>4} {int(Nt):>4} {int(Nd):>10}  {lab}")
    shown+=1
    if shown>=18: break
