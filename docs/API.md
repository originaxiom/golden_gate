# API reference

Public surface of `golden_gate`, by module. Labels: **[exact]** proved by exact arithmetic,
**[numeric]** float/high-precision to a tolerance, **[ported]** reproduced from the research program
and banked by an identity check (`GOVERNANCE.md` §3).

Import the mpmath research engines explicitly (`from golden_gate.core.lie import cohomology`) — they
are not eagerly imported, to keep `import golden_gate.core.cyclo` cheap.

## Public API contract & versioning policy

- **Public vs internal.** A name is **public** iff it is listed in a module's `__all__` (equivalently:
  it does not start with an underscore, and appears in this reference). Everything with a leading `_`
  (`_key`, `_validate_target`, `ad_root_raw`, the import-time globals, …) is **internal** — it may
  change or vanish in any release without notice.
- **Typing.** The package ships a `py.typed` marker (PEP 561); the public API carries type hints, and
  the whole tree is `mypy`-clean. Internal numeric helpers are annotated incrementally.
- **Versioning (SemVer, from v1.0.0).** MAJOR = a breaking change to a public name/signature/documented
  behavior; MINOR = additive (new public API, back-compatible); PATCH = fixes. Before v1.0.0 the API may
  still shift. A public name to be removed is **deprecated** first (a `DeprecationWarning` for at least
  one MINOR release) before removal in the next MAJOR.
- **Result labels are part of the contract.** An `[exact]` result will not silently become `[numeric]`;
  a convention (e.g. the Jones normalization) will not silently flip (`GOVERNANCE.md` §2).
- **The research core** (`core.lie` / `core.jets`) is `[ported]` machinery: its *values* are banked and
  stable, but its API is held to the same policy only from v1.0.0 onward.

---

## `core.cyclo` — exact ℚ(ζ₆₀) arithmetic  **[exact]**

Field elements are length-16 `Fraction` vectors in the power basis mod `Φ₆₀`. Constants:
`CONDUCTOR=60`, `DEG=16`, `LEVEL=15`, `ZERO`, `ONE`, `I_UNIT`, and the radicals
`SQRT5`, `SQRTm3`, `SQRTm15`, `G15` (Gauss sum `i√15`).

| function | returns |
|----------|---------|
| `add/sub/scal(c,a)/mul(a,b)` | field ops (`scal` by a `Fraction`) |
| `zeta(k)` | `ζ₆₀^k` |
| `e15(t)` | `ζ₁₅^t = ζ₆₀^{4t}` |
| `conj(a)` | complex conjugation (`ζ→ζ⁻¹`) |
| `eq(a,b)` / `is_zero(a)` | exact equality / zero test |
| `mmul(A,B)` / `is_identity(M)` | matrix product / exact identity test |
| `Tmat()/Tinv()/Smat()/Sinv()` | the level-15 Weil `T`/`S` matrices and inverses |
| `galois(a,c)` | apply `ζ→ζ^c` |
| `H_avg(t)` | Galois-average of `t` into `H = ℚ(√5,√−3)` |
| `solve_H(t)` | coordinates of `t∈H` in the basis `{1, √5, √−3, √−15}` |

## `core.charvar` — theta-lift / seam toolkit  **[ported]**

| function | returns |
|----------|---------|
| `build_theta_W(m)` | the level-15 Weil matrix `W_m` |
| `matrix_order(W, cap=64)` | `(order, …)` — the multiplicative order of `W` |
| `par_trace(A,B)` | partial trace pairing |
| `pair_smatrix(pow1,pow2)` | S-matrix pairing between two seeds |
| `projector_gates(powers)` / `single_controls(powers)` | DFT eigenprojector checks (`ΣP=I`, `P²=P`) |
| `rank_over_Q(rows,cols,table)` | exact rank of a submatrix over ℚ |
| `solve_model(recs)` | multiplicative tensor completion |

## `core.precision` — scoped mpmath precision

| name | meaning |
|------|---------|
| `working_precision(dps)` | context manager: run a block at `dps` digits, then restore |
| `at_precision(dps)` | decorator form |
| `DPS_E6=100`, `DPS_REP=70`, `DPS_BOUNDARY=60` | the engine precisions |

No engine mutates the global `mp.mp.dps` at import; every entry point re-scopes and restores.

## `core.lie.e6` — exact Chevalley 𝔢₆  **[exact]**

`DIM=78`, `EXPONENTS=[1,4,5,7,8,11]`, `PRINCIPAL_C=[16,22,30,42,30,16]`, `BRACKET`, `ROOTS`.

| function | returns |
|----------|---------|
| `brk(x,y)` | Lie bracket of sparse vectors |
| `jacobi_residual_count()` | violations over all 76,076 triples (**0**) |
| `principal_sl2()` / `principal_relations_hold()` | the principal `(e,h,f)` and its relations |
| `exponent_weights()` | `[2,8,10,14,16,22] = 2×exponents` |
| `theta_checks()` | `(automorphism, involution, dim_fixed=52, dim_minus=26)` |
| `theta_signs_on_exponent_lines()` | `(−1)^{m+1}` per exponent |
| `run_all()` | the full bundle |

## `core.lie.rep` — E₆ character-variety tangent of 4₁  **[ported]** (mpmath, DPS_REP)

`EXPONENTS`, `REL="abbbaBAAB"`.

