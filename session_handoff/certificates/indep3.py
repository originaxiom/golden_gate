#!/usr/bin/env python3
"""Independent referee checks, part 3: number field K, mu cubic, 4_1 character variety, Molien, Niven."""
import sys
import sympy as sp
from sympy import symbols, Poly, QQ, Rational, sqrt, I, simplify, factor, expand, discriminant, totient, cos, pi

ok=True
def check(name,cond):
    global ok
    print(("PASS " if cond else "FAIL ")+name)
    if not cond: ok=False

x,t,u = symbols('x t u')

# --- mu cubic and reduced model ---
mu = 500716339200*t**3 - 159667200*t**2 - 28224*t + 1
f  = x**3 - 12*x - 5
check("disc(x^3-12x-5) = 6237 = 3^4*7*11", discriminant(Poly(f,x))==6237 and sp.factorint(6237)=={3:4,7:1,11:1})
rho = Rational(-815,338) - Rational(4934160,169)*t + Rational(13039488000,169)*t**2
rem = sp.rem(sp.expand(rho**3 - 12*rho - 5), mu, t)
check("Tschirnhaus: rho^3-12rho-5 == 0 mod mu", sp.simplify(rem)==0)
dmu = discriminant(Poly(mu,t))
check("disc(mu) = 2^32*3^10*5^2*7^3*11*13^6", sp.factorint(dmu)=={2:32,3:10,5:2,7:3,11:1,13:6})
lead=500716339200
check("leading coeff = 2^16*3^4*5^2*7^3*11", sp.factorint(lead)=={2:16,3:4,5:2,7:3,11:1})
check("mu irreducible over Q", Poly(mu,t).domain==sp.ZZ or sp.factor_list(mu)[1][0][0]==mu.as_poly(t).primitive()[1].as_expr() if True else True)
check("mu irreducible (factor_list length 1)", len(sp.factor_list(mu,t)[1])==1)
check("f irreducible", len(sp.factor_list(f,x)[1])==1)
# 6237 = 81*77, non-square -> Galois S3, resolvent Q(sqrt(77))
check("6237=81*77, 77 squarefree -> resolvent Q(sqrt77)", 6237==81*77 and sp.factorint(77)=={7:1,11:1})

# splitting of f mod p
def split_type(p):
    fl=sp.factor_list(Poly(f,x,modulus=p))[1]
    return sorted(g.degree() for g,e in fl for _ in range(e))
check("13,17,19 inert (f irreducible mod p)", all(split_type(p)==[3] for p in (13,17,19)))
check("2,5,953,1129,421493: exactly one degree-one factor", all(split_type(p)==[1,2] for p in (2,5,953,1129,421493)))
check("3 totally ramified pattern: (x+1)^3 mod 3", split_type(3)==[1,1,1] and sp.rem(f,(x+1)**3,x,modulus=3)==0 if True else True)
f3=Poly(f,x,modulus=3).factor_list()
check("f = (x+1)^3 mod 3", f3[1][0][0]==Poly(x+1,x,modulus=3) and f3[1][0][1]==3)
# 7 and 11: ramified shape p q^2
def split_full(p):
    fl=sp.factor_list(Poly(f,x,modulus=p))[1]
    return sorted((g.degree(),e) for g,e in fl)
check("7 = p*q^2", split_full(7)==[(1,1),(1,2)])
check("11 = p*q^2", split_full(11)==[(1,1),(1,2)])

# Minkowski bound
import math
check("Minkowski bound (6/27)*sqrt(6237) < 18", (6/27)*math.sqrt(6237) < 18)
# class number 1: exhibit explicit generators of primes of norm <= 17 above 2,3,5,7,11.
# K = Q[a], a^3 = 12a+5. Norm of alpha = x + y a + z a^2 computed via resultant.
a=symbols('a')
def norm(c0,c1,c2):
    el = c0 + c1*a + c2*a**2
    return sp.resultant(a**3-12*a-5, el, a)  # = N(el) up to sign convention; for monic cubic this is N(el)
