# golden_gate — Progress Log

Append-only, chronological. Every work session: what was built, what was verified, what was
found. Governed by `GOVERNANCE.md` §8. Newest entries at the bottom.

---

## 2026-07-05 — M1: scaffold + core.cyclo (the exact cyclotomic engine)

Founded the repo inside-out. Package scaffold (src-layout, MIT, `pyproject` with
`pythonpath=["src","."]`), and the first core engine.

- **`core.cyclo`** — exact `Q(zeta_60)` arithmetic as length-16 `Fraction` vectors mod
  `Phi_60`: field ops, the radical constants `sqrt5 / sqrt(-3) / sqrt(-15)` and the Gauss
  sum `g(15)=i*sqrt15`, the level-15 `T`/`S` Weil matrices, the metallic Weil generators,
  and exact projection into `H = Q(sqrt5, sqrt(-3))` (`H_avg`, `solve_H`). Ported clean from
  origin-axiom `B358` (conductor-60 vs level-15 named apart; `sys.path` hacks and JSON
  side-effects removed; stdlib-only).
- **`core.gates`** — stdlib-only deterministic banked-identity + hygiene gates.
- Verified: 20 exact lock tests green; gates exit 0.

## 2026-07-05 — M1 self-audit

Adversarial pass before building on M1. Found and fixed three real issues:

1. The engine was self-consistent but unverified as **faithful** — added 7 independent
   numeric cross-validation tests (mpmath, 1e-30): every constant and the T/S matrices
   evaluate to their analytic definitions (the MB6 reproduction-is-not-interpretation
   guard). Caught + fixed a test-helper precision bug (Python `complex()` cast dropped
   fractional coefficients to float64).
2. Hygiene gate hardened: case-insensitive detection, a unit-tested pure `contains_forbidden`,
   a non-vacuity guard (fails if 0 files scanned), a positive control.
3. Applied the scoped-precision discipline (MB3): a `workdps` autouse fixture, no global
   `mp.dps` mutation; verified the global stays at default after the suite.

## 2026-07-05 — M2: exact-backed demo layer + core.charvar

