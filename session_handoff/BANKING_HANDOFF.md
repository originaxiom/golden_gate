# BANKING HANDOFF — the outside bench's complete record
## Repository: `originaxiom/golden_gate` · Branch: **`claude/paper-hostile-review-alero0`** · Directory: `session_handoff/`
## Outside bench (independent Claude session), 2026-08-19 → 2026-08-21. Everything below is on this branch.

**START HERE.** This file is the index. The session ran in two phases: (I) the original
verification session (hostile referee → physics road → corpus audits → origin →
M-theory → L79), packaged in `HANDOFF.md` with its `VERIFY_MANIFEST.md`; (II) the memo
run (eight breakthrough memos + one resolved anomaly), after the corpus banked phase I as
B1083–B1087. **Firewall status of the entire record: structure, negatives, and two
literature-standard identities. No measured SM value is claimed anywhere; Gate 5
untouched; every interpretive passage is labeled.** Standing grades: MACHINE-VERIFIED
(certificate + expected output named), CITED (literature-standard, not re-derived),
INTERPRETIVE (labeled, proposed for firewalled rooms only).

---

## DIRECTORY MAP

| path | contents |
|---|---|
| `HANDOFF.md` | Phase I master document: Parts I–VII (referee verification; six no-gos; G₂ cone; SL(3) landscape; Wilson menu; corpus two-axis census; six-gap docs sweep; origin/heartbeat; edge observability; origin torsor; AW stratification; L79 spectrum law + genericity sweep), the ten-error sobriety block, suggested arc bankings. Banked by the seat as B1083–B1087; kept as provenance. |
| `VERIFY_MANIFEST.md` | Re-run commands, runtimes, expected output tails for every phase-I certificate. NOTE: two scripts import `paper/verify/check_charge_bracket.py` by absolute path — edit the path to your checkout of the paper's verify directory. |
| `memos/` | The thirteen memos of phases II–III, in order below. |
| `certificates/` | All 17 exact-arithmetic scripts of phase I (the phase-II computations are inline in the transcript; their full stdout is in `outputs/`). |
| `outputs/` | 14 raw output files — the certificates of phase II plus phase-I extras. |
| `reports/` | 4 HTML session reports; `capstone.html` (§0–§12) is the readable narrative of everything. |
| `data/` | The two-axis census data (`batches.json`, `full_census.txt`, `final_classifications.json`). |

## THE MEMOS (phase II), in reading order — each with verdict, certificate, and its cells

1. **`JORDAN_MEMO.md`** — forced = semisimple/class-function/closed-orbit, free =
   unipotent/frame/torsor; nine-result audit; NEW VERIFIED: the t-meter (tr[B_L,B_R]
   separates every dial value; tr(A·B_R) is dial-blind) ⟹ *free data of one object =
   forced data of the coupled pair*. Output: `outputs/jordan_probe_out.txt`. Cells C-J1..3.
2. **`PROJECTIVE_HATCH.md`** — the spin-bit repricing: a stratum is projective (lift-free)
   iff its 27-weights are even; 6 of 16 Levi-regular strata are; **of the two
   SM-compatible landings only the trinification A2 is projective** — the object's
   unlifted PSL(2,ℂ) holonomy selects it uniquely; hatch price 4.3 → ~2.6 bits, 0
   SM-facing. Cross-checked against B1098/B1100 banked numbers.
   Output: `outputs/projective_hatch_out.txt`. Cells C-P1..3.
3. **`LORENTZ_ON_THE_DOUBLE.md`** — a real form cannot contain a complex subalgebra ⟹
   B715's complexity explained; so(3,1)ℂ = sl₂⊕sl₂ conjugation-swapped ⟹ Lorentz needs
   the mirror double; VERIFIED: two commuting A2-class triples with joint commutant
   exactly one su(3) (color); the ℚ-rational ideal split ⟹ **the signature is the
   observer's, exhibited at Lie-algebra level**; the gravity/EW double-duty competition.
   Outputs: `outputs/lorentz_double3_out.txt` (canonical), `lorentz_double2_out.txt`
   (SUPERSEDED first method, kept for the error ledger — its printed VERIFIED lines are wrong). Cells C-L1..3.
4. **`SPENDING_ORDER.md`** — the hatch DAG (definitional-dependency order of the freedom
   ledger) matches the cosmological freezing order with zero inversions; the fork
   explains un-unified gravity; NEW VERIFIED: the 27's joint bi-weight table
   {(±2,±2):1,(±2,0):4,(0,±2):4,(0,0):7} exact ⟹ in the gravity reading
   **27 = (1,1)⊗1_c ⊕ (1,0)⊗3 ⊕ (0,1)⊗3̄ — the spin-2 slot + colored SD/ASD vectors —
   and no half-integer spin anywhere**: fermionicity = the spin bit = chirality's
   supplier, one purchase three faces (extends banked B428).
   Output: `outputs/spending_order_out.txt`. Cells C-S1..3.
