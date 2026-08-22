# THE DESCENT — the beat reaches the algebra: Σ = exp(ad qE)∘gal extends the Gieseking element to e₆, and Σ² = Ad(tick) — the object supplies antilinearity but can never supply a real structure while it is ticking
## (outside bench, 2026-08-22; seventeenth memo; B1127's relayed bridge COMPLETED; exact over ℚ(q))

### The question (B1127's open bridge, relayed to cc3)
B1127 fenced its own headline on exactly this: the object's arithmetic Galois is
trivial on the ℚ-rational color layer, so the compactifying conjugation looked like the
observer's — UNLESS "the object's holonomy-layer mirror descends to a nontrivial
antilinear action on the combinatorial layer." Memo 16 produced the holonomy-layer
mirror explicitly (the Gieseking beat W = [[1,q],[0,1]]). Does it descend?

### THE ANSWER: it descends, canonically — and what descends is not an involution
All verified exactly (`certificates/beat_descent.py`):
1. **The 2×2 beat on the Lie algebra**: e ↦ e, h ↦ h − 2q·e, f ↦ f + q·h − q²·e
   (and beat(A) = A) — precisely the unipotent exp(ad(q·e)) composed with Galois.
2. **The descent**: Σ := exp(ad(q·E)) ∘ gal on e₆ (E = the paper's principal e6e,
   gal = coefficientwise q ↦ 1−q) reproduces exactly those formulas on the principal
   sl₂ (checked) and is an antilinear bracket-automorphism of e₆ (checked). **The
   holonomy dictionary extends from Γ to the full non-orientable Γ_G**: the object's
   entire Gieseking symmetry acts on the combinatorial e₆.
3. **THE OBSTRUCTION — the theorem-shaped fact**:
   > **Σ² = exp(ad E) = Ad(meridian), verified on all 78 basis vectors — and it is not
   > the identity. The object's own antilinear element squares to the TICK, not to 1.**
   The same mechanism as memo 16's cusp picture (q + q̄ = 1), now on the algebra:
   Σ² = exp(ad((q+q̄)E)) = exp(ad E).
4. **The color slot**: dim(Σ(I2) ∩ I2) = **2** of 8 — the beat MOVES the color slot off
   itself. Combined with B1114's fact that bare Galois fixes it pointwise: the object's
   antilinear resources either act trivially on color (gal) or displace the slot (Σ) —
   neither ever furnishes a conjugation ON color.

### What it settles (the B1127 framing fence, resolved in a precise middle)
A real structure requires σ² = 1. The object's own antilinear element has
**σ² = Ad(tick)** — it can never be a real structure while the object is ticking. So:
- The "object's own" reading is REVIVED at the level of antilinearity: the mirror is
  not abstract Galois bookkeeping — it is a geometric operator that genuinely acts on
  the e₆ layer (B1127's bridge: YES, it descends).
- The "observer's" reading is CONFIRMED at the level of real structure: no involution
  is available from the object; the observer's closing (memos 10–13) is genuinely new
  data — but now with an exact relationship: **the observer's σ and the object's Σ
  share the C∘P factorization and differ by exactly one meridian: σ² = 1 versus
  Σ² = Ad(tick). The observer's conjugation is the beat with the tick stopped.**
- Physical framing (labeled): the object beats; a fixed frame (a real structure, a
  signature, compactness) exists only for whoever stops the clock. Reality-as-closing
  = freezing the beat — the arrow (the tick) and the mirror (the conjugation) cannot
  be held simultaneously; the observer trades the first for the second.

### Fences
The descent is THROUGH the principal dictionary (the paper's rep layer), the canonical
extension; other extensions differ by centralizer elements and share Σ² = Ad(tick)
modulo inner (the obstruction is the extension class, not the choice). The
clock-stopping language is labeled framing; every displayed identity is exact. Gate 5
untouched.

### Certificates
`certificates/beat_descent.py`; output `outputs/beat_descent_out.txt`.

### One sentence for the ledger
The Gieseking beat descends canonically to the algebra as Σ = exp(ad qE)∘gal, squares
to the tick rather than to one — so the object supplies the mirror but never a frame —
and the observer's closing is revealed as exactly the beat with its tick removed.
