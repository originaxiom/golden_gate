"""Exact lock tests for golden_gate.core.cyclo.

Everything here is exact `Fraction` arithmetic -- no tolerances, no floats.
"""

from fractions import Fraction as Fr

from golden_gate.core import cyclo as C

# --- field structure -------------------------------------------------------

def test_dimensions():
    assert C.CONDUCTOR == 60
    assert C.DEG == 16          # phi(60)
    assert C.LEVEL == 15
    assert len(C.ONE) == C.DEG
    assert len(C.ZERO) == C.DEG


def test_one_zero_are_neutral():
    a = C.SQRT5
    assert C.add(a, C.ZERO) == a
    assert C.mul(a, C.ONE) == a
    assert C.mul(a, C.ZERO) == C.ZERO


def test_zeta_is_a_60th_root_of_unity():
    z = C.zeta(1)
    p = C.one()
    for _ in range(60):
        p = C.mul(p, z)
    assert p == C.ONE                       # zeta^60 = 1
    # and primitive: zeta^k != 1 for 0 < k < 60
    p = C.one()
    for k in range(1, 60):
        p = C.mul(p, z)
        assert p != C.ONE, f"zeta^{k} = 1 (not primitive)"


def test_e15_character():
    # e15(t) = zeta^{4t}; e15 is a character of Z/15
    for s in range(15):
        for t in range(15):
            assert C.mul(C.e15(s), C.e15(t)) == C.e15(s + t)
    assert C.e15(0) == C.ONE
    assert C.e15(15) == C.ONE


def test_multiplication_is_commutative_and_associative():
    a, b, c = C.SQRT5, C.SQRTm3, C.zeta(7)
    assert C.mul(a, b) == C.mul(b, a)
    assert C.mul(C.mul(a, b), c) == C.mul(a, C.mul(b, c))
    # distributive
    assert C.mul(a, C.add(b, c)) == C.add(C.mul(a, b), C.mul(a, c))


# --- radical constants (exact) ---------------------------------------------

def test_radical_squares():
    assert C.mul(C.SQRT5, C.SQRT5) == C.scal(Fr(5), C.ONE)
    assert C.mul(C.SQRTm3, C.SQRTm3) == C.scal(Fr(-3), C.ONE)
    assert C.mul(C.SQRT15, C.SQRT15) == C.scal(Fr(15), C.ONE)
    assert C.mul(C.SQRTm15, C.SQRTm15) == C.scal(Fr(-15), C.ONE)
    assert C.mul(C.I_UNIT, C.I_UNIT) == C.scal(Fr(-1), C.ONE)


def test_sqrtm15_factorization():
    # sqrt(-15) = sqrt5 * sqrt(-3)
    assert C.SQRTm15 == C.mul(C.SQRT5, C.SQRTm3)
    # sqrt15 = sqrt5 * sqrt3, and sqrt(-15) = i * sqrt15
    assert C.SQRTm15 == C.mul(C.I_UNIT, C.SQRT15)


def test_gauss_sum():
    # g(15) = i*sqrt15, |g|^2 = 15, g^2 = -15
    assert C.mul(C.G15, C.G15) == C.scal(Fr(-15), C.ONE)
    assert C.mul(C.G15, C.G15_INV) == C.ONE          # 1/g exact
    # |g|^2 = g * conj(g) = 15
    assert C.mul(C.G15, C.conj(C.G15)) == C.scal(Fr(15), C.ONE)


# --- conjugation -----------------------------------------------------------

def test_conjugation_is_an_involution():
    for a in (C.SQRT5, C.SQRTm3, C.SQRTm15, C.G15, C.zeta(7), C.e15(4)):
        assert C.conj(C.conj(a)) == a


def test_conjugation_signs():
    # real radical fixed; imaginary radicals negated
    assert C.conj(C.SQRT5) == C.SQRT5
    assert C.conj(C.SQRTm3) == C.scal(Fr(-1), C.SQRTm3)
    assert C.conj(C.I_UNIT) == C.scal(Fr(-1), C.I_UNIT)
    assert C.conj(C.SQRTm15) == C.scal(Fr(-1), C.SQRTm15)


# --- T / S Weil matrices ---------------------------------------------------

def test_T_S_are_invertible_exactly():
    T, Ti, S, Si = C.Tmat(), C.Tinv(), C.Smat(), C.Sinv()
    assert C.is_identity(C.mmul(T, Ti))
    assert C.is_identity(C.mmul(S, Si))


def test_T_diagonal_order_15():
    # T = diag(e15(x^2)); T^15 = I since e15 has order dividing 15 on integers
    T = C.Tmat()
    p = C.mat_identity()
    for _ in range(15):
        p = C.mmul(p, T)
    assert C.is_identity(p)


def test_S_squared_is_parity_up_to_sign():
    # S^2 permutes x -> -x mod 15, up to a global sign (rho(-I))
    S2 = C.mmul(C.Smat(), C.Smat())
    sign = None
    for i in range(C.LEVEL):
        for j in range(C.LEVEL):
            expect_pos = C.ONE if ((-i) % C.LEVEL) == j else C.ZERO
            entry = S2[i][j]
            if entry == expect_pos:
                s = 1
            elif entry == C.scal(Fr(-1), expect_pos):
                s = -1
            else:
                raise AssertionError(f"S^2[{i}][{j}] is not +-parity")
            if entry != C.ZERO:
                assert sign in (None, s)
                sign = s
    assert sign in (1, -1)


# --- Weil generators: exact orders -----------------------------------------

def test_weil_generator_orders():
    # rho(A_1) has order 20, rho(A_2) has order 12 -- exactly.
    W1 = C.weil_generator(1)
    p = C.mat_identity()
    for k in range(1, 21):
        p = C.mmul(p, W1)
        if k < 20:
            assert not C.is_identity(p), f"W1^{k} = I too early"
    assert C.is_identity(p), "W1^20 != I"

    W2 = C.weil_generator(2)
    q = C.mat_identity()
    for k in range(1, 13):
        q = C.mmul(q, W2)
        if k < 12:
            assert not C.is_identity(q), f"W2^{k} = I too early"
    assert C.is_identity(q), "W2^12 != I"


# --- projection into H = Q(sqrt5, sqrt(-3)) --------------------------------

def test_solve_H_on_basis():
    assert C.solve_H(C.ONE) == (Fr(1), Fr(0), Fr(0), Fr(0))
    assert C.solve_H(C.SQRT5) == (Fr(0), Fr(1), Fr(0), Fr(0))
    assert C.solve_H(C.SQRTm3) == (Fr(0), Fr(0), Fr(1), Fr(0))
    assert C.solve_H(C.SQRTm15) == (Fr(0), Fr(0), Fr(0), Fr(1))


def test_solve_H_roundtrip():
    t = C.add(C.add(C.scal(Fr(2), C.ONE), C.scal(Fr(-3, 2), C.SQRT5)),
              C.add(C.scal(Fr(5), C.SQRTm3), C.scal(Fr(7, 4), C.SQRTm15)))
    assert C.solve_H(t) == (Fr(2), Fr(-3, 2), Fr(5), Fr(7, 4))


def test_solve_H_rejects_outside_H():
    # zeta_60 itself is not in H = Q(sqrt5, sqrt-3)
    assert C.solve_H(C.zeta(1)) is None


def test_H_avg_projects_into_H():
    # For t already in H, H_avg is the identity; for a general element it lands in H.
    assert C.H_avg(C.SQRT5) == C.SQRT5
    assert C.H_avg(C.ONE) == C.ONE
    projected = C.H_avg(C.zeta(1))
    assert C.solve_H(projected) is not None      # the projection is in H
