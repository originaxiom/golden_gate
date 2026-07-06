"""Centralized mpmath working-precision discipline (the MB3/MB13 lesson).

``mp.mp.dps`` is a **global**, shared by every mpmath call in the process. In a
multi-engine library (and, worse, a shared test suite) any module that writes it at
import time silently changes the precision every *other* engine runs at, by nothing
more than import order. The origin-axiom engines learned this the hard way: six B347
locks passed in isolation and failed suite-wide once a different probe set ``dps=25``
before them (root-caused 2026-07-02; the ``mp.mp.dps=70`` at module load was long gone
by the time the functions ran).

The rule this module enforces:

* **Never** mutate ``mp.mp.dps`` at import time.
* Every public entry point that needs a given precision opens it **scoped** -- via the
  :func:`working_precision` context manager or the :func:`at_precision` decorator -- so
  it is saved and restored around the call and cannot leak to a caller or a sibling test.

The three engine precisions are named here so they live in exactly one place:

===================  =====  =========================================================
constant             dps    engine
===================  =====  =========================================================
``DPS_E6``           100    the E6 cup-product stack (``core.lie.cohomology``, the
                            depth-2 Massey jets); dominates the ``e^{+-2m*mu}`` block
                            dynamic range (~1e20 at m=11) with ~60 digits to spare.
``DPS_REP``           70    the geometric SL(2,C) rep / tangent gradings
                            (``core.lie.rep``).
``DPS_BOUNDARY``      60    the peripheral / boundary-restriction engine
                            (``core.jets.boundary``); its 1e-35 / 1e-18 SVD tolerances
                            are tuned for this precision.
===================  =====  =========================================================
"""

from __future__ import annotations

import functools

import mpmath as mp

# The engine precisions -- the single source of truth (see the table above).
DPS_E6 = 100
DPS_REP = 70
DPS_BOUNDARY = 60


def working_precision(dps):
    """Context manager that runs its body at ``dps`` decimal places, then restores.

    A thin, explicitly-named wrapper over :func:`mpmath.workdps` so every engine opens
    precision the same way and the intent (*scoped*, never global) is legible at the
    call site::

        with working_precision(DPS_E6):
            ...  # all mpmath here runs at 100 dps; the caller's dps is untouched
    """
    return mp.workdps(dps)


def at_precision(dps):
    """Decorator form of :func:`working_precision`: run the whole call at ``dps``.

    Use on a public entry point whose entire body needs a fixed precision::

        @at_precision(DPS_E6)
        def rep_checks():
            ...

    The wrapped call is scoped exactly like the context manager -- the global
    ``mp.mp.dps`` is saved on entry and restored on return (even on exception).
    """
    def deco(fn):
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            with mp.workdps(dps):
                return fn(*args, **kwargs)
        return wrapper
    return deco