| function | returns |
|----------|---------|
| `geometric_rep_residual()` | `‖ρ(relator)−I‖ ≈ 7e-71` |
| `symrep(g,d)` | `Sym^d` of a `2×2` matrix (inherits caller precision) |
| `H1_dim(m)` | `dim H¹(4₁, Sym^{2m}) = 1` |
| `e6_tangent_total()` | `6 = rank E₆` |
| `amphichiral_indicator(m)` / `hyperelliptic_sign(m)` | the two ℤ/2 gradings; hyperelliptic `=(−1)^{m+1}` |

## `core.lie.cohomology` — cup-product obstruction  **[ported]** (mpmath, DPS_E6)

`DIM=78`, `EXPONENTS`, `N_OF`, `OFFSET`; import-built `S`, `S_INV`, `INTERTWINERS`, `BLK`, `FOX`.

| function | returns |
|----------|---------|
| `rep_checks(n_pairs=4, seed=3)` | `(relator_residual, automorphism_residual)` — the load-bearing assembly check |
| `ad_root(v)` | `ad(v)` as a 78×78 matrix in root coords |
| `fox_block(m)` | `(d¹_m, d⁰_m)` for the `Sym^{2m}` block |
| `h1_line(m)` / `h2_functional(m)` | the H¹ representative / the H² coker functional |
| `obstruction_vector(za,zb)` | `(q, first_order_residual, ad_solve_residual)` |
| `obstruction_class(za,zb)` | `(per-block class dict, diagnostics)` — vanishing ⇒ unobstructed to 2nd order |
| `control_coboundary()` / `control_pairing_not_vacuous()` | the C2 / MB12 controls |
| `run_all(full=True)` | the six-direction sweep (opt-in reproducer) |

## `core.jets` — higher-order deformation jets  **[ported]** (mpmath)

- **`boundary`** (DPS_BOUNDARY): `MU_WORD`, `LAM_WORD`, `CUSP_SHAPE`; `peripheral_gates()`,
  `block(m)`, `restriction(m)`, `tau_identity(m)` (`τ=−2√3·i`), `pairing(dim)`, `omega(blk,c1,c2)`,
  `symplectic_controls(m)`, `omega_on_h1(m)` (the genuine nondegeneracy certificate), `run_all()`.
- **`massey`** (DPS_E6): `solve_z2`, `relator_jet3`, `class_complex`, `massey_direction`, `run_all`
  (the depth-3 Massey obstruction; opt-in `python -m …massey`).
- **`massey_legB`** (DPS_E6): `word_jet2`, `chain_block_TG`, `run` (the depth-2 τ-defect δ-matrix).

## `core.harness` — the gate-attack harness

| name | meaning |
|------|---------|
| `Preregistration(name, hypothesis, nulls, kill_conditions, banked_identities)` | frozen pre-registration |
| `run_gated(prereg, banked_check, computation)` | runs the banked gate first; refuses to compute past a failed gate; returns a `CampaignRecord` |
| `CampaignRecord` | `(prereg, gate_passed, gate_detail, computed, verdict)` |
| `harness.demo_e6.run(m=4)` | the E₆ escape-obstruction campaign, gated end-to-end |

## `core.gates` — banked-identity + hygiene gates

`GATES` (dict), `run_all()`, `python -m golden_gate.core.gates` (exits non-zero on any failure).
Checks: cyclo radicals, Weil unitarity, charvar theta-lift order, e6 Jacobi, no forbidden tokens in
tracked text, license present, governance docs present.

---

## `demo` — the braid compiler (exact-backed, float64 search)

- **`constants`** — `PHI`, `PHI_INV`, `SQRT_PHI_INV`, `D_TAU`, `D_TOTAL`, `R_VACUUM`, `R_TAU`, `F_MATRIX`.
- **`braiding`** — `sigma1()`, `sigma2()`, `sigma1_inv()`, `sigma2_inv()`, `evaluate_braid(word)`
  (a word is `list[(gen∈{1,2}, power)]`).
- **`gates`** — `golden_gate()`, `golden_gate_mirror()`, `golden_gate_word()`, `gate_properties(U)`
  (`rotation_angle` **[numeric]**, `is_clifford`, `determinant`, `eigenvalues`, `pauli_decomposition`),
  `gate_fidelity(U,V)` `=|tr(U†V)|²/4`, `infidelity(U,V)`, `is_clifford(U)`.
- **`exact`** — the exact backing: `F²=I`, Yang–Baxter, unitarity **[exact]** (sympy + `core.cyclo`).
- **`jones`** — `jones_polynomial(name)`, `jones_symbolic(name)`, `jones_at_fibonacci(name)`
  (`figure_eight → 1−√5` **[exact]**), `bracket_convention_factor()` (`φ²/2`),
  `figure_eight_is_one_minus_sqrt5()`.
- **`knots`** — `KNOT_BRAIDS`, `knot_braid(name)`, `knot_to_gate(name)`, `jones_value(name)`.
- **`compiler`** — `compile_gate(target, max_length, tolerance, method)` (`method` ∈ `brute_force`,
  `golden`), `brute_force(...)`, `golden(...)`, `compress_word(word)`, `CompilationResult`
  (`word, gate, fidelity, length, error`).
- **`visualize`** — `braid_diagram(word, n_strands=3, fmt)` (`fmt` ∈ `text`, `svg`), `gate_summary(U)`.
