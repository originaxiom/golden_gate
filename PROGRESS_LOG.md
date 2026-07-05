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
