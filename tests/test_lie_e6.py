"""Exact structural locks for core.lie.e6 (the integer Chevalley e6, ported B351).

All exact (integer / Fraction) -- no precision fixture needed. Fast tier.
"""

from golden_gate.core.lie import e6


def test_jacobi_exact_zero():
    # the load-bearing exactness fact: Jacobi holds over all 76,076 basis triples.
    assert e6.jacobi_residual_count() == 0


def test_antisymmetry():
    assert e6.antisymmetry_holds()


def test_dimensions():
    assert e6.DIM == 78
    assert len(e6.POS) == 36
    assert e6.NROOTS == 72


def test_principal_c():
    assert [int(x) for x in e6.PRINCIPAL_C] == [16, 22, 30, 42, 30, 16]


def test_principal_sl2_relations():
    assert e6.principal_relations_hold()


def test_exponent_weights_are_twice_exponents():
    assert e6.exponent_weights() == [2, 8, 10, 14, 16, 22]
    assert e6.EXPONENTS == [1, 4, 5, 7, 8, 11]


def test_theta_is_an_involutive_automorphism():
    auto, invol, fixed, minus = e6.theta_checks()
    assert auto and invol
    assert fixed == 52   # f4
    assert minus == 26   # e6/f4 coset


def test_theta_commutes_with_principal_sl2():
    assert e6.theta_commutes_with_principal_sl2()


def test_theta_signs_are_minus_one_to_the_m_plus_one():
    signs = e6.theta_signs_on_exponent_lines()
    assert signs == {m: (-1) ** (m + 1) for m in e6.EXPONENTS}
    # the escape sector {4,8} is exactly the theta-odd part
    assert sorted(m for m, s in signs.items() if s < 0) == [4, 8]


def test_run_all_bundle():
    r = e6.run_all()
    assert r["jacobi_violations"] == 0
    assert r["theta_fixed_dim"] == 52 and r["theta_minus_dim"] == 26
    assert r["exponent_weights"] == [2, 8, 10, 14, 16, 22]
