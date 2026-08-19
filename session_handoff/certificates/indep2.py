#!/usr/bin/env python3
"""Independent referee checks, part 2: E6 root system / Levi claims + rung spectrum from scratch."""
import itertools, sys
from fractions import Fraction

ok=True
def check(name,cond):
    global ok
    print(("PASS " if cond else "FAIL ")+name)
    if not cond: ok=False

# Build E6 root system from Cartan matrix (Bourbaki), roots as integer vectors in simple-root basis.
C=[[2,0,-1,0,0,0],
   [0,2,0,-1,0,0],
   [-1,0,2,-1,0,0],
   [0,-1,-1,2,-1,0],
   [0,0,0,-1,2,-1],
   [0,0,0,0,-1,2]]
# closure under simple reflections
simple=[tuple(1 if i==j else 0 for j in range(6)) for i in range(6)]
def refl(i,root):
    # s_i(a) = a - <a, alpha_i^v> alpha_i ; <a,alpha_i^v> = sum_j a_j C[j][i]  (simply-laced, symmetric C)
    c=sum(root[j]*C[j][i] for j in range(6))
    r=list(root); r[i]-=c
    return tuple(r)
roots=set(simple)
frontier=list(simple)
while frontier:
    nf=[]
    for r in frontier:
        for i in range(6):
            s=refl(i,r)
            if s not in roots: roots.add(s); nf.append(s)
    frontier=nf
roots|={tuple(-x for x in r) for r in roots}
roots=set(roots)
check("E6 has 72 roots", len(roots)==72)

# Levi subsystems: for each subset S of simple roots, roots in span(S)
counts={}
from itertools import combinations
def in_span(r,S):
    return all(r[i]==0 for i in range(6) if i not in S)
levi_counts=set()
count_types={}
for k in range(7):
    for S in combinations(range(6),k):
        n=sum(1 for r in roots if in_span(r,S))
        levi_counts.add(n)
        count_types.setdefault(n,set()).add(frozenset(S))
check("Levi root counts = {0,2,4,6,8,10,12,14,20,22,24,30,40,72}",
      levi_counts=={0,2,4,6,8,10,12,14,20,22,24,30,40,72})
dims=sorted(6+n for n in levi_counts)
check("ambient Levi dims = 6,8,10,12,14,16,18,20,26,28,30,36,46,78",
      dims==[6,8,10,12,14,16,18,20,26,28,30,36,46,78])
check("no Levi root count 16,18,26,28,32..38 (so dims 22,24,32,34,38-44 impossible)",
      all(n not in levi_counts for n in [16,18,26,28,32,34,36,38]))

# Determine type multiset at counts 8,20,24,40 (uniqueness) and 6,12,14 (ambiguity):
# classify subsystem type by decomposition of the subdiagram
def diagram_type(S):
    # connected components of induced subgraph, each a simply-laced diagram; classify by size+branch
    S=set(S); comps=[]
    seen=set()
    adj={i:[j for j in range(6) if j!=i and C[i][j]==-1] for i in range(6)}
    for i in S:
        if i in seen: continue
        comp={i}; fr=[i]
        while fr:
            nf=[]
            for x in fr:
                for y in adj[x]:
                    if y in S and y not in comp: comp.add(y); nf.append(y)
            fr=nf
        seen|=comp
        # type: A_n if path; D_n if one degree-3 node
        degs=sorted(sum(1 for y in adj[x] if y in comp) for x in comp)
        n=len(comp)
        if not degs or degs[-1]<=2: t=f"A{n}"
        else: t=f"D{n}" if n>=4 else "?"
        comps.append((t,n))
    return tuple(sorted(c[0] for c in comps))
types_at={}
for k in range(7):
    for S in combinations(range(6),k):
        n=sum(1 for r in roots if in_span(r,S))
        types_at.setdefault(n,set()).add(diagram_type(S))
