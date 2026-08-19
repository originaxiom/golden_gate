#!/usr/bin/env python3
"""Independent check of Theorem smtfull's combinatorics from the rational weight arrangement:
at a wall (dim z = 46) point x1, the nonzero weights vanishing on x1 fall into 7 lines of
multiplicities (1,1,3,3,3,3,3) [root counts (2,2,6,6,6,6,6)], and the induced stratification of
2-planes through x1 gives dim z values {46,30,14,18,16,20,26,12} with two 30-points, four
26-points, six triple points + three double points, and no value 24."""
import sys
from fractions import Fraction as F
from itertools import combinations

# rebuild E6 roots and the A2-perp model (as indep2)
C=[[2,0,-1,0,0,0],[0,2,0,-1,0,0],[-1,0,2,-1,0,0],[0,-1,-1,2,-1,0],[0,0,0,-1,2,-1],[0,0,0,0,-1,2]]
simple=[tuple(1 if i==j else 0 for j in range(6)) for i in range(6)]
def refl(i,root):
    c=sum(root[j]*C[j][i] for j in range(6))
    r=list(root); r[i]-=c
    return tuple(r)
roots=set(simple); frontier=list(simple)
while frontier:
    nf=[]
    for r in frontier:
        for i in range(6):
            s=refl(i,r)
            if s not in roots: roots.add(s); nf.append(s)
    frontier=nf
roots|={tuple(-x for x in r) for r in roots}
assert len(roots)==72

def nullspace(rows,n):
    m=[list(r) for r in rows]
    piv=[]; r0=0
    for c in range(n):
        pr=None
        for r in range(r0,len(m)):
            if m[r][c]!=0: pr=r; break
        if pr is None: continue
        m[r0],m[pr]=m[pr],m[r0]
        inv=F(1)/m[r0][c]
        m[r0]=[x*inv for x in m[r0]]
        for r in range(len(m)):
            if r!=r0 and m[r][c]!=0:
                f=m[r][c]; m[r]=[a-f*b for a,b in zip(m[r],m[r0])]
        piv.append(c); r0+=1
    free=[c for c in range(n) if c not in piv]
    basis=[]
    for fc in free:
        v=[F(0)]*n; v[fc]=F(1)
        for i,c in enumerate(piv):
            v[c]=-m[i][fc]
        basis.append(v)
    return basis

rows=[tuple(F(x) for x in C[4]),tuple(F(x) for x in C[5])]
Vb=nullspace(rows,6)  # 4-dim annihilator of the A2 {a5,a6}
def pair(r,v):
    return sum(F(r[i])*sum(F(C[i][j])*v[j] for j in range(6)) for i in range(6))
