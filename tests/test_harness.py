"""Locks for core.harness -- the gating discipline, tested with stubs (no E6 compute).

These verify the load-bearing rule: run_gated runs the banked gate FIRST and refuses to call
the computation past a failed gate. A sentinel flips if the computation is ever called, so a
gated-out computation is provably never run.
"""

import os

import pytest

from golden_gate.core.harness import Preregistration, run_gated
from golden_gate.core.harness.campaign import CampaignRecord

_SLOW = pytest.mark.skipif(os.environ.get("OA_SLOW") != "1",
                           reason="set OA_SLOW=1 for the real E6 obstruction campaign")


def _prereg():
    return Preregistration(
        name="stub-campaign",
        hypothesis="the stub verdict is returned iff the gate passes",
        nulls=["nothing"],
        kill_conditions=["gate fails"],
        banked_identities=["a trivial banked check"],
    )


def test_preregistration_is_frozen():
    p = _prereg()
    with pytest.raises(Exception):
        p.name = "mutated"           # frozen dataclass -> attribute assignment blocked


def test_preregistration_normalizes_to_tuples():
    p = Preregistration(name="x", hypothesis="y", nulls=["a", "b"])
    assert p.nulls == ("a", "b")     # lists at construction become immutable tuples
    assert isinstance(p.kill_conditions, tuple)


def test_passing_gate_runs_the_computation():
    calls = []

    def gate():
        return True, "banked identity holds"

    def computation():
        calls.append(1)
        return {"verdict": "unobstructed"}

    rec = run_gated(_prereg(), gate, computation)
    assert isinstance(rec, CampaignRecord)
    assert rec.gate_passed and rec.computed
    assert rec.verdict == {"verdict": "unobstructed"}
    assert calls == [1]              # computation ran exactly once


def test_failed_gate_refuses_to_run_the_computation():
    calls = []

    def gate():
        return False, "banked identity REGRESSED"

    def computation():
        calls.append(1)              # must never happen
        return "should not be read"

    rec = run_gated(_prereg(), gate, computation)
    assert not rec.gate_passed
    assert not rec.computed
    assert rec.verdict is None       # never read past a failed gate
    assert calls == []               # the sentinel proves the computation was skipped
    assert "REGRESSED" in rec.gate_detail


def test_crashing_gate_is_a_failed_gate():
    calls = []

    def gate():
        raise RuntimeError("gate blew up")

    def computation():
        calls.append(1)
        return "unreached"

    rec = run_gated(_prereg(), gate, computation)
    assert not rec.gate_passed and not rec.computed
    assert calls == []
    assert "gate raised" in rec.gate_detail


def test_record_summaries_are_legible():
    passed = run_gated(_prereg(), lambda: (True, "ok"), lambda: 42)
    failed = run_gated(_prereg(), lambda: (False, "bad"), lambda: 42)
    assert "gate PASS" in passed.summary() and "verdict: 42" in passed.summary()
    assert "gate FAIL" in failed.summary() and "REFUSED" in failed.summary()
    assert "preregistration: stub-campaign" in _prereg().summary()


@_SLOW
def test_demo_e6_campaign_passes_the_gate_and_finds_unobstructed():
    # the harness on a real gate: the rep-assembly banked identity passes, so the
    # obstruction is computed, and the m=4 escape direction is unobstructed.
    from golden_gate.core.harness import demo_e6
    rec = demo_e6.run(4)
    assert rec.gate_passed and rec.computed
    assert rec.verdict["unobstructed"]
    assert rec.verdict["worst_component"] < 1e-20
    # the prereg is frozen and names the banked identity that gated the run
    assert rec.prereg.banked_identities and "rep_checks" in rec.prereg.banked_identities[0]
