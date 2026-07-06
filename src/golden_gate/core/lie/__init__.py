"""golden_gate.core.lie -- the E6 cup-product / {4,8}-integrability engine stack.

A subpackage (not a flat module) because the three ported engines each carry a
``run_all`` and an internal ``_nullspace`` -- namespacing them apart is exactly what a
subpackage is for.

Modules
-------
e6         : the exact Chevalley e6 (integer structure constants; Jacobi-verified;
             principal sl2; the theta diagram involution). Stdlib-only. (ported B351)
rep        : the E6 character-variety tangent of the figure-eight and its two Z/2
             gradings (mpmath, DPS_REP). (ported B347)
cohomology : the two-basis cup-product obstruction [z u z] in H^2(4_1, e6)
             (mpmath, DPS_E6). Depends on e6 + rep. (ported B352)
"""

# e6 (stdlib) and rep (cheap import; its heavy internals are lazy) are eager. cohomology is
# NOT -- its import builds the dps-100 assembly (S / INTERTWINERS / BLK / FOX, ~3 s), so it is
# left for explicit import (`from golden_gate.core.lie import cohomology`). This keeps the
# cheap `e6-exact` banked gate cheap.
from . import e6  # noqa: F401
from . import rep  # noqa: F401
