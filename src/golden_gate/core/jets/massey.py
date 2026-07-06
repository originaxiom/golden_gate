"""The third-order (Massey) obstruction on the E6 character variety of 4_1 (ported).

Ported from origin-axiom B370 leg A (``frontier/B370_massey_depth2/massey.py``).

METHOD (jet arithmetic through the relator; no transcription of the BCH formula anywhere):
deform each generator image as ``rho_t(g) = exp(t z1(g) + t^2 z2(g)) rho(g)`` and expand the
relator product ``X_t(rel)`` as a formal series ``I + t P1 + t^2 P2 + t^3 P3`` in the adjoint
representation (the two-basis architecture of :mod:`..lie.cohomology`, dps 100). Self-gating:

* ``||P1|| ~ 0`` gates that z1 is a cocycle (the first-order gate);
* ``||P2|| ~ 0`` gates that z2 solves the second order (solved per Fox block);
* ``ad(q3) = P3`` defines the third-order obstruction vector (exact-Gram normal equations).

The class of ``q3`` in ``H^2`` is read per exponent block against the coker functionals, as
COMPLEX components (phases kept -- span arithmetic needs them). The Massey verdict is taken
MODULO the indeterminacy: ``z2`` is defined up to ``Z^1``, and shifting ``z2`` by a basis
cocycle moves the class by a finite difference on the same jet machinery; the per-direction
readout is the least-squares residual of ``class(q3)`` against that indeterminacy span,
against (i) the m=1 integrable control and (ii) an MB12 random-vector control.

**Precision (the port's surgery).** origin-axiom reached B352 via ``sys.path.insert`` +
``import cup_product``; here it is a real import (:mod:`..lie.cohomology`), the JSON
side-effect in the driver is gone (``run_all`` returns the dict), and every public entry
point re-scopes with :func:`~golden_gate.core.precision.at_precision` at ``DPS_E6``.
Firewalled research machinery; no physics claim.
"""

import time

import mpmath as mp

from ..lie import cohomology as CP
from ..precision import DPS_E6, at_precision

DIM = CP.DIM
EXPONENTS = CP.EXPONENTS
REL = CP.REL


def _to_root(vec_c):
    return CP.S * vec_c


def _solve_ad(P):
    """q with ad(q) = P via the exact-Gram normal equations (cohomology's solve)."""
    ads = CP._ad_sparse()
    b = mp.matrix([sum(c * P[k, j] for (k, j), c in ads[i].items()) for i in range(DIM)])
    q = mp.lu_solve(CP._gram(), b)
    R = mp.zeros(DIM, DIM)
    for i in range(DIM):
        qi = q[i]
        if qi != 0:
            for (k, j), c in ads[i].items():
                R[k, j] += qi * c
    res = mp.norm(R - P) / max(mp.norm(P), mp.mpf(10) ** -200)
    return q, res


@at_precision(DPS_E6)
def solve_z2(za_c, zb_c):
    """Blockwise least-squares z2 with d1_m w = -q2_chain_m; returns chain vectors
    (wa, wb, first_order_residual, z2_least_squares_residual)."""
    q2, first, res = CP.obstruction_vector(za_c, zb_c)
    q2_c = CP.S_INV * q2
    wa, wb = mp.zeros(DIM, 1), mp.zeros(DIM, 1)
    worst_ls = mp.mpf(0)
    for m in EXPONENTS:
        d1, _ = CP.FOX[m]
        n, o = CP.N_OF[m], CP.OFFSET[m]
        rhs = mp.matrix([-q2_c[o + k] for k in range(n)])
        U, sv, Vh = CP._svd(d1)
        # pseudo-inverse solve (rank n-1; the H^2 residual is the banked block zero)
        y = U.transpose_conj() * rhs
        w = mp.zeros(2 * n, 1)
        smax = max(abs(s) for s in sv)
        for i in range(len(sv)):
            if abs(sv[i]) > smax * mp.mpf(10) ** -40:
                for j in range(2 * n):
                    w[j] += mp.conj(Vh[i, j]) * y[i] / sv[i]
        worst_ls = max(worst_ls, mp.norm(d1 * w - rhs))
        for k in range(n):
            wa[o + k] = w[k]
            wb[o + k] = w[k + n]
    scale = max(mp.norm(q2_c), mp.mpf(10) ** -200)
    return wa, wb, float(first), float(worst_ls / scale)


