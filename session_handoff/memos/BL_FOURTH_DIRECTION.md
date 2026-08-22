# B−L, THE FOURTH DIRECTION — solved from forced targets alone, physical on all 27, and provably independent of {Y, T₃L, T₃R}; the table invariant across all 36 assignments; the four-slot ℤ₂ is the antipode
## (outside bench, 2026-08-22; twenty-fifth memo; masterplan Lane A = cells SP-1, SP-3, SP-4; exact)

### SP-1 — THE B−L SOLVE (`certificates/sp1_bl.py`, `sp1b.py`)
Sought: a Cartan functional commuting with color and su(2)_L, pinned by the FORCED
targets only (Q_L ↦ +1/3 ×6, u^c ↦ −1/3 ×3, e^c ↦ +1 ×1 — ten equations, nothing else
imposed). Result:
> The system is solvable with **exactly one free parameter c₅ — and that parameter is
> precisely the textbook E₆ d^c ↔ D̄ ambiguity** (the two colored Y = 1/3 triplets get
> B−L = 2/3−c₅ and c₅−1/3; their sum is forced to 1/3). **On the physical branch
> (c₅ = 1): B−L is physical on ALL 27 states** — quarks +1/3, antiquark singlets −1/3,
> the exotic D forced to −2/3 *without being imposed*, leptons ±1, Higgs 0 — with
> **Tr(B−L) = Tr(B−L)³ = 0** exactly.
> **And B−L is NOT a combination of the closing's visible charges**: it is provably
> outside span{Y, T₃R} and outside span{Y, T₃R, T₃L} (exact non-solvability over all
> 27 states) — **a genuinely independent fourth Cartan direction.**
This EXPLAINS memo 24's negative: Pati–Salam's Y/2 = T₃R + (B−L)/2 fails not because
B−L is absent but because in the E₆ trinification frame B−L is its own direction — the
non-color charge space is EXACTLY {T₃L, T₃R, Y, B−L}, filling the rank-4 Cartan. The
closing's symmetry-point charge lattice is complete: two su(2)'s, hypercharge, and
B−L, with the only residual freedom being the known d^c↔D̄ swap.

### SP-3 — TOTAL INVARIANCE (`certificates/sp1_bl.py`)
Over **all 36 physical assignments** (9 generic closings × selected Y's × kept
su(2)'s): the (color, T₃L, Y, Q) table is **ONE multiset — a single table, no
variants** — and **all five Y/Q anomaly traces vanish in every one (36/36)**. Memos
23–24 used one representative; the whole family is now certified identical.

### SP-4 — THE FOUR-SLOT ℤ₂ IDENTIFIED (`certificates/sp4_idx2.py`, `sp4b.py`)
Memo 19 left the index-2 refinement of the E₈ four-slot stabilizer (2592 = 2×1296)
typed. Resolved: **the extra element is the E₈ antipode w₀ = −1** (−1 ∈ W(E₈),
CITED), which fixes every slot setwise and acts **OUTER on all four slots
simultaneously — pattern OOOO** (verified: its per-slot action lies outside each
slot's 6-element inner Weyl; ⟨W(A₂)⁴, −1⟩ has order exactly 2592). No mixed pattern
exists — the only non-inner dressing E₈ offers its four slots is the total antipode,
i.e. the simultaneous charge-conjugation of all four sectors at once. (Composes with
memo 12's "compactness requires the flip": at E₈ the flip is inner and total.)

### Fences
SP-1's identifications are by quantum numbers; the c₅ freedom is reported, not hidden —
it is the standard E₆ embedding ambiguity and the ONLY one. A first SP-4 attempt
sampled only shallow Schreier generators (all inner — insufficient sampling, reported);
superseded by the direct candidate verification, which is complete since the index is
exactly 2. Symmetry-point structure only; no measured value; Gate 5 untouched.

### One sentence for the ledger
Given only the quark doublet, the up singlet, and the positron, the closing's Cartan
completes itself: B−L appears as an independent fourth direction, physical on every
state and traceless, unique up to the one swap E₆ always had — the charge space of a
generation is exactly four directions deep, the same on all thirty-six closings, and
the only extra symmetry E₈ grants its four slots is conjugating everything at once.
