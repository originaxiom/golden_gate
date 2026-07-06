"""Locks for core.jets.boundary (the E6 boundary restriction of 4_1, ported B357).

Fast tier: the peripheral gates, K-invariance, the true symplectic-nondegeneracy certificate
(omega_on_h1's 2x2 determinant), a restriction rank, and the universal-tau = cusp-shape
identity for m=1. All at DPS_BOUNDARY, self-scoped by each entry point.

Note on nondegeneracy: the E_mu/E_lam "ambient" pairing omega(E_mu, E_lam) = h^T K h is
identically ~0 (h is a peripheral invariant weight vector paired with itself), so
`symplectic_controls[...]['nondegenerate']` is always False -- the honest nondegeneracy
certificate is the determinant of omega on the actual 2-dim H^1 basis (`omega_on_h1`).
"""

import os

import mpmath as mp
import pytest

from golden_gate.core.jets import boundary as B

_SLOW = pytest.mark.skipif(os.environ.get("OA_SLOW") != "1",
                           reason="set OA_SLOW=1 for the full six-block boundary sweep")


def test_peripheral_gates():
    # mu, lam commute; both parabolic (tr=-2); the relator holds.
    assert B.peripheral_gates()


def test_K_is_rep_invariant_and_coboundaries_pair_to_zero():
    for m in (1, 4):
        sc = B.symplectic_controls(m)
        assert sc["K_invariance_err"] < mp.mpf(10) ** -40
        assert abs(sc["coboundary_pairing"]) < mp.mpf(10) ** -40


def test_omega_on_h1_is_antisymmetric_and_nondegenerate():
    # the real symplectic certificate: on the 2-dim H^1(T^2, Sym^{2m}) basis, omega is a
    # nonzero antisymmetric 2x2 form, for EVERY exponent (not just 1,4).
    #
    # Threshold: |det| decays ~exponentially with m from the e^{2m*mu} block dynamic range
    # (0.64 at m=1 down to ~3e-11 at m=11), so a fixed 1e-6 gate would MISFIRE at m>=7 -- it
    # only survived before because the loop was restricted to {1,4}. The principled gate is
    # "det is far above the dps-60 noise floor (~1e-50)": 1e-30 clears the true det at m=11
    # by ~19 decades and the noise by ~20, and matches run_all's omega_nondeg gate.
    for m in B.EXPONENTS:
        M = B.omega_on_h1(m)
        assert abs(M[0, 1] + M[1, 0]) < mp.mpf(10) ** -30 * (abs(M[0, 1]) + 1)
        det = M[0, 0] * M[1, 1] - M[0, 1] * M[1, 0]
        assert abs(det) > mp.mpf(10) ** -30


def test_restriction_rank_is_one():
    # the H^1(M) class survives restriction to the cusp (no peripherally-invisible
    # deformation) -- rank 1 per block.
    for m in (1, 3):
        assert B.restriction(m)["rank"] == 1


def test_universal_tau_is_the_cusp_shape():
    tau, dev = B.tau_identity(1)
    # the comparison arithmetic must run at the boundary precision -- at ambient dps 15
    # abs(tau) and abs(CUSP_SHAPE) each round to ~3.4641 BEFORE subtracting, flooring the
    # residual at ~1e-14 and silently passing a 1e-40 assertion (the MB3 lesson).
    with mp.workdps(B.DPS_BOUNDARY):
        # tau = -CUSP_SHAPE (up to tol): the conjugate of the cusp shape 2*sqrt(3)*i under
        # this rep's orientation (see tau_identity's sign-convention note).
        assert abs(tau - (-B.CUSP_SHAPE)) < mp.mpf(10) ** -40
        assert abs(tau.real) < mp.mpf(10) ** -40    # purely imaginary
    assert dev < mp.mpf(10) ** -40                  # single tau over the whole Z^1 basis


def test_no_global_dps_leak():
    before = mp.mp.dps
    B.peripheral_gates()
    B.restriction(1)
    B.tau_identity(1)
    assert mp.mp.dps == before


@_SLOW
def test_full_sweep_certifies_lagrangian():
    out = B.run_all()
    assert out["total_rank"] == 6
    assert out["lagrangian_certified"]
    # one universal tau across all six exponent blocks
    assert out["tau_uniform_dev"] < mp.mpf(10) ** -40
    for m in B.EXPONENTS:
        assert out["blocks"][m]["omega_nondeg"]
