"""A demonstration campaign: the harness run on a real gate (the E6 escape obstruction).

This wires :func:`~golden_gate.core.harness.campaign.run_gated` to an actual research
computation from :mod:`golden_gate.core.lie.cohomology`: does the theta-odd escape direction
``m=4`` (the e6/f4 = 26 sector of the E6 character variety of the figure-eight) integrate
past second order, or does the cup-product obstruction ``[z u z]`` in ``H^2`` kill it?

The point is the *shape*, not just the answer: the banked-identity gate (the rep-assembly
validation -- relator + bracket-automorphism residuals) runs FIRST, and only if it passes is
the obstruction actually computed. It is the harness discipline applied to a real gate.

This is the heavy end of the library (mpmath at dps 100); the obstruction solve takes ~1-2
minutes. Run it as ``python -m golden_gate.core.harness.demo_e6``.
"""

from __future__ import annotations

from ..lie import cohomology as CP
from .campaign import CampaignRecord, run_gated
from .prereg import Preregistration

_REL_TOL = 1e-40      # the banked relator/automorphism residual ceiling
_CLASS_TOL = 1e-20    # an obstruction component this small is "vanishing"


def escape_prereg(m: int = 4) -> Preregistration:
    """The frozen pre-registration for the m-block escape-obstruction campaign."""
    return Preregistration(
        name=f"e6-escape-obstruction-m{m}",
        hypothesis=(f"the theta-odd escape direction m={m} is UNobstructed at second order "
                    "(the cup-product class [z u z] vanishes in every exponent block)"),
        nulls=(f"the obstruction class is nonzero in some block (|component| > {_CLASS_TOL:.0e})",),
        kill_conditions=(f"rep-assembly relator or automorphism residual > {_REL_TOL:.0e} "
                         "(the two-basis machinery is not trustworthy)",),
        banked_identities=("cohomology.rep_checks: X(rel)=I per block AND X_root preserves "
                           "the exact integer e6 bracket",),
    )


def banked_gate():
    """The banked-identity gate: the rep-assembly must reproduce before any verdict is read."""
    worst_rel, worst_auto = CP.rep_checks()
    ok = float(worst_rel) < _REL_TOL and float(worst_auto) < _REL_TOL
    detail = (f"rep_checks relator={float(worst_rel):.2e} automorphism={float(worst_auto):.2e} "
              f"(ceiling {_REL_TOL:.0e})")
    return ok, detail


def compute_escape_obstruction(m: int = 4):
    """Compute the H^2 obstruction class of the m-block escape direction; return the verdict."""
    z = CP.h1_line(m)
    comps, diag = CP.obstruction_class(*z)
    worst = max(comps.values())
    return {
        "m": m,
        "components": comps,
        "worst_component": worst,
        "unobstructed": worst < _CLASS_TOL,
        "diagnostics": diag,
    }


def run(m: int = 4) -> CampaignRecord:
    """Run the full gated campaign for the m-block escape direction."""
    prereg = escape_prereg(m)
    return run_gated(prereg, banked_gate, lambda: compute_escape_obstruction(m))


if __name__ == "__main__":
    print("harness demo -- the E6 escape-obstruction campaign (gated)\n")
    rec = run(4)
    print(rec.prereg.summary())
    print()
    print(rec.summary())
