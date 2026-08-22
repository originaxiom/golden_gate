#!/usr/bin/env python3
"""PR-3 down payment: THE VOICE'S LADDER — the cusp-resonance spectrum of the object,
as zeros of zeta_K, K = Q(sqrt-3), with every implementation identity verified.

 1. L(s,chi_-3) via Hurwitz zeta (the banked exact form); completed
    Lam_chi(s) = (3/pi)^((s+1)/2) Gamma((s+1)/2) L(s,chi): verify root number +1
    (Lam(s) = Lam(1-s)) and REALITY on the critical line, numerically to ~25 digits.
 2. Lam_K(s) = (sqrt(3)/(2pi))^s Gamma(s) zeta(s) L(s,chi): verify Lam_K(s)=Lam_K(1-s).
 3. The scattering ratio phi(s) = Lam_K(s-1)/Lam_K(s) (banked structural form, CITED):
    verify unitarity phi(s) phi(2-s) = 1.
 4. THE LADDER: all zeros of L(s,chi_-3) and zeta(s) on the critical line with
    0 < t < 32 -> the merged low resonance ordinates of the object's voice.
"""
import mpmath as mp
mp.mp.dps=30
def Lchi(s):
    return 3**(-s)*(mp.zeta(s,mp.mpf(1)/3)-mp.zeta(s,mp.mpf(2)/3))
def Lam_chi(s):
    return (mp.mpf(3)/mp.pi)**((s+1)/2)*mp.gamma((s+1)/2)*Lchi(s)
# 1. functional equation + reality
err1=max(abs(Lam_chi(s)-Lam_chi(1-s)) for s in (mp.mpf('0.3')+2j, mp.mpf('1.7')-0.5j, mp.mpf('2.2')+5j))
tvals=[1.5,5.0,9.3,20.7]
err_real=max(abs(mp.im(Lam_chi(mp.mpf('0.5')+1j*t))) for t in tvals)
print(f"Lam_chi functional equation (root number +1): max err {mp.nstr(err1,3)}")
print(f"Lam_chi REAL on critical line: max |Im| {mp.nstr(err_real,3)}")
def Lam_K(s):
    return (mp.sqrt(3)/(2*mp.pi))**s*mp.gamma(s)*mp.zeta(s)*Lchi(s)
err2=max(abs(Lam_K(s)-Lam_K(1-s)) for s in (mp.mpf('0.3')+2j, mp.mpf('2.2')+5j, mp.mpf('-0.7')+1.3j))
print(f"Lam_K functional equation: max err {mp.nstr(err2,3)}")
def phi(s): return Lam_K(s-1)/Lam_K(s)
err3=max(abs(phi(s)*phi(2-s)-1) for s in (mp.mpf('1.3')+2j, mp.mpf('0.6')+7j, mp.mpf('1.9')+0.4j))
print(f"scattering unitarity phi(s)phi(2-s)=1: max err {mp.nstr(err3,3)}")
# 4. zeros: L(chi) via sign changes of real Lam_chi on the line; zeta via zetazero
f=lambda t: mp.re(Lam_chi(mp.mpf('0.5')+1j*t))
zeros_chi=[]
t=0.5; step=0.05; prev=f(t)
while t<32:
    t2=t+step; cur=f(t2)
    if prev*cur<0:
        z=mp.findroot(f,(t+t2)/2)
        zeros_chi.append(float(z))
    prev=cur; t=t2
zeros_zeta=[]
k=1
while True:
    z=mp.zetazero(k)
    tz=float(mp.im(z))
    if tz>32: break
    zeros_zeta.append(tz); k+=1
print(f"\nzeros of L(s,chi_-3), 0<t<32: {[round(z,6) for z in zeros_chi]}")
print(f"zeros of zeta(s),     0<t<32: {[round(z,6) for z in zeros_zeta]}")
merged=sorted([(z,'chi') for z in zeros_chi]+[(z,'zeta') for z in zeros_zeta])
print("\nTHE LADDER — the object's low cusp-resonance ordinates (zeros of zeta_K):")
for i,(z,src) in enumerate(merged):
    print(f"  tone {i+1:2d}:  t = {z:11.6f}   [{src}]")
# residue check: the first tone is a chi zero, below zeta's 14.134
assert merged[0][1]=='chi' and merged[0][0]<14
# verify the first chi zero to more digits
z1=mp.findroot(f, merged[0][0])
print(f"\nfirst tone to 20 digits: t1 = {mp.nstr(z1,20)}  (a zero of L(chi_-3), NOT of zeta)")
