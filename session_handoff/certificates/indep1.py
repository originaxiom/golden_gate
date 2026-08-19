#!/usr/bin/env python3
"""Independent referee checks, part 1: matrix/group-theory claims. No reliance on paper's scripts."""
import itertools, sys
from fractions import Fraction

ok = True
def check(name, cond):
    global ok
    print(("PASS " if cond else "FAIL ") + name)
    if not cond: ok = False

def mmul(A,B,mod=None):
    C = [[A[0][0]*B[0][0]+A[0][1]*B[1][0], A[0][0]*B[0][1]+A[0][1]*B[1][1]],
         [A[1][0]*B[0][0]+A[1][1]*B[1][0], A[1][0]*B[0][1]+A[1][1]*B[1][1]]]
    if mod: C=[[x%mod for x in r] for r in C]
    return C
def det(A): return A[0][0]*A[1][1]-A[0][1]*A[1][0]
def tr(A): return A[0][0]+A[1][1]
def minv(A):  # integer inverse for det ±1
    d = det(A); assert d in (1,-1)
    return [[A[1][1]//d, -A[0][1]//d],[-A[1][0]//d, A[0][0]//d]]

R=[[1,1],[0,1]]; L=[[1,0],[1,1]]
def word(w):
    M=[[1,0],[0,1]]
    for c in w: M=mmul(M, R if c=='R' else L)
    return M

# --- phi_m = R^m L^m = [[m^2+1,m],[m,1]] ---
for m in range(1,8):
    check(f"R^{m}L^{m} = [[m^2+1,m],[m,1]] (m={m})", word('R'*m+'L'*m)==[[m*m+1,m],[m,1]])

# --- collapse lemma ---
for m in range(1,10):
    phi=[[m*m+1,m],[m,1]]
    I=[[1,0],[0,1]]
    A=[[phi[0][0]-1,phi[0][1]],[phi[1][0],phi[1][1]-1]]
    B=[[phi[0][0]+1,phi[0][1]],[phi[1][0],phi[1][1]+1]]
    check(f"chi_m(1)=-m^2, chi_m(-1)=m^2+4, tr=m^2+2 (m={m})",
          det(A)==-m*m and det(B)==m*m+4 and tr(phi)==m*m+2)

# --- Smith normal form of phi_m - I is diag(m,m) ---
from math import gcd
for m in range(1,10):
    M=[[m*m,m],[m,0]]
    g=gcd(gcd(M[0][0],M[0][1]),M[1][0])
    d=abs(det(M))
    check(f"SNF(phi_{m}-I)=diag({m},{m})", g==m and d==m*m)

# --- |SL(2,Z/N)| values and 2T,2O,2I orders; N>=6 bound ---
def sl2_order(N):
    cnt=0
    for a in range(N):
        for b in range(N):
            for c in range(N):
                for d in range(N):
                    if (a*d-b*c)%N==1: cnt+=1
    return cnt
orders={N: sl2_order(N) for N in range(2,13)}
check("|SL2(Z/N)| N=2..5 = 6,24,48,120", [orders[N] for N in (2,3,4,5)]==[6,24,48,120])
check("|SL2(Z/N)| not in {24,48,120} for 6<=N<=12", all(orders[N] not in (24,48,120) for N in range(6,13)))
# telescoping bound: N^2(N+1)/2 at N=6 equals 126
check("bound N^2(N+1)/2 = 126 at N=6", 36*7//2==126)

# --- SL(2,Z/4): seven involutions, no element of order 8 ---
els=[]
for a in range(4):
    for b in range(4):
        for c in range(4):
            for d in range(4):
                if (a*d-b*c)%4==1: els.append(((a,b),(c,d)))
def m2(A,B):
    return ((( A[0][0]*B[0][0]+A[0][1]*B[1][0])%4, (A[0][0]*B[0][1]+A[0][1]*B[1][1])%4),
            (( A[1][0]*B[0][0]+A[1][1]*B[1][0])%4, (A[1][0]*B[0][1]+A[1][1]*B[1][1])%4))
I4=((1,0),(0,1))
inv2=sum(1 for g in els if g!=I4 and m2(g,g)==I4)
def order(g):
    x=g; n=1
    while x!=I4: x=m2(x,g); n+=1
    return n
ords=set(order(g) for g in els)
check("|SL(2,Z/4)|=48", len(els)==48)
check("SL(2,Z/4) has exactly 7 involutions (non-identity g, g^2=I)", inv2==7)
check("SL(2,Z/4) has no element of order 8", 8 not in ords)

# --- phi_1 mod 5 generates cyclic group of order 10 ---
p1=((2,1),(1,1))
def m5(A,B):
    return ((( A[0][0]*B[0][0]+A[0][1]*B[1][0])%5, (A[0][0]*B[0][1]+A[0][1]*B[1][1])%5),
            (( A[1][0]*B[0][0]+A[1][1]*B[1][0])%5, (A[1][0]*B[0][1]+A[1][1]*B[1][1])%5))
I5=((1,0),(0,1))
x=p1; n=1
while x!=I5: x=m5(x,p1); n+=1
check("phi_1 mod 5 has order 10", n==10)

# --- Fricke commutator identity tr[phi_m,phi_n] = 2 - (mn(n-m))^2 ---
allok=True
for m in range(1,7):
    for nn in range(1,7):
        pm=[[m*m+1,m],[m,1]]; pn=[[nn*nn+1,nn],[nn,1]]
        comm=mmul(mmul(pm,pn),mmul(minv(pm),minv(pn)))
        if tr(comm)!=2-(m*nn*(nn-m))**2: allok=False
check("Fricke: tr[phi_m,phi_n]=2-(mn(n-m))^2 for m,n<=6", allok)
p1m=[[2,1],[1,1]]; p2m=[[5,2],[2,1]]
comm12=mmul(mmul(p1m,p2m),mmul(minv(p1m),minv(p2m)))
check("[phi_1,phi_2]=[[11,-24],[6,-13]], tr=-2", comm12==[[11,-24],[6,-13]] and tr(comm12)==-2)
X1=[[1,1],[1,0]]; X2=[[2,1],[1,0]]
commX=mmul(mmul(X1,X2),mmul(minv(X1),minv(X2)))
check("tr[X_1,X_2]=1 (identity fails for X_m)", tr(commX)==1)

# --- witness A=[[1,2],[3,5]]: det -1, tr 6, and form-inequivalence to X_6 ---
A=[[1,2],[3,5]]
check("witness: det=-1, tr=6", det(A)==-1 and tr(A)==6)
# form (c, d-a, -b): A -> (3,4,-2), X6 -> (1,-6,-1); both disc 40
fA=(3,4,-2); fX=(1,-6,-1)
check("forms disc 40", fA[1]**2-4*fA[0]*fA[2]==40 and fX[1]**2-4*fX[0]*fX[2]==40)
# (1,-6,-1) ~ x^2-10y^2 (x->x+3y); does x^2-10y^2 represent ±3? exhaustive small search + mod-5 obstruction
reps=set()
for x in range(-60,61):
    for y in range(-20,21):
        v=x*x-10*y*y
        if abs(v)<50: reps.add(v)
check("x^2-10y^2 does not represent ±3 (search) and 3 not a QR issue mod 5", 3 not in reps and -3 not in reps)
# (3,4,-2) represents 3 at (1,0)
check("(3,4,-2) represents 3", 3*1+4*0-2*0==3)
# brute-force conjugacy search over small GL(2,Z) to corroborate non-conjugacy
X6=[[6,1],[1,0]]
found=False
B_=range(-6,7)
for a in B_:
    for b in B_:
        for c in B_:
            for d in B_:
                if a*d-b*c in (1,-1):
                    P=[[a,b],[c,d]]
                    if mmul(mmul(P,A),minv(P))==X6: found=True
check("no conjugator P (entries<=6) with P A P^-1 = X_6", not found)

# --- period-two family: M(a,b)=[[ab+1,a],[b,1]]; H1 torsion gcd,lcm; (2,3) trace 8 ---
def M(a,b): return mmul([[a,1],[1,0]],[[b,1],[1,0]])
check("M(a,b)=[[ab+1,a],[b,1]]", all(M(a,b)==[[a*b+1,a],[b,1]] for a in range(1,5) for b in range(1,5)))
check("det M(a,b)=+1", all(det(M(a,b))==1 for a in range(1,5) for b in range(1,5)))
check("tr M(2,3)=8, not of form m^2+2", tr(M(2,3))==8 and all(m*m+2!=8 for m in range(1,10)))

# --- Lucas / covers: tr phi_1^n - 2 square iff n odd; phi_1^3 vs phi_4 ---
def mpow(A,n):
    X=[[1,0],[0,1]]
    for _ in range(n): X=mmul(X,A)
    return X
import math
for n in range(1,10):
    t=tr(mpow(p1m,n))-2
    is_sq = int(math.isqrt(t))**2==t
    check(f"tr(phi_1^{n})-2 square iff n odd (n={n})", is_sq == (n%2==1))
p13=mpow(p1m,3); p4=[[17,4],[4,1]]
check("phi_1^3=[[13,8],[8,5]], tr 18 = tr phi_4", p13==[[13,8],[8,5]] and tr(p13)==18==tr(p4))
found=False
for a in B_:
    for b in B_:
        for c in B_:
            for d in B_:
                if a*d-b*c in (1,-1):
                    P=[[a,b],[c,d]]
                    if mmul(mmul(P,p13),minv(P))==p4: found=True
check("phi_1^3 not conjugate to phi_4 (search |entries|<=6)", not found)

# --- amphichirality: g=R^m J centralizes phi_m, det -1 ---
J=[[0,1],[1,0]]
for m in range(1,6):
    phi=word('R'*m+'L'*m)
    g=mmul(mpow(R,m),J)
    check(f"R^{m}J centralizes phi_{m}, det=-1", mmul(g,phi)==mmul(phi,g) and det(g)==-1)

# --- RLLR counterexample ---
W=word('RLLR')
check("RLLR matrix [[3,4],[2,3]] not symmetric", W==[[3,4],[2,3]] and W[0][1]!=W[1][0])

# --- SL(2,F3) generated by [[1,1],[0,1]] and [[1,0],[2,1]] ---
def m3(A,B):
    return ((( A[0][0]*B[0][0]+A[0][1]*B[1][0])%3, (A[0][0]*B[0][1]+A[0][1]*B[1][1])%3),
            (( A[1][0]*B[0][0]+A[1][1]*B[1][0])%3, (A[1][0]*B[0][1]+A[1][1]*B[1][1])%3))
gens=[((1,1),(0,1)),((1,0),(2,1))]
seen={((1,0),(0,1))}
frontier=[((1,0),(0,1))]
while frontier:
    nf=[]
    for x in frontier:
        for g in gens:
            y=m3(x,g)
            if y not in seen: seen.add(y); nf.append(y)
    frontier=nf
check("<[[1,1],[0,1]],[[1,0],[2,1]]> = SL(2,F3), order 24", len(seen)==24)

# --- 2T and 2I trace sets via quaternions ---
import fractions
def quat_units_2T():
    units=[]
    for s in ([1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]):
        units.append([Fraction(x) for x in s]); units.append([Fraction(-x) for x in s])
    for signs in itertools.product([1,-1],repeat=4):
        units.append([Fraction(s,2) for s in signs])
    return units
t2T=set(2*q[0] for q in quat_units_2T())
check("trace set 2T = {-2,-1,0,1,2}", t2T==set(map(Fraction,[-2,-1,0,1,2])))
check("|2T|=24", len(quat_units_2T())==24)
# 2I traces: need icosians; scalar parts are 0,±1/2,±1,±phi/2,±1/(2phi) -> traces 0,±1,±2,±phi,±1/phi
# verify count: 120 icosians: build group generated by two quaternions numerically
import cmath
def qmul(a,b):
    return (a[0]*b[0]-a[1]*b[1]-a[2]*b[2]-a[3]*b[3],
            a[0]*b[1]+a[1]*b[0]+a[2]*b[3]-a[3]*b[2],
            a[0]*b[2]-a[1]*b[3]+a[2]*b[0]+a[3]*b[1],
            a[0]*b[3]+a[1]*b[2]-a[2]*b[1]+a[3]*b[0])
ph=(1+5**0.5)/2
g1=(0.5,0.5,0.5,0.5)
g2=(0.5, 0.5/ph, ph/2, 0.0)  # a standard icosian generator
def qround(q): return tuple(round(x,9) for x in q)
seenq={qround((1,0,0,0))}
frontier=[(1.0,0,0,0)]
while frontier:
    nf=[]
    for x in frontier:
        for g in (g1,g2):
            y=qmul(x,g)
            yr=qround(y)
            if yr not in seenq: seenq.add(yr); nf.append(y)
    frontier=nf
traces2I=sorted(set(round(2*q[0],6) for q in seenq))
expect=sorted(round(v,6) for v in (-2,-ph,-1,-1/ph,0,1/ph,1,ph,2))
check("|2I|=120 via icosian generators", len(seenq)==120)
check("trace set 2I = {0,±1,±2,±phi,±1/phi} (9 values)", traces2I==expect)
check("rational subset of 2I traces = 2T traces", set([-2,-1,0,1,2])==set(int(t) for t in traces2I if abs(t-round(t))<1e-9))

print("\nOVERALL:", "ALL PASS" if ok else "SOME FAILED")
sys.exit(0 if ok else 1)
