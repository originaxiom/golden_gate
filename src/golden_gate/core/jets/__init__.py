"""golden_gate.core.jets -- the higher-order deformation jets on top of core.lie.

A subpackage (like ``core.lie``) so each ported engine keeps its own ``run``/``run_all``
and helpers namespaced apart.

Modules
-------
boundary     : the E6 boundary restriction of 4_1 -- rank, the Neumann-Zagier slopes, the
               universal-tau identity, the symplectic controls (mpmath, DPS_BOUNDARY).
               Depends on core.lie.rep. (ported B357)
massey       : the third-order (Massey) obstruction via relator jet arithmetic (mpmath,
               DPS_E6). Depends on core.lie.cohomology. (ported B370 leg A)
massey_legB  : the depth-2 tau-defect matrix on the boundary torus (mpmath, DPS_E6).
               Depends on massey + boundary. (ported B370 leg B)
"""

from . import boundary  # noqa: F401
from . import massey  # noqa: F401
from . import massey_legB  # noqa: F401
