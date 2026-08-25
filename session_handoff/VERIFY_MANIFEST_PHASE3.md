# VERIFY MANIFEST — PHASE III certificates
## Run from `session_handoff/`; scripts importing the paper's `check_charge_bracket.py` use an absolute path — repoint to your checkout. Extracted mechanically (haiku lane of the masterplan workflow), tails verbatim from `outputs/`. Late-phase-III entries (spacetime64 … sp2_seat) appended 2026-08-25 at seat-close.

### `simul_closing.py`
- run: `python3 certificates/simul_closing.py`
- expected tail:
```
antipodal: solutions=64, compact-color=16, so(3,1)-double=0, BOTH=0
permute: solutions=8, compact-color=0, so(3,1)-double=8, BOTH=0
mixed: solutions=8, compact-color=0, so(3,1)-double=8, BOTH=0
```

### `simul_sweep.py`
- run: `python3 certificates/simul_sweep.py`
- expected tail:
```
color signatures over ALL (swapper, sign-solution) pairs: {(4, 4): 216, (0, 8): 24, (5, 3): 240}
SIMULTANEOUS CLOSING (so(3,1) + compact color (0,8)): 24 hits
>>> EXISTS — first hit at swapper 13
```

### `simul_verify.py`
- run: `python3 certificates/simul_verify.py`
- expected tail:
```
total hits verified: 24
summary {(char, double_sig, coset, S2-action): count}:
   (-26, (3, 3, 0), 'W', 'nontrivial') : 24
```

### `fork_theorem.py`
- run: `python3 certificates/fork_theorem.py`
- expected tail:
```
B1118's fusing swap (3,2,1,0) exchanges the p1-block and p2-block of the
hypercharge Cartan coordinates = the transposition of the two orthogonal A2's.
The simultaneous-closing swap is the S0<->S1 transposition. Same S3 conjugacy class.
```

### `ew_menu.py`
- run: `python3 certificates/ew_menu.py`
- expected tail:
```
  S0=(0, 8)=su(3)  EW-slot S1=(4, 4)=su(2,1)  char +2 [E6(2)] : 9
  S0=(4, 4)=su(2,1)  EW-slot S1=(0, 8)=su(3)  char +2 [E6(2)] : 9
  S0=(4, 4)=su(2,1)  EW-slot S1=(4, 4)=su(2,1)  char -14 [E6(-14)] : 81
```

### `g1_yselect.py`
- run: `python3 certificates/g1_yselect.py`
- expected tail:
```
   Y=('2', '4', '-1', '-2')  annihilated roots (surviving su(2) candidates): 4
   Y=('2', '4', '-1', '1')  annihilated roots (surviving su(2) candidates): 4
   Y=('2', '4', '2', '1')  annihilated roots (surviving su(2) candidates): 4
```

### `g1_followup.py`
- run: `python3 certificates/g1_followup.py`
- expected tail:
```
distinct 2-selections among the generic closings: 9
total mirror pairs among the 18: 9
generic selections that are exactly mirror pairs: 3
```

### `g1_followup2.py`
- run: `python3 certificates/g1_followup2.py`
- expected tail:
```
  pair straddles orbits: True   members-orbit: (O1,O2)
  pair straddles orbits: True   members-orbit: (O1,O2)
union of the 9 pairs covers: 18 of 18; pairwise disjoint: True
```

### `e7_ladder.py`
- run: `python3 certificates/e7_ladder.py`
- expected tail:
```
  dim z(T1) <= 78  [mod p sandwich upper bound]
  dim z(T1,T2) <= 16  [mod p sandwich upper bound]
  dim z(T1,T2 u color) <= 8  [mod p sandwich upper bound]
```

### `e8_lower.py`
- run: `python3 certificates/e8_lower.py`
- expected tail:
```
fourth-slot sl3 (8 elements) commutes with ALL of T1,T2,color: True
rank of the 8 exhibited elements: 8 (expect 8)
closure spot-check bracket nonzero-or-zero computed OK
```

