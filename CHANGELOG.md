# Changelog

All notable changes to `golden_gate` are recorded here. Format follows
[Keep a Changelog](https://keepachangelog.com/); this project is pre-1.0. Detailed working
history is in `PROGRESS_LOG.md`.

---

## [Unreleased]

### Added
- **`core.cyclo`** — exact arithmetic in `Q(zeta_60)` (Fraction-vector power basis mod
  `Phi_60`): field operations, the radical constants `sqrt5 / sqrt(-3) / sqrt(-15)` and the
  Gauss sum `g(15) = i*sqrt15`, the level-15 `T`/`S` Weil matrices, the metallic Weil
  generators, and exact projection into `H = Q(sqrt5, sqrt(-3))` (`H_avg`, `solve_H`).
  Verified analytically faithful (each constant evaluates to its definition to 1e-30).
- **`core.charvar`** — the theta-lift / seam toolkit: level-15 Weil matrices `W_m`, `Par`
  traces, DFT eigenprojectors, exact H-readouts, exact rank, and multiplicative tensor
  completion. Reproduces the origin-axiom B367 results exactly (seed orders 20/12/6/20/12;
  the +-1/48 seam value).
- **`core.gates`** — stdlib-only banked-identity + hygiene discipline gates.
- **Demo layer** — `demo.braiding` / `demo.gates` (the golden gate = the figure-eight braid,
  a non-Clifford ~0.245*pi rotation); `demo.exact` (F^2=I, Yang-Baxter, unitarity proved
  exactly — sympy for the sqrt(phi) braid data, core.cyclo for the cyclotomic R-matrix);
  `demo.jones` (V(4_1; zeta_5) = 1-sqrt5, proved exactly); `demo.knots`, `demo.compiler`
  (brute-force + golden-power), `demo.visualize` (text braid diagrams).
- **Governance** — `GOVERNANCE.md` (exact/numeric honesty lock, result labels, CI gates,
  method-bug guards), `PROGRESS_LOG.md` (append-only), this `CHANGELOG.md`.

### Notes
- The standard Jones value is `1 - sqrt5`; the brief's `-phi` is the unnormalized Kauffman
  bracket convention (`= standard * phi^2/2`). The library computes and documents the
  standard value (see `GOVERNANCE.md` §2, convention honesty).
- The braid compiler is a clean, tested implementation, not a novel algorithm — exact
  Fibonacci-anyon synthesis over `Z[phi]` is prior art (Kliuchnikov et al.).
- Tests are two-tier: a fast tier (~26 s) and heavy exact proofs behind `OA_SLOW=1`.
