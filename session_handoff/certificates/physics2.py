#!/usr/bin/env python3
"""Step 2: h^1(M; 27∘rho_0) by Fox calculus, independently.
pi_1(4_1) = <a,b | r>, r = a w b^{-1} w^{-1}, w = b a^{-1} b^{-1} a  (verified relator: a w = w b).
Geometric parabolic rep: a -> [[1,1],[0,1]], b -> [[1,0],[q,1]] with q^2 - q + 1 = 0
(q = -u, u the Riley parameter; trace field Q(sqrt-3)).
27∘rho_0 = Sym^16 ⊕ Sym^8 ⊕ Sym^0 as a pi_1-module (rho_0 factors through the principal SL2).
Compute dim H^1 for V = Sym^n, n = 16, 8, 0, over Q(q)."""
import sympy as sp
import sys

q = sp.symbols('q')
MOD = q**2 - q + 1

def red(e):
    return sp.rem(sp.expand(e), MOD, q)

A2 = sp.Matrix([[1,1],[0,1]])
B2 = sp.Matrix([[1,0],[q,1]])

def minv(M):
    d = red(M[0,0]*M[1,1]-M[0,1]*M[1,0])
    assert d == 1, d
    return sp.Matrix([[M[1,1],-M[0,1]],[-M[1,0],M[0,0]]])

def mmul(*Ms):
    R = sp.eye(Ms[0].shape[0])
    for M in Ms:
        R = (R*M).applyfunc(red)
    return R

# check relator in SL2: a w = w b
W2 = mmul(B2, minv(A2), minv(B2), A2)
assert mmul(A2,W2) == mmul(W2,B2), "relator fails"

def symrep(M, n):
    """Sym^n of a 2x2 matrix, acting on monomials x^{n-k} y^k."""
    if n == 0:
        return sp.Matrix([[1]])
    a,b,c,d = M[0,0],M[0,1],M[1,0],M[1,1]
    x,y = sp.symbols('x y')
    basis = [x**(n-k)*y**k for k in range(n+1)]
    S = sp.zeros(n+1, n+1)
    for k in range(n+1):
        img = sp.expand(((a*x+c*y)**(n-k))*((b*x+d*y)**k))
        img = sp.Poly(img, x, y)
        for j in range(n+1):
            S[j,k] = red(img.coeff_monomial(x**(n-j)*y**j))
    return S

def foxH1(n):
    An, Bn = symrep(A2,n), symrep(B2,n)
    Ai, Bi = symrep(minv(A2),n), symrep(minv(B2),n)
    N = n+1
    I = sp.eye(N)
    # r = a w b^{-1} w^{-1},  w = b a^{-1} b^{-1} a
    # Fox derivatives (left convention: d(uv)=du + u dv):
    # dw/da = b(-a^{-1}) + b a^{-1} b^{-1} = -B Ai + B Ai Bi... careful:
    # w = b * a^{-1} * b^{-1} * a
    # dw/da = b * d(a^{-1})/da + b a^{-1} b^{-1} * d(a)/da = b*(-a^{-1}) + b a^{-1} b^{-1} * 1
    Wn = mmul(Bn, Ai, Bi, An)
    dw_da = (-mmul(Bn,Ai) + mmul(Bn,Ai,Bi)).applyfunc(red)
    # dw/db = 1 + b a^{-1} * d(b^{-1})/db = 1 + b a^{-1} * (-b^{-1})
    dw_db = (I - mmul(Bn,Ai,Bi)).applyfunc(red)
    # r = a * w * b^{-1} * w^{-1}
    # dr/da = 1 + a*dw/da + a w b^{-1} * d(w^{-1})/da ; d(w^{-1})/da = -w^{-1} dw/da
    Wi = mmul(An.inv() if False else sp.eye(N),sp.eye(N))  # placeholder
    Wninv = symrep(minv(W2) if False else W2, n)  # need inverse of W2 in SL2
    W2i = minv(W2)
    Wninv = symrep(W2i, n)
    dr_da = (I + mmul(An,dw_da) - mmul(An,Wn,Bi,Wninv,dw_da)).applyfunc(red)
    # dr/db = a*dw/db + a w * d(b^{-1})/db + a w b^{-1} * d(w^{-1})/db
    dr_db = (mmul(An,dw_db) - mmul(An,Wn,Bi) - mmul(An,Wn,Bi,Wninv,dw_db)).applyfunc(red)
    # sanity: fundamental identity  dr/da (a-1)... skip; instead verify r acts trivially:
    Rn = mmul(An,Wn,symrep(minv(B2),n),Wninv)
    assert Rn == sp.eye(N), f"relator not trivial in Sym^{n}"
    # d1: V^2 -> V, (v1,v2) -> dr/da v1 + dr/db v2  ;  d0: V -> V^2, v -> ((A-1)v,(B-1)v)
    D1 = dr_da.row_join(dr_db)
    D0 = (An-I).col_join(Bn-I)
    # ranks over Q[q]/(q^2-q+1): work in QQ(sqrt(-3)) via algebraic substitution
    w0 = sp.Rational(1,2) + sp.sqrt(3)*sp.I/2  # primitive 6th root, satisfies q^2-q+1=0
    D1s = D1.subs(q,w0); D0s = D0.subs(q,w0)
    r1 = D1s.rank(); r0 = D0s.rank()
    h0 = N - r0
    h1 = (2*N - r1) - (N - h0)
    return h0, h1

tot = 0
for n in (16, 8, 0):
    h0, h1 = foxH1(n)
    print(f"Sym^{n}: dim H^0 = {h0}, dim H^1 = {h1}")
    tot += h1
print("h^1(M; 27∘rho_0) =", tot)
sys.exit(0 if tot == 3 else 1)