@at_precision(DPS_E6)
def relator_jet3(za_c, zb_c, wa_c, wb_c):
    """(||P1||, ||P2||, q3_root, ad_res, q3_norm) of the order-3 relator expansion.

    Letter jets (exp of a single Lie element -- no BCH), with A = ad(z1(g)), B = ad(z2(g))
    in root coordinates, X = Ad rho(letter):
      lowercase g:  [X, A X, (B + A^2/2) X, ((AB+BA)/2 + A^3/6) X]
      uppercase g:  [Xi, -Xi A, Xi (A^2/2 - B), Xi ((AB+BA)/2 - A^3/6)]
    """
    za, zb = _to_root(za_c), _to_root(zb_c)
    wa, wb = _to_root(wa_c), _to_root(wb_c)
    A = {"a": CP.ad_root(za), "b": CP.ad_root(zb)}
    B = {"a": CP.ad_root(wa), "b": CP.ad_root(wb)}
    J = {}
    for g in "ab":
        Ag, Bg = A[g], B[g]
        A2 = Ag * Ag
        AB = Ag * Bg + Bg * Ag
        A3 = A2 * Ag
        X = CP.X_root(g)
        Xi = CP.X_root(g.upper())
        half = mp.mpf(1) / 2
        sixth = mp.mpf(1) / 6
        J[g] = [X, Ag * X, (Bg + A2 * half) * X, (AB * half + A3 * sixth) * X]
        J[g.upper()] = [Xi, -(Xi * Ag), Xi * (A2 * half - Bg),
                        Xi * (AB * half - A3 * sixth)]
    P = [mp.eye(DIM), mp.zeros(DIM, DIM), mp.zeros(DIM, DIM), mp.zeros(DIM, DIM)]
    for ch in REL:
        L = J[ch]
        P = [P[0] * L[0],
             P[1] * L[0] + P[0] * L[1],
             P[2] * L[0] + P[1] * L[1] + P[0] * L[2],
             P[3] * L[0] + P[2] * L[1] + P[1] * L[2] + P[0] * L[3]]
    q3, res = _solve_ad(P[3])
    return float(mp.norm(P[1])), float(mp.norm(P[2])), q3, float(res), float(mp.norm(q3))


@at_precision(DPS_E6)
def class_complex(q_root):
    """COMPLEX H^2 class components per exponent block (phases kept for span math)."""
    q_c = CP.S_INV * q_root
    comps = []
    for m in EXPONENTS:
        u = CP.h2_functional(m)
        o, n = CP.OFFSET[m], CP.N_OF[m]
        comps.append(sum(mp.conj(u[k]) * q_c[o + k] for k in range(n)))
    return mp.matrix(comps)


def _span_residual(c0, deltas):
    """Least-squares residual of c0 against span{deltas} in C^6 (relative)."""
    Mcols = [d for d in deltas if mp.norm(d) > mp.mpf(10) ** -60]
    if not Mcols:
        return float(mp.norm(c0)), 0
    M = mp.zeros(6, len(Mcols))
    for j, d in enumerate(Mcols):
        for i in range(6):
            M[i, j] = d[i]
    U, sv, Vh = CP._svd(M)
    y = U.transpose_conj() * c0
    x = mp.zeros(len(Mcols), 1)
    smax = max(abs(s) for s in sv)
    rank = 0
    for i in range(len(sv)):
        if abs(sv[i]) > smax * mp.mpf(10) ** -30:
            rank += 1
            for j in range(len(Mcols)):
                x[j] += mp.conj(Vh[i, j]) * y[i] / sv[i]
    resid = mp.norm(M * x - c0) / max(mp.norm(c0), mp.mpf(10) ** -200)
    return float(resid), rank


