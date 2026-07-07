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

## 2026-07-06 — Round-2 scrutiny (deep adversarial pass) + hardening

A second, deeper 3-agent pass (owner-scoped to adversarial-only, skipping the ~40-min opt-in
reproducers): a **verdict-breaker** (tried to break the banked results via seed/perturbation/
dps variation), a **numerical-&-state-robustness** auditor (test-order independence, cache
poisoning, conditioning), and a **math-convention critic** (is the *interpretation* sound, not
just "matches origin-axiom"). Headline: **every banked verdict SURVIVED; no CRITICAL/HIGH/
substantive-math defect.** Key adversarial results:

- **Verdict robustness (survives):** `rep_checks` automorphism residual stays ~1e-81 across
  seeds {1,2,3,17,99}; `control_pairing` never below 0.030; the obstruction class tracks the
  precision floor (1.5e-42 @ dps80 → 7e-63 @ 100 → 8e-83 @ 120, always ≥22 orders under the
  1e-20 gate — a genuine numerical zero, not tuned to dps 100); a 1e-6 input perturbation drives
  `first_order_residual` 6e-53 → 4.85e+19 (the gate loudly rejects non-cocycles — the verdict is
  discriminating, not vacuous); rank cliffs are 45–100 decades below their cut.
- **State discipline (robust):** full suite order-independent (incl. the exact B347 case — dps 25
  set *before* cohomology holds full 3.8e-54 quality); no global-dps leak (decorator save/
  restores from a non-default dps too); memoized caches (`_XROOT`, `_BASE_CACHE`, …) bit-identical
  whether first-touched at ambient dps 15 or 100. Gram cond 57.7, `lu_solve` residual 0.0,
  `S·S_INV−I` = 7.6e-104.
