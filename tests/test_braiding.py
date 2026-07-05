"""Braiding-layer tests (float64 runtime). Exact versions live in test_exact.py."""

import numpy as np

from golden_gate.demo import braiding as B


def _unitary(U):
    return np.allclose(U @ U.conj().T, np.eye(2))


def test_generators_unitary():
    assert _unitary(B.sigma1())
    assert _unitary(B.sigma2())


def test_generator_inverses():
    assert np.allclose(B.sigma1() @ B.sigma1_inv(), np.eye(2))
    assert np.allclose(B.sigma2() @ B.sigma2_inv(), np.eye(2))


def test_yang_baxter():
    s1, s2 = B.sigma1(), B.sigma2()
    assert np.allclose(s1 @ s2 @ s1, s2 @ s1 @ s2)


def test_empty_braid_is_identity():
    assert np.allclose(B.evaluate_braid([]), np.eye(2))


def test_single_generator():
    assert np.allclose(B.evaluate_braid([(1, 1)]), B.sigma1())
    assert np.allclose(B.evaluate_braid([(2, 1)]), B.sigma2())
    assert np.allclose(B.evaluate_braid([(1, -1)]), B.sigma1_inv())


def test_power_and_cancellation():
    # sigma1^3 == three sigma1 factors; sigma1 sigma1^-1 == I
    assert np.allclose(B.evaluate_braid([(1, 3)]),
                       B.sigma1() @ B.sigma1() @ B.sigma1())
    assert np.allclose(B.evaluate_braid([(1, 1), (1, -1)]), np.eye(2))


def test_bad_generator_rejected():
    import pytest
    with pytest.raises(ValueError):
        B.evaluate_braid([(3, 1)])
