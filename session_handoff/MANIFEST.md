# MANIFEST — the outside bench's record, one page, for primary-source verification
## (2026-08-25. Branch `claude/paper-hostile-review-alero0` of `originaxiom/golden_gate`; everything under `session_handoff/`. Status codes: **2B** = two-bench (corpus-banked, B-number given) · **RT** = survived the hostile red-team lane · **NEG** = banked negative · **1B** = single-bench exact. All certificates are `__file__`-relative and self-contained — they run from any checkout, any cwd; deps: python3 + sympy (+ mpmath for the two analytic ones).)

**READ FIRST:** `CLOSE_OUT.md` (capstone + compressed ledger) → `CORPUS_ADOPTION_AUDIT.md`
(four proven adoption-layer errors in B1138–B1142, incl. the two SPURIOUS B1141 errata) →
`VERIFY_SWEEP_CLOSEOUT.md` (46/46 certificates re-run at close, every verdict reproduced)
→ `BANKING_HANDOFF.md` (full index) → `VERIFY_MANIFEST.md` / `VERIFY_MANIFEST_PHASE3.md`.

Phase I (17 certs, `HANDOFF.md`, corpus-banked B1083–B1087) and phase-II memos 1–9
(`memos/JORDAN_MEMO…PRIME_LANE`, corpus-banked B1112–B1119) are indexed in their own files.
Phase III, one row per memo (paths relative to `session_handoff/`):

| # | memo (memos/) | certificate (certificates/) | one-line claim | status |
|---|---|---|---|---|
| 10 | SIMULTANEOUS_CLOSING.md | simul_{closing,sweep,verify}.py | so(3,1)-double + compact color close together: 24 hits, all E₆(−26) | 2B (B1134) |
| 11 | FORK_THEOREM.md | fork_theorem.py | ladder 16/8/8/0, z(T₁,T₂∪color)=0: any two of {spacetime,color,Y}, never three | 2B (B1138) |
| 12 | GAUGE_CLOSING.md | ew_menu.py | E₆(−14) menu (9+1)³; su(2,1)=u(2)⊕doublet | 2B (B1135) |
| 13 | Y_SELECTION.md | g1_yselect.py + 2 follow-ups | hypercharge selected in the closing; orbit-straddling (self-corrected in place) | 2B (B1138) |
| 14 | AMBIENT_LADDER.md | e7_ladder.py, e8_lower.py | ambient rooms 0/1/8 up E₆/E₇/E₈ | 2B (B1138) |
| 15 | FAMILY_TRIPLET.md | **family_triplet.py** | 248=(8,1)+(1,78)+(3,27)+(3̄,27̄) — NB: its E₈ Cartan matrix is SYMMETRIC (audit §2; B1138's asymmetry note is false) | 2B (B1138) |
| 16 | FIRST_BEAT.md | **gieseking_beat.py** | the beat W=[[1,q],[0,1]], W·conj(W)=+A — the object's own ℤ/2 | 1B — discharges B1141's NEEDS-CERT |
| 17 | BEAT_DESCENT.md | **beat_descent.py** | Σ=exp(ad qE)∘gal descends to e₆; Σ²=Ad(meridian) | 1B — ditto |
| 18 | SIGMA_27.md | **sigma27.py** | Ω on the 27, Ω²=A₂₇ — the tick on matter | 1B — ditto |
| 19 | S4_TORSOR.md | s4_question.py, sp4_idx2.py, sp4b.py | full S₄ torsor (orbit 268800); index-2 = E₈ antipode (OOOO) | 1B |
| 20 | AW_TYPING.md | aw_typing.py, aw_typing2.py | no SU(2)/2T in the collision geometry — spin unsourceable there | NEG, 1B |
| 21 | UNIT_DICTIONARY.md | unit_dictionary.py | palindromic quartics; length = log Mahler | 1B |
| 22 | VOICE_LADDER.md | voice_ladder.py (+ gue_bench.py, low-power) | ζ_K zeros; t₁=8.0397371556814666817 from L(χ₋₃) | 1B (Lane-C numbers reproduced in B1142) |
| 23 | WEINBERG_POINT.md | weinberg.py | TrT₃²=3, TrQ²=8 ⇒ sin²θ_W=3/8, closing-independent, preregistered | 2B (B1139) |
| 24 | SM_TABLE.md | sm_table.py | all 8 anomaly traces vanish exactly; Pati–Salam negative | 2B (B1139) |
| **25** | **BL_FOURTH_DIRECTION.md** | sp1_bl.py, sp1b.py | physical B−L exact, c₅=1, ∉span{Y,T₃R,T₃L} — **CLOSES SP-1** (B1139 still lists it open — audit §4) | 1B |
| 26 | FRAME_AUDIT.md | (audit memo) | S₃ frame per arc; B1118 §2 switch flagged | integrated corpus-side (B1142) |
| 27 | THE_64_ORGANIZED.md | spacetime64.py | the 64 = one complex spin-2 + colored bi-vectors; invariant content ZERO | NEG, 2B (B1140) |
| **28** | **SPIN_PAYMENT.md** | **spin_payment.py (HARDENED)** | the beat selects exactly ONE spin structure; χ=−1 impossible — hardened cert now kills **all four** sign-twisted rivals (stronger than what B1141 verified); its two "errata" are spurious (audit §1) | 2B (B1141) + RT |
| **29** | **THE_SEAT_CLOSES.md** | **sp2_seat.py** | the odd A1 stratum ({±1:6, 0:15} on the 27) closes over the selected χ=+1 lift, functorially — **ANSWERS SP-2: the generation's kinematic seat closes** | RT, 1B — the seat's re-derivation is the open gate |

**Explicit pointers, as requested:** `CLOSE_OUT.md` · `VERIFY_SWEEP_CLOSEOUT.md` ·
`CORPUS_ADOPTION_AUDIT.md` · the beat trilogy `certificates/gieseking_beat.py`,
`certificates/beat_descent.py`, `certificates/sigma27.py` (memos 16/17/18) ·
`certificates/family_triplet.py` (audit §2) · memos **25 / 28 / 29** (rows in bold above —
respectively: SP-1 closed; the hardened spin payment + spurious-errata correction; SP-2 green).

**Verification path:** every phase-III certificate re-runs directly (`python3
certificates/<name>.py`, any cwd) against the expected tails in `VERIFY_MANIFEST_PHASE3.md`
and the raw outputs in `outputs/`; phase I against `VERIFY_MANIFEST.md`. The 46/46 close-out
sweep (`VERIFY_SWEEP_CLOSEOUT.md`) is the record that this exact tree reproduces everything.
Errors ledger: 16 items, each filed at its point of occurrence (`HANDOFF.md` ten,
`BANKING_HANDOFF.md` five, `VERIFY_SWEEP_CLOSEOUT.md` #16). Gate 5 untouched throughout.