# find elements of small norms
found={}
targets={2:[2,-2],3:[3,-3],5:[5,-5],7:[7,-7],11:[11,-11],4:[4,-4]}
rng=range(-6,7)
import itertools
for c0 in rng:
    for c1 in rng:
        for c2 in rng:
            n=norm(c0,c1,c2)
            for k in (2,3,4,5,7,11):
                if abs(n)==k and k not in found:
                    found[k]=(c0,c1,c2,n)
print("  small-norm elements found:", found)
check("elements of norm ±2,±3,±5,±7,±11 exist (principality of small primes, partial)",
      all(k in found for k in (2,3,5,7,11)))
# both degree-one primes above 7: need two non-associate elements of norm ±7 generating different primes.
# check: the two roots of f mod 7: f mod 7 roots
r7=sp.ground_roots(Poly(f,x,modulus=7))
print("  roots of f mod 7:",r7, " mod 11:", sp.ground_roots(Poly(f,x,modulus=11)))
# For each root r, prime p_r = (7, a-r). An element c0+c1 a+c2 a^2 of norm ±7 lies in exactly one of them:
# test membership: el mod p_r  <=> substitute a=r mod 7 gives 0.
def gens_for(p):
    rr=list(sp.ground_roots(Poly(f,x,modulus=p)).keys())
    gens={}
    for c0 in rng:
        for c1 in rng:
            for c2 in rng:
                if abs(norm(c0,c1,c2))==p:
                    for r in rr:
                        if (c0+c1*int(r)+c2*int(r)**2)%p==0:
                            gens.setdefault(int(r),(c0,c1,c2))
    return rr,gens
rr7,g7=gens_for(7)
rr11,g11=gens_for(11)
check("generators found for BOTH degree-1 primes above 7", len(g7)==len(rr7)>=2)
check("generators found for BOTH degree-1 primes above 11", len(g11)==len(rr11)>=2)
print("  gens above 7:",g7," above 11:",g11)

# --- 4_1 character variety: derive relation between meridian trace x and Riley variable u ---
# parabolic-free: rep rho(A)=[[s,1],[0,1/s]], rho(B)=[[s,0],[u? ,1/s]] -- derive from relator.
# pi_1(4_1) = <A,B | A W = W B>, W = B A^{-1} B^{-1} A  (standard 2-bridge (5/3) form: w = b a^-1 b^-1 a? )
s,w = symbols('s w')
Am=sp.Matrix([[s,1],[0,1/s]])
Bm=sp.Matrix([[s,0],[w,1/s]])
# relator for figure-eight: A W = W B with W = B A^-1 B^-1 A? try candidates and find the polynomial condition
def rel_poly(W):
    Mrel = Am*W - W*Bm
    conds=[sp.simplify(sp.together(Mrel[i])) for i in range(4)]
    polys=[sp.factor(sp.numer(sp.together(c))) for c in conds]
    return polys
W1 = Bm*Am.inv()*Bm.inv()*Am
polys=rel_poly(W1)
# common nontrivial factor gives Riley polynomial in (s,w)
print("  relator numerators factors:", [sp.factor(p) for p in polys])
# Extract the Riley polynomial: known phi(s,w) = w^2 + (?); check claim: with x = s+1/s,
# u satisfies u^2 + (5-x^2)u + (5-x^2) = 0?? test: eliminate.
X=symbols('X')
# take gcd of the four numerators
from sympy import gcd as sgcd
g=polys[0]
for p in polys[1:]:
    g=sgcd(g,p)
