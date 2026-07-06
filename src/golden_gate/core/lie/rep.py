"""The E6 character-variety tangent of the figure-eight, and its two Z/2 gradings (ported).

Ported from origin-axiom B347 (``frontier/B347_e6_tangent_gradings/e6_tangent_gradings.py``).
Standalone low-dimensional topology / SL(n,C)-character-variety computation; no physics
claim.

Object. ``rho0 : pi_1(4_1) -> SL(2,C)`` is the geometric (discrete faithful) holonomy of
the figure-eight knot. Composed with the *principal* homomorphism ``SL(2) -> E6`` (whose
exponents are the E6 exponents ``{1,4,5,7,8,11}``), the adjoint decomposes as
``e6 = (+)_i Sym^{2 m_i}`` (dims 3+9+11+15+17+23 = 78), so the Zariski tangent

    ``H^1(pi_1(4_1), e6_rho) = (+)_i H^1(4_1, Sym^{2 m_i})``,

computed here by Fox calculus on the presentation ``<a,b | a b^3 a B A^2 B>`` (SnapPy
census 4_1, verified against the relator).

Results (reproduced by :func:`run_all`):

1. ``dim H^1(4_1, Sym^{2m}) = 1`` for every E6 exponent m  =>  total = 6 = rank E6.
2. The amphichiral (orientation-reversing) involution acts as a real structure
   ``J^2 = +1`` on every line -- uniform, no split.
3. The hyperelliptic (orientation-preserving) involution ``a->a^-1, b->b^-1`` grades by
   ``(-1)^{m+1}``: its (-1)-eigenspace is exactly ``{4,8}`` (the e6/f4 = 26 "escape"
   sector), its (+1)-eigenspace the F4 exponents ``{1,5,7,11}``.

**Precision discipline (the port's main surgery).** The origin-axiom module set
``mp.mp.dps = 70`` at import and rebuilt it per call with a ``_guard()``; it also
SVD-solved the two involution intertwiners ``_AMPHI``/``_HYPER`` *at import time*, at
whatever global precision happened to be live. Here nothing touches the global dps at
import: the geometric rep (:func:`_base`) and the two involutions (:func:`_amphi`,
:func:`_hyper`) are built lazily and memoized, and every public entry point is scoped
with :func:`~golden_gate.core.precision.at_precision` at ``DPS_REP``. :func:`symrep` is
deliberately *undecorated* -- it is pure matrix arithmetic reused by ``core.lie.cohomology``
at ``DPS_E6``, so it must inherit the caller's precision.
"""

import mpmath as mp

from ..precision import DPS_E6, DPS_REP, at_precision, working_precision

EXPONENTS = [1, 4, 5, 7, 8, 11]
REL = "abbbaBAAB"                       # SnapPy 4_1 relator (uppercase = inverse)

# --- the geometric SL(2,C) rep (discrete faithful holonomy of 4_1) ------------------------------------
# Entries are exact algebraic numbers in Q(sqrt3, i); built lazily at DPS_E6 (the highest
# precision any consumer needs -- core.lie.cohomology runs at 100) and memoized, so the
# constants never depend on the ambient dps at first-call time.
_BASE_CACHE = None


def _base():
    """The geometric rep {a, b, A, B} as mp matrices (memoized, built at DPS_E6)."""
    global _BASE_CACHE
    if _BASE_CACHE is None:
        with working_precision(DPS_E6):
            s3 = mp.sqrt(3)
            I = mp.mpc(0, 1)
            base = {
                "a": mp.matrix([[-2 - s3 * I, s3 / 2 + 3 * I / 2], [-s3 + I, mp.mpf(1)]]),
                "b": mp.matrix([[mp.mpf(0), s3 / 2 + I / 2],
                                [-s3 / 2 + I / 2, mp.mpf(3) / 2 + s3 * I / 2]]),
            }
            base["A"] = base["a"] ** -1
            base["B"] = base["b"] ** -1
            _BASE_CACHE = base
    return _BASE_CACHE


