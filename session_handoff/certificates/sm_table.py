#!/usr/bin/env python3
"""THE SYMMETRY-POINT TABLE — the closing's complete one-generation quantum numbers.

From a PHYSICAL closing assignment (memo 23: charges come out physical), with zero
further choices: T3L (kept su(2), root beta_L), T3R (the OTHER annihilated root,
beta_R), Y_phys = (6Y-eigenvalue)/6, Q = T3L + Y_phys, and the DERIVED
   B-L := 2(Y_phys - T3R)     [the Pati-Salam relation Y/2 = T3R + (B-L)/2]
Checks, all exact:
 1. the (color, T3L, T3R, Y, Q, B-L) table of all 27 states — quarks/leptons/Higgs/
    exotics classified by color content (size-3 wt4-classes = triplets);
 2. B-L multiset physical: colored states at +-1/3 (quarks) or -+2/3 (exotics),
    singlets at -+1 (leptons) or 0 (Higgs/singlet);
 3. the anomaly table: Tr Y, Tr Y^3, Tr(T3L^2 Y), Tr Q, Tr Q^3, Tr(B-L),
    Tr(B-L)^3 over the 27 (exact rationals).
"""
import itertools
from fractions import Fraction as F
exec(open('g1_yselect.py').read().split("solset=set(sols)")[0])
solset=set(sols)
import sympy as sp
from collections import Counter

def y_eig(y, lam): return sum(y[i]*wt_ip(lam,cor[i]) for i in range(4))

# find one physical assignment (as in memo 23)
found=None
for g in FP:
    ok=False
    for c in solve_lift(g):
        if slot_sig(g,c,sorted(S0),(a0,a2))!=(0,8): continue
        if slot_sig(g,c,sorted(G1c),p1)==(4,4) and slot_sig(g,c,sorted(G2c),p2)==(4,4):
            ok=True; break
    if not ok: continue
    M4=cartan_mat4(g)
    anti=[y for y in sols if tuple(-x for x in y)==tuple(sum(M4[i,j]*y[j] for j in range(4)) for i in range(4))]
    if len(anti)!=2: continue
    for y in anti:
        zs=[r for r in list(G1c)+list(G2c) if sum(y[i]*iprr(cor[i],r) for i in range(4))==0]
        for bL in zs:
            Qs=[sp.Rational(wt_ip(lam,bL),2)+sp.Rational(y_eig(y,lam),6) for lam in weights]
            if set(Qs)<= {sp.Rational(0),sp.Rational(1,3),sp.Rational(-1,3),sp.Rational(2,3),
                          sp.Rational(-2,3),sp.Rational(1),sp.Rational(-1)}:
                # beta_R = an annihilated root in the OTHER slot from bL
                slotL = G1c if bL in G1c else G2c
                bRs=[r for r in zs if (r in G1c)!=(bL in G1c)]
                for bR in bRs:
                    found=(g,y,bL,bR); break
            if found: break
        if found: break
    if found: break
assert found
g,y,bL,bR=found
print("physical assignment located: Y =",tuple(int(v) for v in y),
      " beta_L in", "S1" if bL in G1c else "S2", " beta_R in", "S1" if bR in G1c else "S2")
# color classes (B1102: size-3 wt4-classes = color triplets, color = S0)
cls=Counter(W4)
colored={i for i,lam in enumerate(weights) if cls[W4[i]]==3}
rows=[]
for i,lam in enumerate(weights):
    t3l=sp.Rational(wt_ip(lam,bL),2); t3r=sp.Rational(wt_ip(lam,bR),2)
    yy=sp.Rational(y_eig(y,lam),6); q=t3l+yy; bl=2*(yy-t3r)
    rows.append((i in colored, t3l, t3r, yy, q, bl))
# 2. B-L physicality
ok_bl=all((bl in (sp.Rational(1,3),sp.Rational(-1,3),sp.Rational(2,3),sp.Rational(-2,3))) if col
          else (bl in (sp.Rational(1),sp.Rational(-1),sp.Rational(0))) for col,_,_,_,_,bl in rows)
print("B-L multiset physical (colored: +-1/3 or +-2/3; singlets: +-1 or 0):", ok_bl)
mult=Counter((col,str(t3l),str(t3r),str(yy),str(q),str(bl)) for col,t3l,t3r,yy,q,bl in rows)
print("\nTHE TABLE (color?, T3L, T3R, Y, Q, B-L) : count")
for k,v in sorted(mult.items()):
    print(f"  colored={k[0]!s:5s} T3L={k[1]:>4s} T3R={k[2]:>4s} Y={k[3]:>5s} Q={k[4]:>5s} B-L={k[5]:>5s}  x{v}")
# 3. anomaly table
def tr(f): return sum(f(r) for r in rows)
print("\nANOMALY TABLE (exact):")
print("  Tr Y      =", tr(lambda r: r[3]))
print("  Tr Y^3    =", tr(lambda r: r[3]**3))
print("  Tr T3L^2 Y=", tr(lambda r: r[1]**2*r[3]))
print("  Tr Q      =", tr(lambda r: r[4]))
print("  Tr Q^3    =", tr(lambda r: r[4]**3))
print("  Tr (B-L)  =", tr(lambda r: r[5]))
print("  Tr (B-L)^3=", tr(lambda r: r[5]**3))
print("  Tr T3R^2 Y=", tr(lambda r: r[2]**2*r[3]))