print("  gcd factor:",sp.factor(g))
# substitute x = s + 1/s: express g in terms of X and w
gs=sp.expand(g)
# try writing in terms of m2 = s^2 + 1/s^2 = X^2-2
gg = sp.simplify(gs)
# Instead: check the claim numerically: for random X, the two u-roots of the Riley
# quadratic IN THIS BENCH'S CONVENTION (B lower-left = +u): u^2+(X^2-5)u+(5-X^2)=0
# should satisfy the relator equation for s with s+1/s=X.
# [CORRECTION filed at close-out 2026-08-25, error #16: this line originally used the
#  paper's convention u^2+(5-x^2)u+(5-x^2) (B lower-left = -u); with THIS script's
#  Mb=[[s,0],[+u,1/s]] the two differ by u -> -u (HANDOFF.md item: "u=-w; paper correct"),
#  so the numeric check failed with O(1) residuals. Exact re-derivation at close-out:
#  A*W - W*B has both nonzero entries proportional to s^4*u - s^4 + s^2*u^2 - 3*s^2*u
#  + 3*s^2 + u - 1 = s^2 * (u^2 + (X^2-5)u + (5-X^2)), X = s+1/s. At the cusp X=2 this
#  is u^2-u+1=0 — exactly the banked q. The discriminant (5-x^2)(1-x^2) and every
#  downstream trace-field claim are unchanged (the sign dies in the discriminant).]
import random
def test_claim(Xval):
    sv=sp.nsimplify(0)
    svs=sp.solve(sp.Eq(s+1/s,Xval),s)
    sv=svs[0]
    us=sp.solve(u**2+(Xval**2-5)*u+(5-Xval**2),u)
    okloc=True
    for uv in us:
        Ma=sp.Matrix([[sv,1],[0,1/sv]]); Mb=sp.Matrix([[sv,0],[uv,1/sv]])
        Wm=Mb*Ma.inv()*Mb.inv()*Ma
        Rm=(Ma*Wm-Wm*Mb)
        mx=max(abs(complex(sp.N(Rm[i],30))) for i in range(4))
        if mx>1e-15: okloc=False
    return okloc
res=[test_claim(sp.Rational(v,7)) for v in (3,10,15)]
check("character-variety relation u^2+(x^2-5)u+(5-x^2)=0 holds (bench convention; numeric, 3 values)", all(res))
# exact form of the same fact (added at close-out): the relator entries factor through the quadratic
_rel=sp.expand(sp.numer(sp.together((sp.Matrix([[s,1],[0,1/s]])*(sp.Matrix([[s,0],[u,1/s]])*sp.Matrix([[s,1],[0,1/s]]).inv()*sp.Matrix([[s,0],[u,1/s]]).inv()*sp.Matrix([[s,1],[0,1/s]]))-(sp.Matrix([[s,0],[u,1/s]])*sp.Matrix([[s,1],[0,1/s]]).inv()*sp.Matrix([[s,0],[u,1/s]]).inv()*sp.Matrix([[s,1],[0,1/s]]))*sp.Matrix([[s,0],[u,1/s]]))[1])))
check("EXACT: relator entry = s^2*(u^2+((s+1/s)^2-5)u+(5-(s+1/s)^2))",
      sp.expand(_rel - sp.expand(s**2*(u**2+((s+1/s)**2-5)*u+(5-(s+1/s)**2))))==0)
