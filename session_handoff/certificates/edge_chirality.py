#!/usr/bin/env python3
"""THE MONOID-LEVEL CHIRALITY QUESTION.
Object level (two-sided hull): the two rules a->ab and a->ba generate the SAME
language (verified in heartbeat.py) -> every hull/bulk invariant is hand-blind.
Observer level (positive register, half-line): the two constructions pick
DIFFERENT POINTS of that hull. Questions:
  A. Quantify the hand as a PHASE: compute the Sturmian intercept rho of each
     fixed word (slope alpha = 2-phi for both). Different rho = the hand is an
     intercept, i.e. exactly the quantity the hull forgets (phase-blindness).
  B. Physics: Fibonacci Hamiltonian H = laplacian_offdiag + V (V=1 on letter b)
     on the HALF-LINE with Dirichlet edge, for both hands. Compare:
       - bulk spectra (should coincide: same language, same IDS)
       - boundary-localized states in gaps (may differ: different phase at the cut)
  C. Control: spectra of interior windows (no natural edge) — hand-blind.
"""
import numpy as np

PHI = (1 + 5**0.5) / 2
ALPHA = 2 - PHI                      # frequency of 'b' in the Fibonacci word

def fixed_word(rule, seed, n):
    w = seed
    while len(w) < n:
        w2 = ''.join(rule[c] for c in w)
        assert w2.startswith(w), "not prefix-stable"
        w = w2
    return w[:n]

AB  = {'a': 'ab', 'b': 'a'}                       # sigma
BA2 = {'a': 'aba', 'b': 'ba'}                     # sigma'^2 where sigma'(a)=ba, sigma'(b)=a
# check BA2 really is sigma'^2:
SP = {'a': 'ba', 'b': 'a'}
assert ''.join(SP[c] for c in SP['a']) == BA2['a'] and ''.join(SP[c] for c in SP['b']) == BA2['b']

N = 4000
w_ab = fixed_word(AB,  'a', N)
w_ba = fixed_word(BA2, 'a', N)
print("fixed words   ab-hand:", w_ab[:32], "...")
print("              ba-hand:", w_ba[:32], "...")
assert w_ab != w_ba

# same language check (sanity, already proved):
F = lambda w, L: {w[i:i+L] for i in range(len(w)-L+1)}
assert all(F(w_ab, L) == F(w_ba, L) for L in (2, 5, 8, 11))

# ---------- A. the intercept ----------
# mechanical word with slope alpha, intercept rho in [0,1):  #b in first n letters
# count_b(n) = floor(n*alpha + rho).  So rho in [c_n - n*alpha, c_n + 1 - n*alpha) for all n.
def intercept_interval(w, nmax):
    lo, hi = 0.0, 1.0
    c = 0
    for n in range(1, nmax + 1):
        c += (w[n-1] == 'b')
        lo = max(lo, c - n * ALPHA)
        hi = min(hi, c + 1 - n * ALPHA)
    return lo, hi

lo1, hi1 = intercept_interval(w_ab, 3000)
lo2, hi2 = intercept_interval(w_ba, 3000)
r1, r2 = (lo1 + hi1) / 2, (lo2 + hi2) / 2
print(f"\nA. intercepts (slope alpha = 2-phi = {ALPHA:.12f}):")
print(f"   ab-hand rho = {r1:.12f}   (width {hi1-lo1:.2e})")
print(f"   ba-hand rho = {r2:.12f}   (width {hi2-lo2:.2e})")
print(f"   candidates: alpha={ALPHA:.12f}  2alpha-? 1-alpha={1-ALPHA:.12f}  alpha^2={ALPHA**2:.12f}  2alpha={2*ALPHA:.12f}")
print(f"   rho_ba - rho_ab = {r2-r1:.12f}   vs alpha^2 = {ALPHA**2:.12f}   vs 1-2alpha = {1-2*ALPHA:.12f}")
distinct = (hi1 < lo2) or (hi2 < lo1)
print("   VERDICT:", "DISTINCT points of the same hull — the hand IS an intercept (a phase)"
      if distinct else "intervals overlap (inconclusive)")

# ---------- B. half-line spectra ----------
LAM = 1.0
def spectrum(word):
    n = len(word)
    V = np.array([LAM if c == 'b' else 0.0 for c in word])
    H = np.diag(V) + np.diag(np.ones(n-1), 1) + np.diag(np.ones(n-1), -1)
    E, U = np.linalg.eigh(H)
    return E, U

