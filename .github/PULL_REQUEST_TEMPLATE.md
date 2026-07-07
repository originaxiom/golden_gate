## What & why

<!-- What does this change, and why? Link any issue. -->

## Checklist

- [ ] `ruff check .` and `mypy` clean
- [ ] `pytest -q` green (and `OA_SLOW=1 pytest -q` if you touched the research core)
- [ ] `python -m golden_gate.core.gates` exits 0
- [ ] Tests added/updated (equality assertions for `exact` results; positive/negative controls)
- [ ] `CHANGELOG.md` updated
- [ ] New public API has a type hint, an `__all__` entry, and a docs line
- [ ] Honesty (see `GOVERNANCE.md` §2/§3): results labelled `exact`/`numeric`/`ported` correctly; no
      tolerance sold as exact; conventions stated; no novelty overclaim
