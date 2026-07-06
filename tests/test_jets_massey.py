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


@_SLOW
def test_massey_m1_gates_vanish():
    # leg A, m=1 integrable control: z1 is a cocycle (P1~0), z2 solves order 2 (P2~0),
    # and the order-3 ad-solve is clean. (The full transverse-residual verdict modulo the
    # indeterminacy span is the opt-in `python -m ...massey` sweep.)
    z1 = CP.h1_line(1)
    wa, wb, first2, lsres = M.solve_z2(*z1)
    assert first2 < 1e-30                        # first-order residual (z1 a cocycle)
    assert lsres < 1e-20                         # z2 least-squares residual
    p1, p2, q3, adres, q3n = M.relator_jet3(z1[0], z1[1], wa, wb)
    assert p1 < 1e-30                            # order-1 gate
    assert p2 < 1e-30                            # order-2 gate
    assert adres < 1e-30                         # order-3 ad-solve residual


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
