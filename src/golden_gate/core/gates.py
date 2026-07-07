"""Banked-identity & hygiene gates -- stdlib-only, deterministic, no network.

Mirrors the origin-axiom ``scripts/gates`` discipline: a dict of cheap checks each
returning ``(ok: bool, detail: str)``. ``run_all()`` runs them; ``python -m
golden_gate.core.gates`` prints ``PASS/FAIL`` per gate and exits non-zero on any
failure, so every green CI run enforces them.

Two kinds of gate:

* **banked-identity** -- a core exact identity must reproduce (if the engine ever
  regresses, this fails loudly before any downstream number is trusted).
* **hygiene** -- repo-level invariants (no accidental Claude/session labels in
  tracked source; a license is present).
"""

from __future__ import annotations

import base64
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]

# base64-encoded so the literal tokens are not themselves tracked plaintext matches
_FORBIDDEN_TOKENS = [base64.b64decode("Y2xhdWRl").decode(),              # "claude"
                     base64.b64decode("QW50aHJvcGlj").decode(),          # "Anthropic"
                     base64.b64decode("Q2xhdWRlLVNlc3Npb24=").decode()]  # "Claude-Session"

_TEXT_SUFFIXES = {".py", ".md", ".txt", ".toml", ".cfg", ".ini", ".rst", ".jsx",
                  ".js", ".ts", ".json", ".yaml", ".yml", ".html", ".css"}


def _tracked_files():
    """Git-tracked files (falls back to a filesystem walk if not a git repo)."""
    try:
        out = subprocess.run(["git", "-C", str(ROOT), "ls-files"],
                             capture_output=True, text=True, check=True)
        return [ROOT / line for line in out.stdout.splitlines() if line]
    except Exception:
        return [p for p in ROOT.rglob("*") if p.is_file() and ".git" not in p.parts]


def gate_cyclo_radicals():
    """Banked identity: the core cyclotomic radicals square correctly."""
    from fractions import Fraction as Fr

    from . import cyclo as C
    checks = {
        "sqrt5^2=5": C.mul(C.SQRT5, C.SQRT5) == C.scal(Fr(5), C.ONE),
        "sqrt(-3)^2=-3": C.mul(C.SQRTm3, C.SQRTm3) == C.scal(Fr(-3), C.ONE),
        "sqrt(-15)^2=-15": C.mul(C.SQRTm15, C.SQRTm15) == C.scal(Fr(-15), C.ONE),
        "g(15)^2=-15": C.mul(C.G15, C.G15) == C.scal(Fr(-15), C.ONE),
    }
    bad = [k for k, v in checks.items() if not v]
    return (not bad, "all radical identities hold" if not bad else f"FAILED: {bad}")


def gate_cyclo_weil_unitary():
    """Banked identity: T*T^-1 = I and S*S^-1 = I exactly at level 15."""
    from . import cyclo as C
    ok = C.is_identity(C.mmul(C.Tmat(), C.Tinv())) and \
        C.is_identity(C.mmul(C.Smat(), C.Sinv()))
    return (ok, "T,S invertible exactly" if ok else "T or S inverse FAILED")


def contains_forbidden(text):
    """Return the list of forbidden tokens present in ``text`` (case-insensitive).

    Pure function so the detector can be unit-tested with a positive control -- a
    gate that can never fire is worse than no gate (the vacuity trap).
    """
    low = text.lower()
    return [tok for tok in _FORBIDDEN_TOKENS if tok.lower() in low]


def gate_no_forbidden_tokens():
    """Hygiene: no Claude/session labels leaked into tracked text source."""
    scanned = 0
    hits = []
    for p in _tracked_files():
        if p.suffix.lower() not in _TEXT_SUFFIXES:
            continue
        if p.name == "gates.py" and p.parent.name == "core":
            continue  # this file legitimately holds the (encoded) token list
        try:
            text = p.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        scanned += 1
        for tok in contains_forbidden(text):
            try:
                label = p.relative_to(ROOT)
            except ValueError:
                label = p
            hits.append(f"{label}:{tok}")
    if hits:
        return (False, f"forbidden tokens: {hits}")
    # non-vacuity: a clean verdict only counts if we actually scanned something
    if scanned == 0:
        return (False, "vacuous: no tracked text files scanned (nothing committed?)")
    return (True, f"clean ({scanned} files scanned)")


def gate_license_present():
    """Hygiene: an MIT license file exists."""
    lic = ROOT / "LICENSE"
    ok = lic.exists() and "MIT License" in lic.read_text(encoding="utf-8", errors="ignore")
    return (ok, "MIT LICENSE present" if ok else "LICENSE missing or not MIT")


def gate_governance_docs_present():
    """Hygiene: the governance / log / changelog docs exist (GOVERNANCE.md sec.8)."""
    required = ["GOVERNANCE.md", "PROGRESS_LOG.md", "CHANGELOG.md"]
    missing = [d for d in required if not (ROOT / d).exists()]
    return (not missing, "governance docs present" if not missing
            else f"missing: {missing}")


def gate_charvar_theta_lift():
    """Banked identity: the theta-lift Weil matrix at seed 3 has order 6 exactly."""
    from . import charvar as CV
    order, _ = CV.matrix_order(CV.build_theta_W(3))
    return (order == 6, f"theta-lift seed-3 order = {order} (expect 6)")


def gate_e6_exact():
    """Banked identity: the exact Chevalley e6 is Jacobi-clean and carries the right
    exponent decomposition (cheap: integer arithmetic, ~0.2 s)."""
    from .lie import e6
    jac = e6.jacobi_residual_count()
    weights = e6.exponent_weights()
    ok = jac == 0 and weights == [2, 8, 10, 14, 16, 22]
    return (ok, f"e6 Jacobi violations = {jac} (expect 0); ad-h weights = {weights}")


GATES = {
    "cyclo-radicals": gate_cyclo_radicals,
    "cyclo-weil-unitary": gate_cyclo_weil_unitary,
    "charvar-theta-lift": gate_charvar_theta_lift,
    "e6-exact": gate_e6_exact,
    "no-forbidden-tokens": gate_no_forbidden_tokens,
    "license-present": gate_license_present,
    "governance-docs": gate_governance_docs_present,
}


def run_all():
    results = {}
    for name, fn in GATES.items():
        try:
            results[name] = fn()
        except Exception as exc:  # a crashing gate is a failing gate
            results[name] = (False, f"ERROR: {exc!r}")
    return results


def main():
    results = run_all()
    worst = 0
    for name, (ok, detail) in results.items():
        print(f"[{'PASS' if ok else 'FAIL'}] {name}: {detail}")
        if not ok:
            worst = 1
    sys.exit(worst)


if __name__ == "__main__":
    main()
