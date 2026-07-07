"""The gated campaign runner -- run the banked gate FIRST; never read results past a failure.

This is the load-bearing discipline of the whole harness, lifted from the origin-axiom
METHOD: *never read verdicts past a failed gate.* :func:`run_gated` runs the banked-identity
check before the computation and, if the gate fails, refuses to call the computation at all
-- the returned record carries no verdict, only the gate failure. A result that was never
computed cannot be cherry-picked.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from .prereg import Preregistration


@dataclass
class CampaignRecord:
    """The structured outcome of a gated campaign.

    ``gate_passed`` is the banked-identity verdict. ``verdict`` is the computation's result
    -- and it is ``None`` whenever ``gate_passed`` is False, because the computation was
    never run. ``computed`` records whether the computation actually executed (so a genuine
    ``None`` result is distinguishable from a gated-out one).
    """

    prereg: Preregistration
    gate_passed: bool
    gate_detail: str
    computed: bool = False
    verdict: Any | None = None

    def summary(self) -> str:
        head = f"campaign '{self.prereg.name}': gate {'PASS' if self.gate_passed else 'FAIL'}"
        if not self.gate_passed:
            return (f"{head}\n  {self.gate_detail}\n"
                    "  computation REFUSED (never read past a failed gate)")
        return f"{head} -- {self.gate_detail}\n  verdict: {self.verdict!r}"


def run_gated(prereg: Preregistration,
              banked_check: Callable[[], tuple[bool, str]],
              computation: Callable[[], Any]) -> CampaignRecord:
    """Run ``computation`` only if ``banked_check`` passes.

    ``banked_check`` returns ``(ok, detail)`` -- the banked-identity gate (the campaign's
    ``prereg.banked_identities`` made executable). If ``ok`` is False, the computation is
    NOT called and the record carries ``verdict=None``, ``computed=False``. If the gate
    itself raises, that is a failed gate (a crashing check is not a passing one).

    Returns a :class:`CampaignRecord`.
    """
    try:
        ok, detail = banked_check()
    except Exception as exc:                     # a crashing gate is a failed gate
        return CampaignRecord(prereg=prereg, gate_passed=False,
                              gate_detail=f"gate raised: {exc!r}")
    if not ok:
        return CampaignRecord(prereg=prereg, gate_passed=False, gate_detail=detail)
    result = computation()
    return CampaignRecord(prereg=prereg, gate_passed=True, gate_detail=detail,
                          computed=True, verdict=result)