M = 1597                                    # F_16
E1, U1 = spectrum(w_ab[:M])
E2, U2 = spectrum(w_ba[:M])

edgeW1 = (U1[:25, :]**2).sum(axis=0)        # weight on first 25 sites
edgeW2 = (U2[:25, :]**2).sum(axis=0)
TH = 0.5                                    # edge state: >50% of weight in first 25 of 1597 sites
edge1 = [(E1[k], edgeW1[k]) for k in range(M) if edgeW1[k] > TH]
edge2 = [(E2[k], edgeW2[k]) for k in range(M) if edgeW2[k] > TH]

# bulk comparison: drop states with ANY strong localization at either end (first/last 25)
def bulkE(E, U):
    wl = (U[:25, :]**2).sum(axis=0); wr = (U[-25:, :]**2).sum(axis=0)
    keep = (wl < 0.2) & (wr < 0.2)
    return E[keep]
B1, B2 = bulkE(E1, U1), bulkE(E2, U2)
# correct hull invariant: the integrated density of states, not index-matched levels
grid0 = np.linspace(-2.5, 3.5, 400)
idsB1 = np.searchsorted(np.sort(B1), grid0) / M
idsB2 = np.searchsorted(np.sort(B2), grid0) / M
bulkdiff = np.max(np.abs(idsB1 - idsB2))
print(f"\nB. half-line Fibonacci Hamiltonian (lambda={LAM}, N={M}, Dirichlet edge):")
print(f"   bulk states: {len(B1)} vs {len(B2)}; max |IDS difference| = {bulkdiff:.4f} (finite-size ~ 1/N = {1/M:.4f})")
print(f"   LEFT-edge-localized states (weight>{TH} on first 25 sites):")
print(f"     ab-hand: {len(edge1)} states at E = " + ", ".join(f"{e:+.6f}" for e, _ in edge1[:12]))
print(f"     ba-hand: {len(edge2)} states at E = " + ", ".join(f"{e:+.6f}" for e, _ in edge2[:12]))
s1 = sorted(e for e, _ in edge1); s2 = sorted(e for e, _ in edge2)
if len(s1) == len(s2):
    md = max((abs(x-y) for x, y in zip(s1, s2)), default=0.0)
    print(f"     same count; max |edge-E difference| = {md:.3e}")
    edge_differ = md > 1e-6
else:
    print(f"     DIFFERENT COUNTS: {len(s1)} vs {len(s2)}")
    edge_differ = True

# stability in N (rule out finite-size artifacts): recompute at F_15 = 987
M2 = 987
E1b, U1b = spectrum(w_ab[:M2]); E2b, U2b = spectrum(w_ba[:M2])
e1b = sorted(E1b[k] for k in range(M2) if (U1b[:25, k]**2).sum() > TH)
e2b = sorted(E2b[k] for k in range(M2) if (U2b[:25, k]**2).sum() > TH)
def stab(sA, sB):
    return max((min(abs(x - y) for y in sB) for x in sA), default=0.0) if sA and sB else float('nan')
print(f"   stability: ab-hand edge energies move by <= {stab(s1, e1b):.2e} between N=987 and N=1597")
print(f"              ba-hand edge energies move by <= {stab(s2, e2b):.2e}")

# ---------- C. control: interior windows (object level) ----------
off = 1200
Ec1, Uc1 = spectrum(w_ab[off:off+M2])
# find the SAME window content in the other word? different point, same language ->
# windows differ pointwise, but the SPECTRAL STATISTICS must agree. Compare IDS:
Ec2, Uc2 = spectrum(w_ba[off:off+M2])
# IDS comparison at 200 energy points:
grid = np.linspace(-2.5, 3.5, 200)
ids1 = np.searchsorted(np.sort(Ec1), grid) / M2
ids2 = np.searchsorted(np.sort(Ec2), grid) / M2
print(f"\nC. object-level control (interior windows, N={M2}):")
print(f"   max |IDS difference| = {np.max(np.abs(ids1-ids2)):.4f}  (finite-size ~ 1/N = {1/M2:.4f})")

print("\nSUMMARY:")
print(f"  hand-as-phase: {'YES — distinct intercepts' if distinct else 'unresolved'}")
print(f"  bulk hand-blind: {'YES' if bulkdiff < 3.0/M else 'NO — check'}  (max IDS diff {bulkdiff:.1e}, finite-size {1/M:.1e})")
print(f"  edge distinguishes hands: {'YES' if edge_differ else 'NO'}")
