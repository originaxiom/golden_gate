"""Knot -> braid -> gate tests."""

import numpy as np

from golden_gate.demo import gates as G
from golden_gate.demo import knots as K


def test_unknot_gate_is_identity():
    assert np.allclose(K.knot_to_gate("unknot"), np.eye(2))


def test_figure_eight_gate_is_the_golden_gate():
    assert np.allclose(K.knot_to_gate("figure_eight"), G.golden_gate())


def test_trefoil_gate_differs_from_figure_eight():
    assert not np.allclose(K.knot_to_gate("trefoil"), K.knot_to_gate("figure_eight"))


def test_all_named_knot_gates_are_unitary():
    for name in K.KNOT_BRAIDS:
        U = K.knot_to_gate(name)
        assert np.allclose(U @ U.conj().T, np.eye(2)), name


def test_unknown_knot_raises():
    import pytest
    with pytest.raises(KeyError):
        K.knot_braid("borromean")