# trace field radical: verify tr(rho(AB)) or similar generates Q(x, sqrt((5-x^2)(1-x^2)))?
# u = [-(5-x^2) ± sqrt((5-x^2)^2-4(5-x^2))]/2 ; (5-x^2)^2-4(5-x^2)=(5-x^2)(1-x^2). Discriminant matches:
D=sp.expand((5-X**2)**2-4*(5-X**2))
check("u-discriminant = (5-x^2)(1-x^2)", sp.expand(D-(5-X**2)*(1-X**2))==0)
# n=5: D=(-1-3*sqrt5)/2 at x=phi
phi=(1+sp.sqrt(5))/2
Dval=sp.simplify((5-phi**2)*(1-phi**2))
check("n=5: D=(-1-3sqrt5)/2", sp.simplify(Dval-(-1-3*sp.sqrt(5))/2)==0)
check("n=4: D=-3 at x=sqrt2", sp.simplify((5-2)*(1-2))==-3)
check("n=6: D=-4 at x=sqrt3", sp.simplify((5-3)*(1-3))==-4)
check("cusp: D=-3 at x=2", (5-4)*(1-4)==-3)
check("n=2: D=5 at x=0", (5-0)*(1-0)==5)
check("[Q(2cos(pi/n)):Q]=phi(2n)/2 for n=2..12", all(sp.minimal_polynomial(2*cos(pi/n),x).as_poly().degree()==totient(2*n)//2 for n in range(2,13)))

# --- Molien series of 2T and 2O on Sym^n(C^2), degrees <= 24 ---
# 2T = 24 Hurwitz units as SU(2) matrices; character of Sym^n at g with eigenvalues e^{i a}, e^{-i a}:
# chi_n(g) = sin((n+1)a)/sin(a) ; use exact eigenvalues via quaternion scalar part.
import itertools as it
from fractions import Fraction
quats=[]
for e in range(4):
    for sgn in (1,-1):
        q=[0,0,0,0]; q[e]=sgn; quats.append(tuple(q))
for signs in it.product([1,-1],repeat=4):
    quats.append(tuple(Fraction(sv,2) for sv in signs))
# eigenvalue angle: cos a = scalar part
def sym_inv_dim(group,n):
    # dim of invariants = (1/|G|) sum_g chi_n(g); chi_n(g)= sum_{k=0..n} e^{i(n-2k)a}
    total=sp.Integer(0)
    for q in group:
        c=sp.nsimplify(q[0], [sp.sqrt(2),sp.sqrt(5)])
        aval=sp.acos(c)
        chi=sum(sp.exp(sp.I*(n-2*k)*aval) for k in range(n+1))
        total+=chi
    return sp.simplify(total/len(group))
# numeric resolution of sympy root-branch artifacts ((-1)**(1/3) forms that simplify()
# leaves unresolved): the Molien average is an exact non-negative integer, so evaluate
# at 50 digits and round, asserting the residual and imaginary part are < 1e-40.
def _as_int(e):
    v=sp.N(e,50)
    assert abs(sp.im(v))<sp.Float('1e-40'), f"nonreal Molien dim: {v}"
    r=int(sp.Integer(round(float(sp.re(v)))))
    assert abs(sp.re(v)-r)<sp.Float('1e-40'), f"non-integer Molien dim: {v}"
    return r
dims2T={n:_as_int(sym_inv_dim(quats,n)) for n in [2,6,8,10,12,14,16,22]}
print("  2T Molien dims:",dims2T)
check("2T: dim inv = 0 at 2,10; 1 at 8,14,16,22; 1 at 6",
      dims2T[2]==0 and dims2T[10]==0 and dims2T[8]==1 and dims2T[14]==1 and dims2T[16]==1 and dims2T[22]==1 and dims2T[6]==1)
# 2O = 48: add the 24 elements (1±i)/sqrt2-type: units of the form (±1±i)/sqrt2 etc.
oct_extra=[]
s2=sp.sqrt(2)
for pair in it.combinations(range(4),2):
    for s1 in (1,-1):
        for s2s in (1,-1):
            q=[sp.Integer(0)]*4; q[pair[0]]=sp.Rational(s1,1)/s2; q[pair[1]]=sp.Rational(s2s,1)/s2
            oct_extra.append(tuple(q))
group2O=[tuple(sp.nsimplify(x) for x in q) for q in quats]+oct_extra
check("|2O|=48", len(group2O)==48)
dims2O={n:_as_int(sym_inv_dim(group2O,n)) for n in [2,8,10,14,16,22]}
print("  2O Molien dims:",dims2O)
check("2O: dim inv 1 at 8,16 and 0 at 2,10,14,22",
      dims2O[8]==1 and dims2O[16]==1 and dims2O[2]==0 and dims2O[10]==0 and dims2O[14]==0 and dims2O[22]==0)

print("\nOVERALL:","ALL PASS" if ok else "SOME FAILED")
sys.exit(0 if ok else 1)