check("8 roots -> unique type A2+A1", types_at[8]=={("A1","A2")})
check("20 roots -> unique type A4", types_at[20]=={("A4",)})
check("24 roots -> unique type D4", types_at[24]=={("D4",)})
check("40 roots -> unique type D5", types_at[40]=={("D5",)})
check("30 roots -> unique type A5", types_at[30]=={("A5",)})
check("22 roots -> unique type A4+A1", types_at[22]=={("A1","A4")})
check("6 roots ambiguous: A2 and 3A1", types_at[6]=={("A2",),("A1","A1","A1")})
check("12 roots ambiguous: A3 and 2A2", types_at[12]=={("A3",),("A2","A2")})
check("14 roots ambiguous: A3+A1 and 2A2+A1", types_at[14]=={("A1","A3"),("A1","A2","A2")})

# ---- Independent rung spectrum: pick the standard A2 subsystem {alpha_5,alpha_6} (any A2, all conjugate);
# C := annihilator of that A2 in the (dual) Cartan = vectors v (weights act linearly); model:
# weights of C on e6 are the 72 roots restricted to a 4-dim subspace V = {h : alpha_5(h)=alpha_6(h)=0}.
# Use coweight coordinates: represent h in R^6 with alpha_i(h) = sum_j C[i][j] h_j? Simpler: work in root
# space with the standard inner product B(a,b) = a^T C b /? For simply-laced take Gram = C (Cartan matrix
# symmetric here). alpha(h)=<alpha,h> with Gram C.
# V = {v in Q^6 : <alpha_5,v>=<alpha_6,v>=0}. Restriction of root r to V is the functional <r,.>|_V.
# Two roots have proportional restriction iff r1 - c r2 in span(alpha_5,alpha_6) for scalar c (check c=±1 etc.)
import numpy as np
Cm=np.array(C,dtype=float)
rootsl=sorted(roots)
# basis of V: solve <alpha_i, v>=0 for i in {4,5} (0-indexed 4,5 = alpha_5,alpha_6)
A2idx=[4,5]
M=np.array([Cm[i] for i in A2idx])
# nullspace
from numpy.linalg import svd
u,s,vt=svd(M)
ns=vt[len(s)- (M.shape[1]-np.linalg.matrix_rank(M)):]  # rows spanning nullspace
V=vt[np.linalg.matrix_rank(M):]  # 4 x 6
check("annihilator V of A2 is 4-dimensional", V.shape[0]==4)
# restriction of each root: vector of pairings with V basis
restr={}
zero_ct=0
vecs=[]
for r in rootsl:
    rv=np.array(r,dtype=float)
    w=V@ (Cm@rv)
    if np.allclose(w,0,atol=1e-9): zero_ct+=1
    else: vecs.append((r,w))
check("exactly 6 roots vanish on C (the A2)", zero_ct==6)
# proportionality classes
classes=[]
for r,w in vecs:
    placed=False
    for cl in classes:
        w0=cl[0][1]
        # proportional?
        cross=np.outer(w,w0)
        if np.linalg.matrix_rank(np.vstack([w,w0]),tol=1e-7)==1:
            cl.append((r,w)); placed=True; break
    if not placed: classes.append([(r,w)])
sizes=sorted(len(c) for c in classes)
# weights come in ± pairs; distinct weights = lines counted twice? paper: 30 distinct weights, 12 mult 1, 18 mult 3.
# each ± pair of weights gives same hyperplane; "30 distinct weights with mult 12x1+18x3" counts signed weights:
# so proportionality LINES here = 15, each line containing +w and -w classes.
# count signed-weight multiplicities:
from collections import Counter
sw=Counter()
for r,w in vecs:
    key=tuple(round(x,7) for x in w)
    sw[key]+=1
mults=sorted(sw.values())
check("30 distinct nonzero weights: 12 of mult 1, 18 of mult 3", len(sw)==30 and mults==[1]*12+[3]*18)
check("66 nonzero-restriction roots", sum(sw.values())==66)

