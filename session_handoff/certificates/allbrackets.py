#!/usr/bin/env python3
"""Referee extension: compute ALL SIX pairwise brackets of the four charges,
plus verify C is inside the common centralizer, using the paper's own construction code."""
import importlib.util, sys
import sympy as sp
from fractions import Fraction

spec = importlib.util.spec_from_file_location("ccb",
  "/tmp/claude-0/-home-user-golden-gate/7aec077f-59a6-5129-b1a7-361cc5dcb800/scratchpad/paper/verify/check_charge_bracket.py")
ccb = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ccb)

print("imported; attrs:", [a for a in dir(ccb) if not a.startswith('_')])

# Their main() builds everything locally, so replicate the needed parts using module-level helpers.
br, add, smul, is_zero = ccb.br, ccb.add, ccb.smul, ccb.is_zero
evec, hvec = ccb.evec, ccb.hvec
ROOTS, IDX, N, DIM = ccb.ROOTS, ccb.IDX, ccb.N, ccb.DIM
eps = ccb.eps

# principal sl2 (copy of their steps)
e = [Fraction(0)]*DIM
for i in range(N):
    pos = tuple(1 if k==i else 0 for k in range(N))
    e[N+IDX[pos]] = Fraction(1)
import sympy
Cart = sp.Matrix(6,6, lambda i,j: ccb.ip(tuple(1 if k==i else 0 for k in range(6)), tuple(1 if k==j else 0 for k in range(6))))
hcoef = Cart.solve(sp.Matrix([2]*6))
h = [Fraction(0)]*DIM
for j in range(N):
    h[j] = Fraction(int(hcoef[j]))
# f: solve [e,f]=h with f = sum d_i e_{-alpha_i}
fv = [Fraction(0)]*DIM
for j in range(N):
    neg = tuple(-1 if i2==j else 0 for i2 in range(N))
    fv[N+IDX[neg]] = h[j] / Fraction(eps(tuple(1 if k==j else 0 for k in range(N)), neg))
assert br(e,fv)==h, "[e,f]=h failed"

x,y = sp.symbols('x y')
t_poly = x**5*y - x*y**5
W_poly = x**8 + 14*x**4*y**4 + y**8
charges = {8: W_poly, 14: sp.expand(t_poly*W_poly), 16: sp.expand(W_poly**2), 22: sp.expand(t_poly*W_poly**2)}

def highest_vector(n):
    cands = [r for r in ROOTS if br(h, evec(r))[N+IDX[r]] == n]
    for r in cands:
        v = evec(r)
        if is_zero(br(e, v)):
            return v
    cols=[evec(r) for r in cands]
    Mx = sp.zeros(DIM, len(cols))
    for j,c in enumerate(cols):
        img=br(e,c)
        for i2,val in enumerate(img):
            Mx[i2,j]=sp.Rational(val.numerator, val.denominator)
    ns=Mx.nullspace()
    if not ns: return None
    vec=ns[0]
    out=[Fraction(0)]*DIM
    for j,c in enumerate(cols):
        coef=sp.Rational(vec[j])
        if coef:
            out=add(out, smul(Fraction(coef.p,coef.q), c))
    return out

def embed(poly, n):
    v=highest_vector(n)
    if v is None: return None
    P=sp.Poly(poly,x,y)
    out=[Fraction(0)]*DIM
    cur=v
    for k in range(n+1):
        c=P.coeff_monomial(x**(n-k)*y**k) if n-k>=0 else 0
        if c:
            rat=sp.Rational(c)*sp.factorial(n-k)/sp.factorial(n)
            out=add(out, smul(Fraction(sp.Rational(rat).p, sp.Rational(rat).q), cur))
        cur=br(fv,cur)
    return out

X={}
for n in (8,14,16,22):
    X[n]=embed(charges[n],n)
    print(f"x{n} embedded; nonzero: {not is_zero(X[n])}")

pairs=[(8,14),(8,16),(8,22),(14,16),(14,22),(16,22)]
allzero=True
for a,b in pairs:
    z=is_zero(br(X[a],X[b]))
    print(f"[x{a},x{b}] = 0 : {z}")
    if not z: allzero=False
print("C ABELIAN (all six brackets vanish):", allzero)

# dim of common centralizer z(C): common nullspace of ad(x_n)
M=sp.zeros(4*DIM, DIM)
row=0
for n in (8,14,16,22):
    # ad(x_n) as matrix: columns = bracket with basis vectors
    for j in range(DIM):
        basis=[Fraction(0)]*DIM; basis[j]=Fraction(1)
        img=br(X[n],basis)
        for i2,val in enumerate(img):
            M[row+i2,j]=sp.Rational(val.numerator,val.denominator)
    row+=DIM
ns=M.nullspace()
print("dim z(C) =", len(ns))
sys.exit(0 if allzero and len(ns)==12 else 1)
