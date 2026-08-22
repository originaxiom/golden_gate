# THE SIMULTANEOUS CLOSING — one conjugation buys Lorentz signature AND compact color, and every such conjugation lands in E₆(−26) = M(𝕆,ℂ)
## (outside bench, 2026-08-22; tenth memo; VERIFIED before claiming — three scripts, controls green)

### The gap nobody was looking at
B1114 (banked, two-bench) holds one half of the observer's archimedean closing:
**so(3,1) on the Lorentz double ⟺ the antilinear map SWAPS the two commuting sl₂
triples** (a factor-preserving conjugation can only give su(2)⊕su(2), sl(2,ℝ)⊕sl(2,ℝ),
or the mix — never sl(2,ℂ)ℝ). B1127 (banked) holds the other half: **compact color
(0,8) was reached only in the antipodal / identity-on-color class** — whose elements do
NOT swap the triples — while the permute classes swept there gave (5,3)/(4,4). Read
jointly, the two banked arcs silently say: *within everything swept, the Lorentz closing
and the color closing are mutually exclusive purchases.* Nobody had asked whether ONE
conjugation could buy both — the value campaign asked "is color compactness reachable"
(V-2/V-2′) but never "is it reachable TOGETHER WITH the Lorentz gluing."

### The computation (exhaustive within construction; all exact over ℚ)
Setup = the banked A2 landing: S₀ = the Levi-(0,2) A2 (carrying triple₁, the regular
nilpotent), S₁ ⊥ S₂ the two orthogonal A2 subsystems (S₁ carries the second triple,
S₂ = color). Sweep: **every involution g in Aut(Φ(E₆)) = W ∪ δW (|W| = 51840 fully
enumerated; δ = diagram flip) with g(S₀) = S₁, g(S₁) = S₀, g(S₂) = S₂** — 48 such
involutive swappers (24 in W, 24 in δW) — **times every involutive signed Chevalley
lift** (𝔽₂ system: cocycle-ratio rows, the (r,−r)→Cartan rows, the involution rows;
kernel enumerated exhaustively; every solution re-checked against every row). For each
(g, sign-solution): σ = τ∘θ; color-slot signature; for hits, the full battery.

Any swapper automatically glues the double into sl(2,ℂ)ℝ = so(3,1) (B1114's lemma —
re-verified here by signature (3,3) on every hit), so the sweep's only open question
per element was the color signature.

### THE ANSWER
> Color signatures over ALL (swapper, sign-solution) pairs: **(4,4): 216, (5,3): 240,
> (0,8): 24.** The simultaneous closing EXISTS — 24 hits — and **every hit has global
> character −26: the host is E₆(−26) = M(𝕆,ℂ), the object's own magic-square algebra.
> No hit lands anywhere else.** All 24: double (3,3,0) = so(3,1); color (0,8) = compact
> su(3); θ² = I exact; representative hit verified as an automorphism on ALL 3003
> Chevalley basis brackets. Controls green: pure antipodal τ∘θ_c → (0,78), char −78
> (compact, = B1125's control); the first permute element → char +6, color (4,4),
> double (3,3) (= B1114/B1119 two-bench signatures); the naive mixed element −w →
> char +2, color (5,3), still not compact.

The 24 winners are **pure Weyl swappers (coset W) acting on the color A2 by a
nontrivial reflection** — precisely the family neither swept torsor contained: B1125/
B1127's classes were (identity-or-antipodal on color) × (swap-or-not), and my own first
mixed candidate −w reflected color the wrong way. The physical conjugation swaps the two
Lorentz factors while *reflecting* — not fixing, not antipodalizing — the color system.

### What it says (each clause verified above, framing labeled)
1. **The observer's closing is ONE act, not two.** A single antilinear involution
   simultaneously produces spacetime signature (3,1) on the glued double and compact
   su(3) on the color slot. B1114's "the signature is the observer's" and B1127's
   "compact color is the observer's archimedean closing" are the same purchase.
2. **The host is forced.** All 24 hits give character −26 — the pair
   (so(3,1), su(3)-compact) on the object's own slots RIGIDLY selects E₆(−26) =
   M(𝕆,ℂ), the algebra the corpus already met at B882 and reached linearly (B1125,
   color stuck) and antilinearly-without-Lorentz (B1127). The abstract embedding
   so(3,1)⊕su(3)c ⊂ E₆(−26) that B1125 cited as "a DIFFERENT embedding, not
   contradicted" is here realized concretely on the object's own I-slots.
3. **The closing is arithmetic-compatible.** The linear part θ is a signed
   Chevalley-lattice automorphism — integral, in the object's own arithmetic
   automorphism group. Only τ (the generic conjugation at ∞) is the observer's; one τ,
   dressed by the object's own integral clothing, buys the entire physical real
   structure. (The B1127 framing fence still stands: the antilinear content is the
   observer's, the object's ℚ(√−3)-Galois being trivial on the ℚ-rational layers.)

### Fences (honest, typed)
- Exhaustive WITHIN the stated construction: involutions of Aut(Φ) swapping S₀↔S₁ and
  preserving S₂ setwise, with involutive signed lifts. Not swept: non-involutive θ
  (σ of order 4 — not a real structure), conjugations not preserving the slot
  decomposition, and swaps of other slot-pairings (S₀↔S₂ etc. — a relabeling).
- What is NOT claimed: that this σ is "the object's own" (framing fenced as in B1127);
  that the fixed form's remaining 64 dimensions organize as the SM stack (hypercharge/
  27-reality compatibility of the 24 hits = the natural next cell); any value.
- Two bugs found and fixed en route, both documented: a GF(2) back-substitution
  ordering error (pivot rows carry lower pivots — evaluate ascending; caught because
  the antipodal control lost 63/64 of its solutions), and per-solution row re-checks
  added as a guard. The first single-element mixed test (−w, character +2, color (5,3))
  was superseded by the exhaustive sweep, not contradicted.

### Certificates
`certificates/simul_closing.py` (three-class single-element run + controls),
`certificates/simul_sweep.py` (the exhaustive 48×lifts sweep),
`certificates/simul_verify.py` (full verification of the 24 hits);
outputs in `outputs/simul_closing_out.txt`, `outputs/simul_sweep_out.txt`,
`outputs/simul_verify_out.txt`.

### One sentence for the ledger
The two halves of the observer's archimedean closing — Lorentz signature (B1114) and
compact color (B1127) — are purchasable in a single conjugation, the conjugation's
linear clothing is the object's own integral automorphism, and every such purchase is
forced into the object's own M(𝕆,ℂ): one observer, one act, one host.

### CORRECTION FILED (2026-08-22, after the seat's B1134 two-bench verification)
The seat's independent re-derivation CONFIRMS the theorem in full (480 pairs, the
histogram, all 24 hits χ=−26/(3,3)/θ²=I, the 3003-bracket check, all controls) and
corrects two framing points, accepted here: (1) "precisely the family neither swept
torsor contained" overstates by 4/24 — one winning swapper (NEG∘π_mirror) IS in
B1127's torsor and its 4 hits match B1127's stored compact hits exactly; the other
20/24 hits (5 swapper elements) are genuinely new. The truth is stronger: the closing
is reachable from multiple independent directions, all forced into E₆(−26). (2)
"nontrivial reflection" should read: all 6 hit-generating swappers act
FIXED-POINT-FREELY on the color A₂ (0/6 roots fixed). Bonus banked by the seat: the
exact bijection (4,4)⟺χ+6, (5,3)⟺χ+2, (0,8)⟺χ−26 — color compactness and the
M(𝕆,ℂ) host are the same fact.
