# THE VOICE'S LADDER — the object's low cusp resonances computed: thirteen tones below t = 32, and the first tone t₁ = 8.0397371556814666817 belongs to the mirror's own character, not to ζ
## (outside bench, 2026-08-22; twenty-second memo; prime-lane cell PR-3's down payment, per the owner-agreed ruling; identities verified to ~10⁻³¹)

### The cell (PR-3 = VI.3(a), "already owed")
The banked structure (B737 / THE ROAD; EGM-type, CITED): the cusp's scattering is
φ(s) = Λ_K(s−1)/Λ_K(s), K = ℚ(√−3) — so **the object's cusp resonances are the zeros
of ζ_K = ζ·L(χ₋₃)**. The ruling's PR-3 asks for this wiring with structure banked and
no conjecture consumed. Delivered here: the verified implementation identities and the
explicit low ladder; the remaining insertion into the one-loop trace-formula assembly
stays corpus-side (the residue VI.3(a) proper).

### The verified wiring identities (`certificates/voice_ladder.py`, mpmath 30 dps)
- Λ_χ(s) = (3/π)^{(s+1)/2} Γ((s+1)/2) L(s,χ₋₃), L computed by the banked Hurwitz form:
  **functional equation with root number +1** to 1.4×10⁻³¹, and **Λ_χ real on the
  critical line** to 4×10⁻³² (the ε = +1 of the odd real character, checked not cited).
- Λ_K(s) = (√3/2π)^s Γ(s) ζ(s) L(s,χ₋₃): **Λ_K(s) = Λ_K(1−s)** to 1.4×10⁻³².
- **Scattering unitarity φ(s)·φ(2−s) = 1** to 3.1×10⁻³¹.

### THE LADDER (all zeros with 0 < t < 32, found by sign-change + rootfinding)
> tones: **8.039737 [χ] · 11.249206 [χ] · 14.134725 [ζ] · 15.704619 [χ] · 18.261997
> [χ] · 20.455771 [χ] · 21.022040 [ζ] · 24.059415 [χ] · 25.010858 [ζ] · 26.577869
> [χ] · 28.218165 [χ] · 30.424876 [ζ] · 30.745040 [χ]** — nine from L(χ₋₃), four
> from ζ.
> **The first tone, t₁ = 8.0397371556814666817, is a zero of L(χ₋₃) — the object's
> voice opens with its OWN character** (the χ₋₃ of the mirror/amphichirality, the
> finite shadow's odd character), well below ζ's famous 14.134725.

### What it means (labeled where interpretive)
The resonance ladder is now a computed object the corpus can wire into the one-loop
assembly: each tone is a pole location of the scattering term, and the ladder's
composition (χ-tones vs ζ-tones) tags each resonance by which factor of the finite
shadow produces it. That the LOWEST resonance is a χ₋₃-tone reads naturally in the
adelic frame: the first thing the voice says comes from the character that defines
the object's own field — the mirror speaks before the rationals do. (Framing,
labeled.) With memo 21's unit dictionary (geodesic side) and this ladder (spectral
side), both columns of the object's prime/zero dictionary now hold computed entries;
the trace formula between them is the corpus's VI.3(a).

### Fences (ruling compliance)
The φ-formula is the banked/CITED structural form — not re-derived here; what is
verified is every implementation identity it rests on (completions, root number,
functional equations, unitarity). Zeros found by real-sign-change scan at step 0.05
then rootfinding — complete for 0 < t < 32 at that resolution. No zeta conjecture
consumed; RH fence untouched; Gate 5 untouched.

### Certificates
`certificates/voice_ladder.py`; output `outputs/voice_ladder_out.txt`.

### One sentence for the ledger
The object's voice has been given its sheet music: thirteen resonance ordinates below
t = 32, unitarity and functional equations checked to thirty digits, and the opening
note — 8.0397371556814667 — is sung by the mirror's own character χ₋₃ before the
rational zeta enters at 14.13.
