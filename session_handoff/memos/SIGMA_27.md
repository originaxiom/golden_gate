# Σ-27 — the beat on matter: Ω² = A27 (the tick reaches the module, so matter has no object-side reality), the 27-rep extends to the non-orientable group, and the L79 mirror IS the beat
## (outside bench, 2026-08-22; eighteenth memo; the Σ-27 cell executed; exact over ℚ(q))

### The construction
Ω := exp(ρ₂₇(q·E)) ∘ gal on the 27 (the crystal basis is rational, so the coefficient
Galois gal is well-defined on the module; E = the principal e6e; ρ₂₇ = the banked,
3003-bracket-verified module map). Ω is the matter-level descent of memo 17's
Σ = exp(ad qE)∘gal — the Gieseking beat acting on the 27.

### The verified facts (`certificates/sigma27.py`, all exact)
1. **The beat automorphism as a word** (holonomy level): W·conj(B)·W⁻¹ = **B⁻¹ABA⁻¹B**
   (and W·conj(A)·W⁻¹ = A, memo 16) — the beat is now a concrete group automorphism
   of Γ in the meridian generators.
2. **The tick-square law reaches matter**: **Ω² = A27, exactly** — the same
   q + q̄ = 1 mechanism, now on the 27×27 module. And since A27 ≠ ±1:
   > **The 27 carries neither a real (Ω² = +1) nor a quaternionic (Ω² = −1)
   > structure from the object.** In Frobenius–Schur terms, the object offers matter
   > not a reality but a TICK — matter reality is the observer's, by exactly the same
   > one-meridian gap as the algebra's (memo 17).
3. **The matter representation extends to the non-orientable group**: Ω·A27·Ω⁻¹ = A27
   and Ω·B27·Ω⁻¹ = ρ(B⁻¹ABA⁻¹B), exactly — so the 27-rep of Γ extends to Γ_G with Ω
   as the image of the Gieseking element (consistency: Ω² = A27 = ρ(w²) ✓). The whole
   non-orientable object acts on matter.
4. **The dial slots are beat-fixed**: Ω·ρ(X8)·Ω⁻¹ = ρ(X8) and Ω·ρ(X16)·Ω⁻¹ = ρ(X16),
   exactly. So the beat fixes the dial SLOTS — and, being antilinear, sends the dial
   VALUE t·X8 to gal(t)·X8. **The L79 mirror — banked as "the Galois twist of the
   dial, verified at the cusp" — is the beat**: the operator behind the banked
   spectrum law's mirror symmetry (t = ω ↔ ω̄, rational dials fixed) is the object's
   own Gieseking element, now exhibited at the module level.

### What it composes into
The descent is now complete through every layer the corpus uses: holonomy (memo 16) →
algebra (memo 17) → matter module and dials (this memo). At each layer the same two
facts: the object's antilinear element ACTS (the mirror is real machinery, not
bookkeeping), and it SQUARES TO THE TICK (so no layer receives a reality from the
object). The observer's contributions — signature, compact color, hypercharge
selection, matter reality — are all the same single act at different layers: stopping
the beat's tick to get an involution. And the dial, the one continuous parameter of
the twisted double, is precisely beat-covariant: slots fixed, values mirrored — the
free-of-one/forced-of-pair data (B1113) sits in the beat's antilinear eye.

### Fences
Ω is the canonical extension through the principal dictionary (same fence as memo 17:
alternatives differ by centralizer elements, sharing Ω² = tick modulo inner). The
Frobenius–Schur language is used structurally (Ω² ∈ {±1} is the definition of
real/quaternionic type for antilinear intertwiners); no unitarity claim is made. Gate
5 untouched.

### Certificates
`certificates/sigma27.py`; output `outputs/sigma27_out.txt` (includes the module's own
gate lines: 3003-bracket PASS, relator PASS, rerun live).

### One sentence for the ledger
The beat acts on matter as Ω = exp(ρ(qE))∘gal with Ω² = the meridian — the 27 gets a
mirror but no reality from the object — the non-orientable group acts on the module,
and the dial's Galois mirror of L79 turns out to have been the object's own beat all
along.
