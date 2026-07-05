"""Theta-lift / seam toolkit: the level-15 Weil matrices and their exact readouts.

Built on ``golden_gate.core.cyclo`` (exact ``Q(zeta_60)`` arithmetic). For each seed
``m`` the theta-lift Weil matrix is

    W_m = WR^m * D^m,   D = diag(zeta15^{j(j-1)/2}),   WR = (1/15) F D^{-1} F^{-1}

with the raw DFT ``F[j,k] = zeta15^{jk}``. Pair readouts DFT the ``Par``-inserted
trace table ``C[j][l] = tr(Par * W_{m1}^j * W_{m2}^l)`` into the eigenprojector
pair-traces, Galois-average into ``H = Q(sqrt5, sqrt-3)``, and read off the
sqrt(-15) "seam" coefficient -- all exact.

Ported (cleanly, no ``sys.path`` hacks, no JSON side-effects, no probe-specific
transcribed data) from ``origin-axiom`` ``frontier/B367_value_map/`` +
``frontier/B358_seam_certification/``.
"""

from fractions import Fraction as Fr

from . import cyclo as C

N = C.LEVEL          # 15


def _dmat(power):
    """``D^power = diag(zeta15^{power * j(j-1)/2})`` as an exact matrix."""
    M = [[C.ZERO for _ in range(N)] for _ in range(N)]
    for j in range(N):
        M[j][j] = C.e15((power * (j * (j - 1) // 2)) % N)
    return M


def _fmat(sign):
    """Raw DFT ``F[j,k] = zeta15^{sign*jk}`` (``sign=-1`` gives F^-1 up to 1/15)."""
    return [[C.e15((sign * j * k) % N) for k in range(N)] for j in range(N)]


def build_theta_W(m):
    """``W_m = WR^m * D^m`` with ``WR = (1/15) F D^-1 F^-1`` -- exact."""
    F, Fi = _fmat(+1), _fmat(-1)
    WR = C.mmul(C.mmul(F, _dmat(-1)), Fi)
    WR = [[C.scal(Fr(1, 15), WR[i][j]) for j in range(N)] for i in range(N)]
    P = WR
    for _ in range(m - 1):
        P = C.mmul(P, WR)
    return C.mmul(P, _dmat(m))


def matrix_order(W, cap=64):
    """Multiplicative order of ``W`` (exact) + the power cache ``W^0..W^{ord-1}``."""
    ident = C.mat_identity(N)
    powers = [ident]
    P = W
    for k in range(1, cap + 1):
        if P == ident:
            return k, powers
        powers.append(P)
        P = C.mmul(P, W)
    raise RuntimeError("order cap exceeded")


def par_trace(A, B):
    """``tr(Par * A * B)`` exactly, where ``Par: x -> -x mod 15``."""
    t = C.ZERO
    for x in range(N):
        Arow = A[(-x) % N]
        for y in range(N):
            if Arow[y] != C.ZERO and B[y][x] != C.ZERO:
                t = C.add(t, C.mul(Arow[y], B[y][x]))
    return t


def pair_smatrix(pow1, pow2):
    """Exact H-vectors ``t(a,b) = tr(Par P_a Q_b)`` for a pair of power caches.

    Returns ``{(a, b): (p, q, r, s)}`` over nonzero traces, where the H-vector is
    the exact ``(1, sqrt5, sqrt-3, sqrt-15)`` decomposition; ``s`` (index 3) is
    the seam / sqrt(-15) coefficient.
    """
    o1, o2 = len(pow1), len(pow2)
    Ctab = [[par_trace(pow1[j], pow2[l]) for l in range(o2)] for j in range(o1)]
    z1, z2 = C.CONDUCTOR // o1, C.CONDUCTOR // o2
    out = {}
    for a in range(o1):
        for b in range(o2):
            t = C.ZERO
            for j in range(o1):
                zja = C.zeta((-z1 * j * a) % C.CONDUCTOR)
                for l in range(o2):
                    t = C.add(t, C.mul(C.mul(zja, C.zeta((-z2 * l * b) % C.CONDUCTOR)),
                                       Ctab[j][l]))
            t = C.scal(Fr(1, o1 * o2), t)
            if t == C.ZERO:
                continue
            sol = C.solve_H(C.H_avg(t))
            assert sol is not None, ("outside H", a, b)
            out[(a, b)] = sol
    return out


def single_controls(powers):
    """Single-seed control: every ``tr(Par P_a)`` has zero sqrt-3 and sqrt-15 parts.

    A NECESSARY-condition sanity check, not a sufficient validator: degenerate
    inputs (e.g. all-identity powers) can pass it. It exists to catch a genuine
    seam leaking into a single-seed readout.
    """
    o = len(powers)
    z = C.CONDUCTOR // o
    for a in range(o):
        t = C.ZERO
        for j in range(o):
            tr = C.ZERO
            for x in range(N):
                tr = C.add(tr, powers[j][(-x) % N][x])
            t = C.add(t, C.mul(C.zeta((-z * j * a) % C.CONDUCTOR), tr))
        t = C.scal(Fr(1, o), t)
        if t == C.ZERO:
            continue
        sol = C.solve_H(C.H_avg(t))
        if sol is None or sol[2] != 0 or sol[3] != 0:
            return False
    return True


def projector_gates(powers):
    """Sanity gates on the DFT eigenprojectors: ``sum_a P_a = I`` and ``P_0^2 = P_0``.

    A NECESSARY-condition sanity check, not a sufficient validator: degenerate
    inputs (e.g. all-identity powers) satisfy both conditions vacuously. It catches
    a genuinely broken power cache (wrong order, corrupted entries).
    """
    o = len(powers)
    z = C.CONDUCTOR // o
    ident = C.mat_identity(N)

    def proj(a):
        M = [[C.ZERO] * N for _ in range(N)]
        for j in range(o):
            c = C.scal(Fr(1, o), C.zeta((-z * j * a) % C.CONDUCTOR))
            for i in range(N):
                for k in range(N):
                    if powers[j][i][k] != C.ZERO:
                        M[i][k] = C.add(M[i][k], C.mul(c, powers[j][i][k]))
        return M

    tot = [[C.ZERO] * N for _ in range(N)]
    for a in range(o):
        P = proj(a)
        for i in range(N):
            for k in range(N):
                tot[i][k] = C.add(tot[i][k], P[i][k])
    if tot != ident:
        return False
    P0 = proj(0)
    return C.mmul(P0, P0) == P0


def smat_only(table):
    """Reduce an H-vector table to ``{(a, b): s}`` over nonzero seam coefficients."""
    return {k: v[3] for k, v in table.items() if v[3] != 0}


def rank_over_Q(rows_idx, cols_idx, table):
    """Exact rank of the seam (sqrt-15) matrix on the given exponent grid, over Q."""
    M = [[table.get((a, b), (0, 0, 0, Fr(0)))[3] for b in cols_idx] for a in rows_idx]
    M = [row[:] for row in M]
    r = 0
    for c in range(len(cols_idx)):
        piv = next((i for i in range(r, len(M)) if M[i][c] != 0), None)
        if piv is None:
            continue
        M[r], M[piv] = M[piv], M[r]
        pv = M[r][c]
        M[r] = [v / pv for v in M[r]]
        for i in range(len(M)):
            if i != r and M[i][c] != 0:
                f = M[i][c]
                M[i] = [M[i][j] - f * M[r][j] for j in range(len(cols_idx))]
        r += 1
    return r


def solve_model(recs):
    """Exact multiplicative tensor completion over Q.

    ``recs`` is a list of ``(k3, k5, k4, s)`` records (three CRT factor keys and a
    target seam value). Returns ``(X3, X5, X4)`` dicts with
    ``X3[k3]*X5[k5]*X4[k4] == s`` for every nonzero record (gauge-fixed on spanning
    entries, propagated to a fixpoint; zero entries must sit on a factor cell used
    only by zeros), or ``None`` if no multiplicative model fits.
    """
    nz = [r for r in recs if r[3] != 0]
    zero = [r for r in recs if r[3] == 0]
    X = [{}, {}, {}]

    pending = list(nz)
    while pending:
        progress = False
        rest = []
        for k3, k5, k4, s in pending:
            keys = (k3, k5, k4)
            known = [X[i].get(keys[i]) for i in range(3)]
            unknown = [i for i in range(3) if known[i] is None]
            if not unknown:
                if known[0] * known[1] * known[2] != s:
                    return None
                progress = True
            elif len(unknown) == 1:
                i = unknown[0]
                prod = Fr(1)
                for j in range(3):
                    if j != i:
                        prod *= known[j]
                X[i][keys[i]] = s / prod
                progress = True
            else:
                rest.append((k3, k5, k4, s))
        if not progress and rest:
            k3, k5, k4, s = rest[0]
            keys = (k3, k5, k4)
            unknown = [i for i in range(3) if X[i].get(keys[i]) is None]
            for i in unknown[:-1]:
                X[i][keys[i]] = Fr(1)
        pending = rest

    for k3, k5, k4, s in nz:
        v = (X[0].get(k3), X[1].get(k5), X[2].get(k4))
        if None in v or v[0] * v[1] * v[2] != s:
            return None

    nz_cells = [set(), set(), set()]
    for k3, k5, k4, _s in nz:
        nz_cells[0].add(k3)
        nz_cells[1].add(k5)
        nz_cells[2].add(k4)
    for k3, k5, k4, _s in zero:
        keys = (k3, k5, k4)
        if all(keys[i] in nz_cells[i] for i in range(3)):
            return None
        for i in range(3):
            if keys[i] not in nz_cells[i]:
                X[i][keys[i]] = Fr(0)
                break
    return X
