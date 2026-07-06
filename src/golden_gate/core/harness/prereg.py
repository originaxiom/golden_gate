"""Pre-registration -- freeze the hypothesis, the nulls, and the banked gates BEFORE compute.

The discipline this encodes (from the origin-axiom METHOD): a research readout only counts if
the question, the null hypotheses, the kill conditions, and the banked identities that gate
the machinery were all fixed *before* the numbers were looked at. A :class:`Preregistration`
is a frozen (immutable) record of exactly that -- once constructed it cannot be edited, so a
campaign cannot be quietly re-specified after seeing a result it did not like.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Tuple


@dataclass(frozen=True)
class Preregistration:
    """An immutable pre-registration of a gated computation.

    Fields
    ------
    name              : short identifier for the campaign.
    hypothesis        : the claim under test, in one sentence.
    nulls             : the null hypotheses (what "nothing here" would look like).
    kill_conditions   : conditions under which the readout is void (e.g. a banked
                        identity regressed) -- the computation must not be trusted.
    banked_identities : the exact/numeric identities that must reproduce for the
                        machinery to be trusted (the gate runs these first).

    The tuple fields are frozen; ``frozen=True`` blocks attribute assignment. Construct with
    lists -- they are normalized to tuples so the record stays hashable and un-mutated.
    """

    name: str
    hypothesis: str
    nulls: Tuple[str, ...] = field(default_factory=tuple)
    kill_conditions: Tuple[str, ...] = field(default_factory=tuple)
    banked_identities: Tuple[str, ...] = field(default_factory=tuple)

    def __post_init__(self):
        # accept lists at construction; store immutable tuples (bypasses frozen setattr)
        for f in ("nulls", "kill_conditions", "banked_identities"):
            object.__setattr__(self, f, tuple(getattr(self, f)))

    def summary(self) -> str:
        lines = [f"preregistration: {self.name}",
                 f"  hypothesis         : {self.hypothesis}"]
        for label, seq in (("null", self.nulls),
                           ("kill condition", self.kill_conditions),
                           ("banked identity", self.banked_identities)):
            for item in seq:
                lines.append(f"  {label:<17}: {item}")
        return "\n".join(lines)