- **M2a — braiding + the golden gate.** `demo/constants`, `demo/braiding`, `demo/gates`,
  `demo/exact`. The golden gate = the figure-eight braid `sigma1^-1 sigma2 sigma1^-1 sigma2`
  (non-Clifford, ~0.245*pi rotation). Exact backing: `F^2=I`, `det F=-1`, Yang-Baxter, and
  unitarity proved symbolically (sympy, since the F-matrix's `1/sqrt(phi)` is non-cyclotomic);
  `core.cyclo` proves the R-matrix phases are exact 60th roots of unity and `phi^2=phi+1`.
- **M2b — Jones, knots, compiler, visualize.** `demo/jones` proves `V(4_1; zeta_5) = 1-sqrt5`
  **exactly** in `core.cyclo`. **Convention honesty (MB4):** the brief's `-phi` is the
  unnormalized Kauffman bracket (`= standard * phi^2/2`); a test asserts the standard value
  is `1-sqrt5` and NOT `-phi`, matching origin-axiom's B314 colored-Jones data. `demo/knots`,
  `demo/compiler` (brute-force + golden-power, with an honest prior-art note — Kliuchnikov
  et al.), `demo/visualize` (text braid diagrams).
- **M2c — `core.charvar`.** The theta-lift / seam toolkit ported onto `core.cyclo` (no
  `sys.path`/JSON/transcribed-data). **Banked-identity reproduction:** it reproduces
  origin-axiom's B367 numbers exactly — seed orders `{1:20,2:12,3:6,4:20,7:12}`, the DFT
  eigenprojector gates, and the `+-1/48` seam value (the priced-doors PD4 forced-coupling
  candidate).
- Verified: fast tier 79 passed / 4 skipped (~26 s); full `OA_SLOW=1` suite 83 passed, no
  global-dps leak; all discipline gates exit 0.

## 2026-07-05 — Governance instituted

Adopted `GOVERNANCE.md` (axiom discipline adapted to a software library: the exact/numeric
honesty lock, result labels, the CI gates, the red-team lens, method-bug guards MB1-MB6),
this `PROGRESS_LOG.md` (append-only), and `CHANGELOG.md`. Standing directive: commit and push
constantly; never touch origin-axiom (read-only reference).

## 2026-07-05 — Independent multi-agent audit of M2 + hardening

Three adversarial auditors (math correctness; test rigor/code quality; port faithfulness/
honesty), each read-only/run-only. Headline: **no CRITICAL/HIGH correctness defects** — the
exact core (`cyclo`, `charvar`) is faithful and strong, ports verified line-for-line, the
banked B367 numbers (orders 20/12/6/20/12, the ±1/48 seam) reproduced, the previously-fixed
traps (global `mp.dps`, circular mirroring, vacuous hygiene gate) confirmed remediated. All
findings addressed:

- **Honesty (§2 lock):** three stale `Jones = -phi` docstrings (`core/cyclo`, `demo/exact`,
  `demo/__init__`) contradicted the corrected `1-sqrt5` framing — fixed. The `jones.py`
  bracket factor `phi^2/2` was named "the Kauffman bracket normalization" without derivation
  — renamed `bracket_convention_factor`, reframed as an algebraic identity (no claim `-phi`
  is a canonical invariant). Chirality label made honest (the tabulated trefoil/cinquefoil
  are the mirror of `knots.py`'s positive-crossing braids; figure-eight amphichiral, immune).
- **Compiler (H1/H2/M2/M5):** the `golden` method's refinement branch was untested and it is
  not competitive as a general method — scoped honestly (best only near powers of G), and
  now fully covered: a refinement-branch test (with an honest "brute_force >= golden" check),
  a brute-force best-effort-fallback test, and `compile_gate` now passes `max_length` through
  to golden instead of silently dropping it. `compiler.py` coverage 100%.
- **Vacuity (M1/M3):** replaced a tautological `error == 1-fidelity` test with a real `repr`
  test; added **negative controls** for the charvar sanity gates (a perturbed power cache is
  rejected) and documented them as *necessary-condition* checks (degenerate all-identity
  input passes vacuously — stated, not hidden).
- **Hygiene robustness (M4):** added a hit-path test for the token gate — which exposed a
  real bug: `gate_no_forbidden_tokens` crashed (`relative_to`) on a path outside the repo
  root; fixed to degrade gracefully.
- **Naming/edges (L1–L4):** `trace_distance` (which returned `1-fidelity`, not the trace
  distance) renamed `infidelity`; `rotation_axis` sign-convention caveat documented;
  `braid_diagram` now validates `n_strands`; thin wrappers (`jones_symbolic`, `jones_value`)
  tested; redundant `golden_word` removed.

Verified: fast tier 86 passed / 4 skipped (~29 s); full `OA_SLOW=1` suite 90 passed, no
dps leak; coverage 92% overall (`compiler`/`jones`/`knots`/`visualize`/`braiding` 100%,
`cyclo` 97%); all discipline gates exit 0.

## 2026-07-05 — Review follow-ups (SVG renderer, examples)

Acting on a peer review's polish suggestions:

- **SVG braid renderer** — `demo/visualize.braid_diagram(..., fmt="svg")` now returns a
  standalone, theme-aware SVG with strands that actually permute through each crossing
  (over/under gaps by exact cubic-Bezier subdivision; gold over-strand). Tested for
  well-formedness and crossing count; `n_strands` validated.
- **`docs/EXAMPLES.md`** — three copy-pasteable worked examples (compile a Hadamard;
  the golden gate's properties + ASCII/SVG diagrams; verify `Jones = 1-sqrt5` exactly), all
  verified to run as written (Hadamard → 11 crossings at fidelity 0.99).
- **GitHub topics** — flagged as an owner action (the integration cannot set repo topics):
  `quantum-computing`, `topological-quantum-computation`, `fibonacci-anyons`, `knot-theory`,
  `braid-group`.

Suite 88 passed / 4 skipped; gates exit 0.

## 2026-07-06 — M3: the heavy mpmath research core (core.lie / core.jets / core.harness)

Ported the E6 cup-product / {4,8}-integrability engine stack (origin-axiom B351/B347/B352/
B370/B357) into clean package subpackages, and built the gate-attack harness on top. All
read-only-ported from `origin/main` via `git show`; origin-axiom never written.

- **`core.precision`** — the scattered `_guard()` (`mp.mp.dps = …` at import) replaced by one
  shared discipline: a `working_precision(dps)` context manager + `@at_precision(dps)`
  decorator, and the named constants `DPS_E6=100`, `DPS_REP=70`, `DPS_BOUNDARY=60`. Nothing
  in M3 mutates the global dps at import; every public entry point re-scopes and restores
  (verified: the global stays at default after the whole suite — the MB3/MB13 lesson).

- **M3a — `core.lie`** (subpackage; `run_all`/`_nullspace` name collisions namespaced apart):
  - `e6` (ported B351) — exact Chevalley e6, integer structure constants, Jacobi-clean over
    all 76,076 triples, principal sl2, the theta diagram involution. Stdlib-only.
  - `rep` (ported B347) — the E6 character-variety tangent of 4_1, `H^1(Sym^{2m})=1` per
    exponent, the two Z/2 gradings. **Surgery:** the geometric rep and the two involution
    intertwiners `_AMPHI`/`_HYPER` were SVD-solved *at import* at the live global dps in
    origin-axiom (fragile) — now lazy + memoized, each built under a scoped precision block;
    `symrep` left undecorated so `cohomology` can reuse it at DPS_E6.
  - `cohomology` (ported B352) — the two-basis cup-product obstruction. **Surgery:** the two
    `importlib._load` shims → real imports; the heavy import-time assembly (`S`, `S_INV`,
    `INTERTWINERS`, `BLK`, `FOX`) built once inside a scoped `working_precision(DPS_E6)` block.
  - Banked (fast): `e6` Jacobi=0 + exponent weights `{2,8,10,14,16,22}`; `rep` residuals
    `<1e-50`; `cohomology.rep_checks` relator `3.8e-54` / automorphism `1.6e-81`. Banked
    (OA_SLOW): the m=1 curve control + the m=4 escape obstruction both vanish (max component
    `7.2e-63`), with the MB12 positive-pairing control. Full 6-direction sweep is an opt-in
    reproducer (`python -m golden_gate.core.lie.cohomology`).

- **M3b — `core.jets`** (subpackage on top of `core.lie`):
  - `boundary` (ported B357) — the E6 boundary restriction of 4_1: rank, the Neumann-Zagier
    slopes, the universal-tau = cusp-shape identity (`|tau| = 2sqrt3`), the symplectic
    controls. **Surgery:** two dead `if False` branches and an unused `_lstsq` dropped;
    `block`/`pairing` made public **and self-scoped** (a calibration run caught them crashing
    at ambient dps — the invariant-vector nullspace needs the working precision).
  - `massey` / `massey_legB` (ported B370 A/B) — the depth-3 Massey obstruction (jet
    arithmetic through the relator; m=1 gates `P1=6e-53`, `P2=2.3e-52`, class `2.5e-62`) and
    the depth-2 tau-defect matrix. **Surgery:** the 3 `sys.path.insert` sites → real imports;
    the two `massey_leg*.json` side-effects removed (`run`/`run_all` return dicts); the
    vestigial `TAU` in leg B (overwritten from data) dropped.

- **M3c — `core.harness`** (the gate-attack harness):
  - `prereg.Preregistration` — a frozen (immutable) record of hypothesis / nulls / kill
    conditions / banked identities, fixed before compute.
  - `campaign.run_gated` — runs the banked-identity gate FIRST and **refuses to call the
    computation past a failed gate** (the METHOD "never read verdicts past a failed gate"); a
    sentinel test proves the gated-out computation is never run. A crashing gate is a failed
    gate.
  - `demo_e6` — the harness wired to a real gate: the E6 escape obstruction (m=4). Banked
    identity = `cohomology.rep_checks`; computation = `obstruction_class`; verdict =
    "unobstructed". (OA_SLOW end-to-end test.)

- **Governance/plumbing:** `mpmath` moved back to runtime `dependencies`; a cheap `e6-exact`
  banked-identity gate added to `core.gates` (Jacobi=0 + exponent weights); fixed a brittle
  hygiene-gate test (`"0 files"` matched inside `"30 files"`).

Firewall/honesty: this is exact/numeric research machinery (Lie theory + low-dim topology),
not a physics claim — mirrors the origin-axiom firewall. **Honesty note:** the ported
`boundary.symplectic_controls[...]['nondegenerate']` field (the E_mu/E_lam self-pairing
`h^T K h`) is identically ~0 and thus always False — the genuine symplectic-nondegeneracy
certificate is `omega_on_h1`'s 2x2 determinant (0.64 at m=1, 1.2e-3 at m=4); the tests assert
that, and the field is documented as the faithful-but-misleading origin-axiom value.

## 2026-07-06 — Independent 3-agent audit of M3 + hardening

Three adversarial auditors (port faithfulness/precision; test rigor/vacuity; honesty/
governance/hygiene), each read-only/run-only. Headline: **no CRITICAL/HIGH correctness
defects** — all five engines diffed clean against origin-axiom (no changed constant/sign/
ordering), no global-dps leak, the risk areas (the `ad_root` split, cohomology's two scoped
assembly blocks, the lazy `_base`/`_amphi`/`_hyper` memoization) verified correct, and the
OA_SLOW banked verdicts (33 tests) all reproduced. Findings addressed:

- **Honesty (§2 lock):** the ported `boundary` docstrings still asserted `omega(E_mu,E_lam)
  != 0` as a *passing* "ambient nondegeneracy" control — but it is identically ~0. Rewrote
  the `symplectic_controls` + module docstrings with the honest note at the definition site
  (not only in the test), pointing to `omega_on_h1` as the real certificate. The universal-tau
  sign (MB4): the computed `tau = -2√3 i = -CUSP_SHAPE` (the conjugate of the SnapPy cusp
  shape) is now documented on `tau_identity`, and the test asserts `tau == -CUSP_SHAPE`
  (scoped) instead of comparing magnitudes past a "declared convention" that did not exist.
- **Test rigor:** (a) `test_universal_tau` did its comparison at ambient dps 15 — the residual
  floored at ~1e-14 while advertising 1e-40 (the MB3 trap, in the one M3 test file that forgot
  it); now scoped to `DPS_BOUNDARY`. (b) The depth-2/3 Massey payload (`massey_direction`,
  `class_complex`, `_span_residual`, `word_jet2` order 2) had ZERO coverage — added fast unit
  tests (`class_complex` linearity + **nonzero** discriminating control; `_span_residual`
  in-span/transverse/empty) and OA_SLOW tests (the m=1 raw Massey **class** vanishes while
  `q3 != 0` — this exercises the order-3 jet → class path a P1/P2 gate cannot; `word_jet2`
  order-2 solves cleanly). The full 6-direction transverse-residual sweep and the leg-B
  δ-matrix stay opt-in `python -m` reproducers (~10 min each, too heavy for the suite — logged
  here rather than silently dropped). (c) Added a **discriminating non-zero control** to the
  obstruction tests (`q_norm > 1`): "unobstructed" now means "q is a coboundary", not a silent
  `q ≈ 0` bug. (d) Strengthened the tautological `h1_line` off-block check with a genuine
  scoped cocycle test (`d^1 z = 0`). (e) Added fast coverage of the demo-campaign
  pre-registration; tightened `pytest.raises(Exception)` → `FrozenInstanceError`.
- **Precision (port):** `boundary.omega` was the one public entry point not self-scoped —
  decorated it `@at_precision(DPS_BOUNDARY)`.

The two precision "observations" (rep `_base` built at DPS_E6=100; leg-B mixing dps-100 jets
with dps-60 boundary data) were confirmed deliberate and adequately documented — not defects.
