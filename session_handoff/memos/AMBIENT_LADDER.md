# THE INSTALLMENT PLAN — the hypercharge room after Lorentz + color is 0 in E₆, exactly 1 in E₇, exactly 8 in E₈: the exceptional series sells the Standard Model one layer per step
## (outside bench, 2026-08-22; fourteenth memo; cell G-2/F-2 executed; exact + rigorous mod-p sandwich)

### The question (G-2)
Memo 11 proved the fork inside E₆: dim z(T₁, T₂ ∪ color) = 0 — after the Lorentz double
and color, E₆ has nothing left to sell; hypercharge is unaffordable. Is that
E₆-specific, or a law of the exceptional series?

### The computation (`certificates/e7_ladder.py`, `certificates/e8_lower.py`)
A **generic simply-laced Chevalley builder** (Cartan matrix → root closure →
Frenkel–Kac cocycle → brackets), with the same slot construction as the banked landing
(S₀ = adjacent-simple-pair A2 carrying triple₁; S₁ = an orthogonal A2 carrying
triple₂; S₂ = a further-orthogonal A2 as color). **Control: on E₆ the generic builder
reproduces the banked ladder 16 / 8 / 0 exactly** — validating the whole apparatus
against the paper-derived machinery. E₇ runs exact over ℚ; E₈ runs as a rigorous
sandwich (nullity mod p ≥ nullity over ℚ for every p, so two primes give the upper
bound; explicit exactly-verified commuting elements give the lower bound).

### THE TOWER (the room left after buying Lorentz + color)
> **E₆ (78): z-ladder 16 / 8 / 0 — room 0.** Any two of {spacetime, color, EW}, never
> three (memo 11).
> **E₇ (133): z-ladder 35 / 9 / 1 — room EXACTLY 1**, and the surviving generator is
> verified by direct bracket to commute with all fourteen spent generators and to be
> **pure Cartan: precisely one u(1). E₇ affords {Lorentz double, color, hypercharge} —
> with nothing to spare.** (35 = the sl₆ of E₇ ⊃ A₂×A₅; 9 = color ⊕ the u(1).)
> **E₈ (248): z-ladder ≤78 / ≤16 / = 8 — room EXACTLY 8**: the mod-p bound meets an
> explicitly exhibited **fourth orthogonal A2's full sl₃** (6 roots ⊥ S₀,S₁,S₂; its 8
> basis elements bracket-verified to commute with everything spent; rank 8). **E₈
> affords the entire stack: Lorentz pair + color + the whole EW slot** — the u(2) ⊕
> doublet room of memo 12, as one more A2. (E₈ ⊃ A₂×E₆, the complement E₆ carrying the
> full trinification: E₈ holds FOUR orthogonal A2 slots.)

### The reading (labeled where interpretive)
**The room sequence is 0 → 1 → 8: nothing, a u(1), an sl₃.** Each exceptional step
buys exactly the next Standard-Model layer: E₆ pays for spacetime + color and is then
spent (the fork); E₇ adds hypercharge — exactly one u(1), no slack; E₈ adds the
complete electroweak slot, and the fork DISSOLVES: all four purchases coexist. The
exceptional series is the Standard Model's installment plan. In E₈ the assignment is
clean: spacetime double on (S₀,S₁), color on S₂, electroweak on S₃ — with the
complement-E₆ carrying the gauge trinification while the spacetime A2 stands outside
it.

**A hook for the AW lane (typed, not claimed):** B1111's isolated-collision candidates
carry order-24 stabilizers — 2T, the E₆ McKay group. The McKay partners of E₇/E₈ are 2O
(48) and 2I (120). If the chirality mechanism ever needs the FULL stack at a point,
this memo says the point must be an E₈ point (binary icosahedral stabilizer) — an
E₆-at-a-point can host at most two of the three. A concrete, checkable refinement of
what W5's residue should look for.

### Fences
- The object supplies E₆ (the 27/charge lattice); nothing here claims m004's chain
  produces E₇/E₈ — this memo types the PRICE STRUCTURE of the ambient series. Whether
  the corpus's geometry ever reaches E₇/E₈ (the G₂/M-theory lane, the McKay hook) is
  open.
- E₈'s middle rungs are honest bounds (≤78, ≤16); both match the structural
  identifications (z(T₁) = the complement e₆; z(T₁,T₂) = sl₃⊕sl₃ inside it) but only
  the final rung was closed exactly, since it carries the claim.
- Slot choices are canonical up to W (memo 11's frame torsor); the ladder dims are
  conjugation-invariant.

### Certificates
`certificates/e7_ladder.py` (builder + E₆ control + E₇ exact + E₈ bounds),
`certificates/e8_lower.py` (the E₈ lower-bound exhibit); outputs
`outputs/e7_ladder_out.txt`, `outputs/e8_lower_out.txt`.

### One sentence for the ledger
After spacetime and color the exceptional algebras hold nothing (E₆), one u(1) (E₇),
one full sl₃ (E₈) — the Standard Model is sold in installments up the exceptional
series, and only at E₈, where four A2 slots stand orthogonal, does the observer's fork
disappear.
