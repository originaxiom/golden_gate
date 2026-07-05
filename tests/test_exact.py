"""EXACT backing of the demo -- the rigor differentiator.

sympy proves the sqrt(phi) braid identities symbolically; core.cyclo proves the
cyclotomic facts; and the exact golden gate is cross-checked against the float64
runtime.
"""

import os

import numpy as np
import pytest
import sympy as sp

from golden_gate.demo import exact as X
from golden_gate.demo import gates as G

# The full symbolic Yang-Baxter proof needs sympy to collapse exp(i*pi/5) mixed
# with sqrt(phi) (expand_complex over a triple matrix product): ~60 s. It is the
# banked exact result; gate it behind OA_SLOW. The always-on tier proves YB in
# float64 (test_braiding.py) and to high precision (below).
_slow = pytest.mark.skipif(os.environ.get("OA_SLOW") != "1",
                           reason="symbolic Yang-Baxter proof (~60s); set OA_SLOW=1")


# --- sympy exact braid identities ------------------------------------------

def test_F_matrix_exact():
    assert X.F_squared_is_identity()          # F^2 = I (uses 1 + phi = phi^2)
    assert X.F_determinant() == -1
    assert X.F_is_symmetric()


@_slow
def test_yang_baxter_exact_symbolic():
    assert X.yang_baxter_holds()


def test_yang_baxter_high_precision():
    # fast always-on exact-ish check: the braid relation holds to 40+ digits.
    import mpmath as mp
    with mp.workdps(50):
        def num(M):
            return mp.matrix([[mp.mpc(sp.N(sp.re(M[i, j]), 50), sp.N(sp.im(M[i, j]), 50))
                               for j in range(2)] for i in range(2)])
        s1, s2 = num(X.SIGMA1_EXACT), num(X.SIGMA2_EXACT)
        defect = mp.norm((s1 * s2 * s1) - (s2 * s1 * s2))
        assert defect < mp.mpf(10) ** -40, defect


def test_sigmas_unitary_exact():
    assert X.sigma_is_unitary(1)
    assert X.sigma_is_unitary(2)


def test_golden_gate_exact_is_special_unitary():
    gge = X.golden_gate_exact()
    assert sp.simplify(gge.det()) == 1


def test_exact_golden_gate_matches_float_runtime():
    gge = X.golden_gate_exact()
    exact_num = np.array([[complex(sp.N(gge[i, j], 30)) for j in range(2)]
                          for i in range(2)])
    assert np.allclose(exact_num, G.golden_gate(), atol=1e-12)


# --- core.cyclo cyclotomic facts -------------------------------------------

def test_phi_squared_identity_in_cyclo():
    assert X.phi_squared_identity_cyclo()     # phi^2 = phi + 1 exactly in Q(zeta_60)


def test_R_phases_are_exact_roots_of_unity():
    assert X.r_phases_are_roots_of_unity()


def test_cyclo_R_phases_match_float_constants():
    import mpmath as mp

    from golden_gate.core import cyclo as C
    from golden_gate.demo import constants as K

    def _ev(a):
        with mp.workdps(30):
            z = mp.e ** (2j * mp.pi / C.CONDUCTOR)
            return complex(sum(mp.mpf(a[k].numerator) / mp.mpf(a[k].denominator) * z ** k
                               for k in range(C.DEG)))

    r1, r2 = X.r_matrix_cyclo()
    assert np.isclose(_ev(r1), K.R_VACUUM)
    assert np.isclose(_ev(r2), K.R_TAU)