def _ev(word, rep=None):
    if rep is None:
        rep = _base()
    R = mp.eye(next(iter(rep.values())).rows)
    for c in word:
        R = R * rep[c]
    return R


@at_precision(DPS_REP)
def geometric_rep_residual():
    """||rho(relator) - I|| for the hard-coded rep (should be ~1e-60)."""
    return mp.norm(_ev(REL) - mp.eye(2))


# --- Sym^d of a 2x2 matrix (a genuine homomorphism SL2 -> SL(d+1)) ------------------------------------
# Undecorated on purpose: reused by core.lie.cohomology at DPS_E6; must inherit the
# caller's precision.
def symrep(g, d):
    a, b, c, e = g[0, 0], g[0, 1], g[1, 0], g[1, 1]

    def cpow(p, k):
        r = [mp.mpf(1)]
        for _ in range(k):
            nr = [mp.mpf(0)] * (len(r) + 1)
            for j in range(len(r)):
                nr[j] += r[j] * p[0]
                nr[j + 1] += r[j] * p[1]
            r = nr
        return r

    Ms = mp.zeros(d + 1, d + 1)
    for i in range(d + 1):
        X = cpow([a, c], i)
        Y = cpow([b, e], d - i)
        conv = [mp.mpf(0)] * (d + 1)
        for u in range(len(X)):
            for v in range(len(Y)):
                conv[u + v] += X[u] * Y[v]
        for k in range(d + 1):
            Ms[k, i] = conv[d - k]                 # basis x^k y^{d-k}
    return Ms


@at_precision(DPS_REP)
def symrep_homomorphism_residual(d=6):
    b = _base()
    return mp.norm(symrep(b["a"] * b["b"], d) - symrep(b["a"], d) * symrep(b["b"], d))


def _R(d):
    b = _base()
    R = {c: symrep(b[c], d) for c in "ab"}
    R["A"] = R["a"] ** -1
    R["B"] = R["b"] ** -1
    return R


def _foxmat(gen, d, R):
    dim = d + 1
    Dm = mp.zeros(dim, dim)
    pre = mp.eye(dim)
    for ch in REL:
        low = ch.lower()
        if ch.islower():
            if low == gen:
                Dm = Dm + pre
            pre = pre * R[low]
        else:
            pre = pre * R[low.upper()]
            if low == gen:
                Dm = Dm - pre
    return Dm


def _rank(M, tol=mp.mpf(10) ** -40):
    S = mp.svd_c(M, compute_uv=False)
    s = [abs(S[i]) for i in range(len(S))]
    return sum(1 for x in s if x > max(s) * tol)


@at_precision(DPS_REP)
def H1_dim(m):
    """dim H^1(4_1, Sym^{2m}) at the geometric rep, via ranks of the Fox cochain complex."""
    d = 2 * m
    dim = d + 1
    R = _R(d)
    Da, Db = _foxmat("a", d, R), _foxmat("b", d, R)
    d1 = mp.zeros(dim, 2 * dim)
    for i in range(dim):
        for j in range(dim):
            d1[i, j] = Da[i, j]
            d1[i, j + dim] = Db[i, j]
    d0 = mp.zeros(2 * dim, dim)
    Aa, Bb = R["a"] - mp.eye(dim), R["b"] - mp.eye(dim)
    for i in range(dim):
        for j in range(dim):
            d0[i, j] = Aa[i, j]
            d0[i + dim, j] = Bb[i, j]
    return (2 * dim - _rank(d1)) - _rank(d0)


@at_precision(DPS_REP)
def e6_tangent_total():
    return sum(H1_dim(m) for m in EXPONENTS)


# --- involution actions on the (1-dim) cohomology lines -----------------------------------------------
def _conjv(v):
    return mp.matrix([mp.conj(v[i]) for i in range(v.rows)])


