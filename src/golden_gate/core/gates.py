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
                  ".js", ".ts", ".json", ".yaml", ".yml"}


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


def gate_no_forbidden_tokens():
    """Hygiene: no Claude/session labels leaked into tracked text source."""
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
        for tok in _FORBIDDEN_TOKENS:
            if tok in text:
                hits.append(f"{p.relative_to(ROOT)}:{tok}")
    return (not hits, "clean" if not hits else f"forbidden tokens: {hits}")


def gate_license_present():
    """Hygiene: an MIT license file exists."""
    lic = ROOT / "LICENSE"
    ok = lic.exists() and "MIT License" in lic.read_text(encoding="utf-8", errors="ignore")
    return (ok, "MIT LICENSE present" if ok else "LICENSE missing or not MIT")


GATES = {
    "cyclo-radicals": gate_cyclo_radicals,
    "cyclo-weil-unitary": gate_cyclo_weil_unitary,
    "no-forbidden-tokens": gate_no_forbidden_tokens,
    "license-present": gate_license_present,
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
