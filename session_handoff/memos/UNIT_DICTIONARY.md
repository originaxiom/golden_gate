# THE UNIT DICTIONARY — every geodesic eigenvalue is a unit of an explicit palindromic quartic labeled by two rational integers, and geodesic length is its log-Mahler measure
## (outside bench, 2026-08-22; twenty-first memo; prime-lane cell PR-2 executed per the owner-agreed ruling; exact census + 10⁻¹⁵ numeric identity)

### The cell (PR-2 of the prime-lane ruling: "geodesics ↔ primes/units of ℚ(√−3)")
Extend the ruling's verified anchor (five words, min-polys with constant coefficient
±1) to the full dictionary, with the mechanism exhibited rather than sampled.

### THE THEOREM-SHAPED CORE (`certificates/unit_dictionary.py`, exact)
For γ ∈ Γ loxodromic with trace t ∈ ℤ[ω] (automatic — the Riley matrices lie in
SL₂(ℤ[q])), the eigenvalue λ satisfies the **palindromic integer quartic**

> **P_{T,N}(x) = x⁴ − T·x³ + (N+2)·x² − T·x + 1,  T = Tr_{K/ℚ}(t), N = N_{K/ℚ}(t)**

with constant term 1 — so **λ is an algebraic unit, always**, and the geodesic's
"prime label" is the PAIR OF RATIONAL INTEGERS (T, N). Verified EXACTLY (the
ℤ[ω]-expansion identity, no floats) on **all 672 loxodromic classes** among the 693
cyclically-reduced words to length 8 (up to rotation and inversion): PASS, no
exceptions. The census carries **122 distinct (T,N) labels**.

### THE LENGTH ENTRY OF THE DICTIONARY
> **ℓ(γ) = 2 log|λ| = log Mahler(P_{T,N})** — verified across the whole census to a
> maximum error of **3.8×10⁻¹⁵**.

The object's prime lengths — the "log p" of its prime-geodesic theorem — are exactly
the logarithmic Mahler measures of integer palindromic (reciprocal) quartics indexed
by two integers. The shortest geodesic (word Ab) carries (T,N) = (3,3):
P = x⁴−3x³+5x²−3x+1. (Pointer, labeled, no conjecture consumed: reciprocal integer
polynomials and small Mahler measures are Lehmer territory — the object's length
spectrum lives in that arithmetic, which is exactly the kind of instrument-grade fact
the ruling wanted from this lane.)

### The splitting doorway (exhibited, not proven)
Per class, the splitting datum is disc(γ) = t²−4 ∈ ℤ[ω] with rational norm N(t²−4);
the census table factors it and marks each rational prime by its behavior in ℚ(√−3)
(p ≡ 1 mod 3 split, p ≡ 2 inert, 3 ramified). First entries: Ab → 13 [split];
AB → 3·7 [ram·split]; AAb → 2⁴·3 [inert⁴·ram]; AAAB → 3²·37; AAbbAb → 5²·61 … The
geodesic-to-prime incidence — which primes of ℚ(√−3) each "prime of the object"
sees — is now a computed table: the Chebotarev-type doorway of PR-2, opened as data.

### Fences (ruling compliance)
Census scope: cyclically-reduced words to length 8, deduped by rotation+inversion
(trace-level labels; full conjugacy enumeration in Γ not claimed). Structure only:
no zeta conjecture consumed, RH fence untouched; the cell rides with C-AD3 exactly as
the ruling's queue prescribes. Gate 5 untouched.

### Certificates
`certificates/unit_dictionary.py`; output `outputs/unit_dictionary_out.txt`.

### One sentence for the ledger
Every prime of the object is a unit twice over — its eigenvalue satisfies a
palindromic integer quartic with constant term one, its label is a pair of rational
integers, its length is the quartic's log-Mahler measure to fifteen digits, and its
discriminant's prime factors read off the splitting of rational primes in ℚ(√−3):
the prime-geodesic dictionary of PR-2, executed as a table instead of an aspiration.
