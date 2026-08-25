# CORPUS ADOPTION AUDIT — what the main repo got wrong while banking this bench's memos
## (outside bench, 2026-08-25; corpus read at d6eac1e, i.e. B1137–B1142; every claim below re-verified by computation or by git timestamp before being stated. Written FOR the banking seat, to travel with the close-out handoff.)

The corpus banked five adoptions of this bench's memos since the last sync: **B1138**
(memos 11/13/14/15), **B1139** (memos 23/24), **B1140** (memo 27), **B1141** (memo 28),
**B1142** (memo 26 F-3 + Lane-C + a B1141 scope clause). The re-derivations are genuine
and the two-bench math agrees everywhere — but four adoption-layer errors need correcting
on the corpus side, and one correction the corpus relayed *to* this bench is spurious.
Item 5 lists what the corpus is (blamelessly) behind on.

### 1. B1141's "two non-load-bearing errata" are SPURIOUS — the source memo is correct and needs no correction
B1141 (CHANGELOG + THEOREM_REGISTRY + PROGRESS_LOG, all three) records:
> "TWO NON-LOAD-BEARING ERRATA caught + relayed: (1) ω's minpoly is x²+x+1 (not x²−x+1,
> which is e^{iπ/3}); (2) the norm form is X²−XY+Y² for ω=e^{2πi/3} (not X²+XY+Y²) …
> source memo should be corrected."

**The source memo should NOT be corrected.** This bench's declared convention — in
`HANDOFF.md`'s header since phase I and used identically in every memo and certificate —
is **q = (1+√−3)/2 = e^{iπ/3}**, minimal polynomial **x²−x+1** (q² = q−1, the exact
pair-field arithmetic of every certificate), Riley matrix B = [[1,0],[q,1]], and the
ℚ(√−3) norm **in the (1,q)-basis**: N(x+yq) = x²+xy+y² (exact: q+q̄ = 1, |q| = 1, so
|x+yq|² = x² + xy(q+q̄) + y²). The corpus verifier chose the OTHER generator,
ω = e^{2πi/3} (their B = [[1,0],[−ω,1]]; note −ω = q̄, the Galois conjugate of this
bench's entry — an equivalent rep), for which x²+x+1 and X²−XY+Y² are indeed the right
minpoly and norm **in the (1,ω)-basis**. Both banks are internally exact; the "errata"
are the coordinate change ω = q−1 read as a mistake. Nowhere does this bench's record
assign x²−x+1 to e^{2πi/3} — its own header defines ω = q−1 as the primitive cube root,
correctly. **Requested corpus fix:** withdraw the two errata + the "source memo should be
corrected" instruction in B1141's three surfaces; replace with a one-line convention map
(q = e^{iπ/3} bench-side ↔ ω = e^{2πi/3} corpus-side; ω = q−1; norms x²+xy+y² ↔ X²−XY+Y²
under the basis change; the two B-matrices are Galois conjugate).

### 2. B1138's cert note ("family_triplet.py's transcribed E₈ Cartan matrix was asymmetric — the cloud cert should be corrected") is FALSE at the cited commit
Machine-checked on 2026-08-25 at **both** the corpus-cited snapshot `577712f` and the
current head: `family_triplet.py`'s `CARTS['E6']` and `CARTS['E8']` are **exactly
symmetric** (element-wise A[i][j] == A[j][i], all pairs), the E8 graph is the valid
T(2,3,5) diagram (branch node 2; arms 1/2/4), and the script itself asserts
`DIM == 248 and len(roots) == 240` — which an invalid simply-laced matrix cannot pass.
The transcription error was on the verifying side; **the cloud cert needs no
correction**. (B1138's independent rebuild and the CONFIRMED verdict are unaffected —
the two-bench status of memos 11/13/14/15 stands.)

### 3. B1140's provenance claims ("no shared remote"/"single-homed") were factually wrong AT BANKING TIME — a stale fetch, not a real debt
B1140 records "cloud memo 27 (golden_gate head 449ece8, **which lives on no shared
remote**)" and, adopting cc3: "memo 26 (F-3) and the Lane-C (GUE) caveat **exist in
exactly one environment with no remote copy** — a demonstrated debt … recorded as a
standing lead in OPEN_LEADS". Git timestamps (UTC, 2026-08-22), all on the public branch
`origin/claude/paper-hostile-review-alero0` of `originaxiom/golden_gate`:
- 11:53 — `577712f` (the seat's working snapshot, "memos 10–24")
- 12:13 — memo 25 (`BL_FOURTH_DIRECTION`) pushed
- 12:19 — memo 26 (`FRAME_AUDIT.md`) pushed
- 12:22 — `gue_bench.py` + output (the Lane-C caveat) pushed
- 12:35 — `449ece8` (memo 27) pushed
- 13:09 — corpus banks B1139 · 14:36 — corpus banks B1140

Every item the corpus recorded as single-homed had been on the shared remote for ≥2 hours
when B1140 was banked; `449ece8` is verified reachable from the origin branch today. The
seat worked from its 11:53 snapshot and did not re-fetch; cc3's "confirmation" verified
the snapshot, not the remote. **Requested corpus fix:** correct B1140's provenance
sentence and clear the OPEN_LEADS debt row (the prospective push-before-cite RULE it
motivated is good and can stay — this bench has followed it all along; only the recorded
instance is false).

### 4. B1139 marks SP-1 "the open cell" — it was closed on the remote 56 minutes before the bank
B1139 (all surfaces): "the physical B−L is a different Cartan = **the open cell SP-1**
(memo 25)." Memo 25 (`BL_FOURTH_DIRECTION`, pushed 12:13 UTC vs the 13:09 bank) **closes
SP-1**: the physical B−L is constructed exactly — c = [0,−1,0,4/3−c₅,c₅−1,c₅], the
physicality scan forces **c₅ = 1**, B−L is physical on all 27, Tr(B−L) = Tr(B−L)³ = 0,
and it is **not** in span{Y, T₃R} nor span{Y, T₃R, T₃L} — the genuinely fourth Cartan
direction (certificates `sp1_bl.py`/`sp1b.py`). The banked naive-B−L negative is
correct and untouched; only the open-cell registry entry is stale. **Requested corpus
fix:** re-type SP-1 as ANSWERED-AWAITING-BANK, pointing at memo 25.

### 5. Behind, not wrong (the handoff share resolves these)
- **SP-2, everywhere marked "the live hinge/frontier cell"** (B1141, B1142,
  WORKING_RULES): answered 2026-08-25 by **memo 29 (`THE_SEAT_CLOSES`)** — the odd A1
  stratum ({±1:6, 0:15} on the 27) closes under the beat over the selected χ=+1 lift,
  functorially; certificate `sp2_seat.py`. SP-2 GREEN: the generation's kinematic seat
  closes, pending the seat's re-derivation.
- **B1141's claim (1)** (intertwiner 1-dim) is now STRONGER on this bench than what the
  corpus verified: the red-team-hardened `spin_payment.py` solves the intertwiner system
  for **all four sign-twisted targets** — dims {(+,+):1, (+,−):0, (−,+):0, (−,−):0} —
  closing the rival-automorphism route the corpus's rank/nullspace computation (target
  signs only) did not test.