### `family_triplet.py`
- run: `python3 certificates/family_triplet.py`
- expected tail:
```
27 weights rebuilt (minuscule node 0)
charge multiset (3*alpha_node coefficient): {-2: 10, 1: 16, 4: 1}
multiplicities: [16, 10, 1] (expect [16,10,1] = spinor family + vector + singlet)
```

### `gieseking_beat.py`
- run: `python3 certificates/gieseking_beat.py`
- expected tail:
```
  => Gamma_G = <Gamma, w>, w antiholomorphic, w^2 = meridian x fiber:
     THE OBJECT'S OWN FIRST BEAT = (Galois conjugation) o (Fibonacci step),
     and m004's monodromy (the tick^2) is its square.
```

### `beat_descent.py`
- run: `python3 certificates/beat_descent.py`
- expected tail:
```
    (and exp(ad E) != identity, so Sigma is NOT an involution: True )
e6: Sigma is a bracket-automorphism (120 random pairs): True
color slot: dim( exp(ad qE)(I2) meet I2 ) = 2  (8 = preserved; <8 = the beat MOVES color)
```

### `sigma27.py`
- run: `python3 certificates/sigma27.py`
- expected tail:
```
   t -> gal(t): the L79 mirror (the Galois twist of the dial) IS the beat,
   now exhibited at the matter-module level; and matter carries no object-side
   real structure — Omega^2 is the tick, one meridian short of a reality.
```

### `s4_question.py`
- run: `python3 certificates/s4_question.py`
- expected tail:
```
    (3, 2, 0, 1)
    (3, 2, 1, 0)
=> realized group order 24 - the FULL S4
```

### `aw_typing.py`
- run: `python3 certificates/aw_typing.py`
- expected tail:
```
order-24 subgroup #2: element orders {1: 1, 4: 2, 6: 2, 3: 2, 2: 13, 12: 4}  2T=SL(2,3): False  acts on H by LEFT unit quaternions (SU(2)/McKay-E6 condition): False  H-fixed vectors on R^7: 0  |kernel of R^3 action|: 6
order-24 subgroup #3: element orders {1: 1, 4: 2, 12: 4, 2: 13, 3: 2, 6: 2}  2T=SL(2,3): False  acts on H by LEFT unit quaternions (SU(2)/McKay-E6 condition): False  H-fixed vectors on R^7: 0  |kernel of R^3 action|: 6
order-24 subgroup #4: element orders {1: 1, 6: 2, 4: 2, 2: 13, 12: 4, 3: 2}  2T=SL(2,3): False  acts on H by LEFT unit quaternions (SU(2)/McKay-E6 condition): False  H-fixed vectors on R^7: 0  |kernel of R^3 action|: 6
```

### `aw_typing2.py`
- run: `python3 certificates/aw_typing2.py`
- expected tail:
```
  #4: orders {1: 1, 2: 13, 3: 2, 4: 2, 6: 2, 12: 4}  involutions 13  left-quat(SU2): False  SU2-possible: False  fixed-dim 0
order 96: 1 distinct subgroups from transversal pairs
  #1: orders {1: 1, 2: 31, 3: 8, 4: 8, 6: 8, 8: 24, 12: 16}  involutions 31  left-quat(SU2): False  SU2-possible: False  fixed-dim 0
```

### `unit_dictionary.py`
- run: `python3 certificates/unit_dictionary.py`
- expected tail:
```
AAABB        10   52       2736  2^4[2], 3^2[ram], 19^1[1]
AbAbAb       -9   27        637  7^2[1], 13^1[1]
AAbbAb       -9   39       1525  5^2[2], 61^1[1]
```

### `voice_ladder.py`
- run: `python3 certificates/voice_ladder.py`
- expected tail:
```
  tone 12:  t =   30.424876   [zeta]
  tone 13:  t =   30.745040   [chi]
first tone to 20 digits: t1 = 8.0397371556814666817  (a zero of L(chi_-3), NOT of zeta)
```

