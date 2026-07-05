"""Compiler tests -- correctness on reachable targets."""

import numpy as np

from golden_gate.demo import gates as G
from golden_gate.demo.compiler import (CompilationResult, compile_gate,
                                        compress_word)


def test_identity_compiles_to_empty_word():
    r = compile_gate(np.eye(2, dtype=complex))
    assert r.fidelity >= 1 - 1e-9
    assert r.word == []


def test_recover_golden_gate_word():
    r = compile_gate(G.golden_gate(), max_length=6, tolerance=1e-6)
    assert r.fidelity >= 1 - 1e-6
    # the recovered gate matches (the word may differ but the gate is the target)
    assert np.allclose(r.gate, G.golden_gate(), atol=1e-6)


def test_recover_a_short_braid_target():
    from golden_gate.demo.braiding import evaluate_braid
    target = evaluate_braid([(1, 1), (2, 1), (1, 1)])   # sigma1 sigma2 sigma1
    r = compile_gate(target, max_length=6, tolerance=1e-6)
    assert r.fidelity >= 1 - 1e-6


def test_golden_method_recovers_powers_of_G():
    G3 = np.linalg.matrix_power(G.golden_gate(), 3)
    r = compile_gate(G3, method="golden", tolerance=1e-6)
    assert r.fidelity >= 1 - 1e-6


def test_compress_word():
    assert compress_word([(1, 1), (1, 1), (2, -1)]) == [(1, 2), (2, -1)]
    assert compress_word([(1, 1), (1, -1)]) == []


def test_result_repr_and_fields():
    r = compile_gate(G.golden_gate(), max_length=6, tolerance=1e-6)
    assert isinstance(r, CompilationResult)
    assert r.length == len(r.word)
    assert abs(r.error - (1 - r.fidelity)) < 1e-12


def test_bad_method_rejected():
    import pytest
    with pytest.raises(ValueError):
        compile_gate(np.eye(2, dtype=complex), method="quantum_magic")
