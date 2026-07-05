"""Exact arithmetic in the cyclotomic field Q(zeta_60), and the level-15 Weil data.

This is the foundational engine of ``golden_gate``: everything the library proves
"exactly" (Yang-Baxter, ``F**2 = I``, ``Jones(4_1; zeta_5) = -phi``, the seam
readouts) reduces to identities in this field, computed over ``fractions.Fraction``
with **no floating point anywhere**.

Representation
--------------
An element of ``Q(zeta_60)`` is a length-``DEG`` (=16) coefficient vector of
``Fraction`` in the power basis ``1, z, ..., z**15`` reduced modulo the 60th
cyclotomic polynomial::

    Phi_60(z) = z**16 + z**14 - z**10 - z**8 - z**6 + z**2 + 1

so ``z**16 = -z**14 + z**10 + z**8 + z**6 - z**2 - 1``.  The type alias ``Elt`` is
``list[Fraction]``.

Two integers are easy to confuse and are named apart here:

* ``CONDUCTOR = 60`` -- the cyclotomic conductor (``z = zeta_60``, ``DEG = phi(60) = 16``).
* ``LEVEL = 15``     -- the quantum level / dimension of the T and S matrices.

Conventions follow the origin-axiom ``B355`` line: ``T = e_15(x**2)`` diagonal,
``S = e_15(-2 x y) / g(15)`` with the Gauss sum ``g(15) = i * sqrt(15)``.

Ported (cleanly, no ``sys.path`` hacks, no import-time file I/O) from
``origin-axiom`` ``frontier/B358_seam_certification/{cyclo_engine,seam_certification}.py``.
"""

from __future__ import annotations

from fractions import Fraction as Fr

Elt = list  # list[Fraction], length DEG

CONDUCTOR = 60
DEG = 16          # phi(60)
LEVEL = 15        # T/S matrix dimension

# --- reduction table modulo Phi_60 -----------------------------------------
# z**16 = -z**14 + z**10 + z**8 + z**6 - z**2 - 1


def _reduce_high(v):
    """Fold a single degree-DEG coefficient ``v[DEG]`` back down via Phi_60."""
    c = v[DEG]
    v = v[:DEG]
    if c:
        v[14] -= c
        v[10] += c
        v[8] += c
        v[6] += c
        v[2] -= c
        v[0] -= c
    return v


def _build_red():
    """``RED[k]`` = ``z**k`` reduced to a DEG-vector, for ``k`` in ``0..2*DEG-1``."""
    red = []
    for k in range(DEG):
        v = [Fr(0)] * DEG
        v[k] = Fr(1)
        red.append(v)
    for k in range(DEG, 2 * DEG):
        prev = red[k - 1]
        v = [Fr(0)] * (DEG + 1)
        for i in range(DEG):
            v[i + 1] = prev[i]
        red.append(_reduce_high(v))
    return red


RED = _build_red()


def _zmul_mono(a):
    """Multiply an element by ``z`` (with one reduction step)."""
    v = [Fr(0)] * (DEG + 1)
    for i in range(DEG):
        v[i + 1] = a[i]
    return _reduce_high(v)


# cache all 60 monomials z**0 .. z**59
_ZP = []
_cur = [Fr(0)] * DEG
_cur[0] = Fr(1)
for _k in range(CONDUCTOR):
    _ZP.append(list(_cur))
    _cur = _zmul_mono(_cur)


# --- field operations ------------------------------------------------------

def zero():
    """The additive identity, a fresh DEG-vector of zeros."""
    return [Fr(0)] * DEG


def one():
    """The multiplicative identity ``1``."""
    return list(_ZP[0])


ZERO = zero()
ONE = one()


def add(a, b):
    return [a[i] + b[i] for i in range(DEG)]


def sub(a, b):
    return [a[i] - b[i] for i in range(DEG)]


def scal(c, a):
    """Scalar multiple ``c * a`` (``c`` a ``Fraction`` or ``int``)."""
    return [c * x for x in a]


def mul(a, b):
    """Field product, exact, via convolution + reduction modulo Phi_60."""
    raw = [Fr(0)] * (2 * DEG - 1)
    for i in range(DEG):
        ai = a[i]
        if ai:
            for j in range(DEG):
                if b[j]:
                    raw[i + j] += ai * b[j]
    out = [Fr(0)] * DEG
    for k in range(2 * DEG - 1):
        if raw[k]:
            rk = RED[k]
            for i in range(DEG):
                if rk[i]:
                    out[i] += raw[k] * rk[i]
    return out


def zeta(k):
    """``zeta_60**k`` = the primitive 60th root of unity to the ``k``."""
    return list(_ZP[k % CONDUCTOR])


def e15(t):
    """``exp(2*pi*i*t/15) = zeta_60**(4t)`` -- the level-15 additive character."""
    return zeta(4 * (t % LEVEL))


def conj(a):
    """Complex conjugation ``z -> z**-1 = z**59`` (an involution on the field)."""
    out = [Fr(0)] * DEG
    for k in range(DEG):
        if a[k]:
            out = add(out, scal(a[k], zeta((-k) % CONDUCTOR)))
    return out


def is_zero(a):
    return all(x == 0 for x in a)


def eq(a, b):
    return a == b