### `weinberg.py`
- run: `python3 certificates/weinberg.py`
- expected tail:
```
  Tr T3^2 = 3   Tr Q^2 = 8   sin^2 theta_W = 3/8
VERDICT: physical assignments occur: True; their sin^2 values: ['3/8']
closing-independence: YES — single value
```

### `sm_table.py`
- run: `python3 certificates/sm_table.py`
- expected tail:
```
  Tr (B-L)  = 0
  Tr (B-L)^3= 0
  Tr T3R^2 Y= 0
```

### `spacetime64.py`
- run: `python3 certificates/spacetime64.py`
- expected tail:
```
color-singlet (0,0) content in the complement: 2 (0 = NO hypercharge room; matches memo 11)
spin-2 tops: S0-side weight-(4,0) roots: 1 ; S1-side (0,4): 1
theta maps S0 spin-2 top into sl3(S1) span: True -> sigma glues the two spin-2s into ONE complex spin-2 (real dim 10)
```

### `sp1_bl.py`
- run: `python3 certificates/sp1_bl.py`
- expected tail:
```
   colored=True  T3L=   0 Y=  1/3 Q=  1/3 B-L=c5 - 1/3 x3
   colored=True  T3L= 1/2 Y=  1/6 Q=  2/3 B-L=     1/3 x3
```

### `sp1b.py`
- run: `python3 certificates/sp1b.py`
- expected tail:
```
Tr(B-L) = 0   Tr(B-L)^3 = 0
B-L = a*Y + b*T3R exactly? NO — independent third Cartan direction
B-L in span{Y,T3R,T3L}? NO — genuinely fourth direction
```

### `sp4_idx2.py` (superseded control — kept for the record; its "sample more" verdict is answered by `sp4b.py`)
- run: `python3 certificates/sp4_idx2.py`
- expected tail:
```
per-slot inner(I)/outer(O) patterns found: {'IIII': 29}
VERDICT: the index-2 extension acts with pattern(s): none found among sampled Schreier gens (all inner) — sample more
```

### `sp4b.py`
- run: `python3 certificates/sp4b.py`
- expected tail:
```
VERDICT: the index-2 element of the four-slot stabilizer is the E8 antipode
w0 = -1 (CITED: -1 in W(E8)), acting OUTER on all four slots simultaneously (OOOO);
no mixed pattern exists (index is exactly 2).
```

### `gue_bench.py` (numerics down payment, NOT exact — low-power caveat inside)
- run: `python3 certificates/gue_bench.py`
- expected tail: the HONEST REPORT paragraph; key numbers `mean nearest-neighbor spacing of 0.9978`, `KS ... 0.1177 (p=0.103)` vs Poisson `0.2148 (p=0.000)`.

### `spin_payment.py` (memo 28 + red-team hardening block)
- run: `python3 certificates/spin_payment.py`
- expected tail:
```
RED-TEAM (ii): beta^2(b) = a b a^-1 (beta^2 = Ad(meridian)): True
RED-TEAM (iii): (gamma W) conj(gamma W) = gamma * [W conj(gamma) W^-1] * [W conj(W)] on 10 words: True
=> exhaustiveness now MACHINE-VERIFIED: no rival sign-twisted automorphism admits any
   intertwiner; no inner modification escapes; the chi=-1 obstruction is total.
```

### `sp2_seat.py` (memo 29 — THE SEAT CLOSES)
- run: `python3 certificates/sp2_seat.py`
- expected tail:
```
SP-2 GREEN: the beat closes on the fermion-capable (odd) A1 stratum over the
selected chi=+1 lift — functorially, because W = exp(q e) lives upstream of every
embedding. The chi=-1 side needs no rep-level check: the GROUP extension already
fails there (memo 28). THE GENERATION'S KINEMATIC SEAT CLOSES.
```