@at_precision(DPS_E6)
def massey_direction(label, za_c, zb_c, zbasis):
    """Full pre-registered readout for one direction (the class of q3 modulo the z2
    indeterminacy span; with an MB12 random-vector control)."""
    t0 = time.time()
    wa, wb, first2, lsres = solve_z2(za_c, zb_c)
    p1, p2, q3, adres, q3n = relator_jet3(za_c, zb_c, wa_c=wa, wb_c=wb)
    c0 = class_complex(q3)
    deltas = []
    for (ka, kb) in zbasis:
        _, _, q3s, _, _ = relator_jet3(za_c, zb_c, wa + ka, wb + kb)
        deltas.append(class_complex(q3s) - c0)
    resid, rank = _span_residual(c0, deltas)
    # MB12: random vectors must NOT sit in the indeterminacy span
    import random
    rnd = random.Random(11)
    mb12 = []
    for _ in range(3):
        v = mp.matrix([rnd.uniform(-1, 1) + 1j * rnd.uniform(-1, 1) for _ in range(6)])
        r, _ = _span_residual(v, deltas)
        mb12.append(r)
    return {
        "label": label,
        "gate_P1": p1, "gate_P2": p2, "z2_ls_residual": lsres,
        "ad_solve_residual": adres, "q3_norm": q3n,
        "class_abs": [float(abs(c0[i])) for i in range(6)],
        "class_norm": float(mp.norm(c0)),
        "indeterminacy_rank": rank,
        "transverse_residual": resid,
        "mb12_random_residuals": mb12,
        "seconds": round(time.time() - t0, 1),
    }


@at_precision(DPS_E6)
def run_all():
    """The full pre-registered sweep (opt-in reproducer). Returns the report dict; no file
    side-effects (origin-axiom wrote massey_legA.json)."""
    rep = {}
    worst_rel, worst_auto = CP.rep_checks()
    rep["rep_checks"] = {"relator": float(worst_rel), "automorphism": float(worst_auto)}
    z = {m: CP.h1_line(m) for m in EXPONENTS}
    zbasis = [z[m] for m in EXPONENTS]
    # gate (ii): the coboundary control -- its class must be trivial at order 3 too
    import random
    rnd = random.Random(5)
    v = mp.matrix([rnd.uniform(-1, 1) for _ in range(DIM)])
    cza, czb = mp.zeros(DIM, 1), mp.zeros(DIM, 1)
    for m in EXPONENTS:
        o, n = CP.OFFSET[m], CP.N_OF[m]
        vm = mp.matrix([v[o + k] for k in range(n)])
        wa_ = CP.BLK["a"][m] * vm - vm
        wb_ = CP.BLK["b"][m] * vm - vm
        for k in range(n):
            cza[o + k] = wa_[k]
            czb[o + k] = wb_[k]
    nrm = mp.sqrt(mp.norm(cza) ** 2 + mp.norm(czb) ** 2)
    results = []
    r = massey_direction("coboundary", cza / nrm, czb / nrm, zbasis)
    results.append(r)
    print(f"  {r['label']}: P1={r['gate_P1']:.1e} |class|={r['class_norm']:.3e} "
          f"transverse={r['transverse_residual']:.3e}", flush=True)
    order = [1] + [m for m in EXPONENTS if m != 1]        # the m=1 control FIRST
    for m in order:
        r = massey_direction(f"m={m}", z[m][0], z[m][1], zbasis)
        results.append(r)
        print(f"  {r['label']}: P1={r['gate_P1']:.1e} P2={r['gate_P2']:.1e} "
              f"|class|={r['class_norm']:.3e} transverse={r['transverse_residual']:.3e} "
              f"rank={r['indeterminacy_rank']} mb12={min(r['mb12_random_residuals']):.2f} "
              f"({r['seconds']}s)", flush=True)
    rep["directions"] = results
    return rep


if __name__ == "__main__":
    t0 = time.time()
    print("depth-3 Massey obstruction sweep (ported from origin-axiom B370 leg A)\n")
    run_all()
    print(f"total: {time.time() - t0:.0f}s")