- **Math/interpretation (sound):** "class vanishes ⇒ unobstructed to 2nd order (Massey: 3rd)" is
  the correct Goldman–Millson reading, representative-independent; the `rep_checks` bracket-
  automorphism residual is a *sufficient* coherence check (the e6 bracket mixes blocks, so a
  convention error can't cancel into it); the universal-τ and leg-B δ indeterminacy-invariance
  hold. Decisive: at m=4, `q_norm ≈ 2.05e9` while every class component is ~1e-62 — emphatically
  not a silent `q ≈ 0`.

Findings fixed:
- **(MEDIUM) `omega_on_h1` nondegeneracy-gate mismatch / latent trap.** The determinant decays
  ~exponentially with the exponent (0.64 at m=1 → 3.07e-11 at m=11, from the `e^{2m·mu}` block
  range). The **fast** test gated `|det| > 1e-6` but only looped m∈{1,4}; m=7/8/11 fall *below*
  1e-6 and passed only by not being iterated. Fixed: the fast test now iterates **all six** m
  with the principled `|det| > 1e-30` gate (far above the dps-60 noise floor ~1e-50; matches
  `run_all`'s `omega_nondeg`), and `omega_on_h1`'s docstring documents the decay trend.
- **(surface 5) Harness gate protects the real compute.** Added a permanent fast regression:
  with the banked identity forced to regress, `demo_e6.run` refuses — the minutes-long
  obstruction solve runs **zero** times (proven by a spy), verdict `None`.
- **(LOW, framing) F4-content honesty note.** `obstruction_class`'s docstring now states that for
  a θ-odd input the `{4,8}` class components vanish *by parity* (structural, not evidence) — the
  genuine content is the F4 blocks `{1,5,7,11}` vanishing; weight the verdict on all six blocks.

Noted, not changed (deliberate / out of the E6 verdict's path): the m=1 first-order cocycle gate
would thin below ~dps 90 (irrelevant at the pinned 100); the massey `mb12` control could not be
re-seeded without the ~10-min sweep (structurally a generic-position property). Fast suite
125 pass / 15 skip; gates exit 0; origin-axiom untouched.

## 2026-07-06 — M4a: the interactive explorer (the community shopfront)

Built `web/explorer.html` — a single self-contained page (inline CSS+JS, no build, no external
requests, so it works both as a repo file and as a hosted single-page artifact under a strict CSP). It
**reimplements the `demo` braid math in float64 JS**, transcribed exactly from
`demo/constants.py`+`braiding.py`+`gates.py`+`jones.py`+`compiler.py`+`visualize.py`:

- **Braid builder** (σ1/σ2/inverses, undo, clear, knot presets) → a live SVG braid diagram (the
  `visualize.py` geometry ported to JS: cubic-Bézier over/under, gold over-strand, dark-mode).
- **Live gate readout:** the 2×2 matrix, rotation angle (in π), Clifford check, determinant, crossings.
- **Fidelity meter** to a selectable target (H/X/Z/S/T/golden), `|tr(U†V)|²/4`.
- **Compile tool:** a bounded brute-force BFS mirroring `compiler.brute_force` (loads the found braid
  onto the stage; honest "best found in-browser" when it can't hit tolerance).
- **Jones panel** with the exact `1−√5` for the figure-eight + the `−φ` Kauffman convention note.
- Theme-aware (dark-primary "quantum instrument" + warm-ivory light), responsive, a11y focus states,
  `prefers-reduced-motion`. An honesty banner (§2): float64 ~1e-12 here vs proved-exactly in ℚ(ζ₆₀).

**Verified:** a Node harness runs the page's own (DOM-free) math half and checks 11 identities against
the Python `demo` — golden matrix `−0.927051−0.224514i`, angle `0.24467π`, det 1, non-Clifford,
Yang–Baxter `4.7e-16`, `Jones(4₁)=1−√5`, `F²=I`, and compile H → **11 crossings @ 0.9906** (matching
Python exactly). Rendered headless (Chromium) in both themes — layout balanced (braid + compile left;
matrix / fidelity / Jones right). Published as a live Artifact.

Governance: extended `core.gates` `_TEXT_SUFFIXES` to `.html`/`.css` so `web/explorer.html` is
hygiene-scanned (now 50 tracked files scanned, clean). Gates exit 0.

## 2026-07-06 — M4b: docs (README rewrite, MATH.md, API.md)

- **`README.md`** rewritten outward-first: the pitch (exact arithmetic, not tolerance), a "try it"
  link to the explorer, a 30-second quickstart (verified to run exactly as written: `0.2447`,
  `Jones==1−√5` True, compile H `11 @ 0.9906`), the three-layer architecture updated to include the
  M3 research core + harness, a result-label legend, and the prior-art paragraph (§2/MB5:
  contribution = packaging, not new algorithms; Kliuchnikov et al. cited).
- **`docs/MATH.md`** — the conceptual tour, every claim tagged `[exact]`/`[numeric]`/`[ported]`:
  Fibonacci anyons (d_τ=φ, the R/F data), braiding + Yang–Baxter, the golden gate = figure-eight,
  why exact ℚ(ζ₆₀) beats float, `Jones(4₁)=1−√5` with the `−φ` convention note, and an honest
  research-core section with the firewall (Lie-theory/topology machinery, not a physics claim; the
  "unobstructed to 2nd/3rd order" scope stated precisely).
- **`docs/API.md`** — the full public surface by module (core.cyclo/charvar/precision/lie/jets/
  harness/gates + demo.*), each with its epistemic label; transcribed from the code.
- `docs/EXAMPLES.md` links to the explorer + MATH/API.

Every cited value cross-checked against the code (honesty lock, §6). Gates exit 0 (52 files scanned).

## 2026-07-06 — M4c: the tools-paper draft (docs/PAPER.md)

Wrote `docs/PAPER.md` — an honest tools-paper draft, bound by §2/§3/MB5. Marked **DRAFT** and
explicitly **"not a novel-algorithm paper"** in the first line. Frames the contribution as clean,
exact, tested, installable packaging + the research core + the quantum-topology connection — NOT new
braid-synthesis algorithms. Every empirical figure is tagged `[exact]`/`[numeric]`/`[ported]`. §6
"Related work" cites the mature synthesis literature (Kliuchnikov–Bocharov–Svore; Kliuchnikov–Yard
arXiv:1504.04350; the Monte-Carlo compiler PRX Quantum 2.010334) and states no novelty claim. §8
carries the firewall (the research core is math, not a physics result; the compiler is not
competitive; the name collision). §7 makes reproducibility concrete (the two-tier suite, the gates,
the two adversarial audits).

Governance note: the M4b log entries first named the artifact-hosting platform explicitly, which
contains a forbidden hygiene token (an AI-assistant brand name); the `no-forbidden-tokens` gate caught
it (after a non-blocking commit chain let the first push through), and it was reworded to "hosted
single-page artifact" fix-forward. Lesson: run `python -m golden_gate.core.gates` and gate on its exit
code *before* committing, not in a `&&` chain that ignores it — the gate-first check then caught a
second occurrence (this very note) before it was committed. Gates exit 0.

## 2026-07-06 — M5: response to an external audit (verified triage + hardening)

An external reviewer audited the public repo (a fair, competent pass) — but against the **pre-M4**
state. Verified each claim against the current tree and acted only on what is genuinely still-open:

- **Already resolved by M4** (the reviewer didn't see): "no quickstart / thin docs / no examples
  gallery / no start-here API / README too dense / pitched as a compiler" → the M4 README rewrite +
  `docs/{API,MATH,PAPER}.md` + `web/explorer.html` + the label discipline. **No action; noted stale.**
- **Acted on (confirmed absent):**
  - **CI** — added `.github/workflows/ci.yml`: a push/PR job (Python 3.11 + 3.12) running
    `compileall` → `pytest -q` → `python -m golden_gate.core.gates`, and a manual/weekly `slow` job
    for the `OA_SLOW` sweeps + `pip-audit`. This mechanically enforces the discipline run by hand (and
    would have caught the M4b hygiene slip). README gets a CI badge.
  - **Input guards** — `braiding.evaluate_braid` now rejects an absurd `abs(power)` (cap `_MAX_ABS_POWER
    = 10_000`); `compiler.{compile_gate,brute_force,golden}` validate the target is a finite 2×2 matrix,
    reject `max_length < 0`, cap `max_length` (`_MAX_LENGTH = 24`), and honor a `max_nodes` BFS budget
    (default 200k) that returns best-effort instead of hanging. Tests: each rejection path + positive
    controls. Documented the approximate 6-digit dedup key (a collision can only *miss* a shorter word;
    the returned fidelity is always recomputed, never trusted from the key).
  - **Release** — an annotated `v0.1.0` git tag created locally; README gains a plain-language
    one-liner, a "research prototype, not a production compiler" scope note, and a
    relationship-to-Qiskit/Cirq paragraph. **Owner-action:** pushing the tag from this environment is
    blocked by the git proxy (HTTP 403 on tag refs; branch pushes are fine), so publishing the
    `v0.1.0` tag / GitHub release must be done by the owner (`git push origin v0.1.0`, or via the
    GitHub UI) — same category as setting the repo topics.
- **Declined, with rationale (honest response):** PyPI publish (API not stable — the reviewer agrees);
  Dockerfile (a library, not an app); advanced synthesis algorithms (an explicit non-goal, MB5); a
  heavy benchmark suite (deferred); a lockfile (lower-bounds are correct for a library); broad
  secret-scanning (no secrets; the hygiene gate covers provenance); a full typing pass (low value).

Net: the audit was useful external validation, and its CI + input-guard + tag recommendations were
real and cheap; ~half its criticisms were pre-M4 stale. Fast suite green; gates exit 0 (gate-first).

## 2026-07-06 — M6a/M6b: toward a publishable v1.0 (owner-chosen target)

The owner set the "production readiness" target as a **publishable v1.0 library** (not a production
quantum SDK, not a hosted service). First two sub-milestones:

**M6a — the public API contract + typing.** Discovered the tree is already `mypy`-clean (27 files) —
just under-annotated. So M6a was additive: a `py.typed` marker (ship the hints, PEP 561); `__all__` on
the public modules (public = in `__all__` / no leading `_`; everything `_`-prefixed is internal and may
change without notice); type hints across the user-facing API (`demo.compiler`/`jones`/`knots`/`gates`;
`CompilationResult.gate -> np.ndarray | None`); a `[tool.mypy]` config; and a **public-API contract +
SemVer/deprecation policy** section in `docs/API.md`.

**M6b — quality infra.** `ruff` config (`line-length=100`, `E/F/I/W/UP/B/SIM/C4`; `E741` ignored as the
math-idiom `I`). Notable governance call: the **faithfully-ported** `core.lie`/`core.jets` are exempted
from *purely-cosmetic* rules (`C408`/`B008`/`B905`/`UP031`/`E501`) via `per-file-ignores`, so they stay
line-for-line re-verifiable against origin-axiom — real errors (E/F) still apply. Cleaned my own code
to zero findings. Chose **lint-only** in CI (`ruff check`, not `ruff format --check`) to avoid churning
37 files / breaking the ported alignment — documented, not silent. Added `mypy` + a `pytest --cov`
**75%** fast-tier floor to CI (a new `lint` job; the heavy research paths are covered under the OA_SLOW
`slow` job — fast-tier coverage is 78%). Added `.pre-commit-config.yaml` (ruff + basic hooks + a local
gates hook) and `.github/dependabot.yml` (weekly pip + actions). `pyproject` gained `dev`/`docs` extras.

Verified: `ruff check` clean; `mypy` clean; fast suite 128 passed / 15 skipped (78% cov); all
workflow/config YAML+TOML parse; gates exit 0 (gate-first). origin-axiom untouched.

## 2026-07-06 — M6c: packaging metadata + build/publish dry-run

Added the PyPI-ready metadata (`classifiers` incl. `Typing :: Typed`, `keywords`, `[project.urls]`),
a `golden-gate-verify` console script, and a trusted-publishing `publish.yml`. `py.typed` ships in the
wheel (`[tool.setuptools.package-data]`).

**A real fix the dry-run caught:** the first console script pointed at `core.gates:main`, which runs the
**repo-hygiene** gates (license / tokens / governance-docs) — those fail from an installed wheel (no git
tree, no LICENSE in site-packages). Split `core.gates` into `BANKED_GATES` (the exact math identities —
meaningful anywhere) and `HYGIENE_GATES` (repo-only), and pointed the script at a new `verify_main()`
that runs only the banked subset. So `golden-gate-verify` is a genuine "does my install compute
correctly?" check; the full repo check stays `python -m golden_gate.core.gates`. Test added for the split.

**Verified end-to-end:** `python -m build` → valid sdist + wheel; a clean-venv install imports, computes
the golden gate (0.2447π), ships `py.typed`, and `golden-gate-verify` exits 0. (`twine check` fails only
in THIS environment — Debian's pinned `packaging 24.0` predates the Metadata-2.4 `License-File` field
setuptools 68 emits; it passes on a normal runner, and `publish.yml` runs it there.)

**Owner-actions:** pick a non-colliding PyPI **distribution name** (`golden-gate`/`golden-gates` taken)
and set `[project].name`; create the PyPI project + `pypi` trusted-publisher environment.
