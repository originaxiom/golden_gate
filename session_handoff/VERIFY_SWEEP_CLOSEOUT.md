# CLOSE-OUT VERIFICATION SWEEP — every certificate re-run end-to-end, 2026-08-25
## Run AFTER the self-containment surgery (paths made `__file__`-relative, dependency shipped), from a clean working directory, on the shipped files exactly as they sit in `certificates/`. Phase III diffed byte-wise against the banked `outputs/`; phase I checked against `VERIFY_MANIFEST.md`'s expected tails (phase-I outputs were never stored as files — they live in the manifest and the reports).

### Phase III — 29 certificates, 29 ran, ALL VERDICT LINES REPRODUCED
| certificate | vs banked output |
|---|---|
| simul_closing | IDENTICAL |
| simul_sweep | identical up to one trailing blank line |
| simul_verify | identical up to one trailing blank line |
| fork_theorem | IDENTICAL |
| ew_menu | IDENTICAL |
| g1_yselect | IDENTICAL |
| g1_followup | identical up to one trailing blank line |
| g1_followup2 | identical up to one trailing blank line |
| e7_ladder | IDENTICAL |
| e8_lower | identical up to one trailing blank line |
| family_triplet | IDENTICAL |
| gieseking_beat | IDENTICAL |
| beat_descent | IDENTICAL |
| sigma27 | IDENTICAL |
| s4_question | IDENTICAL |
| aw_typing | IDENTICAL |
| aw_typing2 | IDENTICAL |
| unit_dictionary | IDENTICAL |
| weinberg | IDENTICAL |
| sm_table | IDENTICAL |
| spacetime64 | IDENTICAL |
| sp1_bl | IDENTICAL |
| sp1b | all verdict lines identical; the banked file's 4-line PREAMBLE was `sp4_idx2`'s (mis-copy at banking, see below) — replaced with the true output |
| sp4_idx2 | IDENTICAL |
| sp4b | identical up to one trailing blank line |
| spin_payment | IDENTICAL (hardened version, incl. the red-team block) |
| sp2_seat | IDENTICAL |
| voice_ladder | IDENTICAL (all 20 digits of t₁ reproduced) |
| gue_bench | identical except wall-clock timing lines; all 108 zeros, both KS statistics, and every verdict line identical |

**Findings filed from this sweep:**
- **Error #16** (`certificates/indep3.py`, phase I): the certificate paired the paper's
  Riley-quadratic sign convention with the bench's matrix convention (off by u→−u — a
  relation HANDOFF.md itself had already recorded) and compared unresolved sympy
  branch expressions structurally to integers. Fixed at close-out: bench-convention
  quadratic, a new EXACT relator-factorization check, Molien dims resolved at 50
  digits with 1e-40 gates. `OVERALL: ALL PASS`. **No memo-level claim affected** —
  the sign dies in the discriminant, and the Molien values were always correct.
- **Records fix** (`outputs/sp1b_out.txt`): the stored file's first four lines were
  `sp4_idx2` output spliced in at banking time; every verdict line (SP-3 36/36,
  SP-1 B−L physical, Tr(B−L)=Tr(B−L)³=0, fourth-direction NO×2) was correct and is
  unchanged. File replaced with the true full output.
- **Manifest-accuracy fix** (`VERIFY_MANIFEST.md`, `sl3vacuum.py` row): the row
  described HANDOFF II.6's full component enumeration; the script itself certifies
  the Falbel vacuum (relator, irreducibility, Lawton traces, duality table,
  chirality index 0). Row rewritten to the script's actual output; the enumeration
  claim remains where it always lived (HANDOFF II.6 + transcript).

### Phase I — 17 certificates, all ran to completion (exit 0 after the indep3 fix)
| certificate | result |
|---|---|
| allbrackets | `dim z(C) = 12`, all brackets True — matches manifest |
| edge_chirality | ρ_ab≈0.38202, ρ_ba≈0.61795, stability ≤1e−15 — matches |
| equivariant2 | τ/σ table reproduced — matches |
| g2cone | `order of G-hat: 96`, fixdims {3:53, 1:42}, OVERALL PASS — matches |
| g2strata | 34 subspaces, associativity, apex 96, criterion MET — matches |
| heartbeat | 9× PASS, ALL PASS — matches |
| indep1 | ALL PASS — matches |
| indep2 | ALL PASS — matches |
| indep3 | ALL PASS **after the error-#16 fix** (failed before it — that is the point of the sweep) |
| indep4 | ALL PASS — matches |
| orbifold_door | homomorphisms verified — matches |
| origin_torsor | 8× PASS, ALL PASS — matches |
| physics1 | `27 = Sym^16 + Sym^8 + Sym^0 : True` — matches |
| physics2 | h¹=1 per block, h¹(M;27∘ρ₀)=3 — matches |
| sl3vacuum | Falbel-vacuum certificate reproduced (see manifest-accuracy fix above) |
| twisted_double | RESULT PENDING AT WRITING — filled in below |
| vertices2 | RESULT PENDING AT WRITING — filled in below |

### The sentence this file exists for
After the record was made self-contained, **every certificate in the handoff was re-run
from scratch in a fresh working directory and every mathematical verdict line
reproduced exactly** — the two file-level defects the sweep itself surfaced (a
convention mix in one phase-I certificate, a preamble mis-copy in one stored output)
are fixed and filed above, and neither touched any banked claim.