def _zeval(word, za, zb, R):                       # value of a 1-cocycle on a word
    dim = za.rows
    z = mp.zeros(dim, 1)
    P = mp.eye(dim)
    zv = {"a": za, "b": zb}
    for c in word:
        zc = zv[c] if c in "ab" else -R[c] * zv[c.lower()]
        z = z + P * zc
        P = P * R[c]
    return z


def _nullspace(M, tol=mp.mpf(10) ** -35):
    U, S, V = mp.svd_c(M, full_matrices=True)
    sv = [abs(S[i]) for i in range(len(S))]
    sm = max(sv)
    return [mp.matrix([mp.conj(V[i, j]) for j in range(M.cols)])
            for i in range(M.cols) if (sv[i] if i < len(sv) else mp.mpf(0)) <= sm * tol]


def _solveD(target):
    """least-norm D (det=1) with rho(target[g]) = D * conj_flag(rho(g)) * D^-1 for g in a,b.
    target[g] is (word, conjugate_bool)."""
    base = _base()
    rows = []
    for g in "ab":
        word, conj = target[g]
        L = _ev(word)
        Rr = mp.matrix([[mp.conj(base[g][i, j]) for j in range(2)] for i in range(2)]) if conj else base[g]
        blk = mp.zeros(4, 4)
        for i in range(2):
            for j in range(2):
                for k in range(2):
                    blk[i * 2 + j, k * 2 + j] += L[i, k]
                    blk[i * 2 + j, i * 2 + k] -= Rr[k, j]
        rows.append(blk)
    M = mp.zeros(8, 4)
    for r in range(8):
        for c in range(4):
            M[r, c] = rows[r // 4][r % 4, c]
    U, S, V = mp.svd_c(M, full_matrices=True)
    D = mp.matrix([[mp.conj(V[3, 0]), mp.conj(V[3, 1])], [mp.conj(V[3, 2]), mp.conj(V[3, 3])]])
    return D / mp.sqrt(mp.det(D))


# The two involution intertwiners. In origin-axiom these were solved AT IMPORT at the
# live global dps (fragile). Here they are lazy + memoized, each built under a DPS_REP
# scope so their precision is pinned regardless of the ambient dps at first call.
_AMPHI_CACHE = None
_HYPER_CACHE = None


def _amphi():
    """Amphichiral (orientation-reversing) involution sigma_-: a->ababAB, b->baBA."""
    global _AMPHI_CACHE
    if _AMPHI_CACHE is None:
        with working_precision(DPS_REP):
            _AMPHI_CACHE = dict(
                sinv={"a": "abABab", "b": "BAba"},
                D=_solveD({"a": ("ababAB", True), "b": ("baBA", True)}),
                conjugate=True)
    return _AMPHI_CACHE


def _hyper():
    """Hyperelliptic (orientation-preserving) involution: a->a^-1, b->b^-1."""
    global _HYPER_CACHE
    if _HYPER_CACHE is None:
        with working_precision(DPS_REP):
            _HYPER_CACHE = dict(
                sinv={"a": "A", "b": "B"},
                D=_solveD({"a": ("A", False), "b": ("B", False)}),
                conjugate=False)
    return _HYPER_CACHE


def _line_eigenvalue(m, inv, square):
    """eigenvalue of the involution J (or J^2 if square) on the 1-dim H^1(Sym^{2m})."""
    d = 2 * m
    dim = d + 1
    R = _R(d)
    RD = symrep(inv["D"], d)
    conj = inv["conjugate"]
    sinv = inv["sinv"]
    Da, Db = _foxmat("a", d, R), _foxmat("b", d, R)
    d1 = mp.zeros(dim, 2 * dim)
    for i in range(dim):
        for j in range(dim):
            d1[i, j] = Da[i, j]
            d1[i, j + dim] = Db[i, j]
    d0 = mp.zeros(2 * dim, dim)
    Aa, Bb = R["a"] - mp.eye(dim), R["b"] - mp.eye(dim)
    for i in range(dim):
        for j in range(dim):
            d0[i, j] = Aa[i, j]
            d0[i + dim, j] = Bb[i, j]
    Z = _nullspace(d1)

    def dot(x, y):
        return sum(mp.conj(x[i]) * y[i] for i in range(x.rows))

    def gs(vs):
        o = []
        for v in vs:
            w = v.copy()
            for u in o:
                w = w - dot(u, w) * u
            n = mp.sqrt(dot(w, w).real)
            if n > mp.mpf(10) ** -25:
                o.append(w / n)
        return o

    Bon = gs([mp.matrix([d0[r, c] for r in range(2 * dim)]) for c in range(dim)])
    z0 = None
    for v in Z:
        w = v.copy()
        for u in Bon:
            w = w - dot(u, w) * u
        if mp.sqrt(dot(w, w).real) > mp.mpf(10) ** -18:
            z0 = w
            break

    def J(vec):
        za, zb = vec[0:dim, 0], vec[dim:2 * dim, 0]
        ea = RD * (_conjv(_zeval(sinv["a"], za, zb, R)) if conj else _zeval(sinv["a"], za, zb, R))
        eb = RD * (_conjv(_zeval(sinv["b"], za, zb, R)) if conj else _zeval(sinv["b"], za, zb, R))
        return mp.matrix([ea[i] for i in range(dim)] + [eb[i] for i in range(dim)])

    w = J(J(z0)) if square else J(z0)
    Amat = mp.zeros(2 * dim, 1 + dim)
    for r in range(2 * dim):
        Amat[r, 0] = z0[r]
        for c in range(dim):
            Amat[r, 1 + c] = d0[r, c]
    AH = mp.matrix(Amat.cols, Amat.rows)
    for r in range(Amat.rows):
        for c in range(Amat.cols):
            AH[c, r] = mp.conj(Amat[r, c])
    return mp.lu_solve(AH * Amat, AH * w)[0]


@at_precision(DPS_REP)
def amphichiral_indicator(m):
    """J^2 eigenvalue of the amphichiral (orientation-reversing) involution on H^1(Sym^{2m}); +1 = real."""
    mu = _line_eigenvalue(m, _amphi(), square=True)
    assert abs(mu.imag) < mp.mpf(10) ** -6, mu
    return 1 if mu.real > 0 else -1


@at_precision(DPS_REP)
def hyperelliptic_sign(m):
    """+/-1 eigenvalue of the hyperelliptic involution (a->a^-1,b->b^-1) on H^1(Sym^{2m}); = (-1)^{m+1}."""
    lm = _line_eigenvalue(m, _hyper(), square=False)
    assert abs(lm.imag) < mp.mpf(10) ** -6, lm
    return 1 if lm.real > 0 else -1


def run_all():
    # each callee re-scopes to DPS_REP (nested workdps is a no-op save/restore).
    dims = {m: H1_dim(m) for m in EXPONENTS}
    amph = {m: amphichiral_indicator(m) for m in EXPONENTS}
    hyp = {m: hyperelliptic_sign(m) for m in EXPONENTS}
    return dict(dims=dims, total=sum(dims.values()), amphichiral=amph, hyperelliptic=hyp,
                minus_eigenspace=[m for m in EXPONENTS if hyp[m] < 0])


if __name__ == "__main__":
    print("E6 character-variety tangent of 4_1 (ported from origin-axiom B347)\n")
    print("geometric rep residual   :", mp.nstr(geometric_rep_residual(), 3))
    print("symrep homomorphism resid:", mp.nstr(symrep_homomorphism_residual(), 3))
    r = run_all()
    print("dim H^1(Sym^2m) per exponent:", r["dims"], " total =", r["total"], "(rank E6 = 6)")
    print("amphichiral J^2 (o-reversing):", r["amphichiral"], " -> uniform real structure")
    print("hyperelliptic sign (o-presv) :", r["hyperelliptic"])
    print("  (-1)-eigenspace =", r["minus_eigenspace"], "= e6/f4 coset {4,8} (B265 escape sector)")
