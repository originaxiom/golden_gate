#!/usr/bin/env python3
"""Path 2: the Acharya-Witten reading of the flat G2 cone (C^2 x R^3)/G-hat.
Deliverables, all exact:
  S1. every fixed subspace of every nontrivial element (dims already known: {3,1});
  S2. the distinct singular strata, grouped into G-hat-orbits (= loci in the quotient);
  S3. the POINTWISE stabilizer H(V) of each stratum, its structure, and — for the
      codim-4 (3d) strata — its ADE type = the gauge algebra along that locus;
  S4. associativity check: fixed 3-planes of G2-isometries must be associative
      (phi(v1,v2,v3)^2 = Gram det); verified per stratum;
  S5. the enhancement poset: which 3d loci contain which 1d lines, what the line
      stabilizers are, and the apex where all meet (stabilizer = G-hat, order 96);
  S6. the chirality-relevant geometry: does the cone meet the AW criterion
      (codim-7 point where codim-4 ADE loci of DIFFERENT types collide)?
"""
import sympy as sp
import sys
from itertools import combinations

s2 = sp.sqrt(2)

def qmat_left(q):
    a,b,c,d = q
    return sp.Matrix([[a,-b,-c,-d],[b,a,-d,c],[c,d,a,-b],[d,-c,b,a]])
def qmat_right(q):
    a,b,c,d = q
    return sp.Matrix([[a,-b,-c,-d],[b,a,d,-c],[c,-d,a,b],[d,c,-b,a]])

Ri=qmat_right((0,1,0,0)); Rj=qmat_right((0,0,1,0)); Rk=qmat_right((0,0,0,1))
def two_form(M): return (M - M.T)/2
WR=[two_form(Ri),two_form(Rj),two_form(Rk)]

def action_on_triplet(M, Ws):
    A=sp.zeros(3,3)
    for i in range(3):
        P=sp.expand(M.T*Ws[i]*M)
        un=sp.symbols('c0:3')
        Rm=P - (un[0]*Ws[0]+un[1]*Ws[1]+un[2]*Ws[2])
        sol=sp.solve([e for e in Rm], list(un), dict=True)
        if not sol: return None
        for j in range(3): A[i,j]=sp.nsimplify(sol[0][un[j]])
    return A

u=( sp.Rational(1,2), sp.Rational(1,2), sp.Rational(1,2), sp.Rational(1,2) )
w=( 1/s2, 1/s2, 0, 0 )
gens={}
gens['t1'] = ('L', u, None)
gens['t2'] = ('L', (0,1,0,0), None)
gens['g_tau']   = ('R', (0,1,0,0), None)
gens['g_sigma'] = ('RL', (0,0,0,1), w)

def seven(gen):
    kind, r, l = gen
    if kind=='L':
        M4 = qmat_left(r); R3 = sp.eye(3)
    elif kind=='R':
        M4 = qmat_right(r); R3 = action_on_triplet(qmat_right(r), WR)
    else:
        M4 = qmat_left(l)*qmat_right(r)
        R3 = action_on_triplet(qmat_right(r), WR)
    M=sp.zeros(7,7); M[0:3,0:3]=R3; M[3:7,3:7]=M4
    return sp.Matrix(M)

def key(M): return tuple(sp.nsimplify(sp.simplify(x)) for x in M)
I7 = sp.eye(7)
Ms=[seven(g) for g in gens.values()]
seen={key(I7): I7}
frontier=[I7]
while frontier:
    nf=[]
    for X in frontier:
        for Gg in Ms:
            Y=sp.expand(X*Gg).applyfunc(sp.nsimplify)
            k2=key(Y)
            if k2 not in seen: seen[k2]=Y; nf.append(Y)
    frontier=nf
els=list(seen.values())
print("group order:", len(els)); assert len(els)==96
nontriv=[M for M in els if M != I7]

# ---------- S1/S2: fixed subspaces, canonical keys, orbits ----------
def spankey(vs):
    A = sp.Matrix.hstack(*vs).T
    Rr, piv = A.rref()
    rows=[tuple(sp.nsimplify(sp.radsimp(x)) for x in Rr.row(i)) for i in range(len(piv))]
    return tuple(rows)

spaces={}          # skey -> basis (list of column vectors)
fixers={}          # skey -> list of elements whose full fix-space IS this space
for M in nontriv:
    ns=(M-I7).nullspace()
    sk=spankey(ns)
    spaces.setdefault(sk, ns)
    fixers.setdefault(sk, []).append(M)

print("distinct fixed subspaces:", len(spaces),
      " by dim:", {d: sum(1 for v in spaces.values() if len(v)==d) for d in (1,3)})

# pointwise stabilizer of a subspace
def pstab(basis):
    out=[]
    for M in els:
        okk=True
        for v in basis:
            dv=sp.expand(M*v - v).applyfunc(sp.nsimplify)
            if any(x != 0 for x in dv): okk=False; break
        if okk: out.append(M)
    return out

# orbits of subspaces under G-hat
def orbit_of(sk, basis):
    orb={sk}
    for M in els:
        gb=[sp.expand(M*v).applyfunc(sp.nsimplify) for v in basis]
        orb.add(spankey(gb))
    return orb

# group-structure helpers
def mat_order(M):
    P=M; o=1
    while P != I7:
        P=sp.expand(P*M).applyfunc(sp.nsimplify); o+=1
        assert o<=96
    return o
