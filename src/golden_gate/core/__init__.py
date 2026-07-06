"""golden_gate.core — the exact & high-precision computational engines.

Modules / subpackages
---------------------
cyclo     : exact arithmetic in Q(zeta_60); radical constants; level-15 T/S Weil data.
charvar   : theta-lift / seam toolkit (Weil matrices, par-trace, eigenprojectors,
            exact H-readouts, multiplicative tensor completion).
precision : centralized mpmath working-precision discipline (the MB3/MB13 lesson).
lie       : the E6 cup-product stack -- exact Chevalley e6, the character-variety
            tangent of the figure-eight, and the two-basis cup-product obstruction.
jets      : the higher-order deformation jets -- boundary restriction, depth-2/3 Massey.
harness   : the gate-attack harness (pre-registration + gated campaigns).
gates     : banked-identity / hygiene discipline checks (stdlib-only, deterministic).

The mpmath engines (lie / jets / harness) are intentionally NOT imported at package import,
so `import golden_gate.core.cyclo` stays cheap; import them explicitly, e.g.
`from golden_gate.core.lie import cohomology`.
"""

from . import charvar  # noqa: F401
from . import cyclo  # noqa: F401
from . import precision  # noqa: F401
