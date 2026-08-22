# THE GAUGE CLOSING — the EW slot closes as su(2,1) = u(2) ⊕ doublet, the gauge branch's host is E₆(−14), and the five real forms of E₆ are the five postures of the observer
## (outside bench, 2026-08-22; twelfth memo; cell F-1 of FORK_THEOREM executed; verified before claiming)

### The computation (`certificates/ew_menu.py`, exact over ℚ)
Cell F-1: on the fork's GAUGE branch the EW room sl(S₁) survives whole — so sweep all
**factor-preserving** involutions of Aut(Φ(E₆)) = W ∪ δW (g(Sᵢ) = Sᵢ setwise for all
three A2 slots, g² = id: **128 of them, 64 per coset**) × all involutive signed lifts
(**2000 pairs total**), and for each σ = τ∘θ record the signature on each 8-dim slot and
the global character. Same solver and guards as memos 10–11 (row re-checks; spot
automorphism tests per involution).

### THE MENU (exact; nine rows, perfect structure)
> **W-coset (1000 pairs): every single one gives (sl(3,ℝ), sl(3,ℝ), sl(3,ℝ)), char +6 =
> E₆(6).** No compact slot is reachable without the flip.
> **δW-coset (1000 pairs): slot forms are always su(2,1) or su(3) — never sl(3,ℝ) — and
> the counts factorize EXACTLY per slot as (9+1)³ = 1000**: each A2 slot independently
> takes 9 closings to su(2,1) and 1 to su(3). Global form = function of the compact
> count k: **k=0 → E₆(2) (729); k=1 → E₆(−14) (81×3 positions); k=2 → E₆(2) (9×3);
> k=3 → E₆(−78) (1)**.

### What it says
1. **Compactness requires the flip.** Every closing with any compact slot lives in the
   δW coset — the outer (27↔27̄, charge-conjugation) coset. Gauge compactness has
   C-content; the W coset alone can only produce the split object. (Verified: all
   compact rows are [dW].)
2. **The EW slot closes as su(2,1) — u(2) plus one doublet.** In the gauge row the EW
   room's real form is su(2,1), whose maximal compact subalgebra is **exactly u(2) =
   su(2) ⊕ u(1) — the electroweak gauge algebra, nothing more** — and whose 4
   non-compact directions form one complex doublet (the coset su(2,1)/u(2) is the
   complex 2-ball). Labeled interpretive: the closing hands the EW slot its gauge group
   and one doublet's worth of non-compact directions — the Higgs slot's quantum
   numbers — in a single purchase. (sl(3,ℝ) is structurally DISQUALIFIED from hosting
   EW: its maximal compact so(3) is too small for su(2)⊕u(1); the menu never offers it
   on the flip side anyway.)
3. **The gauge branch's host is E₆(−14).** The SM-facing row — exactly ONE compact slot
   (color su(3)), the other two su(2,1) — forces global **E₆(−14)** (81 conjugations per
   color choice). Its maximal compact subalgebra is **so(10) ⊕ u(1) — the SO(10) GUT
   algebra** — and under E₆ ⊃ SO(10)×U(1) the 27 decomposes as **16 ⊕ 10 ⊕ 1** (CITED,
   standard): the spinor 16 = one SM family. The gauge closing's compact core is the
   one-family GUT structure.
4. **The fork now has real-form labels, and the five real forms all have jobs.** The
   spacetime branch (memo 10) closes into E₆(−26) = M(𝕆,ℂ) (compact core f₄); the
   gauge branch closes into E₆(−14) (compact core so(10)⊕u(1)); the unclosed object is
   the split E₆(6) (the Chevalley ℚ-span itself); even-compact-count mixed closings
   give E₆(2); the total closing is E₆(−78). B1119's checksum set {−78,−26,−14,+2,+6}
   — until now just the classification's allowed values — is a **functional taxonomy:
   the five real forms of E₆ are the five postures of the observer.**

### Fences
- Exhaustive within: factor-preserving involutive conjugations with involutive signed
  lifts. Slot-to-physics assignment (which A2 is color) is a frame choice (memo 11's S₃
  torsor); the menu is frame-covariant (its rows permute with the slots — visible in the
  3-fold position symmetry of the counts).
- The su(2,1)-Higgs and 16-family readings are labeled (interpretive / CITED); no value,
  no dynamics, Gate 5 untouched. The per-slot (9+1) product structure is an exact
  observed count, stated as such.

### Open cells
- **G-1**: do any of B1102's 18 hypercharge directions land inside the gauge closing's
  u(2) (σ-compatibly)? The Y-selection question, now posable on the right branch.
- **G-2** (= F-2): the e₇/e₈ ladder — is "any two of three" E₆-specific?
- **G-3**: the 27 under the two branch closings side by side (16⊕10⊕1 vs the (1,1)⊕
  (1,0)⊗3⊕(0,1)⊗3̄ bi-weight table) — one matter table per posture.

### Certificates
`certificates/ew_menu.py`; output `outputs/ew_menu_out.txt`.

### One sentence for the ledger
On the gauge branch the observer's closing factorizes slot by slot — nine ways to u(2)
plus a doublet, one way to compact color — the Standard-Model row is forced into
E₆(−14) whose compact heart is the one-family SO(10) GUT, and with the spacetime branch
already forced into E₆(−26), all five real forms of E₆ now name the five things an
observer can do to this object.
