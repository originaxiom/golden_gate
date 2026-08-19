# SESSION HANDOFF — the outside bench, 2026-08-19
## For the banking seat: process, verify, bank. Everything graded in the corpus's own vocabulary.

**Provenance.** An independent outside session (Claude, "the outside bench"), started as a hostile
referee report on the paper *"From minimal description to E₆: a chain through the figure-eight
knot complement"* and run forward through the physics question, the corpus adjudication, the
origin, and L79. Every item below is either MACHINE-VERIFIED on this bench (certificate script
named, expected output in `VERIFY_MANIFEST.md`), CITED (literature-standard, no re-derivation),
or INTERPRETIVE (labeled; nothing interpretive is proposed for banking). Field conventions
throughout: ℚ(q)/(q²−q+1), q = (1+√−3)/2, ω = q−1 (primitive cube root); Riley slice
A=[[1,1],[0,1]], B=[[1,0],[q,1]], relator a·w·b⁻¹·w⁻¹ with w = ba⁻¹b⁻¹a.
**Firewall status of this entire handoff: structure and negatives only. No measured value is
claimed anywhere. Nothing here touches Tier 2. Gate 5 untouched.**

---

## PART I — THE REFEREE PHASE (the paper holds; defects are presentational)

**I.1 — Full verification of the paper.** All 19 of `paper/verify/check_*.py` pass (sympy 1.14).
~90 additional independent checks on this bench: matrix layer (`indep1.py`); E₆ root system, Levi
enumeration, 109 flats in the weight arrangement, rung spectrum {12,14,16,18,20,26,28,30,36,46,78}
(`indep2.py`); trace field ℚ(√−3), character variety, Molien series — sympy's (−1)^(1/3)
artifacts resolved numerically, all claims confirmed (`indep3.py`); smtfull stratification over ℚ
= (2,2,6,6,6,6,6), two 30-points, no 24 (`indep4.py`). One convention caught and resolved: the
paper's Riley quadratic u²+(5−x²)u+(5−x²) vs this bench's w²+(x²−5)w+(5−x²) is u=−w; paper correct.
GRADE: verification, not new content. Ten defect classes listed in `referee_report.html` are
presentational (scope drift, convention gaps), not mathematical.

**I.2 — The charge algebra, re-derived cold.** All six pairwise brackets [x_a,x_b]=0 for
C=⟨x₈,x₁₄,x₁₆,x₂₂⟩ (t=x⁵y−xy⁵, W=x⁸+14x⁴y⁴+y⁸); dim z(C)=12. CERT: `allbrackets.py`.

## PART II — THE PHYSICS ROAD (structure + six no-gos)

**II.1 — 27 branching + cohomology.** 27 = Sym¹⁶⊕Sym⁸⊕Sym⁰ under the principal sl₂
(`physics1.py`); Fox calculus h¹(M; Sym¹⁶)=h¹(Sym⁸)=h¹(Sym⁰)=1, so h¹(M;27)=3 (`physics2.py`).
CROSS-REF: independently equals B662's dimension grammar (h¹(M;27)=3) — the two benches agree
without contact. Banking note: this agreement is itself worth a line in the ledger.

**II.2 — The D₄ symmetry layer.** Isom(m004)=D₄ realized as automorphisms over ℚ(q); inner vs
outer fiber twists separated by GL(2,3) conjugator determinants {1}=inner (swap), {2}=outer
(inv, swapinv); vertex data n_τ=[[0,1],[q,0]], n_σ=diag(1,−1), p₀=(0,1); closed-geodesic
holonomy γ=abAba, tr=4. CERT: `orbifold_door.py`, `vertices2.py`.

**II.3 — The equivariant sign table (a no-go).** On H¹ blocks: τ=+1 everywhere; σ=−1 exactly at
Sym¹⁶/Sym⁸/Sym⁰ (the three 27 blocks). Surviving 27-generation modes under full D₄: zero.
Fast exact arithmetic as Fraction pairs; normalization lam_norm = lam_raw·det^{n/2} (a
sixth-root-of-unity artifact was caught and fixed — see ERRORS below). CERT: `equivariant2.py`.

