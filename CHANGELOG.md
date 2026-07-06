# Changelog

All notable changes to `golden_gate` are recorded here. Format follows
[Keep a Changelog](https://keepachangelog.com/); this project is pre-1.0. Detailed working
history is in `PROGRESS_LOG.md`.

---

## [Unreleased]

### Added — M3 (the heavy mpmath research core)
- **`core.precision`** — centralized mpmath working-precision discipline: a
  `working_precision(dps)` context manager, an `@at_precision(dps)` decorator, and the named
  engine precisions `DPS_E6=100 / DPS_REP=70 / DPS_BOUNDARY=60`. No engine mutates the global
  `mp.mp.dps` at import; every entry point re-scopes and restores (the MB3/MB13 lesson).
- **`core.lie`** (subpackage) — the E6 cup-product stack, ported clean:
  `e6` (exact Chevalley e6, Jacobi-verified integer structure constants, principal sl2, the
  theta involution; stdlib-only), `rep` (the E6 character-variety tangent of the figure-eight
  and its two Z/2 gradings), `cohomology` (the two-basis cup-product obstruction
  `[z u z]` in `H^2(4_1, e6)`).
- **`core.jets`** (subpackage) — `boundary` (the E6 boundary restriction: rank, the
  Neumann-Zagier slopes, the universal-tau = cusp-shape identity, symplectic controls),
  `massey` + `massey_legB` (the depth-3 Massey obstruction and the depth-2 tau-defect matrix).
- **`core.harness`** — the gate-attack harness: `Preregistration` (frozen hypothesis / nulls
  / kill conditions / banked identities), `run_gated` (runs the banked gate first and refuses
  to read the computation past a failed gate), and `demo_e6` (the harness on a real gate — the
  E6 escape obstruction).
- **`core.gates`** — added the cheap `e6-exact` banked-identity gate (Jacobi = 0 + the
  exponent weights `{2,8,10,14,16,22}`).

### Changed — M3
- **`mpmath` is now a runtime dependency** (the `core.lie` / `core.jets` / `core.harness`
  engines use it), moved out of the test-only extras.
- Port hygiene: deleted 2 `importlib._load` shims + 3 `sys.path.insert` sites (real package
  imports); removed the `massey_leg*.json` file side-effects (drivers return dicts); dropped a
  vestigial `TAU`, two dead `if False` branches, and an unused least-squares helper; made
  B347's involution intertwiners and B357's per-block data lazy + self-scoped.
- Fixed a brittle hygiene-gate test (`"0 files"` matched as a substring of `"30 files"`).

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

### Added
- **SVG braid diagrams** — `demo.visualize.braid_diagram(..., fmt="svg")` renders a
  standalone, theme-aware SVG with permuting strands and proper over/under crossings.
- **`docs/EXAMPLES.md`** — three worked examples (compile a gate, golden-gate properties,
  verify the exact Jones value).

### Changed
- **Multi-agent audit hardening.** Fixed stale `Jones = -phi` docstrings (the corrected value
  is `1 - sqrt5`); reframed the `-phi` bracket factor honestly (`bracket_convention_factor`,
  an algebraic identity, not a claimed canonical invariant); scoped the compiler's `golden`
  method honestly and covered its refinement + fallback paths (compiler 100% covered); added
  negative controls for the charvar sanity gates (documented as necessary-condition checks);
  fixed a `gate_no_forbidden_tokens` crash on out-of-root paths; renamed `trace_distance` →
  `infidelity` (it returns `1 - fidelity`, not the trace distance); `braid_diagram` now
  validates `n_strands`; moved `mpmath` to test-only dependencies (nothing in `src/` uses it
  yet).

### Notes
- The standard Jones value is `1 - sqrt5`; the brief's `-phi` is the unnormalized Kauffman
  bracket convention (`= standard * phi^2/2`). The library computes and documents the
  standard value (see `GOVERNANCE.md` §2, convention honesty).
- The braid compiler is a clean, tested implementation, not a novel algorithm — exact
  Fibonacci-anyon synthesis over `Z[phi]` is prior art (Kliuchnikov et al.).
- Tests are two-tier: a fast tier (~26 s) and heavy exact proofs behind `OA_SLOW=1`.
