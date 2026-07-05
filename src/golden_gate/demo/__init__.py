"""golden_gate.demo -- the outward-facing Fibonacci-anyon braid-gate layer.

Numerical runtime (numpy complex128) for speed, with the headline identities
(Yang-Baxter, F**2 = I, unitarity, Jones(4_1; zeta_5) = 1 - sqrt5) proved EXACTLY in
``golden_gate.demo.exact`` (sympy for the sqrt(phi) braid data; ``core.cyclo`` for
the cyclotomic R-matrix and Jones value). The exactness is the differentiator vs
existing float-only anyon-braiding tools.
"""

from . import constants  # noqa: F401