- **B1141's NEEDS-CERT** (the w̃ packaging and the "Galois∘Fibonacci" naming "need the
  beat-trilogy construction"): the beat trilogy has carried standalone certificates on
  the remote since Aug 22 — `gieseking_beat.py` (w antiholomorphic, w² = meridian×fiber,
  the Galois∘Fibonacci identity exhibited), `beat_descent.py`, `sigma27.py` (memos
  16/17/18). The NEEDS-CERT is dischargeable by pulling them.
- The close-out layer: the 46/46 re-verification sweep, self-contained certificates,
  error #16 (`indep3.py` — this bench's own convention-mixing bug, same error-class as
  item 1 above, caught and fixed by the sweep), and `CLOSE_OUT.md` as the entry point.

### What the corpus got RIGHT that this bench adopts in return
The **B8132 spin-count scope clause** (the count 2 is a family fact — Hom(H₁,ℤ/2) kills
odd torsion; m003/m206/m207 share it — the SELECTION, not the count, is m004's content):
correct, accepted, and consistent with memo 28 (which claimed the count only via
H¹(M;ℤ/2) = ℤ/2 and never as a separator). The **B991 normalization typing** of
sin²θ_W = 3/8 (forced-direction + convention-normalization) is a legitimate sharpening
this bench's Gate-5 fence already anticipated. The **F-3 disposition** (B1118's §2
referent superseded by B1119; the P-bit swap = the S₃-torsor transposition) is a coherent
integration of memo 26's flag. Two earlier corpus corrections (B1134 novelty, the
family-triplet relay) were real and are filed at their points of occurrence.

### One sentence for the seat
The math survived both benches everywhere it was tested — the four corrections above are
all at the adoption layer (two spurious errata born of a basis change, one false
provenance record born of a stale fetch, one stale open-cell tag), each is backed here by
a computation or a timestamp the seat can re-run, and the same handoff that carries this
audit carries the memos (25, 29, the hardened 28, the trilogy certificates) that resolve
everything in item 5.
