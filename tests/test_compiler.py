"""Compiler tests -- correctness on reachable targets, and honest coverage of the
best-effort / golden-refinement paths."""

import numpy as np

from golden_gate.demo import gates as G
from golden_gate.demo.braiding import evaluate_braid
from golden_gate.demo.compiler import CompilationResult, compile_gate, compress_word


def test_identity_compiles_to_empty_word():
    r = compile_gate(np.eye(2, dtype=complex))
    assert r.fidelity >= 1 - 1e-9
    assert r.word == []


def test_recover_golden_gate_word():
    r = compile_gate(G.golden_gate(), max_length=6, tolerance=1e-6)
    assert r.fidelity >= 1 - 1e-6
    assert np.allclose(r.gate, G.golden_gate(), atol=1e-6)


def test_recover_a_short_braid_target():
    target = evaluate_braid([(1, 1), (2, 1), (1, 1)])   # sigma1 sigma2 sigma1
    r = compile_gate(target, max_length=6, tolerance=1e-6)
    assert r.fidelity >= 1 - 1e-6


def test_brute_force_best_effort_fallback():
    # a target unreachable within a tiny max_length -> returns the BEST found
    # (fidelity < 1), not an error and not the identity.
    target = evaluate_braid([(1, 1), (2, 1), (1, -1), (2, 1), (1, 1), (2, -1)])
    r = compile_gate(target, max_length=2, tolerance=1e-9)
    assert r.fidelity < 1 - 1e-9
    assert r.length <= 2


def test_golden_recovers_a_power_of_G_exactly():
    # the golden method's core capability: find n so that G^n == target. G^3 has
    # word length 3*4 = 12.
    G3 = np.linalg.matrix_power(G.golden_gate(), 3)
    r = compile_gate(G3, method="golden", tolerance=1e-6)
    assert r.fidelity >= 1 - 1e-6
    assert r.length == 12                       # found n=3, not merely fid=1


def test_golden_refinement_branch_runs_and_is_not_better_than_brute_force():
    # a general target no power of G matches -> the refinement branch executes;
    # honest check: brute_force is at least as good (golden is a special case).
    target = evaluate_braid([(1, 1), (2, 1), (1, 1), (2, -1)])
    rg = compile_gate(target, max_length=6, method="golden", tolerance=1e-6)
    assert 0.0 <= rg.fidelity <= 1.0 and rg.length >= 1
    rb = compile_gate(target, max_length=6, tolerance=1e-6)
    assert rb.fidelity >= rg.fidelity - 1e-9


def test_compress_word():
    assert compress_word([(1, 1), (1, 1), (2, -1)]) == [(1, 2), (2, -1)]
    assert compress_word([(1, 1), (1, -1)]) == []


def test_result_repr_and_fields():
    r = compile_gate(G.golden_gate(), max_length=6, tolerance=1e-6)
    assert isinstance(r, CompilationResult)
    s = repr(r)
    assert "CompilationResult" in s and "fidelity" in s
    assert r.length == len(r.word)


def test_bad_method_rejected():
    import pytest
    with pytest.raises(ValueError):
        compile_gate(np.eye(2, dtype=complex), method="quantum_magic")


def test_input_guards():
    import pytest

    from golden_gate.demo import compiler as CO
    # target shape + finiteness are validated
    with pytest.raises(ValueError):
        compile_gate(np.eye(3, dtype=complex))
    with pytest.raises(ValueError):
        compile_gate(np.array([[np.inf, 0], [0, 1]], dtype=complex))
    # max_length is bounded (negative and explosive both refused)
    with pytest.raises(ValueError):
        CO.brute_force(np.eye(2, dtype=complex), max_length=-1)
    with pytest.raises(ValueError):
        CO.brute_force(np.eye(2, dtype=complex), max_length=CO._MAX_LENGTH + 1)


def test_max_nodes_budget_returns_best_effort():
    # a tiny node budget must terminate quickly with a valid (best-effort) result, not hang.
    from golden_gate.demo import compiler as CO
    H = np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)
    r = CO.brute_force(H, max_length=20, tolerance=1e-9, max_nodes=500)
    assert isinstance(r, CompilationResult)
    assert 0.0 <= r.fidelity <= 1.0 and r.length == len(r.word)
