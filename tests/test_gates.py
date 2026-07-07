"""The discipline gates must all pass on a clean tree."""

import re

from golden_gate.core import gates


def test_all_gates_pass():
    results = gates.run_all()
    failed = {name: detail for name, (ok, detail) in results.items() if not ok}
    assert not failed, f"gates failed: {failed}"


def test_expected_gates_present():
    assert set(gates.GATES) >= {
        "cyclo-radicals", "cyclo-weil-unitary", "charvar-theta-lift",
        "no-forbidden-tokens", "license-present", "governance-docs",
    }


def test_banked_vs_hygiene_split():
    # the user-facing `verify` (golden-gate-verify) runs ONLY the banked-identity gates, which
    # are meaningful from an installed wheel; hygiene gates are repo-only. The two partition GATES.
    assert set(gates.BANKED_GATES) | set(gates.HYGIENE_GATES) == set(gates.GATES)
    assert set(gates.BANKED_GATES) & set(gates.HYGIENE_GATES) == set()
    assert "no-forbidden-tokens" not in gates.BANKED_GATES     # repo-only, not in verify
    # every banked identity reproduces (this is what `verify` asserts)
    for name, fn in gates.BANKED_GATES.items():
        ok, detail = fn()
        assert ok, f"{name}: {detail}"


def test_forbidden_detector_positive_control():
    # the detector must actually fire (and be case-insensitive) -- a gate that
    # can never fail is vacuous. Build the probe strings from the gate's own
    # (encoded) tokens so no literal forbidden token appears in this tracked file.
    tok0, tok1 = gates._FORBIDDEN_TOKENS[0], gates._FORBIDDEN_TOKENS[1]
    assert gates.contains_forbidden(f"this mentions {tok0.capitalize()} here")
    assert gates.contains_forbidden(f"{tok0.upper()} in caps")
    assert gates.contains_forbidden(f"an {tok1} model")
    assert not gates.contains_forbidden("perfectly clean text about braids")


def test_token_gate_is_non_vacuous():
    # on the committed tree it must scan at least one file (the invariant that
    # guards against a silently-empty ls-files pass).
    ok, detail = gates.gate_no_forbidden_tokens()
    assert ok, detail
    assert "vacuous" not in detail
    # parse the actual scanned count from "clean (N files scanned)" -- a substring
    # check for "0 files" is brittle (it matches inside "30 files").
    n_scanned = int(re.search(r"clean \((\d+) files", detail).group(1))
    assert n_scanned > 0


def test_token_gate_fires_on_a_dirty_file(tmp_path, monkeypatch):
    # the file-scanning wrapper (not just the pure detector) must report a hit.
    dirty = tmp_path / "dirty.md"
    dirty.write_text("this file mentions " + gates._FORBIDDEN_TOKENS[0].capitalize())
    monkeypatch.setattr(gates, "_tracked_files", lambda: [dirty])
    ok, detail = gates.gate_no_forbidden_tokens()
    assert not ok and "forbidden" in detail
