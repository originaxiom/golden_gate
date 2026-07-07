# The mathematics of golden_gate

This is the conceptual tour. Every claim is tagged with its epistemic label —
**[exact]**, **[numeric]**, or **[ported]** (`GOVERNANCE.md` §3) — so you always know whether a
statement is proved by exact arithmetic, computed to a tolerance, or reproduced from the research
program it was consolidated from.

---

## 1. Fibonacci anyons

A Fibonacci anyon `τ` is the simplest non-abelian anyon: it has one nontrivial fusion rule,

```
τ × τ = 1 + τ,
```

so the number of fusion channels of `n` anyons is a Fibonacci number — hence the name. Its quantum
dimension is the golden ratio **[exact]**:

```
d_τ = φ = (1 + √5) / 2.
```

Two data govern the theory: the **R-matrix** (the phase of exchanging two anyons) and the
**F-matrix** (the associator relating the two ways of fusing three). In the qubit encoded by three
`τ`'s with total charge `τ`,

```
R = diag(R_1, R_τ),   R_1 = e^{-4πi/5},   R_τ = e^{3πi/5}     [exact — 60th roots of unity]

F = [[1/φ,   1/√φ ],
     [1/√φ, −1/φ ]]                                            [exact:  F² = I,  det F = −1]
```

`core.cyclo` verifies `R_1, R_τ` are exact powers of `ζ₆₀` (`ζ₆₀³⁶`, `ζ₆₀¹⁸`) and that `φ² = φ + 1`
**[exact]**. The `1/√φ` in `F` is *not* cyclotomic, so `demo.exact` proves the `F`-identities with
sympy instead **[exact]**.

## 2. Braiding: gates from crossings

Exchanging anyons 1–2 and 2–3 gives the two braid generators, as `2×2` unitaries on the qubit:

```
σ₁ = diag(R_1, R_τ),        σ₂ = F · diag(R_1, R_τ) · F.
```

They satisfy the **Yang–Baxter relation** `σ₁σ₂σ₁ = σ₂σ₁σ₂` **[exact]** (`demo.exact`) — the algebraic
statement that a braid is a topological object. A braid *word* composes them; `demo.braiding.evaluate_braid`
returns the resulting gate.

Because braiding is topological, the gate depends only on the braid's isotopy class — this is the
error-resistance that makes anyons interesting for quantum computing.

## 3. The golden gate

The **golden gate** is the figure-eight braid

```
G = σ₁⁻¹ σ₂ σ₁⁻¹ σ₂.
```

It is the quantum-topology face of the axiom object: `σ:a→ab` is the object's own metallic
substitution, and this braid is the figure-eight knot `4₁`. Its gate is:

- **non-Clifford** **[numeric]** — it is not in the Clifford group, so together with the Clifford
  gates it is universal;
- a rotation of the Bloch sphere by **`0.2447π`** **[numeric]** (`= 2·arccos(|Re tr(G/√det G)|/2)`);
- **determinant 1** **[numeric, ≈1 to 1e-16]**.

"Non-Clifford + braiding" is exactly what topological universality needs.

## 4. Why exact arithmetic

A float64 toolkit checks `F² = I` as `‖F² − I‖ < 10⁻¹⁴`. That is a *near-miss*, not a proof — and it
hides genuine questions (is a residual `10⁻¹⁴` a true zero or a real defect one refinement away?).
`golden_gate` computes the cyclotomic data as **exact** vectors of rationals in ℚ(ζ₆₀) = `ℤ[ζ₆₀]⊗ℚ`,
represented as length-16 `Fraction` vectors modulo the 60th cyclotomic polynomial `Φ₆₀`. Field
operations are exact; an identity is locked by an **equality** test, never a tolerance
(`GOVERNANCE.md` §2). The radicals live inside: `√5, √−3, √−15`, and the Gauss sum `g(15) = i√15`
are explicit elements, each verified to square to its definition **[exact]**.

## 5. The Jones polynomial at the Fibonacci point

The Jones polynomial `V(K; t)` is a knot invariant; evaluated at the Fibonacci point `t = ζ₅ = e^{2πi/5}`
it is computed by the same anyon data. For the figure-eight:

```
V(4₁; ζ₅) = 1 − √5 ≈ −1.2360679…         [exact — proved as an equality in ℚ(ζ₆₀)]
```

`demo.jones.jones_at_fibonacci("figure_eight")` returns this as an exact `core.cyclo` element and a test
asserts `== C.sub(C.ONE, C.SQRT5)`.

**Convention honesty (§2).** Some sources quote `−φ ≈ −1.618` for "the Jones value." That is the
*unnormalized Kauffman bracket* convention, related to the standard value by the algebraic identity
`−φ = (1 − √5) · φ²/2`. The library computes and documents the **standard normalized** value `1 − √5`;
`demo.jones.bracket_convention_factor()` returns the exact `φ²/2` **[exact]**.

## 6. The research core — an honest firewall

`core.lie` and `core.jets` are **[ported]** high-precision machinery from the origin-axiom research
program (the `{4,8}`-integrability / E₆ cup-product study). They are *exact/numeric research
machinery in Lie theory and low-dimensional topology* — **not a physics claim**, and nothing here
promotes to a "theory of everything." The firewall is stated in every module docstring.

What they compute, in one paragraph each:

- **`core.lie.e6`** — the exact Chevalley Lie algebra `𝔢₆` (78-dim, integer structure constants), with
  the Jacobi identity **verified exactly over all 76,076 basis triples** **[exact]**, the principal
  `sl₂`, and the diagram involution `θ` (fixed subalgebra `𝔣₄` of dim 52; the `26 = 𝔢₆/𝔣₄` coset).
- **`core.lie.rep`** — the E₆ character-variety tangent of the figure-eight: `H¹(4₁, Sym^{2m}) = 1`
  for each E₆ exponent, and two ℤ/2 gradings; the "escape" sector is exactly the θ-odd exponents `{4,8}`.
- **`core.lie.cohomology`** — the second-order cup-product obstruction `[z∪z] ∈ H²(π₁(4₁), 𝔢₆)`. The
  headline **[ported]** result: the escape directions `m∈{4,8}` are *unobstructed to second order* —
  the obstruction class vanishes in every exponent block (the `{4,8}` components by θ-parity, the F₄
  blocks `{1,5,7,11}` genuinely), while the obstruction *vector* `q` is emphatically nonzero.
- **`core.jets`** — the depth-3 Massey products (unobstructed to third order) and the boundary
  restriction (rank, the Neumann-Zagier slopes, a single universal cusp-shape `τ = −2√3·i`).

Reading of the verdict (the honest scope): "unobstructed to 2nd/3rd order" is the standard
Goldman–Millson deformation reading of a vanishing cup class — it does **not** assert all-orders
integrability.

## 7. The gate-attack harness

`core.harness` makes the research discipline runnable: a frozen `Preregistration` (hypothesis, nulls,
kill conditions, banked identities), and `run_gated` — which runs the banked-identity gate **first**
and refuses to compute (or read) the result past a failed gate. `harness.demo_e6` wires this to the E₆
escape obstruction as a worked example.

---

*Everything above is reproduced by the test suite (`pytest -q`, and the `OA_SLOW=1` sweeps) and the
banked-identity gates (`python -m golden_gate.core.gates`).*