from math import gcd
def normal(w):
    l=1
    for xq in w: l=l*xq.denominator//gcd(l,xq.denominator)
    iv=[int(xq*l) for xq in w]
    g=0
    for xq in iv: g=gcd(g,abs(xq))
    iv=[xq//g for xq in iv]
    for xq in iv:
        if xq!=0:
            if xq<0: iv=[-y for y in iv]
            break
    return tuple(iv)
linemult={}
for r in sorted(roots):
    w=tuple(pair(r,v) for v in Vb)
    if any(x!=0 for x in w):
        key=normal(w)
        linemult[key]=linemult.get(key,0)+1  # counts ROOTS on the line (2m per line)
lines=list(linemult.items())
assert len(lines)==15 and sum(m for _,m in lines)==66

# find 1-dim flats with value 46: subspaces S (dim1) = intersections of kernels; value=12+sum mult of lines vanishing on S
# 1-dim flats: intersect kernels of subsets of lines; enumerate pairs/triples of lines whose kernels meet in dim 1... simpler:
# candidate directions: nullspace of any 3 independent line-normals.
cands={}
for T in combinations(range(15),3):
    B=nullspace([tuple(F(x) for x in lines[i][0]) for i in T],4)
    if len(B)==1:
        v=tuple(B[0])
        key=normal(list(v))
        if key not in cands:
            tot=sum(m for w,m in lines if sum(F(a)*b for a,b in zip(w,B[0]))==0)
            cands[key]=tot
walls=[k for k,tot in cands.items() if 12+tot==46]
print("1-dim flats with dim z=46 found:",len(walls))
vals_at_dirs=sorted(set(12+t for t in cands.values()))
print("values at 1-dim flats:",vals_at_dirs)
ok=True
def check(name,cond):
    global ok
    print(("PASS " if cond else "FAIL ")+name)
    if not cond: ok=False
check("some 46-walls exist", len(walls)>0)

x1=[F(v) for v in walls[0]]
van=[(w,m) for w,m in lines if sum(F(a)*b for a,b in zip(w,x1))==0]
sizes=sorted(m for w,m in van)
print("lines vanishing at wall:",len(van),"root-count sizes:",sizes)
check("7 lines vanish at the wall with root counts (2,2,6,6,6,6,6)", sizes==[2,2,6,6,6,6,6])
check("34 roots vanish at wall beyond the 6 identically-zero ones", sum(sizes)==34)

# stratify 2-planes through x1: a 2-plane P=span(x1,y); lines vanishing on P = subset of `van` whose kernel contains y too.
# The 7 lines restrict to lines in the quotient P(C/<x1>) ~ P^2. Compute their normals in a complement basis.
# choose complement basis of x1 in C-coords (4-dim space with coordinates in Vb basis)
# find intersection pattern of the 7 lines in P^2:
# each line i: functional w_i on 4-space, w_i(x1)=0 -> descends to C/<x1> (3-dim) -> line in P^2.
# points of interest: intersections of pairs of the 7 lines; classify multiplicities.
import itertools as it
def solve2(wa,wb):
    # nullspace of {wa,wb,dual-of-x1?} : direction y (mod x1) with wa(y)=wb(y)=0: 2-dim nullspace containing x1; pick vector indep of x1
    B=nullspace([tuple(F(x) for x in wa),tuple(F(x) for x in wb)],4)
    # B has dim 2 (containing x1); pick element not proportional to x1
    for b in B:
        # check independence with x1
        M=[[b[i] for i in range(4)],[x1[i] for i in range(4)]]
        # rank 2?
        rank2=False
        for i,j in it.combinations(range(4),2):
            if M[0][i]*M[1][j]-M[0][j]*M[1][i]!=0: rank2=True
        if rank2: return b
    # if all proportional to x1, lines coincide in quotient
    return None
pts={}
for i,j in it.combinations(range(7),2):
    y=solve2(van[i][0],van[j][0])
    if y is None: continue
    # normalize point mod x1: canonical rep: reduce y modulo x1? use normal of the 2-plane's Pluecker... simpler: the point in P^2
    # canonicalize by finding which of the 7 lines pass through span(x1,y)
    thru=frozenset(k for k in range(7) if sum(F(a)*b for a,b in zip(van[k][0],y))==0)
    pts.setdefault(thru,None)
patterns=sorted(pts.keys(), key=len)
triples=[p for p in patterns if len(p)==3]
doubles=[p for p in patterns if len(p)==2]
# remove doubles contained in triples? a pair meeting inside a triple point yields the triple pattern directly, so 'doubles' are genuine
print("intersection patterns: triples:",len(triples),"doubles:",len(doubles), "higher:",[len(p) for p in patterns if len(p)>3])
check("six triple points and three double points, none higher", len(triples)==6 and len(doubles)==3 and not any(len(p)>3 for p in patterns))
# values: at a point with pattern p: dim z = 12 + sum root-counts of lines in p
vals={}
for p in patterns:
    v=12+sum(van[k][1] for k in p)
    vals.setdefault(v,0); vals[v]+=1
print("values at intersection points:",vals)
# generic point of a size-2 line: 14; size-6 line: 18; off lines: 12
allvals=set(vals)|{14,18,12,46}
check("no stratum value 24", 24 not in allvals)
check("two 30-points", vals.get(30,0)==2)
check("four 26-points", vals.get(26,0)==4)
check("one 16-point (the double of the two size-2 lines)", vals.get(16,0)==1)
check("two 20-points (size-2 meets size-6 doubles)", vals.get(20,0)==2)
print("full stratification values:",sorted(allvals))
check("stratification values = {12,14,16,18,20,26,30,46}", sorted(allvals)==[12,14,16,18,20,26,30,46])
# 30-points are meetings of three size-6 lines; check pattern root counts
for p in patterns:
    if 12+sum(van[k][1] for k in p)==30:
        check("30-point = triple of size-6 lines", sorted(van[k][1] for k in p)==[6,6,6])
    if 12+sum(van[k][1] for k in p)==26:
        check("26-point = size-2 + two size-6", sorted(van[k][1] for k in p)==[2,6,6])
print("\nOVERALL:","ALL PASS" if ok else "SOME FAILED")
sys.exit(0 if ok else 1)
