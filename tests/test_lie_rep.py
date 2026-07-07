"""Locks for core.lie.rep (the E6 char-variety tangent of 4_1, ported B347).

Every entry point self-scopes precision (the @at_precision(DPS_REP) discipline), so these
tests deliberately do NOT open a workdps fixture -- and one test asserts the global dps is
left untouched, which is the whole point of the port's precision surgery.
"""

import os

import mpmath as mp
import pytest

from golden_gate.core.lie import rep

_SLOW = pytest.mark.skipif(os.environ.get("OA_SLOW") != "1",
                           reason="set OA_SLOW=1 for the heavy involution gradings")


def test_geometric_rep_satisfies_the_relator():
    assert rep.geometric_rep_residual() < mp.mpf(10) ** -50


def test_symrep_is_a_homomorphism():
    assert rep.symrep_homomorphism_residual() < mp.mpf(10) ** -50


def test_h1_dim_is_one_per_exponent():
    dims = {m: rep.H1_dim(m) for m in rep.EXPONENTS}
    assert dims == dict.fromkeys(rep.EXPONENTS, 1)
    assert rep.e6_tangent_total() == 6      # = rank E6


def test_no_global_dps_leak():
    # the MB3/MB13 discipline: entry points scope precision and restore it.
    before = mp.mp.dps
    rep.geometric_rep_residual()
    rep.H1_dim(4)
    assert mp.mp.dps == before


@_SLOW
def test_amphichiral_is_a_uniform_real_structure():
    # orientation-reversing involution: J^2 = +1 on every line, no split.
    assert all(rep.amphichiral_indicator(m) == 1 for m in rep.EXPONENTS)


@_SLOW
def test_hyperelliptic_grades_by_minus_one_to_m_plus_one():
    signs = {m: rep.hyperelliptic_sign(m) for m in rep.EXPONENTS}
    assert signs == {m: (-1) ** (m + 1) for m in rep.EXPONENTS}


@_SLOW
def test_run_all_bundle():
    r = rep.run_all()
    assert r["total"] == 6
    assert r["minus_eigenspace"] == [4, 8]     # the e6/f4 escape sector
