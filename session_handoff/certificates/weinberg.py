#!/usr/bin/env python3
"""THE SYMMETRY-POINT WEINBERG ANGLE — the first SM-facing NUMBER the closing emits.

PREREGISTERED EXPECTATION (declared before the run): if the closing-selected
hypercharge Y and closing-kept su(2) reproduce the standard E6 embedding, then
  charges Q = T3 + Y/6 over the 27 form the physical multiset, and
  sin^2(theta_W) at the symmetry point = Tr(T3^2)/Tr(Q^2) = 3/8.
The TEST: does the object's closing produce this with ZERO free choices, and is it
the SAME for all 9 generic gauge closings (closing-independence = forcedness)?
Gate-5-safe: no measured value enters; 3/8 is group theory.

Data: the banked machinery of memo 13 (g1_yselect): the 18 Y's, the 16 gauge
involutions, the selected pairs; T3 from the su(2) root beta the selected Y
annihilates (one per EW slot — both tried, tagged); Y_phys = (6Y-eigenvalue)/6.
"""
import itertools
from fractions import Fraction as F
exec(open(__import__('os').path.dirname(__import__('os').path.abspath(__file__))+'/g1_yselect.py').read().split("solset=set(sols)")[0])
solset=set(sols)
import sympy as sp

def y_eig(y, lam):  # integer eigenvalue of Y = sum y_i h_{cor_i} on weight lam
    return sum(y[i]*wt_ip(lam,cor[i]) for i in range(4))

def analyze(y, beta):
    """charges and sin^2 for hypercharge y and su(2) root beta."""
    T3s=[]; Qs=[]
    for lam in weights:
        t3=sp.Rational(wt_ip(lam,beta),2)
        yy=sp.Rational(y_eig(y,lam),6)
        T3s.append(t3); Qs.append(t3+yy)
    from collections import Counter
    qm=Counter(Qs)
    sumT3=sum(t*t for t in T3s); sumQ=sum(q*q for q in Qs)
    s2w=sp.Rational(sumT3,1)/sumQ if sumQ else None
    # physical multiset check: charges must all be in {0, +-1/3, +-2/3, +-1}
    phys=set(qm)<= {sp.Rational(0),sp.Rational(1,3),sp.Rational(-1,3),sp.Rational(2,3),
                    sp.Rational(-2,3),sp.Rational(1),sp.Rational(-1)}
    return dict(qm), sumT3, sumQ, s2w, phys

results=[]
for g in FP:
    ok=False
    for c in solve_lift(g):
        if slot_sig(g,c,sorted(S0),(a0,a2))!=(0,8): continue
        if slot_sig(g,c,sorted(G1c),p1)==(4,4) and slot_sig(g,c,sorted(G2c),p2)==(4,4):
            ok=True; break
    if not ok: continue
    M4=cartan_mat4(g)
    anti=[y for y in sols if tuple(-x for x in y)==tuple(sum(M4[i,j]*y[j] for j in range(4)) for i in range(4)) ]
    if len(anti)!=2: continue   # generic closings only
    for y in anti:
        zs=[r for r in list(G1c)+list(G2c) if sum(y[i]*iprr(cor[i],r) for i in range(4))==0]
        # the four annihilated roots = +-beta1, +-beta2; pick positive representatives
        betas=[]
        for r in zs:
            if tuple(-x for x in r) not in [tuple(b) for b in betas]:
                betas.append(r)
        betas=betas[:2] if len(betas)>=2 else betas
        for b in zs:
            qm,sT,sQ,s2w,phys=analyze(y,b)
            results.append((s2w,phys,qm,sT,sQ))
from collections import Counter
tally=Counter((r[0],r[1]) for r in results)
print(f"(closing, selected-Y, su(2)-choice) combinations analyzed: {len(results)}")
print("outcomes (sin^2 theta_W at symmetry point, physical-charge-multiset?):")
for (s2w,phys),cnt in sorted(tally.items(), key=lambda kv:str(kv[0])):
    print(f"   sin^2 = {s2w}   physical charges: {phys}   x{cnt}")
# show one physical example in full
for s2w,phys,qm,sT,sQ in results:
    if phys:
        print("\nexample PHYSICAL assignment:")
        print("  charge multiset:", {str(k):v for k,v in sorted(qm.items(), key=lambda kv: kv[0])})
        print(f"  Tr T3^2 = {sT}   Tr Q^2 = {sQ}   sin^2 theta_W = {s2w}")
        break
phys_vals={r[0] for r in results if r[1]}
print(f"\nVERDICT: physical assignments occur: {any(r[1] for r in results)}; "
      f"their sin^2 values: {sorted(map(str,phys_vals))}")
print("closing-independence:", "YES — single value" if len(phys_vals)==1 else "NO — varies")