5. **`ASYMPTOTIC_CHANNEL.md`** — every value no-go is single-level; growth rates of towers
   are basepoint-free canonical numbers outside their scope; VERIFIED: Vol extracted from
   the Kashaev tower to 6.5×10⁻¹¹, power 3/2, constant 3^{−1/4} ⟹ **"the object refuses
   LEVEL values and emits TOWER values"; the action is the growth rate of the
   description.** Output: `outputs/asymptotic_channel_out.txt`. Cells C-V1..4 (C-V4 =
   the first crossing-candidate CLASS outside B687's atlas and B743's tower; nomination-gated per B1026).
6. **`DEFLATION_RUN.md`** — three cells executed: (1) B1102's 18 hypercharge directions
   re-derived independently (exact cross-check); W = S₃×S₃ orbits = **9+9**, fused to ONE
   by the mirror-class swap ⟹ **the last hypercharge bit is P**; (2) the Lorentz-host
   construction (see ANOMALY_RESOLVED for the corrected verdicts); (3) Ohtsuki
   c₁ ≈ 11π/(36√3) provisional ⟹ the withholding factorization at one loop.
   Outputs: `outputs/hyper_orbits_out.txt`, `outputs/realform*.txt`, `outputs/ohtsuki_out.txt`. Cells C-D1..4.
7. **`ADELIC_OBJECT.md`** — THE OWNER'S FRAME, verified: the object is adelic (Reid's
   arithmeticity as the license); finite shadow = structure (E₆ at the ramified prime,
   CS term, class-field/being face), archimedean shadow = physics (Vol/action/spectra/
   Lorentz); observer = the completion at the infinite place; mirror = Frobenius at ∞;
   the gluing = quantum modularity (proven for 4₁, CITED). TWO VERIFIED ANCHORS:
   **(a) B1106's laboratory windows = the convergent denominators of φ, split by tick
   parity** (377=F₁₄, 987=F₁₆, 2584=F₁₈ close; F₁₃,F₁₅,F₁₇,F₁₉ break);
   **(b) Vol(m004) = 9√3·ζ_K(2)/π², verified to 4×10⁻³²** (Humbert chain CITED) ⟹
   B737's voice-residue 2√3/vol DERIVED. Plus the convergent-ladder synthesis (the rule =
   the CF algorithm of φ; the seven misses = seeking the limit among its convergents; the
   Hurwitz reading, firewalled, with its falsifier = B1106's silver control).
   Output: `outputs/adelic_anchors_out.txt`. Cells C-AD1..5.
8. **`ANOMALY_RESOLVED.md`** — closes memo 6's logged anomaly SAME-BENCH: the defect was
   **a fake invariant form** (τ-invariant, not ad-invariant; the paper's convention has
   [e_r,e_{−r}] = −h_r uniformly ⟹ the invariant form needs ⟨e_r,e_{−r}⟩ = −1);
   detection method banked: **the classification theorem as checksum** (character −10 is
   impossible ⟹ an instrument is lying). Corrected verdicts, exact, controls green:
   mirror-swap variant A → **E₆(2)** (color sl(3,ℝ)); variant B → **E₆(6) split** (color
   su(2,1)). Neither lift gives compact color; the question is now the finite 𝔽₂-kernel
   sweep (C-AR1). The Lorentz memo's algebra is UNAFFECTED (brackets/dimensions only).
   Outputs: `outputs/anomaly_hunt_out.txt`, `outputs/anomaly_resolved_out.txt`.
9. **`PRIME_LANE.md`** — the prime/zeta ruling (owner-agreed): the toolkit enters only
   where it intersects existing open nodes, queue order, never a destination; **RH fenced
   as a BOUNDARY question**; verified anchor: holonomy eigenvalues of primitive geodesics
   are algebraic units (abAba → x²−4x+1 = 2+√3). Gated cells PR-1..5.
10. **`SIMULTANEOUS_CLOSING.md`** (phase III, post-digest) — **one antilinear
   conjugation buys so(3,1) on the Lorentz double AND compact su(3) color, and all 24
   such conjugations land in E₆(−26) = M(𝕆,ℂ)** — exhaustive over the 48 involutive
   slot-swappers of Aut(Φ(E₆)) = W∪δW × all involutive signed lifts (color signatures
   (4,4):216, (5,3):240, (0,8):24). The winners: pure Weyl swappers reflecting the color
   A2 — the family missed by both B1125/B1127's torsor and the naive −w. Composes
   B1114 + B1127 into "one observer, one act, one host". Certificates:
   `certificates/simul_{closing,sweep,verify}.py`; outputs `outputs/simul_*`.