def structure(H):
    n=len(H)
    orders={}
    for M in H:
        if M==I7: o=1
        else: o=mat_order(M)
        orders[o]=orders.get(o,0)+1
    ab=all(key(sp.expand(A*B))==key(sp.expand(B*A)) for A in H for B in H)
    return n, orders, ab
def ade_label(n, orders, ab):
    if ab:
        return f"A_{n-1} (cyclic Z_{n})" if orders.get(n,0)>0 else f"abelian非cyclic order {n}"
    # binary dihedral BD_m has order 4m, a cyclic Z_2m, elements of order 2m
    if n==8  and orders=={1:1,2:1,4:6}: return "D_4 (quaternion Q8 = BD_2)"
    if n==24 and orders.get(6,0)==8 and orders.get(12,0)==0: return "E_6 (binary tetrahedral 2T)"
    if n==24 and orders.get(12,0)>0: return "D_8 (BD_6)"
    if n==16 and orders.get(8,0)>0: return "D_6 (BD_4)"
    if n==12 and orders.get(6,0)>0 and orders.get(4,0)>0: return "D_5 (BD_3)"
    if n==48: return "E_7 (2O)?"
    return f"order {n}, orders {orders}, nonabelian — classify by hand"

# phi as trilinear form (from g2cone): phi = dx012 + sum_i dx_i ^ w_i (right triplet)
phi={}
phi[(0,1,2)]=sp.Integer(1)
for i in range(3):
    Wf=WR[i]
    for a in range(4):
        for b in range(a+1,4):
            c=2*Wf[a,b]
            if c!=0:
                idx=tuple(sorted((i,3+a,3+b)))
                phi[idx]=phi.get(idx,0)+c
def phi_eval(v1,v2,v3):
    tot=sp.Integer(0)
    V=sp.Matrix.hstack(v1,v2,v3)
    for (i,j,k2),c in phi.items():
        d=sp.det(sp.Matrix([[V[i,0],V[i,1],V[i,2]],[V[j,0],V[j,1],V[j,2]],[V[k2,0],V[k2,1],V[k2,2]]]))
        tot+=c*d
    return sp.nsimplify(sp.radsimp(sp.expand(tot)))
def gram_det(vs):
    # phi's mixed terms carry coefficient 2, so phi is the STANDARD G2 form for the
    # metric g = dx_R3^2 + 2 dx_H^2 (check: phi(e0,e1,e2)=1=vol; phi(e0,e5,e6)=2=vol
    # since |e5|^2=|e6|^2=2). Associativity test must use THIS Gram, not Euclid's.
    gmet = sp.diag(1,1,1,2,2,2,2)
    Gm=sp.Matrix(3,3, lambda i,j: sp.expand((vs[i].T*gmet*vs[j])[0,0]))
    return sp.nsimplify(sp.radsimp(sp.det(Gm)))

# ---------- process 3d strata ----------
seen_orbit=set(); orbit_reports=[]
for sk, basis in spaces.items():
    if len(basis)!=3 or sk in seen_orbit: continue
    orb=orbit_of(sk, basis)
    seen_orbit |= orb
    H=pstab(basis)
    n,orders,ab=structure(H)
    lab=ade_label(n,orders,ab)
    # associativity: phi(v1,v2,v3)^2 == Gram det
    p=phi_eval(*basis); gd=gram_det(basis)
    assoc = sp.simplify(p**2 - gd)==0
    orbit_reports.append((len(orb), n, lab, assoc, sk))
print("\nS3: codim-4 (3d) strata — gauge loci   [orbit size = # of planes in R^7 mapping to ONE locus in the quotient]")
for size,n,lab,assoc,sk in sorted(orbit_reports, key=lambda t:-t[1]):
    print(f"  locus: orbit of {size} plane(s) | pointwise stabilizer order {n} | ADE: {lab} | associative: {assoc}")

# ---------- 1d lines ----------
seen_orbit1=set(); line_reports=[]
for sk, basis in spaces.items():
    if len(basis)!=1 or sk in seen_orbit1: continue
    orb=orbit_of(sk, basis)
    seen_orbit1 |= orb
    H=pstab(basis)
    n,orders,ab=structure(H)
    # which 3d strata contain this line? (line basis vector in the 3-space)
    containers=[]
    v=basis[0]
    for sk3, b3 in spaces.items():
        if len(b3)!=3: continue
        A=sp.Matrix.hstack(*b3, v)
        if A.rank()==3: containers.append(sk3)
    line_reports.append((len(orb), n, orders, ab, len(containers)))
print("\nS5: codim-6 (1d) lines — enhancement loci")
for size,n,orders,ab,nc in sorted(line_reports, key=lambda t:-t[1]):
    print(f"  line-locus: orbit of {size} line(s) | stabilizer order {n} (orders {orders}, abelian={ab}) | contained in {nc} 3d planes")

# ---------- apex ----------
n,orders,ab=structure(els)
print(f"\nS5b: apex (the cone point): stabilizer = G-hat, order {n}, element orders {orders}, abelian={ab}")

# ---------- S6: the AW criterion ----------
types={lab for _,_,lab,_,_ in orbit_reports}
print("\nS6: Acharya-Witten criterion — codim-7 point where codim-4 ADE loci of DIFFERENT types meet:")
print(f"   distinct gauge types meeting at the apex: {types}")
print(f"   criterion {'MET' if len(types)>=2 else 'NOT met'}: the apex is "
      f"{'an AW-type collision point' if len(types)>=2 else 'a single-type cone point'}")