# --- named radical constants (exact) ---------------------------------------
# sqrt5   = z5 + z5**4 - z5**2 - z5**3   (z5 = zeta_60**12)
# sqrt(-3)= z3 - z3**2                    (z3 = zeta_60**20)
SQRT5 = sub(add(zeta(12), zeta(48)), add(zeta(24), zeta(36)))
SQRTm3 = sub(zeta(20), zeta(40))
I_UNIT = zeta(15)                                         # i
SQRT15 = mul(mul(SQRT5, SQRTm3), scal(Fr(-1), I_UNIT))    # sqrt5*sqrt(-3)*(-i)
SQRTm15 = mul(SQRT5, SQRTm3)                              # sqrt(-15) = sqrt5*sqrt(-3)
G15 = mul(I_UNIT, SQRT15)                                 # Gauss sum g(15) = i*sqrt15
G15_INV = scal(Fr(1, 15), conj(G15))                     # 1/g = conj(g)/15 (|g|**2 = 15)


# --- matrices over the field (lists of lists of Elt) -----------------------

def mat_identity(n=LEVEL):
    return [[ONE if i == j else ZERO for j in range(n)] for i in range(n)]


def mmul(A, B):
    """Exact product of two square field-matrices."""
    n = len(A)
    C = [[ZERO for _ in range(n)] for _ in range(n)]
    for i in range(n):
        Ai = A[i]
        for k in range(n):
            a = Ai[k]
            if any(a):
                Bk = B[k]
                Ci = C[i]
                for j in range(n):
                    b = Bk[j]
                    if any(b):
                        Ci[j] = add(Ci[j], mul(a, b))
    return C


def mat_eq(A, B):
    n = len(A)
    return all(A[i][j] == B[i][j] for i in range(n) for j in range(n))


def is_identity(M):
    n = len(M)
    return all(M[i][j] == (ONE if i == j else ZERO)
               for i in range(n) for j in range(n))


def Tmat():
    """The exact level-15 T matrix: ``T[x][x] = e_15(x**2)`` diagonal."""
    M = [[ZERO for _ in range(LEVEL)] for _ in range(LEVEL)]
    for x in range(LEVEL):
        M[x][x] = e15(x * x)
    return M


def Tinv():
    """``T**-1`` = ``diag(e_15(-x**2))``."""
    M = [[ZERO for _ in range(LEVEL)] for _ in range(LEVEL)]
    for x in range(LEVEL):
        M[x][x] = e15(-x * x)
    return M


def Smat():
    """The exact level-15 S matrix: ``S[x][y] = e_15(-2 x y) / g(15)``."""
    M = [[ZERO for _ in range(LEVEL)] for _ in range(LEVEL)]
    for x in range(LEVEL):
        for y in range(LEVEL):
            M[x][y] = mul(e15(-2 * x * y), G15_INV)
    return M


def Sinv():
    """``S**-1 = S^dagger``: ``(S**-1)[x][y] = conj(S[y][x])``."""
    S = Smat()
    M = [[ZERO for _ in range(LEVEL)] for _ in range(LEVEL)]
    for x in range(LEVEL):
        for y in range(LEVEL):
            M[x][y] = conj(S[y][x])
    return M


# --- projection into H = Q(sqrt5, sqrt(-3)) --------------------------------
GAL_H = [1, 19, 31, 49]     # Gal(Q(zeta_60)/H), H = Q(sqrt5, sqrt(-3))


def galois(a, c):
    """Apply the Galois automorphism ``z -> z**c`` to an element."""
    out = [Fr(0)] * DEG
    for k in range(DEG):
        if a[k]:
            out = add(out, scal(a[k], zeta((c * k) % CONDUCTOR)))
    return out


def H_avg(t):
    """Average ``t`` over ``Gal(Q(zeta_60)/H)`` -- the projection into ``H``."""
    s = [Fr(0)] * DEG
    for c in GAL_H:
        s = add(s, galois(t, c))
    return scal(Fr(1, 4), s)


def solve_H(t):
    """Write ``t = p + q*sqrt5 + r*sqrt(-3) + s*sqrt(-15)`` exactly.

    Returns the 4-tuple ``(p, q, r, s)`` of ``Fraction`` (the ``s`` component,
    index 3, is the "seam" / sqrt(-15) coefficient), or ``None`` if ``t`` is not
    in ``H``.  Exact Gaussian elimination over ``Q``.
    """
    cols = [ONE, SQRT5, SQRTm3, SQRTm15]
    Ab = [[cols[c][row] for c in range(4)] + [t[row]] for row in range(DEG)]
    r = 0
    piv_cols = []
    for c in range(4):
        piv = next((i for i in range(r, DEG) if Ab[i][c] != 0), None)
        if piv is None:
            continue
        Ab[r], Ab[piv] = Ab[piv], Ab[r]
        pv = Ab[r][c]
        Ab[r] = [v / pv for v in Ab[r]]
        for i in range(DEG):
            if i != r and Ab[i][c] != 0:
                f = Ab[i][c]
                Ab[i] = [Ab[i][j] - f * Ab[r][j] for j in range(5)]
        piv_cols.append(c)
        r += 1
    sol = [Fr(0)] * 4
    for i, c in enumerate(piv_cols):
        sol[c] = Ab[i][4]
    for i in range(r, DEG):
        if Ab[i][4] != 0:
            return None
    chk = ZERO
    for c in range(4):
        chk = add(chk, scal(sol[c], cols[c]))
    if chk != t:
        return None
    return tuple(sol)


# --- level-15 Weil generators (used by higher engines & as exact test data) -

def weil_generator(m):
    """``rho(A_m) = T**m S T**-m S**-1`` -- the metallic Weil generator at level 15.

    ``weil_generator(1)`` has order 20, ``weil_generator(2)`` has order 12
    (checked exactly by the test suite).
    """
    T, S, Si = Tmat(), Smat(), Sinv()
    Tm = mat_identity()
    Tmi = mat_identity()
    for _ in range(m):
        Tm = mmul(Tm, T)
        Tmi = mmul(Tmi, Tinv())
    return mmul(mmul(Tm, S), mmul(Tmi, Si))
