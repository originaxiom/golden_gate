"""Jones polynomials of the named knots, evaluated EXACTLY at the Fibonacci point.

The Fibonacci-anyon evaluation point is ``t = e^{2 pi i / 5} = zeta_5``. Because
this is cyclotomic, the value lives in ``Q(zeta_60)`` and is computed exactly by
``golden_gate.core.cyclo`` -- no floating point.

A convention note (this matters, and the project is honest about it)
--------------------------------------------------------------------
The **standard, normalized** Jones polynomial gives

    V(4_1; zeta_5) = 1 - sqrt(5)  ~= -1.2361 ,

which is exactly the figure-eight's colored-Jones / WRT value recorded in the
origin-axiom program (its B314 data ``{1, 1-sqrt5, 1-sqrt5, 1}``). Some sources
(including the ``golden_gate`` v0.1 brief) quote ``-phi ~= -1.618`` for "the Jones
value"; that is the *unnormalized Kauffman bracket* normalization, related by

    -phi = (1 - sqrt5) * phi**2 / 2 .

``jones_at_fibonacci`` returns the **standard normalized** value ``1 - sqrt5``;
``bracket_convention_factor`` records the algebraic factor ``phi**2/2`` relating it
to the brief's ``-phi`` (stated as an identity, not derived from a canonical
bracket normalization -- we do not claim ``-phi`` is itself a standard invariant).

Standard Jones polynomials below are the textbook Knot Atlas tabulations
(Lickorish, *An Introduction to Knot Theory*). Chirality note: the chiral knots
here (trefoil, cinquefoil) are tabulated in one handedness, while the braid words
in ``golden_gate.demo.knots`` use positive crossings (``sigma1^3``, ``sigma1^5``),
which realize the *mirror* handedness; at ``t = zeta_5`` a mirror sends the value
to its complex conjugate. The figure-eight is amphichiral, so it is unaffected --
and it is the only knot whose exact value (``1 - sqrt5``, real) this library
relies on.
"""

from fractions import Fraction as Fr

import sympy as sp

from ..core import cyclo as C

__all__ = ["jones_polynomial", "jones_symbolic", "jones_at_fibonacci", "bracket_convention_factor", "figure_eight_is_one_minus_sqrt5"]

# V(K; t) as {exponent: integer coefficient}. Right-handed representatives.
JONES_POLYNOMIALS = {
    "unknot": {0: 1},
    "trefoil": {-1: 1, -3: 1, -4: -1},                 # -t^-4 + t^-3 + t^-1
    "figure_eight": {2: 1, 1: -1, 0: 1, -1: -1, -2: 1},  # t^2 - t + 1 - t^-1 + t^-2
    "cinquefoil": {-2: 1, -4: 1, -5: -1, -6: 1, -7: -1},  # -t^-7+t^-6-t^-5+t^-4+t^-2
}

# t = zeta_5 = zeta_60^12
_T_EXP = 12


def jones_polynomial(knot_name: str) -> dict:
    """The standard Jones polynomial of a named knot, as ``{exponent: coeff}``."""
    if knot_name not in JONES_POLYNOMIALS:
        raise KeyError(f"unknown knot {knot_name!r}; "
                       f"known: {sorted(JONES_POLYNOMIALS)}")
    return dict(JONES_POLYNOMIALS[knot_name])


def jones_symbolic(knot_name):
    """The Jones polynomial as an exact sympy expression in ``t``."""
    t = sp.symbols("t")
    return sum(c * t ** e for e, c in JONES_POLYNOMIALS[knot_name].items())


def jones_at_fibonacci(knot_name: str) -> list:
    """Evaluate the standard Jones polynomial at ``t = zeta_5``, EXACTLY.

    Returns the value as a ``core.cyclo`` field element (an exact vector in
    ``Q(zeta_60)``). For the figure-eight this is exactly ``1 - sqrt5``.
    """
    poly = jones_polynomial(knot_name)
    acc = C.zero()
    for e, coeff in poly.items():
        term = C.zeta((_T_EXP * e) % C.CONDUCTOR)          # t^e = zeta_60^{12 e}
        acc = C.add(acc, C.scal(Fr(coeff), term))
    return acc


def bracket_convention_factor() -> list:
    """The algebraic factor between the standard Jones value and the brief's ``-phi``.

    The standard normalized Jones is ``1 - sqrt5``; the brief quotes ``-phi``. They
    differ by exactly ``phi**2 / 2``:  ``-phi = (1 - sqrt5) * phi**2/2``. This is
    stated as an algebraic identity, NOT derived here from a specific Kauffman-bracket
    normalization -- we make no claim that ``-phi`` is a canonical knot invariant.
    Returned as an exact ``core.cyclo`` element.
    """
    phi = C.add(C.scal(Fr(1, 2), C.ONE), C.scal(Fr(1, 2), C.SQRT5))
    phi2 = C.mul(phi, phi)
    return C.scal(Fr(1, 2), phi2)


def figure_eight_is_one_minus_sqrt5() -> bool:
    """The flagship exact identity: ``V(4_1; zeta_5) = 1 - sqrt5`` in ``Q(zeta_60)``."""
    return jones_at_fibonacci("figure_eight") == C.sub(C.ONE, C.SQRT5)
