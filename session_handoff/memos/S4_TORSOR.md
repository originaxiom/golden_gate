# THE S₄ TORSOR — W(E₈) realizes the full S₄ on the four A₂ slots: at E₈ every physical slot assignment is a frame choice, and the normalizer is computed exactly
## (outside bench, 2026-08-22; nineteenth memo; the S₄ open cell closed; exact orbit computation)

### The question (typed open in memos 14–15)
E₈ carries the four orthogonal A₂ slots (spacetime pair, color, EW — with the triplet of
any one slot indexing the three 27's). Does W(E₈) permute the four slots fully (an S₄
frame torsor, one level above memo 11's S₃ on E₆'s three slots), or only partially?
W(E₈) (order 696,729,600) is too large for the enumeration used at E₆ — decided here by
a configuration-orbit method instead.

### The method (`certificates/s4_question.py`)
BFS over the W(E₈)-orbit of the ORDERED 4-tuple of slot root-sets, bitmask-encoded over
the 240 roots — the orbit is the coset space W/Stab, vastly smaller than W. A
permutation π is realized iff the π-permuted initial tuple lies in the orbit.

### THE ANSWER (exact)
> **Orbit of the ordered configuration: 268,800 states.**
> **|Stab_ordered| = 696,729,600 / 268,800 = 2592 = 2 × 1296** — the setwise slot
> stabilizer is W(A₂)⁴ extended by exactly ONE extra ℤ₂ (of the (ℤ₂)⁴ possible per-slot
> outer classes, only an index-2 refinement is realized; the pattern is typed, not
> classified).
> **All 24 of 24 permutations of the four slots are realized: the FULL S₄.**
> Normalizer N_W(A₂⁴) has order 2592 × 24 = 62,208; the number of unordered A₂⁴
> configurations of this type in E₈ is 268,800/24 = **11,200**.

### What it says
1. **The frame torsor is complete at every level.** Memo 11: the three E₆ slots are one
   S₃ torsor. Now: the four E₈ slots are one full S₄ torsor — and at E₈ everything is
   INNER (E₈ has no diagram automorphism; W alone realizes S₄, whereas E₆'s closings
   needed the outer flip). **"Which slot is the spacetime half, which is color, which
   is EW, which indexes the families" carries zero object-side content** — the object
   hands over four indistinguishable A₂'s; every physical label is the observer's frame
   choice, exactly as at E₆, one level up.
2. **The programme's torsor bracket extends**: Klein torsor of rules at the origin → S₃
   torsor of frames at the E₆ exit → S₄ torsor of slots at the E₈ ceiling. At every
   level where the object could have preferred a labeling, it doesn't; preference
   enters only with the closing. (Framing, labeled; the torsors themselves are
   computed.)
3. The index-2 refinement of the stabilizer (2592 vs 1296) is an exact observed fact
   left typed: the setwise stabilizer realizes exactly one nontrivial combined
   per-slot outer class — its pattern (which slots get flipped together) is a small
   follow-up computation, named not run.

### Fences
The result is for THIS configuration type (the A₂⁴ arising from the memo-14
construction; all A₂ subsystems of E₈ are W-conjugate, and the orbit computation is
exhaustive for the configuration's W-orbit). No claim that the object reaches E₈
(memo 14's fence stands). Gate 5 untouched.

### Certificates
`certificates/s4_question.py`; output `outputs/s4_question_out.txt`.

### One sentence for the ledger
The four A₂ slots of E₈ form a single full-S₄ torsor under the inner Weyl group alone —
268,800 ordered configurations, stabilizer 2592, normalizer 62,208 — so at the top of
the installment plan, as at every level below it, the object refuses to name its slots
and the naming is the observer's.
