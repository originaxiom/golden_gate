"""golden_gate.core — the exact computational engines.

Modules
-------
cyclo   : exact arithmetic in Q(zeta_60); radical constants; level-15 T/S Weil data.
charvar : theta-lift / seam toolkit (Weil matrices, par-trace, eigenprojectors,
          exact H-readouts, multiplicative tensor completion).
gates   : banked-identity / hygiene discipline checks (stdlib-only, deterministic).
"""

from . import charvar  # noqa: F401
from . import cyclo  # noqa: F401
