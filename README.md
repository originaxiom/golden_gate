# golden_gate

Exact-arithmetic engines for metallic / Fibonacci-anyon quantum topology — and, on top
of them, a Fibonacci-anyon **braid-gate compiler** and interactive explorer.

`golden_gate` is built **inside-out**. The core is a clean, tested library of exact
computational engines (consolidated from a long research program); the outward-facing
layer is a braid compiler that turns quantum gates into Fibonacci-anyon braid sequences —
and is backed by the core's *exact* arithmetic rather than floating point, so its headline
identities (`F² = I`, the Yang–Baxter relation, `Jones(4₁; e^{2πi/5}) = −φ`) hold as
symbolic equalities, not tolerance checks.

## Status

**v0.1 — in development.** Landed so far:

- `golden_gate.core.cyclo` — exact arithmetic in `ℚ(ζ₆₀)` (Fraction-vector power basis mod
  `Φ₆₀`), the radical constants `√5, √−3, √−15` and the Gauss sum `g(15) = i√15`, the
  level-15 `T`/`S` Weil matrices, and projection into `H = ℚ(√5, √−3)` (`H_avg`, `solve_H`).

## Layout

```
src/golden_gate/
  core/          # the exact engines (the priority: clean, tested, reusable)
    cyclo.py     # ℚ(ζ₆₀) exact arithmetic + level-15 Weil data
    gates.py     # banked-identity / hygiene discipline checks
tests/           # exact lock tests
```

## Install & test

```bash
pip install -e .
pytest -q
python -m golden_gate.core.gates   # discipline gates; exits 0 when clean
```

## License

MIT — see `LICENSE`.
