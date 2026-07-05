"""Golden-gate and gate-metric tests (float64 runtime)."""

import numpy as np

from golden_gate.demo import gates as G


def test_golden_gate_is_the_figure_eight_word():
    assert G.golden_gate_word() == [(1, -1), (2, 1), (1, -1), (2, 1)]


def test_golden_gate_unitary_and_special():
    U = G.golden_gate()
    assert np.allclose(U @ U.conj().T, np.eye(2))
    assert abs(abs(np.linalg.det(U)) - 1.0) < 1e-12


def test_golden_gate_rotation_angle():
    props = G.gate_properties(G.golden_gate())
    assert 0.244 * np.pi <= props["rotation_angle"] <= 0.246 * np.pi


def test_golden_gate_is_non_clifford():
    assert not G.gate_properties(G.golden_gate())["is_clifford"]


def test_is_clifford_controls():
    # positive control: Pauli X and Hadamard are Clifford; negative: golden gate.
    X = np.array([[0, 1], [1, 0]], dtype=complex)
    H = np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)
    assert G.is_clifford(X)
    assert G.is_clifford(H)
    assert not G.is_clifford(G.golden_gate())


def test_mirror_differs_from_golden():
    assert not np.allclose(G.golden_gate(), G.golden_gate_mirror())


def test_fidelity_and_infidelity():
    U = G.golden_gate()
    assert abs(G.gate_fidelity(U, U) - 1.0) < 1e-12
    assert G.gate_fidelity(U, np.eye(2, dtype=complex)) < 1.0
    assert abs(G.infidelity(U, U)) < 1e-12
    assert G.infidelity(U, np.eye(2, dtype=complex)) > 0.0


def test_pauli_decomposition_reconstructs():
    U = G.golden_gate()
    a0, ax, ay, az = G.gate_properties(U)["pauli_decomposition"]
    I = np.eye(2, dtype=complex)
    X = np.array([[0, 1], [1, 0]], dtype=complex)
    Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
    Z = np.array([[1, 0], [0, -1]], dtype=complex)
    assert np.allclose(a0 * I + ax * X + ay * Y + az * Z, U)
