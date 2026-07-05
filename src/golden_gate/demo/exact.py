"""Exact backing for the Fibonacci-anyon braid data -- the rigor differentiator.

The demo runtime computes in float64 (fast, and what a compiler search needs). This
module proves the headline identities *exactly*, in two exact backends chosen to
match the arithmetic:

* **sympy** for the braid data, whose F-matrix entry ``1/sqrt(phi)`` involves
  ``sqrt(phi)`` -- a NON-cyclotomic nested radical (``Q(sqrt(phi))`` is not abelian
  over Q). Here ``F**2 = I``, ``det F = -1``, the Yang-Baxter relation, and
  unitarity are symbolic equalities, not tolerance checks.
* **golden_gate.core.cyclo** for the cyclotomic facts: the R-matrix phases are
  exact 60th roots of unity, and the golden ratio satisfies ``phi**2 = phi + 1``
  exactly in ``Q(zeta_60)``. (The standard Jones value ``1 - sqrt5`` is also
  cyclotomic and is proved exactly in ``golden_gate.demo.jones``; the brief's
  ``-phi`` is the unnormalized Kauffman-bracket convention, ``= (1-sqrt5)*phi^2/2``.)
"""

from fractions import Fraction as Fr

import sympy as sp

from ..core import cyclo as C

# --- sympy exact braid data ------------------------------------------------
_phi = (1 + sp.sqrt(5)) / 2
_sqphi = sp.sqrt(_phi)

F_EXACT = sp.Matrix([[1 / _phi, 1 / _sqphi],
                     [1 / _sqphi, -1 / _phi]])

_R1 = sp.exp(-4 * sp.I * sp.pi / 5)      # R^{tau tau}_1
_R2 = sp.exp(3 * sp.I * sp.pi / 5)       # R^{tau tau}_tau
_D = sp.diag(_R1, _R2)

SIGMA1_EXACT = _D
SIGMA2_EXACT = F_EXACT * _D * F_EXACT    # F^-1 = F since F^2 = I


def _is_zero_matrix(M):
    # expand_complex first: it collapses mixed exp(i*pi/5) / sqrt(phi) entries to a
    # genuine symbolic 0. Plain simplify() falls back to a numerical near-zero
    # (e.g. -0.e-137) on these, which is not a rigorous exact-zero proof.
    return all(sp.simplify(sp.expand_complex(M[i, j])) == 0
               for i in range(M.rows) for j in range(M.cols))


def F_squared_is_identity() -> bool:
    """``F**2 = I`` exactly (rests on the golden identity ``1 + phi = phi**2``)."""
    return _is_zero_matrix(sp.expand(F_EXACT * F_EXACT) - sp.eye(2))


def F_determinant():
    """``det F`` (exactly ``-1``)."""
    return sp.simplify(F_EXACT.det())


def F_is_symmetric() -> bool:
    return _is_zero_matrix(F_EXACT - F_EXACT.T)


def yang_baxter_holds() -> bool:
    """The braid relation ``sigma1 sigma2 sigma1 = sigma2 sigma1 sigma2`` -- exact."""
    lhs = SIGMA1_EXACT * SIGMA2_EXACT * SIGMA1_EXACT
    rhs = SIGMA2_EXACT * SIGMA1_EXACT * SIGMA2_EXACT
    return _is_zero_matrix(lhs - rhs)


def sigma_is_unitary(which: int) -> bool:
    """``sigma_which`` is unitary exactly (``S S^dagger = I``)."""
    S = {1: SIGMA1_EXACT, 2: SIGMA2_EXACT}[which]
    Sdag = S.conjugate().T
    return _is_zero_matrix(sp.simplify(S * Sdag) - sp.eye(2))


def golden_gate_exact():
    """The golden gate ``sigma1^-1 sigma2 sigma1^-1 sigma2`` as an exact sympy matrix."""
    s1i = SIGMA1_EXACT.inv()
    return sp.simplify(s1i * SIGMA2_EXACT * s1i * SIGMA2_EXACT)


# --- core.cyclo bridge (the cyclotomic exact facts) ------------------------

def phi_cyclo():
    """The golden ratio ``phi = (1 + sqrt5)/2`` as an exact ``core.cyclo`` element."""
    return C.add(C.scal(Fr(1, 2), C.ONE), C.scal(Fr(1, 2), C.SQRT5))


def phi_squared_identity_cyclo() -> bool:
    """``phi**2 = phi + 1`` proved exactly in ``Q(zeta_60)``."""
    phi = phi_cyclo()
    return C.mul(phi, phi) == C.add(phi, C.ONE)


# R-matrix phases as exact 60th roots of unity:
#   R_1   = e^{-4 pi i/5} = e^{2 pi i (-24/60)} = zeta_60^{36}
#   R_tau = e^{ 3 pi i/5} = e^{2 pi i ( 18/60)} = zeta_60^{18}
R_VACUUM_CYCLO_EXPONENT = 36
R_TAU_CYCLO_EXPONENT = 18


def r_matrix_cyclo():
    """The R-matrix phases as exact ``core.cyclo`` elements ``(R_1, R_tau)``."""
    return C.zeta(R_VACUUM_CYCLO_EXPONENT), C.zeta(R_TAU_CYCLO_EXPONENT)


def r_phases_are_roots_of_unity() -> bool:
    """Each R phase is an exact 60th root of unity (``z**60 = 1``)."""
    ok = True
    for z in r_matrix_cyclo():
        p = C.one()
        for _ in range(60):
            p = C.mul(p, z)
        ok = ok and (p == C.ONE)
    return ok
