# golden_gate — Governance

**Status:** active. This is the constitution of the `golden_gate` repository. It adapts
the discipline of the origin-axiom research program to the needs of a **software library**:
the goal is not a claims ledger about physics, but a clean, exact, honest, reproducible
computing library that an external expert can clone, run, audit, and trust.

Every other file in this repo is subordinate to the rules here.

---

## 1. Purpose

`golden_gate` is a library of **exact-arithmetic computational engines** for metallic /
Fibonacci-anyon quantum topology (the core), with an outward-facing **braid-gate compiler
and explorer** (the demo) built on top. Priorities, in order:

1. **Correctness** — the mathematics is right.
2. **Exactness where claimed** — a result called "exact" is proved by exact arithmetic,
   never by floating-point tolerance.
3. **Honesty** — no overclaiming: conventions are stated, prior art is cited, numeric is
   not dressed as exact.
4. **Reproducibility** — `pip install -e . && pytest` is green on a clean checkout; the
   heavy proofs are reproducible on demand.
5. **Hygiene** — clean, attributable, secret-free, session-label-free source.

---

## 2. The honesty lock (adapted from the axiom framing lock)

The axiom program's firewall was "form, not contents." The software analogue is the
**exact / numeric / conventional distinction**, and it is binding:

- **Exact vs numeric.** A result presented as **exact** MUST be established by exact
  arithmetic — `core.cyclo` (`Fraction` vectors in `Q(zeta_60)`) or `sympy` symbolic — and
  locked by a test that checks *equality*, not a tolerance. A result computed in `float64`
  is **numeric** and must be labelled as such (tolerance stated). Never present a numeric
  near-miss as an exact identity. *(The figure-eight `Jones = 1 - sqrt5` is exact; the
  golden gate's Bloch angle `~0.245*pi` is numeric.)*
- **Convention honesty.** Where a value depends on a normalization choice, state the
  convention and the standard value. *(The standard Jones is `1 - sqrt5`; the Kauffman
  bracket convention gives `-phi`; the repo says both and does not silently pick the
  flattering one.)*
- **No novelty overclaim.** Where prior art exists, cite it. `golden_gate`'s contribution is
  clean, exact, tested packaging and integration — not new algorithms — unless a genuine
  novelty is demonstrated and cited. *(Fibonacci-anyon braid synthesis is mature literature:
  Kliuchnikov–Bocharov–Svore; Kliuchnikov–Yard.)*

Any prose (README, docstring, commit) that violates this lock has breached governance.

---

## 3. Result labels

Public results carry, in their docstring, exactly one epistemic status:

| label | meaning |
|---|---|
| **exact** | proved by exact arithmetic + a test asserting equality. Safe to rely on. |
| **numeric** | computed in float64 / mpmath, checked to a stated tolerance. |
| **ported** | carried from origin-axiom, faithful, with a banked-identity reproduction test. |
| **experimental** | present but not fully verified; not to be relied on. |

Prose must not assert a stronger label than the code's evidence supports.

---

## 4. What counts as a delivered result

A capability is "delivered" only if it has all three of:

1. **Code** — an implementation in `src/golden_gate/`.
2. **A test** — an assertion in `tests/` that fails if the result changes; for **exact**
   results the assertion checks *equality*, and includes a **positive/negative control**
   where a vacuous pass is possible (a test that can never fail is worse than none).
3. **A doc line** — the docstring (and, for user-facing features, the README) states what it
   does and its label.

Interesting-but-unverified ideas live in `docs/` or issues, never asserted in prose as done.

---

## 5. The gates (CI discipline)

`python -m golden_gate.core.gates` runs stdlib-only, deterministic gates and exits non-zero
on any failure. Two kinds:

- **banked-identity** — a core exact identity (radical squares, T/S unitarity, theta-lift
  order) must reproduce; a regression fails loudly before any downstream number is trusted.
- **hygiene** — no session/author labels in tracked source; a real MIT license present;
  the governance/log/changelog docs present.

Tests are **two-tier**: a fast always-on tier (target < ~30 s) and heavy exact proofs gated
behind `OA_SLOW=1` (documented in the test's skip reason). The gated tier is the banked
proof, reproducible on demand.

---

## 6. The red-team lens (before you claim)

Ask, and record the honest answer:

1. Is this **exact** or **numeric**? Is it labelled correctly?
2. Could the test pass **vacuously**? Is there a positive/negative control?
3. Does **prior art** exist? Is it cited?
4. Is a **convention** hidden behind the value?
5. For a **ported** engine: is the port faithful (a banked-identity reproduction)?

The project's credibility is the honesty of these answers, not the size of the claims.

---

## 7. Method-bug guards (the expensive lessons; extend as they are hit)

- **MB1 — exact means equality, not tolerance.** An "exact" test that uses `< 1e-N` is a
  numeric test mislabelled. Prove equality over `Fraction`/`sympy`.
- **MB2 — no vacuous tests.** Every gate/detector needs a positive control (it fires) and,
  where relevant, a negative control (it stays silent). *(The hygiene detector once caught
  its own control strings — controls are built from encoded tokens.)*
- **MB3 — scoped precision.** Never mutate the global `mpmath` precision at import; use
  `mp.workdps(...)`. Global-dps mutation pollutes other tests by run order. *(Inherited from
  the origin-axiom MB13 §4 lesson.)*
- **MB4 — convention honesty.** State the normalization; report the standard value even when
  a different one is "nicer."
- **MB5 — prior-art before novelty.** Search the literature before any novelty claim.
- **MB6 — reproduction is not interpretation.** A number reproducing exactly does not prove
  it *means* what you think; cross-check against an independent definition (e.g. evaluate an
  exact cyclotomic constant numerically against its analytic form).

---

## 8. Process

- **Commit and push constantly** to `main` on `originaxiom/golden_gate`. Small, green,
  described commits. Never commit to origin-axiom (read-only reference only).
- **`PROGRESS_LOG.md`** — append-only, chronological; every work session logged with what
  was built, verified, and found.
- **`CHANGELOG.md`** — versioned, human-facing (Keep a Changelog).
- **Self-audit before building on a layer** — scrutinize (ideally with independent
  reviewers) before the next layer rests on it.
- **Clean authorship & hygiene** — no session/model/author labels in tracked files; MIT.

---

## 9. Amendments

Amendments to this file are logged in `PROGRESS_LOG.md` with the date and reason.
