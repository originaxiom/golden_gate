#!/usr/bin/env python3
"""SP-2: THE SEAT — does the beat close on the FERMION-CAPABLE (odd) stratum's
matter representation over the selected chi=+1 lift?

The A1 stratum (minimal nilpotent, e = e_r): 27-weights under h_r are {-1,0,+1} —
ODD weights present, so the stratum rep does NOT factor through PSL(2,C): the two
lifts give genuinely different matter reps, differing by the central element
C = rho(-I) = diag((-1)^wt) != I.  The structural claim to verify: the beat lives
at the SL(2,C) level, upstream of the embedding — W = exp(q e_2x2), so
Omega_A1 = exp(rho(q e)) o gal should close FUNCTORIALLY on the odd stratum over
the chi=+1 lift.  Verify exactly:
  1. weights of h_r on the 27: multiset {+1:6, 0:15, -1:6} (odd: B1112's A1 row);
  2. relator R(A27,B27) = +I (genuine SL-rep) and C = exp(i pi h)-analog: the
     central element diag((-1)^wt) satisfies C != I, C^2 = I, C commutes with the
     rep — the two lifts differ exactly by C (oddness has content);
  3. THE HINGE: Omega = exp(rho(q e)) o gal on the 27:
       Omega^2 = A27 (the chi=+1 lifted meridian),
       Omega A27 Omega^-1 = A27,
       Omega B27 Omega^-1 = rho(w(B)) = B27^-1 A27 B27 A27^-1 B27  — all exact.
  => the beat closes on the fermion-capable stratum over the selected lift:
     the generation's kinematic seat CLOSES (chi=-1 needs no rep-level check:
     the GROUP extension already fails there, memo 28).
"""
import importlib.util, sys
from fractions import Fraction as F
SCR="/tmp/claude-0/-home-user-golden-gate/7aec077f-59a6-5129-b1a7-361cc5dcb800/scratchpad"
src=open(SCR+"/twisted_double.py").read()
cut=src.index("# ---------------- stage 4")
exec(src[:cut])          # field ops + e6 + 27 module (rho27_Q verified on 3003 brackets)

# A1 embedding: pick a root r; e = e_r, h = h_r, f = -e_{-r}  ([e_r,e_{-r}] = -h_r)
r0=ROOTS[0]
eA=evec(r0)
hA=[F(0)]*DIM
for k in range(N): hA[k]=F(r0[k])
fA=smul_(-1, evec(tuple(-x for x in r0)))
assert br(eA,fA)==hA and br(hA,eA)==smul_(2,eA) and br(hA,fA)==smul_(-2,fA)
E27=rho27_Q(eA); F27=rho27_Q(fA); H27=rho27_Q(hA)
# 1. weight multiset
from collections import Counter
wts=Counter()
for i in range(27): wts[H27[i][i]]+=1
print("A1 stratum 27-weights:", dict(wts), "(expect {1:6, 0:15, -1:6} — ODD)")
assert dict(wts)=={F(1):6, F(0):15, F(-1):6}
# 2. group rep + central element
E27p=toF(E27); F27p=toF(F27)
A27=nilexp(E27p, ONE); B27=nilexp(F27p, QQ)
A27i=nilexp(E27p, fneg(ONE)); B27i=nilexp(F27p, fneg(QQ))
d27={'a':A27,'A':A27i,'b':B27,'B':B27i}
Rel=wordmat('a'+'bABa'+'B'+'AbaB', d27)
print("relator = +I on the A1 matter rep:", Rel==eye(27))
Cm=[[ (F(-1) if (i==j and H27[i][i]%2!=0) else (F(1) if i==j else F(0)), F(0)) for j in range(27)] for i in range(27)]
CI = Cm==eye(27)
C2 = mmul(Cm,Cm)==eye(27)
comm = mmul(Cm,A27)==mmul(A27,Cm) and mmul(Cm,B27)==mmul(B27,Cm)
print(f"central element C = diag((-1)^wt): C != I: {not CI}; C^2 = I: {C2}; commutes with rep: {comm}")
print("=> the two lifts give genuinely DIFFERENT matter reps (differ by C): oddness certified")
# 3. THE HINGE
def fbar(u): return (u[0]+u[1], -u[1])
def galM(M): return [[fbar(x) for x in row] for row in M]
U=nilexp(E27p, QQ); Ui=nilexp(E27p, fneg(QQ))
Om2=mmul(U, galM(U))
print("Omega^2 = A27 (chi=+1 lifted meridian):", Om2==A27)
def conjO(M): return mmul(U, mmul(galM(M), Ui))
okA = conjO(A27)==A27
wB=wordmat('BabAb', d27)
okB = conjO(B27)==wB
print("Omega A27 Omega^-1 = A27:", okA)
print("Omega B27 Omega^-1 = rho(B^-1 A B A^-1 B):", okB)
assert Rel==eye(27) and Om2==A27 and okA and okB
print("\nSP-2 GREEN: the beat closes on the fermion-capable (odd) A1 stratum over the")
print("selected chi=+1 lift — functorially, because W = exp(q e) lives upstream of every")
print("embedding. The chi=-1 side needs no rep-level check: the GROUP extension already")
print("fails there (memo 28). THE GENERATION'S KINEMATIC SEAT CLOSES.")
