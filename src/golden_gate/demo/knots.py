"""Named knots as 3-strand braid words, and the anyon gate each one implements."""

import numpy as np

from .braiding import evaluate_braid
from .jones import jones_at_fibonacci

# Standard knot braid words on 3 strands (generator, power).
KNOT_BRAIDS = {
    "unknot": [],
    "trefoil": [(1, 1), (1, 1), (1, 1)],                 # sigma1^3
    "figure_eight": [(1, -1), (2, 1), (1, -1), (2, 1)],  # the golden gate word
    "cinquefoil": [(1, 1), (1, 1), (1, 1), (1, 1), (1, 1)],  # sigma1^5
}


def knot_braid(knot_name):
    """The braid word of a named knot (a fresh copy)."""
    if knot_name not in KNOT_BRAIDS:
        raise KeyError(f"unknown knot {knot_name!r}; known: {sorted(KNOT_BRAIDS)}")
    return list(KNOT_BRAIDS[knot_name])


def knot_to_gate(knot_name) -> np.ndarray:
    """The 2x2 Fibonacci-anyon gate implemented by a named knot's braid."""
    return evaluate_braid(knot_braid(knot_name))


def jones_value(knot_name):
    """The knot's Jones polynomial at the Fibonacci point ``zeta_5`` (exact,
    as a ``core.cyclo`` element). See ``golden_gate.demo.jones``."""
    return jones_at_fibonacci(knot_name)
