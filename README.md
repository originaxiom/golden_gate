# golden_gate

[![CI](https://github.com/originaxiom/golden_gate/actions/workflows/ci.yml/badge.svg)](https://github.com/originaxiom/golden_gate/actions/workflows/ci.yml)

**Exact-arithmetic engines for Fibonacci-anyon quantum topology — and a braid-gate compiler
that proves its identities exactly, not to a tolerance.**

> **In one sentence:** most quantum software talks about *circuits*; topological quantum computation
> talks about *braids*. `golden_gate` is a small Python lab for turning Fibonacci-anyon braids into
> quantum gates (and back), and checking the identities **exactly**.

Fibonacci anyons are a candidate for topological quantum computation: you compute by *braiding*
them, and each braid is a quantum gate. `golden_gate` turns gates into braids and braids into
gates — and, unlike a float64 toolkit, it backs the headline facts with **exact arithmetic in
ℚ(ζ₆₀)**, so

```
F² = I,   σ₁σ₂σ₁ = σ₂σ₁σ₂  (Yang–Baxter),   Jones(4₁; e^{2πi/5}) = 1 − √5
```

hold as **symbolic equalities**, not `±1e-14` numerical near-misses.

The **golden gate** itself is the figure-eight braid `σ₁⁻¹σ₂σ₁⁻¹σ₂` — a non-Clifford rotation of
exactly `0.2447π`.

## Try it

Open **[`web/explorer.html`](web/explorer.html)** in any browser (no install, no build): build braids,
watch the gate they weave, compile a target gate to a braid, and read exact Jones values. It is a
single self-contained page — host it anywhere, or open the file directly.

Docs site (MkDocs) + the hosted explorer publish to GitHub Pages via CI:
**https://originaxiom.github.io/golden_gate/** (once the owner enables Pages).

## Quickstart

```bash
pip install -e .
```

```python
import numpy as np
from golden_gate.demo.gates import golden_gate, gate_properties
from golden_gate.demo.compiler import compile_gate
from golden_gate.demo.jones import jones_at_fibonacci
from golden_gate.core import cyclo as C

U = golden_gate()
print(gate_properties(U)["rotation_angle"] / np.pi)      # 0.2447…  (numeric)
print(jones_at_fibonacci("figure_eight") == C.sub(C.ONE, C.SQRT5))   # True  (exact)

H = np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)
r = compile_gate(H, max_length=16, tolerance=1e-2)
print(r.length, round(r.fidelity, 4))                    # 11  0.9906
```

More in [`docs/EXAMPLES.md`](docs/EXAMPLES.md); the mathematics in [`docs/MATH.md`](docs/MATH.md);
the full API in [`docs/API.md`](docs/API.md).

## Architecture — built inside-out

Three layers, core first:

1. **Core engines** (`golden_gate.core`) — clean, tested, exact/high-precision computation:
   - `cyclo` — exact ℚ(ζ₆₀) arithmetic (Fraction-vector power basis mod Φ₆₀): the radical
     constants `√5, √−3, √−15`, the Gauss sum `g(15)=i√15`, the level-15 `T`/`S` Weil matrices,
     and exact projection into `H = ℚ(√5, √−3)`.
   - `charvar` — the theta-lift / seam toolkit (Weil matrices `W_m`, par-traces, DFT
     eigenprojectors, exact rank, multiplicative tensor completion).
   - `lie` / `jets` — the E₆ cup-product research stack (exact Chevalley 𝔢₆; the character-variety
     tangent of the figure-eight; the two-basis cup-product obstruction; depth-2/3 Massey products;
     the boundary restriction). High-precision `mpmath`, scoped via `core.precision`. *Ported
     research machinery — see the firewall note in [`docs/MATH.md`](docs/MATH.md); no physics claim.*
2. **Gate-attack harness** (`golden_gate.core.harness`) — a pre-registration + banked-identity
   discipline: freeze the hypothesis and the checks, run the banked gate first, and **refuse to read
   a result past a failed gate**.
3. **Demo layer** (`golden_gate.demo`) — the outward-facing braid compiler: braiding matrices, the
   named gates, exact-backed Jones/knot data, the compiler, and text/SVG braid diagrams. Plus the
   interactive explorer above.

## Result labels (the honesty lock)

Every public result carries one epistemic status (`GOVERNANCE.md` §3), and the docs mark it:

| label | meaning |
|-------|---------|
| **exact** | proved by exact arithmetic, locked by an *equality* test (e.g. `Jones(4₁)=1−√5`). |
| **numeric** | a floating/high-precision value with a stated tolerance (e.g. the `0.2447π` angle). |
| **ported** | reproduced from the origin-axiom research program, banked by an identity check. |

Convention honesty is enforced: e.g. the standard Jones value is `1−√5`; the `−φ` some sources quote
is the *unnormalized Kauffman bracket*, related by `−φ = (1−√5)·φ²/2` — the library documents both.

## Scope

`golden_gate` is a **research / education prototype** (v0.1), not a production quantum compiler. It is
complementary to the mainstream circuit-model SDKs (Qiskit, Cirq, PennyLane, …): those target the gate/
circuit model on real and simulated hardware; this is a specialized **exact-arithmetic lab for the
braid / topological model**. If you want to run circuits, use those. If you want to compute and *verify*
Fibonacci-anyon braid gates and quantum-topology identities exactly, use this.

## Prior art

Fibonacci-anyon braid synthesis is a mature literature (Kliuchnikov–Bocharov–Svore; Kliuchnikov–Yard,
*A framework for exact synthesis*, arXiv:1504.04350; the Monte-Carlo compiler, PRX Quantum 2.010334).
`golden_gate`'s contribution is **clean, exact, tested, installable packaging + integration** (and the
research core + the axiom quantum-topology connection) — **not** new synthesis algorithms. The
`demo.compiler` is a straightforward bounded brute-force search, deliberately not competitive with the
cited synthesis algorithms.

## Install & test

```bash
pip install -e .
pytest -q                 # fast tier (~70s)
OA_SLOW=1 pytest -q        # + heavy exact/high-precision sweeps
python -m golden_gate.core.gates   # banked-identity + hygiene gates; exits 0 when clean
```

## License

MIT — see [`LICENSE`](LICENSE).
