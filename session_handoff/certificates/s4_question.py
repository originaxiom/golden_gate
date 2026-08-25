#!/usr/bin/env python3
"""THE S4 QUESTION — which permutations of the four A2 slots does W(E8) realize?

Method: BFS over the W(E8)-orbit of the ORDERED 4-tuple of slot root-sets
(bitmask-encoded over the 240 roots). The orbit is the coset space W/Stab_ordered —
far smaller than W itself. A permutation pi is realized iff the pi-permuted initial
tuple lies in the orbit. Also yields |Stab| and the normalizer structure.
"""
import itertools
exec(open(__import__('os').path.dirname(__import__('os').path.abspath(__file__))+'/e7_ladder.py').read().split("CART={")[0])
CART_E8=[[2,-1,0,0,0,0,0,0],[-1,2,-1,0,0,0,0,0],[0,-1,2,-1,0,0,0,-1],[0,0,-1,2,-1,0,0,0],[0,0,0,-1,2,-1,0,0],[0,0,0,0,-1,2,-1,0],[0,0,0,0,0,-1,2,0],[0,0,-1,0,0,0,0,2]]
alg=build_algebra(CART_E8)
ipr=alg['ipr']; allr=alg['roots']; n=alg['n']
IDX={r:i for i,r in enumerate(allr)}
S0,S1,S2,T1,T2,color=slots_and_triples(alg)
perp3=[r for r in allr if all(ipr(r,s)==0 for s in S0|S1|S2)]
S3=set(perp3)
slots=[S0,S1,S2,S3]
masks=[]
for S in slots:
    m=0
    for r in S: m|=1<<IDX[r]
    masks.append(m)
# simple reflections as index permutations
simple=[tuple(1 if k==i else 0 for k in range(n)) for i in range(n)]
gens=[]
for i in range(n):
    ai=simple[i]
    perm=[IDX[tuple(r[k]-ipr(r,ai)*ai[k] for k in range(n))] for r in allr]
    gens.append(perm)
def apply_mask(perm,m):
    out=0
    while m:
        b=m & -m
        out|=1<<perm[b.bit_length()-1]
        m^=b
    return out
start=tuple(masks)
seen={start}; frontier=[start]
cnt=0
while frontier:
    nf=[]
    for st in frontier:
        for perm in gens:
            ns=tuple(apply_mask(perm,m) for m in st)
            if ns not in seen:
                seen.add(ns); nf.append(ns)
    frontier=nf; cnt+=1
    if cnt%5==0: print(f"  BFS depth {cnt}: {len(seen)} states")
orbit=len(seen)
print(f"orbit of the ordered 4-slot configuration: {orbit} states")
WE8=696729600
assert WE8%orbit==0
stab=WE8//orbit
print(f"|Stab_ordered| = |W(E8)|/orbit = {stab}  (contains W(A2)^4 = 1296: index {stab//1296 if stab%1296==0 else 'non-integer!'})")
realized=[]
for pi in itertools.permutations(range(4)):
    if tuple(start[pi[i]] for i in range(4)) in seen: realized.append(pi)
print(f"permutations of the four slots realized by W(E8): {len(realized)} of 24")
for pi in realized: print("   ",pi)
# group structure
ids=len(realized)
print("=> realized group order", ids, "-",
      {24:"the FULL S4",12:"A4",8:"D4",6:"S3",4:"Klein or C4",3:"C3",2:"C2",1:"trivial"}.get(ids,"?"))
