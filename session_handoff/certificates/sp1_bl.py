#!/usr/bin/env python3
"""SP-1 + SP-3: the B-L direction solved from FORCED targets only, and the
cross-closing invariance of the symmetry-point table.

SP-1: seek a Cartan functional f(lam) = sum_j c_j lam_j (lam in simple-root coords)
with (a) f(alpha)=0 for the two color simple roots (commutes with color su(3)),
(b) f(beta_L)=0 (commutes with the kept su(2)); then impose ONLY the forced
targets: f = +1/3 on the 6 Q_L states, -1/3 on the 3 u^c states, +1 on the e^c
state (T3L=0, Q=+1 singlet). Solve exactly; then EVALUATE on all 27 and report
the full multiset — the d^c/D-bar split, the lepton/Higgs pattern, and whether
the result is the physical B-L, all read off rather than imposed.
SP-3: for ALL physical assignments (closing, Y, beta_L) from memo 23: verify the
(color, T3L, Y, Q) table is the SAME multiset, and the 8 anomaly traces vanish.
"""
import itertools
from fractions import Fraction as F
exec(open('g1_yselect.py').read().split("solset=set(sols)")[0])
solset=set(sols)
import sympy as sp
from collections import Counter

def y_eig(y, lam): return sum(y[i]*wt_ip(lam,cor[i]) for i in range(4))
cls=Counter(W4)
colored={i for i,lam in enumerate(weights) if cls[W4[i]]==3}
PHYS={sp.Rational(0),sp.Rational(1,3),sp.Rational(-1,3),sp.Rational(2,3),
      sp.Rational(-2,3),sp.Rational(1),sp.Rational(-1)}

# collect ALL physical assignments
phys_assign=[]
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
            if set(Qs)<=PHYS: phys_assign.append((g,y,bL))
print(f"physical assignments collected: {len(phys_assign)} (expect 36)")

# ---------- SP-3: invariance ----------
tables=set(); anomaly_ok=0
for (g,y,bL) in phys_assign:
    rows=[]
    for i,lam in enumerate(weights):
        t3l=sp.Rational(wt_ip(lam,bL),2); yy=sp.Rational(y_eig(y,lam),6)
        rows.append((i in colored, t3l, yy, t3l+yy))
    tab=frozenset(Counter(rows).items())
    tables.add(tab)
    trs=[sum(r[2] for r in rows), sum(r[2]**3 for r in rows),
         sum(r[1]**2*r[2] for r in rows), sum(r[3] for r in rows), sum(r[3]**3 for r in rows)]
    if all(t==0 for t in trs): anomaly_ok+=1
print(f"SP-3: distinct (color,T3L,Y,Q) tables across all assignments: {len(tables)} (1 = invariant)")
print(f"SP-3: assignments with all five Y/Q anomaly traces zero: {anomaly_ok}/{len(phys_assign)}")

# ---------- SP-1: the B-L solve on one assignment ----------
g,y,bL=phys_assign[0]
def state_rows():
    out=[]
    for i,lam in enumerate(weights):
        t3l=sp.Rational(wt_ip(lam,bL),2); yy=sp.Rational(y_eig(y,lam),6)
        out.append((i,lam,i in colored,t3l,yy,t3l+yy))
    return out
rows=state_rows()
# forced targets
targets=[]
for i,lam,col,t3l,yy,q in rows:
    if col and yy==sp.Rational(1,6): targets.append((lam, sp.Rational(1,3)))       # Q_L
    if col and yy==sp.Rational(-2,3): targets.append((lam, sp.Rational(-1,3)))     # u^c
    if (not col) and t3l==0 and q==1: targets.append((lam, sp.Rational(1)))        # e^c
print(f"SP-1: forced targets imposed: {len(targets)} (expect 10 = 6+3+1)")
cvars=sp.symbols('c0:6')
eqs=[]
# commutation constraints: vanish on color simple roots (a0, a2 tuples) and beta_L
for alpha in (a0, tuple(1 if k==2 else 0 for k in range(6)), bL):
    eqs.append(sum(cvars[j]*alpha[j] for j in range(6)))
for lam,tval in targets:
    eqs.append(sum(cvars[j]*sp.Rational(lam[j]) for j in range(6)) - tval)
sol=sp.solve(eqs, list(cvars), dict=True)
print("SP-1: solvable:", bool(sol), " solutions:", len(sol) if sol else 0)
if sol:
    s=sol[0]
    cval=[sp.nsimplify(s.get(v, v)) for v in cvars]
    free=[v for v in cvars if v in [x for x in cval if hasattr(x,'free_symbols') for x in x.free_symbols]]
    # if underdetermined, report; evaluate B-L on all 27 (symbolic if free vars remain)
    print("SP-1: c =", cval)
    blvals=Counter()
    table=[]
    for i,lam,col,t3l,yy,q in rows:
        bl=sp.simplify(sum(cval[j]*sp.Rational(lam[j]) for j in range(6)))
        table.append((col,str(t3l),str(yy),str(q),str(bl)))
    for k,v in sorted(Counter(table).items()):
        print(f"   colored={k[0]!s:5s} T3L={k[1]:>4s} Y={k[2]:>5s} Q={k[3]:>5s} B-L={k[4]:>8s} x{v}")
    # physical B-L verdict
    allbl=[sp.simplify(sum(cval[j]*sp.Rational(lam[j]) for j in range(6))) for i,lam,col,t3l,yy,q in rows]
    if not any(getattr(b,'free_symbols',set()) for b in allbl):
        ok=all((b in (sp.Rational(1,3),sp.Rational(-1,3),sp.Rational(2,3),sp.Rational(-2,3))) if col
               else (b in (sp.Rational(1),sp.Rational(-1),sp.Rational(0)))
               for (i,lam,col,t3l,yy,q),b in zip(rows,allbl))
        print("SP-1: B-L multiset PHYSICAL on all 27:", ok)
        print("SP-1: Tr(B-L) =", sum(allbl), "  Tr(B-L)^3 =", sum(b**3 for b in allbl))
        # express B-L in the closing's coordinates: components along Y, T3R(beta candidates), rest
        zs=[r for r in list(G1c)+list(G2c) if sum(y[i]*iprr(cor[i],r) for i in range(4))==0]
        bRs=[r for r in zs if (r in G1c)!=(bL in G1c)]
        if bRs:
            bR=bRs[0]
            t3r=[sp.Rational(wt_ip(lam,bR),2) for i,lam,col,t3l,yy,q in rows]
            yv=[yy for i,lam,col,t3l,yy,q in rows]
            # least-squares style exact decomposition attempt: B-L = a*Y + b*T3R + residual?
            av,bv=sp.symbols('av bv')
            import itertools as it2
            # solve on two independent states, then check globally
            solved=None
            for (idx1,idx2) in it2.combinations(range(27),2):
                Mm=sp.Matrix([[yv[idx1],t3r[idx1]],[yv[idx2],t3r[idx2]]])
                if Mm.det()!=0:
                    ab=Mm.solve(sp.Matrix([allbl[idx1],allbl[idx2]]))
                    if all(sp.simplify(ab[0]*yv[k]+ab[1]*t3r[k]-allbl[k])==0 for k in range(27)):
                        solved=(ab[0],ab[1]); break
            print("SP-1: B-L = a*Y + b*T3R exactly?", f"YES with (a,b)=({solved[0]},{solved[1]})" if solved else "NO — B-L is an independent Cartan direction (needs a third generator)")
