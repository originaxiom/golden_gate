"""Braiding matrices on the 3-tau fusion space, and braid-word evaluation.

Three ``tau`` anyons with total charge ``tau`` span a 2-dimensional fusion space
(the qubit). ``sigma1`` exchanges anyons 1,2 (diagonal in this basis);
``sigma2`` exchanges 2,3 (requires recoupling through the F-matrix).

A braid word is a list of ``(generator, power)`` tuples, ``generator in {1, 2}``,
``power`` a (possibly negative) integer.
"""

import numpy as np

from .constants import F_MATRIX, R_TAU, R_VACUUM


def sigma1() -> np.ndarray:
    """Braiding sigma_1 (exchange anyons 1,2): diag(R_1, R_tau)."""
    return np.diag([R_VACUUM, R_TAU]).astype(complex)


def sigma2() -> np.ndarray:
    """Braiding sigma_2 (exchange anyons 2,3): F^-1 diag(R_1,R_tau) F.

    Since F^2 = I, F^-1 = F.
    """
    return F_MATRIX @ np.diag([R_VACUUM, R_TAU]) @ F_MATRIX


def sigma1_inv() -> np.ndarray:
    return np.diag([np.conj(R_VACUUM), np.conj(R_TAU)]).astype(complex)


def sigma2_inv() -> np.ndarray:
    return F_MATRIX @ np.diag([np.conj(R_VACUUM), np.conj(R_TAU)]) @ F_MATRIX


_GEN = {1: sigma1, 2: sigma2}


def evaluate_braid(word) -> np.ndarray:
    """Evaluate a braid word to a 2x2 unitary.

    Parameters
    ----------
    word : list[tuple[int, int]]
        Each ``(generator, power)`` with ``generator in {1, 2}`` and integer
        ``power`` (negative = inverse). The empty word is the identity.

    Examples
    --------
    >>> # figure-eight: sigma1^-1 sigma2 sigma1^-1 sigma2
    >>> _ = evaluate_braid([(1, -1), (2, 1), (1, -1), (2, 1)])
    """
    U = np.eye(2, dtype=complex)
    for gen, power in word:
        if gen not in _GEN:
            raise ValueError(f"generator must be 1 or 2, got {gen!r}")
        base = _GEN[gen]()
        step = base if power >= 0 else np.linalg.inv(base)
        for _ in range(abs(int(power))):
            U = U @ step
    return U
