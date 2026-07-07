# golden_gate

**Exact-arithmetic engines for Fibonacci-anyon quantum topology — and a braid-gate compiler that
proves its identities exactly, not to a tolerance.**

Most quantum software talks about *circuits*; topological quantum computation talks about *braids*.
`golden_gate` is a small Python lab for turning Fibonacci-anyon braids into quantum gates (and back),
and checking the identities **exactly** in the cyclotomic field ℚ(ζ₆₀):

```
F² = I,   σ₁σ₂σ₁ = σ₂σ₁σ₂  (Yang–Baxter),   Jones(4₁; e^{2πi/5}) = 1 − √5
```

hold as **symbolic equalities**, not `±1e-14` numerical near-misses. The **golden gate** itself is the
figure-eight braid `σ₁⁻¹σ₂σ₁⁻¹σ₂` — a non-Clifford rotation of exactly `0.2447π`.

## Start here

- **[Try the interactive explorer](explorer.html)** — build braids, watch the gate, compile targets,
  read exact Jones values (no install).
- **[Worked examples](EXAMPLES.md)** — compile a gate, the golden gate's properties, verify `Jones = 1−√5`.
- **[The mathematics](MATH.md)** — Fibonacci anyons, the golden gate, exact arithmetic, the research core.
- **[API reference](API.md)** — the public surface, each with its epistemic label; and the
  [auto-generated demo reference](reference.md).

## Install

```bash
pip install -e .
golden-gate-verify        # check the exact math engines reproduce
```

## Scope

A **research / education prototype** (v0.1) — a specialized exact-arithmetic lab for the braid /
topological model, complementary to the circuit-model SDKs (Qiskit, Cirq, …), **not** a production
quantum compiler. See the honest positioning in the [tools-paper draft](PAPER.md).
