import importlib.util, itertools
exec(open('g1_yselect.py').read().split("solset=set(sols)")[0])
solset=set(sols)
import sympy as sp
# W(S1)xW(S2) = order 36 on cor-coords (recovered B1102 machinery)
def refl_matrix(ridx):
    Mm=sp.eye(4)
    for j in range(4):
        Mm[ridx,j]=Mm[ridx,j]-iprr(cor[ridx],cor[j])
    return Mm
gensW=[refl_matrix(k) for k in range(4)]
seenW={tuple(sp.eye(4)):sp.eye(4)}; frontier=[sp.eye(4)]
while frontier:
    nf=[]
    for X in frontier:
        for g in gensW:
            Y=g*X; k2=tuple(Y)
            if k2 not in seenW: seenW[k2]=Y; nf.append(Y)
    frontier=nf
assert len(seenW)==36
def act(Mm,y): return tuple(sum(Mm[i,j]*y[j] for j in range(4)) for i in range(4))
orbits=[]; left=set(sols)
while left:
    y0=next(iter(left))
    orb={act(Mm,y0) for Mm in seenW.values()} & solset
    orbits.append(orb); left-=orb
assert sorted(len(o) for o in orbits)==[9,9]
O1,O2=orbits
sels=[]
for g in FP:
    ok=False
    for c in solve_lift(g):
        if slot_sig(g,c,sorted(S0),(a0,a2))!=(0,8): continue
        if slot_sig(g,c,sorted(G1c),p1)==(4,4) and slot_sig(g,c,sorted(G2c),p2)==(4,4):
            ok=True; break
    if not ok: continue
    M4=cartan_mat4(g)
    anti=frozenset(y for y in sols if tuple(-x for x in y)==tuple(sum(M4[i,j]*y[j] for j in range(4)) for i in range(4)))
    if len(anti)==2: sels.append(anti)
print("generic pairs:",len(sels))
for s in sels:
    a,b=sorted(s)
    print(f"  pair straddles orbits: {(a in O1) != (b in O1)}   members-orbit: ({'O1' if a in O1 else 'O2'},{'O1' if b in O1 else 'O2'})")
un=set().union(*sels)
print("union of the 9 pairs covers:", len(un), "of 18; pairwise disjoint:", sum(len(s) for s in sels)==len(un))
