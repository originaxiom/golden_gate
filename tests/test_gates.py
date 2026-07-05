"""The discipline gates must all pass on a clean tree."""

from golden_gate.core import gates


def test_all_gates_pass():
    results = gates.run_all()
    failed = {name: detail for name, (ok, detail) in results.items() if not ok}
    assert not failed, f"gates failed: {failed}"


def test_expected_gates_present():
    assert set(gates.GATES) >= {
        "cyclo-radicals", "cyclo-weil-unitary",
        "no-forbidden-tokens", "license-present",
    }
