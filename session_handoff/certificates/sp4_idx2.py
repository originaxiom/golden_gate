#!/usr/bin/env python3
"""SP-4: the index-2 element of the E8 four-slot stabilizer, identified.

Memo 19: Stab_ordered = 2592 = 2 x |W(A2)^4|. Which per-slot outer pattern does the
extra Z2 realize?  Method: BFS over the ordered-configuration orbit with parent
tracking; each non-tree edge gives a Schreier generator of the stabilizer
(word(t)^-1 g word(s)); test each against W(A2)^4 membership per slot (the slot's
inner Weyl = 6 permutations from its two simple reflections); the first Schreier
element outside gives the outer pattern (which slots are flipped).
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
def find_a2(pool):
    for r1 in pool:
        for r2 in pool:
            if r2!=r1 and ipr(r1,r2)==-1 and tuple(x+y for x,y in zip(r1,r2)) in pool:
                return r1,r2
slot_bases=[find_a2(S) for S in slots]
slot_idx=[sorted(IDX[r] for r in S) for S in slots]
masks=[]
for S in slots:
    m=0
    for r in S: m|=1<<IDX[r]
    masks.append(m)
simple=[tuple(1 if k==i else 0 for k in range(n)) for i in range(n)]
gens=[]
for i in range(n):
    ai=simple[i]
    gens.append(tuple(IDX[tuple(r[k]-ipr(r,ai)*ai[k] for k in range(n))] for r in allr))
nR=len(allr)
def apply_mask(perm,m):
    out=0
    while m:
        b=m & -m
        out|=1<<perm[b.bit_length()-1]
        m^=b
    return out
def compose(p,q): return tuple(p[q[i]] for i in range(nR))
ident=tuple(range(nR))
def invperm(p):
    out=[0]*nR
    for i,v in enumerate(p): out[v]=i
    return tuple(out)
# inner Weyl of each slot: 6 permutations of its 6 root indices
def slot_weyl(si):
    r1,r2=slot_bases[si]
    def refl(a):
        return {IDX[r]: IDX[tuple(r[k]-ipr(r,a)*a[k] for k in range(n))] for r in slots[si]}
    g1,g2=refl(r1),refl(r2)
    idm={i:i for i in slot_idx[si]}
    seen={tuple(sorted(idm.items()))}; frontier=[idm]; out=[idm]
    while frontier:
        nf=[]
        for p in frontier:
            for gg in (g1,g2):
                q={i: gg[p[i]] for i in p}
                k=tuple(sorted(q.items()))
                if k not in seen: seen.add(k); nf.append(q); out.append(q)
        frontier=nf
    return [dict(t) for t in (tuple(sorted(o.items())) for o in out)]
SW=[slot_weyl(si) for si in range(4)]
assert all(len(s)==6 for s in SW)
def outer_pattern(perm):
    """for a permutation stabilizing every slot setwise: per slot, inner (in W(A2)) or outer"""
    pat=[]
    for si in range(4):
        act={i: perm[i] for i in slot_idx[si]}
        pat.append('I' if any(all(w[i]==act[i] for i in slot_idx[si]) for w in SW[si]) else 'O')
    return ''.join(pat)
# BFS with parents
start=tuple(masks)
parent={start:None}
frontier=[start]
schreier_found=[]
while frontier and len(schreier_found)<40:
    nf=[]
    for st in frontier:
        for gi,perm in enumerate(gens):
            ns=tuple(apply_mask(perm,m) for m in st)
            if ns not in parent:
                parent[ns]=(st,gi); nf.append(ns)
            elif len(schreier_found)<40:
                schreier_found.append((st,gi,ns))
    frontier=nf
print(f"orbit states: {len(parent)}")
def word_perm(st):
    p=ident
    while parent[st] is not None:
        prev,gi=parent[st]
        p=compose(gens[gi],p)
        st=prev
    return p
patterns={}
checked=0
for st,gi,ns in schreier_found:
    ws=word_perm(st); wt=word_perm(ns)
    el=compose(invperm(wt), compose(gens[gi], ws))
    # el stabilizes the ordered config
    if tuple(apply_mask(el,m) for m in masks)!=start: continue
    checked+=1
    pat=outer_pattern(el)
    patterns[pat]=patterns.get(pat,0)+1
print(f"Schreier stabilizer elements checked: {checked}")
print("per-slot inner(I)/outer(O) patterns found:", patterns)
nontriv=[p for p in patterns if 'O' in p]
print("VERDICT: the index-2 extension acts with pattern(s):", nontriv if nontriv else
      "none found among sampled Schreier gens (all inner) — sample more")
