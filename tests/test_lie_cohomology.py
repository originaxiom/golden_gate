"""Locks for core.lie.cohomology (the cup-product obstruction, ported B352).

Fast tier: the rep-assembly validation (relator + bracket-automorphism residuals) and the
H^1/H^2 line shapes -- the checks that certify the two-basis machinery is faithfully
assembled, without running the ~minute-scale obstruction solve.

OA_SLOW tier: a BOUNDED banking of the B352 verdict -- the m=1 curve control vanishes and
one escape direction (m=4) is unobstructed, guarded by the MB12 positive-pairing control.
The full six-direction sweep is an opt-in reproducer: `python -m
golden_gate.core.lie.cohomology`.
"""

import os

import mpmath as mp
import pytest

from golden_gate.core.lie import cohomology as CP

_SLOW = pytest.mark.skipif(os.environ.get("OA_SLOW") != "1",
                           reason="set OA_SLOW=1 for the heavy obstruction solve")


def test_rep_assembly_is_faithful():
    # the load-bearing validation: X(rel)=I per block AND X_root preserves the exact
    # integer e6 bracket. If the two-basis assembly were wrong, one of these blows up.
    worst_rel, worst_auto = CP.rep_checks()
    assert worst_rel < mp.mpf(10) ** -40
    assert worst_auto < mp.mpf(10) ** -40


def test_h1_line_is_a_unit_cocycle_per_block():
    with mp.workdps(CP.DPS_E6):
        for m in CP.EXPONENTS:
            za, zb = CP.h1_line(m)
            assert za.rows == CP.DIM and zb.rows == CP.DIM
            o, n = CP.OFFSET[m], CP.N_OF[m]
            block = {o + k for k in range(n)}
            # supported only on this block's chain coordinates (off-block entries are
            # exactly 0 -- za/zb are embedded from the n-dim block cocycle)
            in_block = sum(abs(za[o + k]) + abs(zb[o + k]) for k in range(n))
            off_block = sum(abs(za[i]) + abs(zb[i]) for i in range(CP.DIM) if i not in block)
            assert in_block > 0
            assert off_block == 0
            # the genuine cocycle property (not just the embedding): d^1_m z = 0. Without
            # this the off_block==0 check is tautological (h1_line writes only the block).
            d1, _ = CP.FOX[m]
            zblk = mp.matrix([za[o + k] for k in range(n)] + [zb[o + k] for k in range(n)])
            resid = mp.norm(d1 * zblk) / mp.norm(zblk)
            assert resid < mp.mpf(10) ** -30


def test_h2_functional_annihilates_d1():
    # the returned matrices carry DPS_E6 values; the residual arithmetic must run at
    # that precision too (the MB3 lesson applied to test code -- at ambient dps 15 the
    # sum floors at ~1e-15 and says nothing).
    with mp.workdps(CP.DPS_E6):
        for m in CP.EXPONENTS:
            d1, _ = CP.FOX[m]
            u = CP.h2_functional(m)
            n = CP.N_OF[m]
            # u^H d1 = 0 (u spans the 1-dim coker)
            resid = max(abs(sum(mp.conj(u[i]) * d1[i, j] for i in range(n)))
                        for j in range(2 * n))
            assert resid < mp.mpf(10) ** -30


def test_no_global_dps_leak():
    before = mp.mp.dps
    CP.rep_checks()
    CP.h1_line(1)
    CP.h2_functional(4)
    assert mp.mp.dps == before


def test_pairing_positive_control_is_order_one():
    # MB12 guard: the H^2 functionals pair O(1) with random vectors, so a vanishing
    # obstruction class is genuine information, not a degenerate (near-zero) pairing.
    pair = CP.control_pairing_not_vacuous()
    assert all(0.05 < v < 5 for v in pair.values())


@_SLOW
def test_m1_control_is_tangent_and_unobstructed():
    # C1: the m=1 direction is tangent to the actual A-polynomial curve of characters,
    # so its second-order obstruction class must vanish in every block.
    z1 = CP.h1_line(1)
    comps, diag = CP.obstruction_class(*z1)
    assert diag["first_order_residual"] < 1e-30   # z is a genuine cocycle
    assert diag["ad_solve_residual"] < 1e-30      # A2 = ad(q) solved cleanly
    # DISCRIMINATING control: the obstruction VECTOR q is genuinely nonzero (the 2nd-order
    # deformation exists) -- so "class vanishes" means q is a coboundary, NOT that the
    # pipeline silently produced q~0 (which would make every "unobstructed" pass falsely).
    assert diag["q_norm"] > 1.0
    assert max(comps.values()) < 1e-20            # class = 0 despite q != 0


@_SLOW
def test_coboundary_is_unobstructed():
    # C2: a gauge direction z = d^0 v has vanishing obstruction class.
    comps, diag = CP.control_coboundary()
    assert max(comps.values()) < 1e-20


@_SLOW
def test_escape_direction_m4_is_unobstructed():
    # the headline: the theta-odd escape direction m=4 integrates past second order
    # (the {4,8} components vanish by theta-parity; the F4 components vanish too).
    z4 = CP.h1_line(4)
    comps, diag = CP.obstruction_class(*z4)
    assert diag["first_order_residual"] < 1e-30
    assert diag["q_norm"] > 1.0                    # discriminating: q != 0 (see m=1 test)
    assert comps[4] < 1e-20 and comps[8] < 1e-20   # theta-parity: escape block silent
    assert max(comps.values()) < 1e-20             # unobstructed in every block
