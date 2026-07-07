# Contributing to golden_gate

Thanks for your interest. `golden_gate` is a small, disciplined research/education library; the bar for
contributions is correctness and honesty, not size.

## Dev setup

```bash
git clone https://github.com/originaxiom/golden_gate
cd golden_gate
pip install -e ".[dev]"        # runtime + pytest + ruff + mypy
pre-commit install            # optional: run the checks on every commit
```

## The checks (all must be green)

```bash
ruff check .                              # lint
mypy                                      # types (the tree is mypy-clean)
pytest -q                                 # fast suite (~90 s)
OA_SLOW=1 pytest -q                        # + the heavy exact / high-precision sweeps
python -m golden_gate.core.gates          # banked-identity + hygiene gates (exit 0)
```

CI runs the same on every push/PR. **Run the gates before you commit** — the `no-forbidden-tokens`
hygiene gate has caught real slips.

## The discipline (from `GOVERNANCE.md`)

This library holds itself to an explicit honesty standard. Please keep to it:

- **Exact vs numeric (§2).** A result called **exact** must be proved by exact arithmetic
  (`core.cyclo` / sympy) and locked by an *equality* test — never a tolerance. Never present a numeric
  near-miss as an exact identity.
- **Convention honesty (§2).** State the normalization; don't silently pick the flattering value (e.g.
  the Jones value is `1 − √5`; the `−φ` some quote is a different, named convention).
- **No novelty overclaim (§2 / MB5).** The compiler is prior art; cite the literature, claim packaging
  and integration, not new algorithms.
- **Result labels (§3).** Every public result is `exact` / `numeric` / `ported`. Prose must not assert a
  stronger label than the code supports.
- **The ported research core** (`core.lie` / `core.jets`) is kept line-for-line re-verifiable against its
  origin-axiom source; avoid cosmetic reformatting there (ruff already exempts it).
- **Tests are the record.** A change to behavior comes with a test (an equality assertion for `exact`
  results, with positive/negative controls).

## Pull requests

- Small, focused, with a clear description and green checks.
- Add/adjust tests and a `CHANGELOG.md` line.
- New public API needs a type hint, an `__all__` entry, and a docs line.

## Reporting

Open an issue for bugs or ideas; see `SECURITY.md` for anything security-adjacent.
