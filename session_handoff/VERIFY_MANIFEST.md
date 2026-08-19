# VERIFY MANIFEST — how to re-run every certificate, with expected outputs

Environment: python3 with sympy (1.14 used here) and numpy (2.4 used here; only
`edge_chirality.py` needs it). All scripts exact-arithmetic except the numerically-controlled
parts of `edge_chirality.py` (eigenvalues; stability quoted at 1e-15) and `indep3.py`'s Molien
evaluation (numeric resolution of sympy root-branch artifacts).
`allbrackets.py` and `twisted_double.py` import `paper/verify/check_charge_bracket.py` by
absolute path — EDIT THE PATH at the top of each to your checkout of the paper's verify/ dir.

| script | runtime | expected tail |
|---|---|---|
| `indep1.py`–`indep4.py` | ~min each | all checks PASS; smtfull strata (2,2,6,6,6,6,6), two 30-points, no 24 |
| `allbrackets.py` | ~2 min | all six [x_a,x_b]=0 True; `dim z(C) = 12`; exit 0 |
| `physics1.py` | s | `27 = Sym^16 + Sym^8 + Sym^0 : True` |
| `physics2.py` | s | h1 = 1 per block (Sym16/Sym8/Sym0), total 3 |
| `orbifold_door.py`, `vertices2.py` | s | symmetry homomorphisms verified; dets {1} inner, {2} outer |
| `equivariant2.py` | ~min | table: tau +1 all blocks; sigma −1 at Sym8/Sym16/(Sym0); consistency OK |
| `g2cone.py` | ~min | PASS per generator; `order of G-hat: 96`; fixdims `{3: 53, 1: 42}`; OVERALL PASS |
| `sl3vacuum.py` | ~min | 4 components; Falbel 2p^2−5p+4=0 over Q(√−7); indices 0 |
| `heartbeat.py` | s | 9× PASS; OVERALL ALL PASS (note: only 'bb' unreachable; σ(bbb)='aaa') |
| `edge_chirality.py` | ~1 min | rho_ab≈0.38202 (∋α), rho_ba≈0.61795 (∋1−α); 5 vs 6 edge states; stability ≤1e−15; interior IDS diff = 1/N |
| (edge scaling check) | inline in transcript | half-line IDS diff ×N ∈ {0.00, 1.00} at N=610..4181 |
| `origin_torsor.py` | s | 8× PASS (T1a–T4); OVERALL ALL PASS |
| `g2strata.py` | ~4 min | 34 subspaces; E6 locus (2T, order 24) + 3× A1 (orbits 6/12/12), all `associative: True`; 3 lines order 48; apex 96; criterion MET |
| `twisted_double.py` | ~6 min | stage 1 VERIFY 3003 brackets PASS; strings [16,8,0]; relator PASS; h1(M;27)=3; longitude `bABaaBAb` (trace −2, off-diag 2√3 i); torus h0=3 h1=6; mirror=Galois VERIFIED; MV rows: identity & mirror `t=0: 5 (3+2)`, θ-odd t∈{1,2,ω}: `2 (1+1)`, θ-even hv14: `5 (3+2)` at all t; 27bar rows identical; adjoint sweep: closure 78 at all six (slot,t) cells |
| census data | n/a | `full_census.txt` (3994/7/36 + triage), `batches.json`, `final_classifications.json` (59/12/29 pre-dedup) |

HTML artifacts (session reports, self-contained): `referee_report.html`, `physics_road.html`,
`orbifold_door.html`, `capstone.html` (the running master document, §§0–11: successors, census,
six-gap adjudication, heartbeat postscript, cone stratification, L79 execution, inventory).

Known environment sensitivities: b565-style SnapPy string pinning does not affect any script
here; sympy Molien branch artifacts affect only `indep3.py` (numerically resolved, documented
inline); `edge_chirality.py` seeds nothing (deterministic dense eigensolver).
