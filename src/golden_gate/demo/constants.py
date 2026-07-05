"""Fibonacci anyon data -- numerical (complex128) constants for the runtime.

The exact (symbolic) forms of everything here are in ``golden_gate.demo.exact``;
these float64 values are what the braiding/compiler runtime uses. Cross-checked
against the exact layer by the test suite.

References
----------
Preskill, "Lecture Notes on Topological Quantum Computation" (2004), ch. 9.
Nayak, Simon, Stern, Freedman, Das Sarma, Rev. Mod. Phys. 80, 1083 (2008).
Bonesteel, Hormozi, Zikos, Simon, Phys. Rev. Lett. 95, 140503 (2005).
"""

import numpy as np

# --- the golden ratio ------------------------------------------------------
PHI = (1.0 + np.sqrt(5.0)) / 2.0        # phi = (1+sqrt5)/2
PHI_INV = PHI - 1.0                     # 1/phi = phi - 1
SQRT_PHI_INV = PHI_INV ** 0.5           # 1/sqrt(phi)

# --- quantum dimensions ----------------------------------------------------
D_TAU = PHI                             # d_tau = phi
D_TOTAL = (2.0 + PHI) ** 0.5           # total quantum dimension D = sqrt(2+phi)

# --- R-matrix (braiding phases), cyclotomic: entries in Q(zeta_10) ---------
R_VACUUM = np.exp(-4j * np.pi / 5.0)    # R^{tau tau}_1  (fuse to vacuum)
R_TAU = np.exp(3j * np.pi / 5.0)        # R^{tau tau}_tau (fuse to tau)

# --- F-matrix (recoupling), involves sqrt(phi): NOT cyclotomic -------------
# F = [[1/phi, 1/sqrt(phi)], [1/sqrt(phi), -1/phi]], symmetric, F^2 = I, det = -1.
F_MATRIX = np.array([[PHI_INV, SQRT_PHI_INV],
                     [SQRT_PHI_INV, -PHI_INV]], dtype=complex)
