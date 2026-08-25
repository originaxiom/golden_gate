#!/usr/bin/env python3
"""SIGMA-27 — the beat on the matter module and the dial slots.

Omega := exp(rho27(q E)) o gal  (gal = coefficientwise q -> 1-q; the crystal basis
is rational, so gal is well-defined on the 27).  Verify exactly over Q(q):
 1. Omega^2 = A27  — the tick-square law on MATTER (and A27 != +-1, so the 27 has
    neither a real (Omega^2=+1) nor quaternionic (Omega^2=-1) structure from the
    object: matter reality is the observer's, by the same one-meridian gap).
 2. The 27-rep of Gamma extends to the non-orientable Gamma_G: Omega A27 Omega^-1
    = A27 and Omega B27 Omega^-1 = rho(w(B)) with w(B) = B^-1 A B A^-1 B (the beat
    automorphism; word verified first at the 2x2 holonomy level).
 3. The dial slots are beat-FIXED: Omega rho(X8) Omega^-1 = rho(X8), same for X16
    — so the beat fixes the dial SLOT and (being antilinear) Galois-conjugates the
    dial VALUE t: the L79 mirror (t -> gal t) IS the beat, at the module level.
"""
import importlib.util, itertools, sys
from fractions import Fraction as F
SCR=__import__('os').path.dirname(__import__('os').path.abspath(__file__))+""
src=open(SCR+"/twisted_double.py").read()
cut=src.index("# ---------------- stage 4")
exec(src[:cut])     # field ops, e6, X8/X16, 27 module, A27/B27, nilexp, mmul, eye

def fbar(u): return (u[0]+u[1], -u[1])
def galM(M): return [[fbar(x) for x in row] for row in M]

# 2x2 check of the beat word: W conj(B) W^-1 = B^-1 A B A^-1 B
W2=[[ONE,QQ],[ZERO,ONE]]
def mm2(Aa,Bb):
    return [[fadd(fmul(Aa[0][0],Bb[0][0]),fmul(Aa[0][1],Bb[1][0])), fadd(fmul(Aa[0][0],Bb[0][1]),fmul(Aa[0][1],Bb[1][1]))],
            [fadd(fmul(Aa[1][0],Bb[0][0]),fmul(Aa[1][1],Bb[1][0])), fadd(fmul(Aa[1][0],Bb[0][1]),fmul(Aa[1][1],Bb[1][1]))]]
def mi2(Aa):
    d=fsub(fmul(Aa[0][0],Aa[1][1]),fmul(Aa[0][1],Aa[1][0])); di=finv(d)
    return [[fmul(di,Aa[1][1]),fmul(di,fneg(Aa[0][1]))],[fmul(di,fneg(Aa[1][0])),fmul(di,Aa[0][0])]]
A2=[[ONE,ONE],[ZERO,ONE]]; B2=[[ONE,ZERO],[QQ,ONE]]
lhs=mm2(mm2(W2,galM(B2)),mi2(W2))
rhs=mm2(mm2(mm2(mm2(mi2(B2),A2),B2),mi2(A2)),B2)
print("2x2: W conj(B) W^-1 = B^-1 A B A^-1 B:", lhs==rhs)
assert lhs==rhs

# Omega on the 27
U27=nilexp(E27p, QQ)                    # exp(q rho(E))
U27i=nilexp(E27p, fneg(QQ))
assert mmul(U27,U27i)==eye(27)
# 1. Omega^2 = U27 * gal(U27) = A27
Om2=mmul(U27, galM(U27))
print("27: Omega^2 = A27 (the tick on matter):", Om2==A27)
assert Om2==A27
print("    and A27 != +-1  =>  neither real nor quaternionic structure from the object:",
      A27!=eye(27) and A27!=[[fneg(x) for x in row] for row in eye(27)])

def conjO(M): return mmul(U27, mmul(galM(M), U27i))
# 2. group extension to Gamma_G
print("27: Omega A27 Omega^-1 = A27:", conjO(A27)==A27)
wB=wordmat('BabAb', d27)                # B^-1 A B A^-1 B on the 27
print("27: Omega B27 Omega^-1 = rho(B^-1 A B A^-1 B):", conjO(B27)==wB)
assert conjO(A27)==A27 and conjO(B27)==wB

# 3. dial slots
X16_27p=toF(rho27_Q(X16))
print("27: Omega rho(X8) Omega^-1 = rho(X8)  (dial slot beat-fixed):", conjO(X8_27p)==X8_27p)
print("27: Omega rho(X16) Omega^-1 = rho(X16):", conjO(X16_27p)==X16_27p)
assert conjO(X8_27p)==X8_27p and conjO(X16_27p)==X16_27p
print("\n=> the beat fixes the dial SLOTS and, being antilinear, sends the dial VALUE")
print("   t -> gal(t): the L79 mirror (the Galois twist of the dial) IS the beat,")
print("   now exhibited at the matter-module level; and matter carries no object-side")
print("   real structure — Omega^2 is the tick, one meridian short of a reality.")
