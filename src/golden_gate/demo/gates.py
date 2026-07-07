"""Named gates and gate metrics on the Fibonacci-anyon qubit.

The **golden gate** is the figure-eight knot braid ``sigma1^-1 sigma2 sigma1^-1
sigma2`` -- a non-Clifford single-qubit rotation by ~0.245*pi on the Bloch sphere.
"""

import numpy as np

from .braiding import evaluate_braid

__all__ = ["golden_gate", "golden_gate_mirror", "golden_gate_word", "gate_properties",
           "gate_fidelity", "infidelity", "is_clifford"]

# figure-eight knot as a 3-strand braid word
_GOLDEN_WORD = [(1, -1), (2, 1), (1, -1), (2, 1)]
_GOLDEN_MIRROR_WORD = [(1, 1), (2, -1), (1, 1), (2, -1)]

_I = np.eye(2, dtype=complex)
_X = np.array([[0, 1], [1, 0]], dtype=complex)
_Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
_Z = np.array([[1, 0], [0, -1]], dtype=complex)
_PAULIS = {"I": _I, "X": _X, "Y": _Y, "Z": _Z}


def golden_gate() -> np.ndarray:
    """The figure-eight knot gate: ``sigma1^-1 sigma2 sigma1^-1 sigma2``."""
    return evaluate_braid(_GOLDEN_WORD)


def golden_gate_mirror() -> np.ndarray:
    """The mirror (amphichiral partner) gate: ``sigma1 sigma2^-1 sigma1 sigma2^-1``."""
    return evaluate_braid(_GOLDEN_MIRROR_WORD)


def golden_gate_word() -> list:
    """The braid word of the golden gate (a fresh copy)."""
    return list(_GOLDEN_WORD)


def _su2_part(U):
    """Strip the global phase: return the SU(2) representative U / sqrt(det U)."""
    det = np.linalg.det(U)
    return U / np.sqrt(det)


def is_clifford(U, tol=1e-9) -> bool:
    """True iff ``U`` maps each Pauli to a (signed) Pauli under conjugation."""
    for P in (_X, _Y, _Z):
        C = U @ P @ U.conj().T
        # C must be proportional to a single Pauli with unit coefficient
        coeffs = {name: np.trace(Q.conj().T @ C) / 2 for name, Q in _PAULIS.items()}
        big = [(name, c) for name, c in coeffs.items() if abs(c) > tol]
        if len(big) != 1:
            return False
        name, c = big[0]
        if name == "I" or abs(abs(c) - 1) > tol:
            return False
    return True


def gate_properties(U) -> dict:
    """Properties of a 2x2 unitary: eigenvalues, rotation angle/axis on the Bloch
    sphere, Clifford-ness, trace, determinant, and the Pauli decomposition
    ``U = a0 I + ax X + ay Y + az Z``.
    """
    eig = np.linalg.eigvals(U)
    Usu2 = _su2_part(U)
    tr_su2 = np.trace(Usu2)               # real for a true SU(2) element
    # geodesic rotation angle on the Bloch sphere, in [0, pi]; abs() picks the
    # sqrt(det) branch and folds a reflex angle (theta about n = 2pi-theta about -n).
    angle = 2.0 * np.arccos(np.clip(abs(np.real(tr_su2)) / 2.0, 0.0, 1.0))
    # axis from Usu2 = cos(theta/2) I - i sin(theta/2) (n.sigma): the Pauli
    # coefficients are -i sin(theta/2) n_k, so n_k = -Im(coeff)/sin(theta/2).
    # NOTE: the axis SIGN is convention-dependent -- it is read from Usu2 = U/sqrt(det),
    # and the sqrt(det) branch is arbitrary, so (angle, axis) fix the rotation only up to
    # the simultaneous flip (angle, axis) -> (2pi-angle, -axis). angle is folded to [0,pi]
    # via abs() above; the axis is returned unreconciled with that fold.
    coeffs = np.array([np.trace(P.conj().T @ Usu2) / 2 for P in (_X, _Y, _Z)])
    axis_vec = np.imag(coeffs)
    norm = np.linalg.norm(axis_vec)
    axis = tuple(axis_vec / norm) if norm > 1e-12 else (0.0, 0.0, 0.0)
    pauli = tuple(np.trace(P.conj().T @ U) / 2 for P in (_I, _X, _Y, _Z))
    return {
        "eigenvalues": tuple(eig),
        "rotation_angle": float(angle),
        "rotation_axis": axis,
        "is_clifford": is_clifford(U),
        "trace": complex(np.trace(U)),
        "determinant": complex(np.linalg.det(U)),
        "pauli_decomposition": pauli,
    }


def gate_fidelity(U, V) -> float:
    """Process fidelity ``F = |tr(U^dagger V)|^2 / 4`` in ``[0, 1]``."""
    return float(abs(np.trace(U.conj().T @ V)) ** 2 / 4.0)


def infidelity(U, V) -> float:
    """``1 - gate_fidelity(U, V)`` in ``[0, 1]`` -- the compilation error measure.

    (This is the process infidelity, NOT the trace distance ``(1/2)||U-V||_1``.)
    """
    return 1.0 - gate_fidelity(U, V)
