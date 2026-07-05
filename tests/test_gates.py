"""The discipline gates must all pass on a clean tree."""

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
    assert "0 files" not in detail and "vacuous" not in detail


def test_token_gate_fires_on_a_dirty_file(tmp_path, monkeypatch):
    # the file-scanning wrapper (not just the pure detector) must report a hit.
    dirty = tmp_path / "dirty.md"
    dirty.write_text("this file mentions " + gates._FORBIDDEN_TOKENS[0].capitalize())
    monkeypatch.setattr(gates, "_tracked_files", lambda: [dirty])
    ok, detail = gates.gate_no_forbidden_tokens()
    assert not ok and "forbidden" in detail
