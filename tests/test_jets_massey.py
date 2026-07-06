"""Locks for core.jets.massey + massey_legB (the depth-2/3 jets, ported B370).

Fast tier: the exact-Gram ad-solve round-trip (the arithmetic backbone of both legs), which
is cheap. OA_SLOW tier: a BOUNDED banking of the B370 verdict -- for the m=1 direction, the
order-1 and order-2 relator gates vanish and the ad-solve is clean (leg A), and the leg-B
first-order universal-tau equals the cusp shape. The full pre-registered sweeps are opt-in
reproducers: `python -m golden_gate.core.jets.massey` / `...massey_legB`.
"""

import os
import random

import mpmath as mp
import pytest

from golden_gate.core.jets import massey as M
from golden_gate.core.jets import massey_legB as LB
from golden_gate.core.lie import cohomology as CP

_SLOW = pytest.mark.skipif(os.environ.get("OA_SLOW") != "1",
                           reason="set OA_SLOW=1 for the heavy dps-100 jet readouts")


def test_solve_ad_round_trip_is_exact():
    # ad(q) = P recovered exactly (the exact-integer Gram normal equations); the backbone
    # of the whole jet stack. Must run at DPS_E6 -- ad_root/gram carry 100-digit values.
    with mp.workdps(CP.DPS_E6):
        rnd = random.Random(3)
        q = mp.matrix([rnd.uniform(-1, 1) for _ in range(CP.DIM)])
        P = CP.ad_root(q)
        qrec, res = M._solve_ad(P)
        assert res < mp.mpf(10) ** -60
        assert mp.norm(qrec - q) / mp.norm(q) < mp.mpf(10) ** -60


def test_no_global_dps_leak_from_solve_ad():
    before = mp.mp.dps
    with mp.workdps(CP.DPS_E6):
        q = mp.matrix([mp.mpf(1) / (i + 2) for i in range(CP.DIM)])
        M._solve_ad(CP.ad_root(q))
    assert mp.mp.dps == before


def test_class_complex_is_linear():
    # class_complex reads the 6 block H^2 functionals; it must be linear (a cheap check
    # that the S_INV / h2_functional wiring is a genuine linear readout, not garbled).
    with mp.workdps(CP.DPS_E6):
        import random
        rnd = random.Random(1)
        q = mp.matrix([rnd.uniform(-1, 1) for _ in range(CP.DIM)])
        c1 = M.class_complex(q)
        c2 = M.class_complex(3 * q)
        assert c1.rows == 6
        # NONZERO on a generic input -- the discriminating control that keeps the OA_SLOW
        # "class vanishes" verdicts honest (class_complex is not silently the zero map).
        assert mp.norm(c1) > mp.mpf("0.01")
        assert max(abs(c2[i] - 3 * c1[i]) for i in range(6)) < mp.mpf(10) ** -30


def test_span_residual_projects_correctly():
    # the indeterminacy-span projection (pure C^6 linear algebra): a vector inside the span
    # residuates to ~0; a fully-transverse vector residuates to its own norm; empty span
    # returns the vector's norm and rank 0.
    with mp.workdps(CP.DPS_E6):
        e = [mp.matrix([mp.mpf(1) if i == j else mp.mpf(0) for i in range(6)]) for j in range(6)]
        in_span = 3 * e[0] - 2 * e[1]
        r_in, rank_in = M._span_residual(in_span, [e[0], e[1]])
        assert r_in < 1e-30 and rank_in == 2
        r_out, _ = M._span_residual(e[2], [e[0], e[1]])
        assert abs(r_out - 1.0) < 1e-20          # e2 orthogonal to span -> residual = |e2|
        r_empty, rank_empty = M._span_residual(e[0], [])
        assert abs(r_empty - 1.0) < 1e-20 and rank_empty == 0


@_SLOW
def test_massey_m1_gates_vanish_and_class_is_trivial():
    # leg A, m=1 integrable control: z1 is a cocycle (P1~0), z2 solves order 2 (P2~0),
    # the order-3 ad-solve is clean, AND the raw depth-3 Massey class vanishes -- the m=1
    # direction is tangent to the actual A-poly curve, so it integrates to all orders and
    # its class is already 0 before modding by the indeterminacy. This last assertion is the
    # discriminating one: it exercises the full order-3 jet (the A^3/6, (AB+BA)/2 terms) ->
    # q3 -> class_complex path, so a sign error in those terms (invisible to the P1/P2 gates,
    # which are order 1/2) is caught here. The full transverse-residual verdict modulo the
    # 6-dim indeterminacy span is the opt-in `python -m golden_gate.core.jets.massey` sweep
    # (~10 min, not a suite test).
    z1 = CP.h1_line(1)
    wa, wb, first2, lsres = M.solve_z2(*z1)
    assert first2 < 1e-30                        # first-order residual (z1 a cocycle)
    assert lsres < 1e-20                         # z2 least-squares residual
    p1, p2, q3, adres, q3n = M.relator_jet3(z1[0], z1[1], wa, wb)
    assert p1 < 1e-30                            # order-1 gate
    assert p2 < 1e-30                            # order-2 gate
    assert adres < 1e-30                         # order-3 ad-solve residual
    assert q3n > 1.0                             # discriminating: q3 is genuinely nonzero...
    c0 = M.class_complex(q3)
    assert float(mp.norm(c0)) < 1e-30            # ...yet its H^2 class vanishes (integrable)


@_SLOW
def test_word_jet2_order2_solves_cleanly():
    # covers word_jet2's ORDER-2 path (the c2 extraction M2 = P2 X0^-1 - A1^2/2), which the
    # first-order tau test does not (it passes zero z2). A short word keeps it bounded; the
    # ad-solve residuals of both c1 and c2 must be clean.
    z1 = CP.h1_line(1)
    wa, wb, _first, _ls = M.solve_z2(*z1)
    c1, c2, r1, r2 = LB.word_jet2("ab", z1[0], z1[1], wa, wb)
    assert r1 < 1e-30 and r2 < 1e-30
    assert c1.rows == CP.DIM and c2.rows == CP.DIM


@_SLOW
def test_legB_first_order_tau_is_the_cusp_shape():
    # leg B first-order gate: the universal tau (phi_lam / phi_mu) equals the boundary
    # engine's cusp shape (magnitude 2*sqrt(3)), block-diagonally.
    from golden_gate.core.jets import boundary as B
    z1 = CP.h1_line(1)
    zero = mp.zeros(CP.DIM, 1)
    c1mu, _c2, r1mu, _ = LB.word_jet2(LB.MU, z1[0], z1[1], zero, zero)
    c1la, _c2, r1la, _ = LB.word_jet2(LB.LAM, z1[0], z1[1], zero, zero)
    blk = B.block(1)
    K = B.pairing(blk["dim"])

    def phi(v):
        u = LB.chain_block_TG(v, 1)
        return (u.T * K * blk["h"])[0, 0]

    with mp.workdps(CP.DPS_E6):
        tau = phi(c1la) / phi(c1mu)
        assert abs(abs(tau) - abs(B.CUSP_SHAPE)) < mp.mpf(10) ** -30
        assert abs(tau.real) < mp.mpf(10) ** -30     # purely imaginary
    assert max(r1mu, r1la) < 1e-30                    # order-1 ad-solve residual clean