# flats of the arrangement of the 30 (15 up to sign) hyperplanes in V* (4-dim):
# enumerate intersections of normal-span subspaces; value dim z(S) = 12 + sum of mults of weights vanishing on S.
# For every subspace S of V arising as a flat of the dual arrangement: equivalently, for each subset of the
# 15 lines W_i (weight lines), the set of S on which exactly those vanish. dim z depends on which weights vanish
# on S; possible "vanishing sets" = for subspace S, {i : W_i(S)=0} = weights in S^perp... The attained values:
# choose any subspace T of span of weight-lines (in V*, dim 4); vanishing weights = weight lines contained in T^0...
# Simpler: enumerate flats of the hyperplane arrangement in V (dim 4): intersections of the 15 hyperplanes ker(w_i).
# For a point p in a flat F (generic in F), dim z(p-span... ) -- but S ranges over subspaces of C, and
# z(S) determined by weights vanishing on all of S. For S = generic subspace of flat... Let's directly enumerate:
# every subset of the 15 weight-lines determines subspace S = intersection of their kernels; the weights vanishing
# on S = lines whose kernel contains S. Enumerate over all 2^15 subsets (32768) using exact fractions.
from fractions import Fraction as F
def exact_nullspace(rows):
    # rows: list of tuples over Fraction, in 4 vars; return basis of nullspace
    import copy
    m=[list(r) for r in rows]; n=4
    # gaussian elimination
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
        if r0==len(m): break
    free=[c for c in range(n) if c not in piv]
    basis=[]
    for fc in free:
        v=[F(0)]*n; v[fc]=F(1)
        for i,c in enumerate(piv):
            v[c]=-m[i][fc]
        basis.append(v)
    return basis
# exact weight vectors: recompute V basis exactly.
# Solve <alpha_5,v>=<alpha_6,v>=0 over Q: rows of Cm[4],Cm[5]
rows=[tuple(F(int(x)) for x in C[4]),tuple(F(int(x)) for x in C[5])]
# nullspace in 6 vars:
def exact_nullspace6(rows):
    m=[list(r) for r in rows]; n=6
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
Vb=exact_nullspace6(rows)  # 4 vectors in Q^6
check("exact V basis dim 4", len(Vb)==4)
# weight of root r on V-coords: w_j = <r, Vb_j> with Gram C
def pair(r,v):
    return sum(F(int(r[i]))*sum(F(int(C[i][j]))*v[j] for j in range(6)) for i in range(6))
wexact={}
for r in rootsl:
    w=tuple(pair(r,v) for v in Vb)
    wexact.setdefault(w,0)
    wexact[w]+=1
wnz=[(w,m_) for w,m_ in wexact.items() if any(x!=0 for x in w)]
check("exact: 30 nonzero weights", len(wnz)==30)
# 15 lines up to sign
lines={}
def normal(w):
    # scale to primitive with first nonzero positive
    from math import gcd
    dens=[x.denominator for x in w]
    l=1
    for d in dens:
        l=l*d//gcd(l,d)
    iv=[int(x*l) for x in w]
    g=0
    for x in iv: g=gcd(g,abs(x))
    iv=[x//g for x in iv]
    for x in iv:
        if x!=0:
            if x<0: iv=[-y for y in iv]
            break
    return tuple(iv)
linemult={}
for w,m_ in wnz:
    key=normal(w)
    linemult[key]=linemult.get(key,0)+m_
check("15 weight lines; multiplicities sum 66", len(linemult)==15 and sum(linemult.values())==66)
linelist=list(linemult.items())
vals=set()
seen_flats=set()
flats=set()
for mask in range(1<<15):
    sel=[linelist[i][0] for i in range(15) if mask>>i&1]
    if sel:
        B=exact_nullspace([tuple(F(x) for x in s) for s in sel])
    else:
        B=[[F(1) if i==j else F(0) for i in range(4)] for j in range(4)]
    # S = nullspace; which lines vanish on S: line w vanishes on S iff w.b=0 for all b in B
    van=[]
    tot=0
    for w,m_ in linelist:
        if all(sum(F(x)*b[i] for i,x in enumerate(w))==0 for b in B):
            van.append(w); tot+=m_
    flats.add((tuple(sorted(van)),len(B)))
    vals.add(12+tot)
check("attained dim z values = {12,14,16,18,20,26,28,30,36,46,78}",
      vals=={12,14,16,18,20,26,28,30,36,46,78})
print("number of distinct flats (vanishing-set,dim):",len(flats))
print("\nOVERALL:","ALL PASS" if ok else "SOME FAILED")
sys.exit(0 if ok else 1)
