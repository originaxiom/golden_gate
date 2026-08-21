# THE ANOMALY, RESOLVED — a fake Killing form, caught by the classification itself
## (outside bench, 2026-08-21; addendum to DEFLATION_RUN.md §2, closing its C-D2 cell
## same-bench; certificates `anomaly_hunt_out.txt`, `anomaly_resolved_out.txt`)

### The defect
The paper's Chevalley basis has **[e_r, e_{−r}] = −h_r for all 72 roots** (η ≡ −1,
extracted and verified). The invariant form I used (⟨h,h'⟩ = Cart, ⟨e_r, e_{−r}⟩ = +1) is
the invariant form of the STANDARD convention — under this convention it is **τ-invariant
but not ad-invariant**: the invariance identity ⟨[x,y],z⟩ + ⟨y,[x,z]⟩ = 0 fails on
(e_r, e_{−r}, h) triples. The correct form has **⟨e_r, e_{−r}⟩ = η(r) = −1**
(ad-invariance now verified on 300 random triples, exact).

### Why five checks missed it
τ² = 1, full 3003-pair automorphy, T-invariance of the form, eigenspace dims, exact
congruence signature — all genuinely passed, because **none of them tests ad-invariance
of the form**. The split control was structurally insensitive (hyperbolic planes have
signature (1,1) under either sign choice) and the compact control was itself invalid (a
non-automorphism that coincidentally produced (0,78)). Error-class for the ledger:
**"the fake invariant form" — an inner product invariant under the symmetry being studied
but not under the algebra, indistinguishable from the Killing form by every
symmetry-side check.** Detection method, worth keeping as an instrument: **the
classification theorem as checksum** — an "impossible" invariant value (character −10
∉ {−78,−26,−14,2,6}) is not a paradox but a proof that some instrument is broken; chase
it until the toolchain confesses. It did.

### The corrected results (exact, controls green)
- control τ = id → split E₆(6), character +6 ✓
- **variant A** (mirror swap, identity on the color factor): **E₆(2)** (unchanged — its
  signature was insensitive to the defect, and is now honestly established), character
  +2; color sector **sl(3,ℝ)**.
- **variant B** (mirror swap, duality on the color factor): **E₆(6), the split form**,
  character +6 — the former "−10" in full; color sector **su(2,1)**.

### What this settles and what it opens
The mirror-swap class provably realizes at least two real forms of E₆ — the quaternionic
E₆(2) and the split E₆(6) — as hosts of the realified Lorentz pair. **Neither constructed
lift yields compact su(3) color** (signatures (5,3) and (4,4)). The compact-color
question is now well-posed and finite: sign-lifts form a torsor over the 𝔽₂-kernel of
the constraint system (each kernel element = a character twist = potentially a different
real form); sweep the kernel over both lattice classes and read off the characters —
with the CORRECTED form, this is a mechanical enumeration. E₆(−26) = M(𝕆,ℂ) has not yet
been reached by any mirror-swap lift; whether it can be is part of the same sweep.
(The abstract hosting of so(3,1) ⊕ su(3)-compact inside E₆(−26) via so(9,1) ⊃ so(3,1)
with commutant su(4) ⊃ su(3) remains CITED and untouched by this defect.)

### Ledger notes
Memo 6's §2 anomaly: CLOSED, same bench, same day. The Lorentz memo's algebra
(the commuting A2 pair, the joint su(3) commutant, ℚ-rationality) is UNAFFECTED — it
used brackets and dimensions only, never the form. The DEFLATION_RUN's variant-A E₆(2)
claim survives with its proof upgraded. New cell C-AR1: the kernel sweep (compact-color
existence over the full lift torsor, both lattice classes; instrument now validated).
