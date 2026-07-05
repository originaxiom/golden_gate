# golden_gate

Exact-arithmetic engines for metallic / Fibonacci-anyon quantum topology — and, on top
of them, a Fibonacci-anyon **braid-gate compiler** and interactive explorer.

`golden_gate` is built **inside-out**. The core is a clean, tested library of exact
computational engines (consolidated from a long research program); the outward-facing
layer is a braid compiler that turns quantum gates into Fibonacci-anyon braid sequences —
and is backed by the core's *exact* arithmetic rather than floating point, so its headline
identities (`F² = I`, the Yang–Baxter relation, `Jones(4₁; e^{2πi/5}) = 1 − √5`) hold as
symbolic equalities, not tolerance checks.

## Status — v0.1 in development

**Core engines**

- `core.cyclo` — exact arithmetic in `ℚ(ζ₆₀)` (Fraction-vector power basis mod `Φ₆₀`), the
  radical constants `√5, √−3, √−15` and the Gauss sum `g(15) = i√15`, the level-15 `T`/`S`
  Weil matrices, and exact projection into `H = ℚ(√5, √−3)` (`H_avg`, `solve_H`). Verified
  analytically faithful (each constant evaluates to its definition to 1e-30).
- `core.charvar` — the theta-lift / seam toolkit: the level-15 Weil matrices `W_m`, `Par`
  traces, DFT eigenprojectors, exact H-readouts, and multiplicative tensor completion.
  Reproduces the research program's banked results exactly (seed orders `20,12,6,20,12`;
  the ±1/48 seam value).

**Demo layer (exact-backed)**

- `demo.braiding` / `demo.gates` — the braiding matrices `σ₁, σ₂` and the **golden gate**
  = the figure-eight braid `σ₁⁻¹σ₂σ₁⁻¹σ₂`, a non-Clifford ~0.245π rotation.
- `demo.exact` — F² = I, Yang–Baxter, unitarity proved *exactly* (sympy for the `√φ`
  braid data, `core.cyclo` for the cyclotomic R-matrix).
- `demo.jones` — the figure-eight Jones value `1 − √5` proved exactly in `core.cyclo`
  (the standard normalization; the brief's `−φ` is the unnormalized Kauffman bracket).
- `demo.knots`, `demo.compiler`, `demo.visualize` — knots → gates, a braid compiler
  (brute-force + golden-gate-power methods), and text braid diagrams.

## Install & test

```bash
pip install -e .
pytest -q                 # fast tier (~25s)
OA_SLOW=1 pytest -q        # + heavy exact sweeps (symbolic Yang–Baxter, full theta-lift)
python -m golden_gate.core.gates   # banked-identity + hygiene gates; exits 0 when clean
```

## License

MIT — see `LICENSE`.