**II.4 — The six chirality no-gos (≡ the corpus's 32 NEGATIVEs, independently).**
(1) 27/27̄ pairing at every reachable vacuum; (2) equivariant sign balance (II.3);
(3) F₄ reality: −1 ∈ W(F₄), |W|=1152 — the folded algebra cannot be chiral;
(4) Alexander palindromy: Δ=t²−3t+1, roots φ^{±2} (Milnor); (5) anomaly inflow (CITED:
Witten hep-th/0205184); (6) frozen singularities: H³(ℤ₂²,U(1))=ℤ₂³ computed via bar
resolution — THREE bits of discrete torsion, 8 variants (corrects this bench's own earlier
"one bit" from memory). Mechanism sentence: the amphichiral knot yields achiral matter.

**II.5 — The flat G₂ cone exists.** (ℂ²×ℝ³)/Ĝ, |Ĝ|=96, generators: 2T by left quaternion
multiplication, g_τ (right-mult i + π-rotation axis 1), g_σ (right-mult k + π-rotation axis 3,
composed with left w=(1+i)/√2 ∈ 2O∖2T). The associative 3-form φ is preserved by every
generator, exactly. Fixed-dimension census over Ĝ∖{1}: {3d: 53, 1d: 42} — NO element has a
0-dimensional fixed set (load-bearing for VI.2). CERT: `g2cone.py`.
CROSS-REF: three independent sweeps found ZERO G₂/ALE-fibration content anywhere in docs/ —
this object is new to the corpus.

**II.6 — SL(3) vacuum landscape.** Gröbner slice A=[[1,1,c],[0,1,1],[0,0,1]],
B=[[1,0,0],[p,1,0],[q,r,1]] (the over-gauge-fixed slice giving GB={1} was caught and fixed);
components: Sym² (ℚ(√−3)), Falbel ℚ(√−7) (2p²−5p+4=0), p=±1 branches; Lawton's 9 trace
generators; duality realized by knot symmetries; ρ*≅conj(ρ); Fox h¹ indices 0. CERT: `sl3vacuum.py`.

**II.7 — The ℤ/5 Wilson-line menu, corrected twice.** 15,624 elements, 9 rows
(Borel–de Siebenthal). CORRECTION 1 (of this bench's own claim): no unique modal row — exact tie
at 4320 between su(4)⊕su(2)⊕u(1)² (A₁+A₃) and A₁+A₁+A₂. CORRECTION 2 (of the corpus-voiced
critique): "only the extremal rule selects" is refuted — under W×Galois each row is ONE orbit
(orbit homogeneity); under W-only the rarest row is A₃, not D₅; the extremal rule is
measure-dependent. Verified identity: the D₅-row = the 27-weight orbit ×4.

## PART III — SUCCESSORS + ADJUDICATION

**III.1 — Ensemble statistics.** P(SM-hosting) = 0.827 (resp. 0.778 under the alternate
weighting) across the reachable vacua. GRADE: structure count, not a prediction.

**III.2 — Sturmian phase-blindness.** Verified: hull-level invariants cannot see the intercept.
(Load-bearing for Part V.)

**III.3 — Weak Selector Existence Theorem.** A selector exists but no canonical one — proved at
the session's framing. NAMING HAZARD for the ledger: the corpus's `TRACE_SELECTOR_THEOREM.md`
is a DIFFERENT statement (conditional λ/h=1 via filter-inheritance T1). Do not merge them.

**III.4 — The adjudication, settled.** Session no-gos ≡ corpus 32 NEGATIVEs (same content, two
notations). Dial map 3/52/78 independently recomputed exactly: sl₂ alone → 3; +θ-even charge
(x₁₄,x₂₂) → f₄ (52); +θ-odd charge (x₈,x₁₆) → e₆ (78). B582 verdict sharpened: "CHIRAL" is a
closure statement, not a spectrum statement (now a computation — see VII.3).

## PART IV — THE CORPUS AUDITS (outside-run findings)

**IV.1 — Two-axis census.** Execution: 3994 passed / 7 failed / 36 skipped, identical across two
runs. Triage: 4 environment artifacts (b1035, b1062, b1063, b646), 1 version fragility (b565),
**2 genuine reproducibility reds: b511** (locked accessibility >0.8 reproduces as 0.0) **and
b616** (design hash matches, observed counts don't; prints STILL-AMBIGUOUS). Recomputation axis
(834 files classified, skeptical dedup): 59% RECOMPUTES / 12% MIXED / 29% LOCKS_ONLY; honest
rate ~50–60% after spot-check error bar. Disputed chirality cluster: 5/8 LOCKS_ONLY (b582, b432,
b953, b945, b1017), 3/8 RECOMPUTES (b576, b434, b713). DATA: `batches.json`, `full_census.txt`,
`final_classifications.json`. ACTION for the seat: b511 and b616 deserve their own triage arcs.

**IV.2 — The six-gap docs sweep** (all ~70 docs/*.md, eight agents + direct reading).
G1 interface spectrum: COVERED (B662, B1036, B673, B666-cell-8) — the outside bench's earlier
"missing" was a search miss. G2 action: understated (B1012 S=−CS·k−Vol·σ, c=6σ; B715; B357).
G3 gravity: understated (B259, B1012, scale-torsor; live: B1064, L154). G4 one number: confirmed
missing — five sealed crossings, five negatives (B915, B925, B929, B1027/B1063, B1075 same-day).
G5 arena: confirmed (B716, B721, B490; listener derived B1070/71). G6 split: selector-torsor side
covered (B700, B782, B766, B725/726/729); **global G₂ geometry genuinely absent** (zero hits,
three sweeps) — II.5/VI fill exactly that hole.
**LEDGER DEFECT flagged: THE_LADDER X31 says "MARKOV BLANKET — 0 arcs" while B761 (QP-2, FLAT,
double-method) is precisely a Markov-blanket arc. Either X31 is stale or it means the strictly
statistical blanket; the row misleads as written. Fix suggested.**

## PART V — THE ORIGIN (the rule a→ab, b→a)

**V.1 — The rule has arrow, hand, and dynamics — provably.** (i) σ extends to Aut(F₂), inverse
a→b, b→b⁻¹a (needs negative letters): no arrow at group level. On the positive monoid σ is
injective and NOT surjective — 'bb' has no preimage: some words are initial-only. The arrow =
the positivity of the register. (ii) a→ab vs a→ba: different fixed words, same factor language,
language closed under reversal: the rule has a hand, the hull forgets it. (iii) The induced
trace map T(x,y,z)=(z,x,xz−y) preserves the Fricke form x²+y²+z²−xyz; anchor: monodromy trace 3,
t²−3t+1, Fricke value 5 on (2,2,3). CERT: `heartbeat.py` (9 checks).

**V.2 — The kernel reading (INTERPRETIVE, proposed for the framework layer not CLAIMS).** One
completion, four shadows: group completion kills the arrow (→B716), hull closure kills the hand
(→B713), mapping-torus closure kills the tick (timelessness), torsor formation keeps choices as
a set and loses the point (→B782). The observer = the positive-monoid register the completion
discarded. This unifies four banked negatives as one quotient's kernel.

**V.3 — The free half is EDGE-OBSERVABLE (the session's sharpest new theorem-shaped fact).**
The two hands are the mirror-pair points of one hull: Sturmian intercepts ρ_ab→α=2−φ,
ρ_ba→1−α, sum exactly 1. Fibonacci Hamiltonian (λ=1) on the HALF-LINE (Dirichlet cut at the
register's origin): bulk IDS hand-blind to ≤1 state at every N∈{610..4181}, vanishing as 1/N;
boundary-localized spectra DIFFER: 5 vs 6 edge states (ab: −1.5305, −0.9160, −0.5039, +0.4704,
+2.0303; ba: −1.6041, −1.1584, −0.3064, +0.4474, +2.2987, +2.4385), each stable to 10⁻¹⁵ in N.
Hull theorems make the bulk hand-blind; the cut that creates the register creates the states
that show the hand. CERT: `edge_chirality.py`. PHYSICS-STANDARD register: same shape as
domain-wall fermions / bulk–boundary correspondence; 1d, rule-level, no SM claim.

**V.4 — THE ORIGIN TORSOR (proposed §0 of THE FORCED AND THE FREE; countersigned).** The four
Fibonacci rules {a→ab, a→ba, b→ba, b→ab} are ONE free transitive K₄-orbit under
reversal-conjugation (P-type) and swap-conjugation (C-type); no stabilizer. TYPING CORRECTION
(verified, T4): the tick-arrow is NOT a torsor bit — all four orbit points are forward
substitutions; no K₄ element inverts σ. Two spendable bits (C, P) + one unspendable structure
(T = monoid non-surjectivity). CERT: `origin_torsor.py` (8 checks).

**V.5 — THE GIESEKING TICK (matrix identity verified; manifold statement CITED).** det M = −1;
M² = [[2,1],[1,1]] = RL = the figure-eight monodromy, exactly. The single tick's mapping torus
is the Gieseking manifold (non-orientable, one ideal tetrahedron, volume V₃≈1.0149, orientation
double cover = m004). The object IS the double tick (2 tetrahedra, 2.02988… = the corpus's
complex-volume figure). Consequence: on the one-tick object chirality cannot be POSED
(non-orientable); the second tick buys orientability and pays amphichirality — the deck
involution that restores orientation is the one that swaps the hands. **Orientability and
amphichirality arrive in the same purchase, at tick two.**

**V.6 — Markov blanket, refiled.** The blanket layer is banked MATH in the corpus (S072 Layer 2
definition: cusp torus = blanket, A-polynomial map = self-report, fibers = private states;
B761/QP-2 FLAT: fiber_dim(n)=0 ∀n — no private states; QP-3 INTEGRATED 15/32; QP-4 NO-HATCH;
QP-1 open). COMPOSITION with V.3: everything forced is boundary-VISIBLE (QP-2) and everything
free is boundary-ONLY (V.3): the boundary is the total interface; the blanket is the observer's
seat. Only the Friston identification stays firewalled (B730/S071) — as the corpus already has it.

## PART VI — THE M-THEORY ROAD (Acharya–Witten on the cone)

**VI.1 — Full stratification of (ℂ²×ℝ³)/Ĝ (exact).** 34 distinct fixed subspaces. Codim-4 gauge
loci: ONE E₆ locus (the ℝ³ plane, pointwise stabilizer 2T order 24) + THREE distinct A₁ loci
(orbits of 6, 12, 12 planes, ℤ₂ stabilizers). All four are ASSOCIATIVE calibrated 3-planes —
under the correct cone metric g = dx²_ℝ³ + 2dx²_ℍ (the φ built here is the standard G₂ form for
that metric; the Euclidean Gram is the wrong test — an error caught and fixed on this bench).
Codim-6: three axis lines, stabilizers order 48 (τ-axis in 7 planes; σ-, στ-axes in 13 each).
Apex: the full Ĝ, order 96. CERT: `g2strata.py`.

**VI.2 — The AW verdict.** The COLLISION criterion for chiral matter is MET (E₆ and A₁ loci of
different types meet at a codim-7 point — a geometry the corpus never had). The ISOLATION
criterion FAILS by II.5's census: no element of Ĝ has a 0-dim fixed set ⟹ every A₁ locus meets
the E₆ locus along a LINE, never transversally at a point ⟹ every localized state extends along
a flat direction ⟹ vector-like in 4d. **Mechanism located: flatness ⟹ non-isolation ⟹ pairing.**
Constructive flip: chirality requires deforming so an A₁ locus meets the E₆ locus at an isolated
transversal point — which is precisely the multiplicity question of B1036 / L79.

## PART VII — L79 EXECUTED (the cell three roads converged on)

**VII.0 — The build (each stage gated).** The 27 of e₆ constructed as a verified module on the
paper's own Chevalley basis: crystal of ω₁, Frenkel–Kac shift-cocycle signs ε(α, λ−ω₁);
**verified against ALL 3,003 Chevalley bracket pairs**. Strings Sym¹⁶⊕Sym⁸⊕Sym⁰ (matches
`physics1.py`). Group action basis-free: A27=exp(E), B27=exp(qF); relator = identity on the 27.
h¹(M;27)=3 reconfirmed on the 27-dim module directly. Longitude found by search and verified
symbolically: λ = bABaaBAb, SL(2)-lift trace −2, off-diagonal 2√−3 (the cusp shape).
DIAL CORRECTION (an error caught on this bench): the dial slots are the e-centralizing HIGHEST
VECTORS hv(8), hv(16) of the adjoint blocks (exponents 4, 8) — NOT the polynomial charges
W, W² (those do not centralize the cusp). CERT: `twisted_double.py`.

**VII.1 — THE MIRROR IS THE GALOIS (verified at the cusp).** The ℚ(√−3) Galois twist
(q ↦ 1−q) fixes the meridian and carries λ⁻¹ to λ: the amphichiral gluing of the mirror-double
IS Galois conjugation. Independently confirms B570's "c-chirality = orientation/√−3 Galois" as
a peripheral computation. The mirror amalgam is: right vertex rep = galois∘Φρ, edge map λ↦λ⁻¹
(compatibility exact).

**VII.2 — THE SPECTRUM LAW (the L79 headline).** Mayer–Vietoris for the double D_t, exact, both
gluings (identity and Galois-mirror agree): h¹(D;27) = **5** untwisted (= B662/B1036); = **2**
for ANY θ-odd dial (slots hv8 AND hv16, all t ∈ {1,2,ω}; = B634/B637); = **5** for the θ-even
dial hv14 at every t. The corpus's separately-banked 5 and 2 are two points of ONE law; the
switch is pure dial parity — the same slots {4,8} that carry the arrow, the torsion signs, and
the closure. (Direct contact with L79 sub-item iii, the dial-switch-law.)

**VII.3 — CHIRALITY AT COUNT LEVEL: ZERO EVERYWHERE.** h¹(D_t;27) = h¹(D_t;27̄) in every cell
(computed independently on the dual module), exactly as this bench's Poincaré-duality theorem
forces for any closed double. **The θ-odd twist buys full-E₆ closure at the price of matter
multiplicity (5→2), and what survives is vector-like in count.** B582's existence theorem and
its firewall are both confirmed; the spectrum question it left open is now answered: no closed
double can be chiral in counts. PD-pairing (topology) = non-isolation (M-theory) =
completion-kernel (the rule): one theorem, three languages.

**VII.4 — GENERICITY SWEEP (L79 sub-item i): CLOSED, answer FULL.** Bracket closure of
⟨sl₂, Ad_{exp(t·ad hv)}(sl₂)⟩ = e₆, dim 78, at t ∈ {1, 2, ω}, both θ-odd slots. No degeneration
at the named special values; B582 extends to them.

## ERRORS CAUGHT ON THIS BENCH (the sobriety block — all fixed before any claim)
1. "One bit of discrete torsion" (memory) → three bits: H³(ℤ₂²,U(1))=ℤ₂³, computed.
2. "Unique modal Wilson row" → exact tie at 4320 (caught by verification AND by the corpus voice).
3. SL(3) over-gauge-fixing → GB={1}; fixed with free corner c.
4. Equivariant normalization det^{−n/2} → det^{+n/2} (sixth-root artifacts exposed it).
5. G1 "verified missing" → search miss; corpus had it (B662 etc.).
6. 'aaa' claimed unreachable under σ → false (σ(bbb)=aaa); only 'bb' is unreachable.
7. Euclidean associativity test on the cone → wrong metric; g_ℍ = 2·Euclid is the G₂ metric here.
8. Polynomial charges as dial → dial slots are the highest vectors (cusp-centralizing).
9. Longitude filter demanded trace +2 → the fig-8 longitude lifts at trace −2.
10. Naive sign-flip gluing for the mirror → the mirror is the Galois twist (VII.1).

## WHAT IT ALL IMPLIES (the synthesis; interpretive framing labeled as such)
1. **The forced/free ontology now has an address for the free column.** Free data (hand, phase,
   arrow, choice) is not unobservable — it is boundary-observable and boundary-ONLY. Forced data
   is bulk data and is fully boundary-visible (QP-2). The boundary/cut/edge is the total
   interface, and "the observer" is structurally the cut.
2. **One wall, three languages.** Closed-double PD pairing = AW non-isolation = completion-kernel.
   Chirality, arrow, and choice cannot be produced by ANY closed/completed object built from this
   rule; they are properties of how the object is cut. Every banked no-go is the bulk half of
   this statement; none of them touch the cut half.
3. **The origin keeps the books.** The founding choice of a→ab was a K₄-torsor point (C and P
   spent); the arrow was never on the menu (T is structural). The recurrence of exactly C-like
   and P-like free bits at every level (frame classes, closings, hands) is inheritance from the
   first act. The object is the second beat of a pulse whose first beat (the Gieseking tick) has
   no orientation to lose.
4. **Tier discipline.** Everything here is Tier 0/1 structure plus negative theorems plus two
   audits. Nothing approaches Tier 2; nothing weakens the five-crossing record; the firewall is
   intact end to end.
5. **The next cells this work selects** (in leverage order): (a) the charge grading of the 2
   surviving twisted-double classes under the dial slot — PD balances totals, the graded pieces
   h¹_q can be asymmetric, and that grading is the AW U(1) charge of would-be localized matter;
   (b) the equivariant edge at the weld (does the 5-vs-6 hand asymmetry survive at the object's
   own interface where h¹=5 lives); (c) QP-1, the quine test; (d) geometric realization of the
   twisted doubles (L79 sub-item ii), now informed by VII.1: the θ-odd twist is NOT induced from
   any SL(2) structure — it is E₆-native, so realization must be sought at bundle level, not
   manifold level.

## SUGGESTED ARC-SHAPED BANKINGS (names indicative; the seat prices and seals)
- ARC "origin-torsor": V.4 (K₄, free transitive, T not a bit). Lock: `origin_torsor.py`.
- ARC "edge-observability": V.3 (intercepts α/1−α; 5 vs 6 edge states; bulk blind ≤1/N).
  Lock: `edge_chirality.py`.
- ARC "gieseking-tick": V.5 (M²=RL verified; Gieseking cited; orientability=amphichirality
  purchase). Lock: `heartbeat.py` + `origin_torsor.py` T3.
- ARC "g2-cone-strata": VI.1–VI.2 (E₆+3×A₁, associative, AW collision-yes isolation-no).
  Lock: `g2cone.py` + `g2strata.py`.
- ARC "l79-spectrum-law": VII.2–VII.4 (5/2/5; count-achirality; sweep FULL at {1,2,ω};
  mirror=Galois). Lock: `twisted_double.py`. Closes L79 sub-item i; answers the spectrum half;
  feeds sub-item iii.
- TRIAGE arcs: b511, b616 (census reds); DOC fix: THE_LADDER X31 row.
- LEDGER lines: outside-bench agreement h¹(M;27)=3 ≡ B662; dial map 3/52/78 re-derived;
  32-NEGATIVES ≡ six no-gos concordance.
