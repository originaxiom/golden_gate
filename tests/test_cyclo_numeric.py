"""Independent numeric cross-validation of the EXACT cyclo engine.

The exact tests (test_cyclo.py) check the engine against itself. These check that
the exact constructions *mean* what they claim: evaluate each Fraction-vector at
the primitive 60th root of unity and compare, at high precision, to the analytic
definition. This is the "reproduction is not interpretation" guard -- it catches a
whole class of "exact but wrong constant" bugs the self-consistent tests cannot.
"""

import mpmath as mp
import pytest

from golden_gate.core import cyclo as C

_DPS = 40


@pytest.fixture(autouse=True)
def _high_precision():
    """Scope every test in this module to dps 40, restoring the global on exit.

    Precision is never written to the global mp.mp.dps at import time -- that
    global is shared test-suite state, and mutating it pollutes other tests by
    run order (the MB13 lesson). workdps saves and restores it per test, and it
    wraps BOTH the exact-element evaluation and the analytic reference values.
    """
    with mp.workdps(_DPS):
        yield


def _evaluate(a):
    """Evaluate a field element (16-vector) at zeta_60 = exp(2*pi*i/60).

    Stays entirely in mpmath (mp.mpf coefficients) so rational coefficients like
    1/5 or 4/15 keep full dps precision -- casting through Python complex() would
    silently drop the whole evaluation to float64.
    """
    z = mp.e ** (2j * mp.pi / C.CONDUCTOR)
    return sum(mp.mpf(a[k].numerator) / mp.mpf(a[k].denominator) * z ** k
               for k in range(C.DEG))


def _close(x, y, tol=1e-30):
    return abs(complex(x) - complex(y)) < tol


def test_radicals_evaluate_analytically():
    assert _close(_evaluate(C.SQRT5), mp.sqrt(5))                 # +sqrt5, real
    assert _close(_evaluate(C.SQRTm3), 1j * mp.sqrt(3))          # +i*sqrt3
    assert _close(_evaluate(C.SQRT15), mp.sqrt(15))              # +sqrt15, real
    assert _close(_evaluate(C.SQRTm15), 1j * mp.sqrt(15))        # +i*sqrt15
    assert _close(_evaluate(C.I_UNIT), 1j)


def test_gauss_sum_evaluates_analytically():
    # g(15) = i*sqrt(15) in this convention; |g| = sqrt(15)
    assert _close(_evaluate(C.G15), 1j * mp.sqrt(15))
    assert _close(abs(_evaluate(C.G15)), mp.sqrt(15))


def test_e15_is_the_analytic_character():
    for t in range(15):
        assert _close(_evaluate(C.e15(t)), mp.e ** (2j * mp.pi * t / 15))


def test_zeta_is_the_analytic_primitive_root():
    for k in (1, 7, 12, 20, 31, 59):
        assert _close(_evaluate(C.zeta(k)), mp.e ** (2j * mp.pi * k / 60))


def test_Tmat_is_the_analytic_T():
    T = C.Tmat()
    for x in range(C.LEVEL):
        assert _close(_evaluate(T[x][x]), mp.e ** (2j * mp.pi * (x * x) / 15))


def test_Smat_is_the_analytic_S():
    # S[x][y] = e^{-2*pi*i*2xy/15} / (i*sqrt15)
    S = C.Smat()
    g = 1j * mp.sqrt(15)
    for x in range(C.LEVEL):
        for y in range(C.LEVEL):
            analytic = mp.e ** (-2j * mp.pi * 2 * x * y / 15) / g
            assert _close(_evaluate(S[x][y]), analytic), (x, y)


def test_conj_is_complex_conjugation():
    for a in (C.SQRT5, C.SQRTm3, C.SQRTm15, C.G15, C.zeta(7)):
        assert _close(_evaluate(C.conj(a)), complex(_evaluate(a)).conjugate())
