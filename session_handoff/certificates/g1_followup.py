import importlib.util, itertools
exec(open(__import__('os').path.dirname(__import__('os').path.abspath(__file__))+'/g1_yselect.py').read().split("solset=set(sols)")[0])
solset=set(sols)
P=lambda y:(y[3],y[2],y[1],y[0])
rows=[]
for g in FP:
    has_gauge=False
    for c in solve_lift(g):
        if slot_sig(g,c,sorted(S0),(a0,a2))!=(0,8): continue
        if slot_sig(g,c,sorted(G1c),p1)==(4,4) and slot_sig(g,c,sorted(G2c),p2)==(4,4):
            has_gauge=True; break
    if not has_gauge: continue
    M4=cartan_mat4(g)
    anti=frozenset(y for y in sols if tuple(-x for x in y)==tuple(sum(M4[i,j]*y[j] for j in range(4)) for i in range(4)))
    coset="W" if g in seen else "dW"
    rows.append((coset,anti))
print("gauge involutions:",len(rows),"cosets:",{c for c,_ in rows})
pairs=set()
for coset,anti in rows:
    pc = all(P(y) in anti for y in anti)
    print(f"  |sel|={len(anti):2d}  P-closed={pc}  coset={coset}")
    if len(anti)==2: pairs.add(anti)
print("distinct 2-selections among the generic closings:", len(pairs))
allpairs={frozenset({y,P(y)}) for y in sols if P(y)!=y}
print("total mirror pairs among the 18:", len(allpairs))
print("generic selections that are exactly mirror pairs:", sum(1 for s in pairs if s in allpairs))
