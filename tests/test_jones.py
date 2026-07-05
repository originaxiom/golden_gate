"""Jones-polynomial tests -- the figure-eight value is exact and axiom-consistent."""

from fractions import Fraction as Fr

from golden_gate.core import cyclo as C
from golden_gate.demo import jones as J


def test_unknot_is_one():
    assert J.jones_at_fibonacci("unknot") == C.ONE


def test_figure_eight_is_exactly_one_minus_sqrt5():
    # the flagship exact identity; matches the origin-axiom B314 colored-Jones data
    assert J.figure_eight_is_one_minus_sqrt5()
    assert J.jones_at_fibonacci("figure_eight") == C.sub(C.ONE, C.SQRT5)


def test_figure_eight_is_NOT_minus_phi():
    # honesty guard: the STANDARD normalized Jones is 1 - sqrt5, not -phi.
    minus_phi = C.scal(Fr(-1), C.add(C.scal(Fr(1, 2), C.ONE), C.scal(Fr(1, 2), C.SQRT5)))
    assert J.jones_at_fibonacci("figure_eight") != minus_phi


def test_bracket_convention_factor_recovers_minus_phi():
    # standard_value * (phi^2 / 2) = -phi, exactly (an algebraic identity)
    v = J.jones_at_fibonacci("figure_eight")
    norm = J.bracket_convention_factor()
    minus_phi = C.scal(Fr(-1), C.add(C.scal(Fr(1, 2), C.ONE), C.scal(Fr(1, 2), C.SQRT5)))
    assert C.mul(v, norm) == minus_phi


def test_trefoil_differs_from_figure_eight():
    assert J.jones_at_fibonacci("trefoil") != J.jones_at_fibonacci("figure_eight")


def test_jones_symbolic():
    import sympy as sp
    t = sp.symbols("t")
    expr = J.jones_symbolic("figure_eight")
    # V(4_1;t) = t^2 - t + 1 - t^-1 + t^-2
    assert sp.simplify(expr - (t**2 - t + 1 - 1 / t + 1 / t**2)) == 0


def test_unknown_knot_raises():
    import pytest
    with pytest.raises(KeyError):
        J.jones_at_fibonacci("borromean")
