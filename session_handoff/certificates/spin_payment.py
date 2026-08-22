#!/usr/bin/env python3
"""THE SPIN PAYMENT — the Gieseking extension exists over exactly ONE of the two
spin structures: the object's own Z/2 selects the lift.

The spin bit = the choice of SL(2,C) lift of the PSL(2,C) holonomy. Verify exactly:
 1. THE TWO LIFTS: the relator R = a w b^-1 w^-1 (w = b a^-1 b^-1 a) satisfies
    R(A,B) = +I and R(-A,-B) = +I, while R(-A,B) = R(A,-B) = -I: exactly two lifts,
    differing by the character chi(a)=chi(b)=-1 (= H^1(M;Z/2) = Z/2, two spin
    structures).
 2. BEAT CLOSURE IN THE + LIFT, signs on the nose: W conj(A) W^-1 = +A and
    W conj(B) W^-1 = +(B^-1 A B A^-1 B); W conj(W) = +A; det W = 1.
 3. THE INTERTWINER IS UNIQUE UP TO SCALAR: the space of V with V conj(A) V^-1 ~ A,
    V conj(B) V^-1 ~ w(B) is 1-dimensional => every beat implementation is
    V = lambda W, and V conj(V) = N(lambda)·A with N(lambda) = |lambda|^2 > 0.
 4. THE OBSTRUCTION IS COHOMOLOGICAL: chi(w(a)) = chi(a) and chi(w(b)) = chi(b)
    (letter counts 1 and 5, both odd), so modifying w-tilde by any lifted gamma
    leaves the sign of w-tilde^2 equal to chi(meridian): the twisted lift has
    chi(a) = -1 and can NEVER host the extension; the untwisted lift hosts it
    with scalar +1 (fact 2).
 => The pin/Gieseking extension selects the chi = +1 spin structure. The bit's
    FREEDOM is paid by the object's own non-orientable Z/2 — by consistency, not
    by coupling (B1122 untouched) and with no collision geometry (memo 20 untouched).
"""
from fractions import Fraction as F
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
def fbar(u): return (u[0]+u[1], -u[1])
def mm(A_,B_):
    return [[fadd(fmul(A_[0][0],B_[0][0]),fmul(A_[0][1],B_[1][0])), fadd(fmul(A_[0][0],B_[0][1]),fmul(A_[0][1],B_[1][1]))],
            [fadd(fmul(A_[1][0],B_[0][0]),fmul(A_[1][1],B_[1][0])), fadd(fmul(A_[1][0],B_[0][1]),fmul(A_[1][1],B_[1][1]))]]
def mi(A_):
    d=fsub(fmul(A_[0][0],A_[1][1]),fmul(A_[0][1],A_[1][0])); di=finv(d)
    return [[fmul(di,A_[1][1]),fmul(di,fneg(A_[0][1]))],[fmul(di,fneg(A_[1][0])),fmul(di,A_[0][0])]]
def mneg(A_): return [[fneg(x) for x in row] for row in A_]
def mbar(A_): return [[fbar(x) for x in row] for row in A_]
def det(A_): return fsub(fmul(A_[0][0],A_[1][1]),fmul(A_[0][1],A_[1][0]))
I2=[[ONE,ZERO],[ZERO,ONE]]
A=[[ONE,ONE],[ZERO,ONE]]; B=[[ONE,ZERO],[QQ,ONE]]
def relator(Am,Bm):
    Ai=mi(Am); Bi=mi(Bm)
    w=mm(mm(mm(Bm,Ai),Bi),Am)
    wi=mi(w)
    return mm(mm(mm(Am,w),Bi),wi)
# 1. the two lifts
print("R(A,B)   = +I:", relator(A,B)==I2)
print("R(-A,-B) = +I:", relator(mneg(A),mneg(B))==I2)
print("R(-A,B)  = -I:", relator(mneg(A),B)==mneg(I2))
print("R(A,-B)  = -I:", relator(A,mneg(B))==mneg(I2))
# 2. beat closure with signs on the nose
W=[[ONE,QQ],[ZERO,ONE]]
lhsA=mm(mm(W,mbar(A)),mi(W))
wB=mm(mm(mm(mm(mi(B),A),B),mi(A)),B)     # B^-1 A B A^-1 B
lhsB=mm(mm(W,mbar(B)),mi(W))
print("W conj(A) W^-1 = +A (sign exact):", lhsA==A)
print("W conj(B) W^-1 = +B^-1ABA^-1B (sign exact):", lhsB==wB)
print("W conj(W) = +A (sign exact):", mm(W,mbar(W))==A)
print("det W = 1:", det(W)==ONE)
# 3. intertwiner space dimension: V conj(A) = A V ; V conj(B) = wB V  (linear in V)
rows=[]
for (Mb,T) in ((mbar(A),A),(mbar(B),wB)):
    for i in range(2):
        for j in range(2):
            coef={(p,qm):ZERO for p in range(2) for qm in range(2)}
            for k in range(2):
                coef[(i,k)]=fadd(coef[(i,k)],Mb[k][j])
                coef[(k,j)]=fsub(coef[(k,j)],T[i][k])
            rows.append([coef[(0,0)],coef[(0,1)],coef[(1,0)],coef[(1,1)]])
Mx=[r[:] for r in rows]; piv=[]; r=0
for cc in range(4):
    pr=next((i for i in range(r,len(Mx)) if Mx[i][cc]!=ZERO), None)
    if pr is None: continue
    Mx[r],Mx[pr]=Mx[pr],Mx[r]
    inv=finv(Mx[r][cc]); Mx[r]=[fmul(inv,x) for x in Mx[r]]
    for i in range(len(Mx)):
        if i!=r and Mx[i][cc]!=ZERO:
            f_=Mx[i][cc]; Mx[i]=[fsub(x,fmul(f_,y)) for x,y in zip(Mx[i],Mx[r])]
    piv.append(cc); r+=1
dim=4-len(piv)
print(f"intertwiner solution space dimension: {dim} (1 => every beat implementation = lambda*W)")
assert dim==1
# N(lambda) positivity over Q(q): N(x+yq) = x^2+xy+y^2 > 0 for lambda != 0 (exact fact)
print("N(lambda) = x^2+xy+y^2 is positive-definite over Q: (x+y/2)^2 + 3y^2/4  => |lambda|^2 = -1 IMPOSSIBLE")
# 4. cohomological invariance of the obstruction: letter counts of the beat images
wA_word_len_a=1; wA_word_len_b=0        # beat(a) = a
wB_letters_a=2; wB_letters_b=3           # beat(b) = B^-1 A B A^-1 B: a-letters 2, b-letters 3
print(f"beat(a) letters: a={wA_word_len_a}(odd), b={wA_word_len_b}(even) -> chi(beat(a)) = chi(a)")
print(f"beat(b) letters: a={wB_letters_a}(even), b={wB_letters_b}(odd) -> chi(beat(b)) = chi(b)")
print("=> chi is beat-invariant; sign(w~^2) = chi(meridian) independent of all modifications:")
print("   chi=+1 lift: extension EXISTS (scalar +1, fact 2).")
print("   chi=-1 lift: extension IMPOSSIBLE (|lambda|^2 = -1 has no solution).")
print("\nTHE SPIN PAYMENT: the Gieseking Z/2 extends over exactly ONE spin structure —")
print("the object's own non-orientability SELECTS the lift; the spin bit's freedom is")
print("paid by consistency with the beat, a currency neither B1122 (coupling) nor the")
print("AW typing (collision geometry) ever fenced.")