11. **`FORK_THEOREM.md`** (phase III) — **the D5 fork is a centralizer theorem**: exact
   ladder dim z(T₁)=16, z(T₁∪color)=8=sl(S₁) (the EW room, where B1102's 18 live),
   z(T₁,T₂)=8, **z(T₁,T₂∪color)=0** — any TWO of {spacetime Lorentz, color, EW}, never
   three. Plus the **S₃ frame torsor** (N_W(A₂³)/W(A₂)³ ≅ S₃ full, 216=6³ per class;
   "which factor is color" is a frame choice) with a **ledger flag**: B1102/B1118 and
   B1114/B1125/B1127 run different color frames, consistent only because the fork
   branches are exclusive. σ = τ∘θ = C∘P; the spin lift (B1122) is the one bit no CP act
   pays. Certificate: `certificates/fork_theorem.py`; output `outputs/fork_theorem_out.txt`.
12. **`GAUGE_CLOSING.md`** (phase III) — F-1 executed: sweep of all 128 factor-preserving
   involutions × lifts (2000 pairs). W-coset: uniformly split E₆(6); δW-coset factorizes
   EXACTLY per slot as (9+1)³ — 9 closings to su(2,1), 1 to su(3) per A2 — global form by
   compact count {0:E₆(2), 1:**E₆(−14)**, 2:E₆(2), 3:E₆(−78)}. **The EW slot closes as
   su(2,1) = u(2)⊕doublet; the gauge branch's host is E₆(−14) (compact core = the SO(10)
   GUT algebra; 27 = 16⊕10⊕1 CITED); compactness requires the outer (27↔27̄) coset. The
   five real forms of E₆ = the five postures of the observer.** Certificate:
   `certificates/ew_menu.py`; output `outputs/ew_menu_out.txt`.
13. **`Y_SELECTION.md`** (phase III) — G-1 executed: the 18 hypercharge directions
   recomputed independently (18, orbits 9+9 ✓); 16/128 FP involutions admit gauge-row
   lifts, ALL in the flip coset; **no Y is ever kept split**; selection hierarchy 9/6/1;
   **each generic closing selects exactly one Y per W-orbit (9/9 straddle) = ONE
   hypercharge after W+P identification — B1118's last bit is spent by the closing
   itself**; the 9 pairs partition all 18 (perfect matching, closings ↔ pairs
   bijectively); every selected Y commutes with one su(2) per EW slot (L-R symmetric).
   Self-correction filed: literal P-closure holds only 3/9 — orbit-straddling is the
   invariant. After the closing the freedom ledger holds spin alone. Certificates:
   `certificates/g1_yselect.py` + 2 follow-ups; outputs `outputs/g1_*`.

## ERRORS CAUGHT ON THIS BENCH (phases I+II — the seat should read these first)
Phase I: ten, listed in `HANDOFF.md` (discrete-torsion bits; modal-row tie; SL(3)
over-gauge-fixing; equivariant normalization; G1 search miss; 'aaa' reachability; the
cone's Euclidean-metric associativity test; polynomial-charges-as-dial; longitude trace
sign; naive mirror gluing). Phase II adds four: (11) the Lorentz first-method ideal
split via generic primary decomposition (mixes Galois-conjugate eigenvalues across
rational ideals — superseded by the root-subsystem construction); (12) the missing
(r,−r)→Cartan constraint class in the sign lift (caught, added); (13) THE FAKE INVARIANT
FORM (the anomaly; see memo 8 — five checks passed because none tested ad-invariance);
(14) an mpmath nsum failure on a stepwise character (caught by a 1% mismatch; replaced
by Hurwitz-zeta exact evaluation). Phase III adds one: (15) a GF(2) back-substitution
ordering error in the sign-lift solver (pivot rows carry lower-indexed pivots — evaluate
ascending; caught because the antipodal control lost 63/64 of its solutions; per-solution
row re-checks added as a permanent guard). Every one is documented at its point of
occurrence.

## OPEN CELLS, CONSOLIDATED (ranked by leverage)
C-AR1 the 𝔽₂-kernel sweep (compact-color hosting; instrument now validated) ·
C-S2 the matter–geometry bridge (does B1107's Ruelle tower couple to the (1,1) block?) ·
C-V2/C-V4 Ohtsuki arithmetic at 50 digits + the tower-invariant crossing class
(nomination-gated) · C-AD3 the Habiro/congruence-tower match · C-J2 the Jordan ledger
(with its stated falsifier) · C-P1 the 4 distinguished strata's parities ·
C-D3 the ledger conjecture (discrete freedom = {C, P, spin lift} exactly) ·
the Gieseking first beat (untouched) · QP-1 the quine (the corpus's own open cell).

## FOR THE SEAT'S PROCESS
Every phase-II claim is re-derivable from the outputs plus the transcript's inline
scripts; where a script lives only in the transcript, the output file carries the full
stdout including all gate lines. Verification culture as in phase I: two-outcome cells,
controls before trust, errors filed at point of occurrence. The outside bench requests
the usual treatment: independent re-derivation before banking, integrate-don't-merge,
and the anomaly chain (memo 6 §2 → memo 8) banked as a pair so the error-class and the
checksum method travel with the result.

**Branch to pull: `claude/paper-hostile-review-alero0` on `originaxiom/golden_gate`. Everything is in `session_handoff/`. Nothing of this session exists only in the container.**
