# THE Y-SELECTION — the gauge closing spends the last hypercharge bit itself: one closing, one hypercharge, and the nine closings tile all eighteen directions
## (outside bench, 2026-08-22; thirteenth memo; cell G-1 of GAUGE_CLOSING executed; verified, with one mid-run self-correction)

### The question (G-1)
B1102 found 18 hypercharge directions; B1118 priced the residual choice at 1 bit (two
W-orbits of 9, fused by P). Does the gauge closing (memo 12's E₆(−14) row) SELECT among
them? A rational Cartan direction Y survives the real form g^σ as a **compact** u(1)
generator iff θ(Y) = −Y (then iY ∈ g^σ with negative form); θ's Cartan action depends
only on the root involution, not the sign lift — so the selection is exactly computable.

### The computation (`certificates/g1_yselect.py` + two follow-ups; exact)
The 18 directions were RECOMPUTED from scratch (27 minuscule weights rebuilt
independently of the phase-II script; 18 solutions, W = S₃×S₃ order 36, orbits 9+9 —
matching B1102/B1118 exactly). Then all 128 factor-preserving involutions were tested
for gauge-row lifts (slot signatures ((0,8), (4,4), (4,4)) — color compact, both EW
slots su(2,1)), and each gauge involution's ±1 Cartan eigenspaces were intersected with
the 18.

### THE ANSWER (five exact facts)
1. **16 of 128** factor-preserving involutions admit a gauge-row lift — **all 16 in the
   δW (outer/flip) coset**, reconfirming memo 12's "compactness requires the flip".
2. **No hypercharge is ever split**: across all 16, not one of the 18 satisfies
   θY = +Y. Every direction a gauge closing keeps, it keeps COMPACT — the closing never
   hands back a non-compact hypercharge.
3. **The selection hierarchy is 9 / 6 / 1**: nine generic closings select exactly **2**
   directions each; six select 6; one (fully antipodal on the rank-4 Cartan) keeps all
   18.
4. **Each generic pair straddles the two W-orbits — one Y from each 9-orbit** (9/9
   checked). So after gauge (W) equivalence and the P-identification of the two orbits,
   **each generic gauge closing selects exactly ONE hypercharge. The bit B1118 priced
   is paid by the closing itself** — no residual hypercharge freedom survives the
   observer's conjugation.
5. **The nine pairs are pairwise disjoint and cover all 18** — the generic closings
   induce a perfect matching O₁ ↔ O₂ and are in bijection with its 9 pairs: closings
   and hypercharge pairs tile each other exactly (a 9 × 2 grid with no overlap and no
   remainder).

Bonus structure: every selected Y annihilates exactly **4 roots — one su(2) candidate
in EACH electroweak slot**. The closing-level structure is left–right symmetric (an
SU(2)×SU(2) commuting with Y, of which the SM gauges the left) — the L-R symmetric
shape appearing without being asked for. (Descriptive; the L/R naming is interpretive.)

### The self-correction (filed per house rules)
Mid-run I conjectured from one example that each generic pair is a literal P-mirror
pair under B1118's (3,2,1,0) swap. **Systematic check: only 3 of 9 pairs are
P-closed** — the true invariant is orbit-straddling (5/5 above), not literal
P-conjugacy. The eyeballed version is retracted; the checked version is banked.

### What it composes into
Memos 10–13 now chain: one conjugation buys Lorentz signature + compact color and is
forced into E₆(−26) (10); paying for both forecloses hypercharge — the fork is a
centralizer theorem (11); on the gauge branch the closing factorizes per slot, hands the
EW room u(2) ⊕ doublet, and is forced into E₆(−14) (12); and the same closing spends
the last hypercharge bit, selecting exactly one Y (13). **On each branch, the
observer's single act pays every remaining SM-facing bit except the spin lift** — which
B1122 independently proved unpayable by any coupling. The freedom ledger after the
closing: spin alone.

### Fences
Exhaustive within: factor-preserving involutive conjugations, gauge row as defined,
B1102's 18 as the hypercharge menu (their defining multiset taken as banked). Frame
choice per memo 11. No values; Gate 5 untouched.

### Certificates
`certificates/g1_yselect.py`, `certificates/g1_followup.py`,
`certificates/g1_followup2.py`; outputs `outputs/g1_yselect_out.txt`,
`outputs/g1_followup_out.txt`, `outputs/g1_followup2_out.txt`.

### One sentence for the ledger
The gauge closing keeps every hypercharge it touches compact, the generic closing keeps
exactly one per W-orbit — one physical Y — and the nine closings partition all eighteen
directions between them: the last hypercharge bit is not chosen after the closing, it
is the closing.
