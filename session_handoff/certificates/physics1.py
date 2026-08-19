#!/usr/bin/env python3
"""Step 1: decompose the 27 of E6 under the principal sl2.
Weights of the minuscule 27 = Weyl orbit of omega_1; h_principal eigenvalue of a weight
= 2 * (sum of its coefficients in the simple-root basis)."""
from fractions import Fraction as F
import sys

C=[[2,0,-1,0,0,0],
   [0,2,0,-1,0,0],
   [-1,0,2,-1,0,0],
   [0,-1,-1,2,-1,0],
   [0,0,0,-1,2,-1],
   [0,0,0,0,-1,2]]  # Bourbaki E6 Cartan matrix

# omega_1 in the simple-root basis: solve C^T? For simply-laced, omega_i = sum_j (C^{-1})_{ji} alpha_j.
# Work with weights in the fundamental-weight basis (integer coords), reflect, and convert.
# s_i(lambda)_j = lambda_j - lambda_i * C[i][j]  (weight in omega-basis; <lambda,alpha_i^v> = lambda_i)
def reflect(lam,i):
    li=lam[i]
    return tuple(lam[j]-li*C[i][j] for j in range(6))

start=(1,0,0,0,0,0)  # omega_1
orbit={start}; frontier=[start]
while frontier:
    nf=[]
    for lam in frontier:
        for i in range(6):
            mu=reflect(lam,i)
            if mu not in orbit: orbit.add(mu); nf.append(mu)
    frontier=nf
print("orbit size (should be 27):",len(orbit))
assert len(orbit)==27

# convert omega-basis -> alpha-basis: lambda_alpha = C^{-1 T}? For symmetric C (simply laced): alpha-coeffs a with C a = lambda(omega coords)
# lambda = sum_j a_j alpha_j ; <lambda, alpha_i^v> = sum_j a_j C[j][i] = lam_i  => C^T a = lam; C symmetric -> C a = lam.
import itertools
def solve(Cm,b):
    n=6
    M=[[F(Cm[i][j]) for j in range(n)]+[F(b[i])] for i in range(n)]
    for c in range(n):
        pr=next(r for r in range(c,n) if M[r][c]!=0)
        M[c],M[pr]=M[pr],M[c]
        inv=F(1)/M[c][c]
        M[c]=[x*inv for x in M[c]]
        for r in range(n):
            if r!=c and M[r][c]!=0:
                f=M[r][c]; M[r]=[x-f*y for x,y in zip(M[r],M[c])]
    return [M[i][6] for i in range(6)]

levels={}
for lam in orbit:
    a=solve(C,lam)
    h=2*sum(a)
    assert h.denominator==1 or (h*3).denominator==1
    levels.setdefault(h,0); levels[h]+=1

lv=sorted(levels.items())
print("h-eigenvalue multiplicities:",[(str(k),v) for k,v in lv])
# decompose into sl2 strings: peel from the top
mult=dict(levels)
strings=[]
top=max(mult)
while any(v>0 for v in mult.values()):
    top=max(k for k,v in mult.items() if v>0)
    strings.append(top)
    k=top
    while True:
        mult[k]-=1
        if k==-top: break
        k-=2
strings.sort(reverse=True)
print("principal-sl2 strings in the 27 (highest weights):",strings)
print("=> 27 =",' + '.join(f"Sym^{s}" for s in strings),"; dims",[s+1 for s in strings],"sum",sum(s+1 for s in strings))
ok = strings==[16,8,0]
print("27 = Sym^16 + Sym^8 + Sym^0 :", ok)
sys.exit(0 if ok else 1)
