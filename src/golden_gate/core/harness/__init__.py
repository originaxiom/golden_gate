"""golden_gate.core.harness -- the gate-attack harness (pre-registration + gated campaigns).

The research face of the library: a small, stdlib-only discipline layer that rides on top of
the core engines. A :class:`~golden_gate.core.harness.prereg.Preregistration` freezes the
hypothesis, nulls, kill conditions, and banked identities before any compute;
:func:`~golden_gate.core.harness.campaign.run_gated` runs the banked-identity gate first and
refuses to read the computation past a failed gate. :mod:`demo_e6` wires this to a real gate
(the E6 cup-product escape obstruction).
"""

from .campaign import CampaignRecord, run_gated  # noqa: F401
from .prereg import Preregistration  # noqa: F401
