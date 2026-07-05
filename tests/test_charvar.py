"""core.charvar tests -- theta-lift engine, gates, and the banked B367 numbers.

The full exact theta-lift readouts are heavy (~50s); they are banked behind
OA_SLOW and reproduce origin-axiom's B367 results exactly (seed orders, the DFT
eigenprojector gates, and the +-1/48 seam value = the priced-doors PD4
forced-coupling candidate). The fast tier exercises the smallest seed and the
pure-rational solvers.
"""

import os
from fractions import Fraction as Fr

import pytest

from golden_gate.core import charvar as CV

_slow = pytest.mark.skipif(os.environ.get("OA_SLOW") != "1",
                           reason="full exact theta-lift sweep (~50s); set OA_SLOW=1")


# --- fast tier (smallest seed + pure-rational solvers) ---------------------

def test_theta_lift_smallest_seed():
    # seed m=3 has order 6 (cheapest); check the order and the projector gate.
    W = CV.build_theta_W(3)
    order, powers = CV.matrix_order(W)
    assert order == 6
    assert CV.projector_gates(powers)
    assert CV.single_controls(powers)


def test_solve_model_separable():
    X3, X5, X4 = {0: Fr(2), 1: Fr(3)}, {0: Fr(1), 1: Fr(5)}, {0: Fr(1), 1: Fr(7)}
    recs = [(a, b, c, X3[a] * X5[b] * X4[c])
            for a in (0, 1) for b in (0, 1) for c in (0, 1)]
    sol = CV.solve_model(recs)
    assert sol is not None
    for a in (0, 1):
        for b in (0, 1):
            for c in (0, 1):
                assert sol[0][a] * sol[1][b] * sol[2][c] == X3[a] * X5[b] * X4[c]


def test_solve_model_rejects_non_separable():
    X3, X5, X4 = {0: Fr(2), 1: Fr(3)}, {0: Fr(1), 1: Fr(5)}, {0: Fr(1), 1: Fr(7)}
    recs = [(a, b, c, X3[a] * X5[b] * X4[c])
            for a in (0, 1) for b in (0, 1) for c in (0, 1)]
    recs[-1] = (1, 1, 1, Fr(999))
    assert CV.solve_model(recs) is None


def test_rank_over_Q():
    table = {(a, b): (0, 0, 0, Fr(a + 1) * Fr(b + 1)) for a in range(3) for b in range(3)}
    assert CV.rank_over_Q(range(3), range(3), table) == 1     # rank-1 outer product


# --- slow tier: the full exact sweep + the banked B367 numbers -------------

@pytest.fixture(scope="module")
def seeds():
    out = {}
    for m in (1, 2, 3, 4, 7):
        W = CV.build_theta_W(m)
        out[m] = CV.matrix_order(W)
    return out


@_slow
def test_all_seed_orders(seeds):
    assert {m: seeds[m][0] for m in seeds} == {1: 20, 2: 12, 3: 6, 4: 20, 7: 12}


@_slow
def test_all_projector_and_single_gates(seeds):
    for m in (1, 2, 3, 4, 7):
        assert CV.projector_gates(seeds[m][1]), m
        assert CV.single_controls(seeds[m][1]), m


@_slow
def test_pair_smatrix_reproduces_banked_1_over_48(seeds):
    # banked-identity gate: origin-axiom B367 recorded s(0,4) = 1/48, s(0,8) = -1/48
    # for the (1,2) pair -- the +-1/48 forced-coupling candidate.
    sm = CV.smat_only(CV.pair_smatrix(seeds[1][1], seeds[2][1]))
    assert sm[(0, 4)] == Fr(1, 48)
    assert sm[(0, 8)] == Fr(-1, 48)
