# Worked examples

Three things a newcomer runs first. Each is copy-pasteable after `pip install -e .`.

---

## 1. Compile a gate into a Fibonacci-anyon braid

Compile the Hadamard gate into a braid word and check the fidelity:

```python
import numpy as np
from golden_gate.demo.compiler import compile_gate

H = np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)

r = compile_gate(H, max_length=16, tolerance=1e-2)
print("braid word :", r.word)          # list of (generator, power) unit crossings
print("crossings  :", r.length)
print("fidelity   :", round(r.fidelity, 4))
```

`compile_gate` searches braid words over the two generators `sigma1, sigma2` (and their
inverses). Longer `max_length` / tighter `tolerance` buys higher fidelity at more crossings.
The `golden` method (`method="golden"`) is a special case that shines only when the target is
near a power of the golden gate; `brute_force` (the default) is the general workhorse.

---

## 2. The golden gate and its properties

The **golden gate** is the figure-eight knot braid `sigma1^-1 sigma2 sigma1^-1 sigma2`:

```python
from golden_gate.demo.gates import golden_gate, gate_properties
from golden_gate.demo.visualize import braid_diagram, gate_summary
from golden_gate.demo.knots import knot_braid

U = golden_gate()
p = gate_properties(U)
print("rotation angle :", round(p["rotation_angle"] / 3.14159265, 4), "* pi")  # ~0.2447
print("non-Clifford   :", not p["is_clifford"])                                  # True
print("determinant    :", round(p["determinant"].real, 6))                       # 1.0

print(gate_summary(U))
print(braid_diagram(knot_braid("figure_eight")))          # ASCII braid
open("golden.svg", "w").write(
    braid_diagram(knot_braid("figure_eight"), fmt="svg"))  # SVG braid
```

---

## 3. Verify the Jones value **exactly**

The figure-eight's Jones polynomial at the Fibonacci point `t = e^{2*pi*i/5}` is
`1 - sqrt5` — and `golden_gate` proves it as an exact identity in `Q(zeta_60)`, not a float
approximation:

```python
from golden_gate.demo.jones import jones_at_fibonacci, figure_eight_is_one_minus_sqrt5
from golden_gate.core import cyclo as C

val = jones_at_fibonacci("figure_eight")
print("== 1 - sqrt5 exactly :", val == C.sub(C.ONE, C.SQRT5))   # True
print("flagship identity     :", figure_eight_is_one_minus_sqrt5())  # True

# decompose the exact value in the basis {1, sqrt5, sqrt(-3), sqrt(-15)}:
print("H-coords (p,q,r,s)    :", C.solve_H(val))               # (1, -1, 0, 0)
```

**Convention note.** The *standard normalized* Jones value is `1 - sqrt5 ~= -1.236`, matching
the figure-eight's colored-Jones data. Some sources quote `-phi ~= -1.618`; that is the
*unnormalized Kauffman bracket* convention, related by the algebraic identity
`-phi = (1 - sqrt5) * phi^2 / 2` (see `demo.jones.bracket_convention_factor`). The library
computes and documents the standard value — see `GOVERNANCE.md` §2 on convention honesty.
