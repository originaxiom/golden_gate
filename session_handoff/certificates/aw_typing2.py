# type ALL subgroup orders arising from transversal pairs (8, 16, 24, 96)
exec(open(__import__('os').path.dirname(__import__('os').path.abspath(__file__))+"/aw_typing.py").read().split("for si,Sg in enumerate")[0])
from collections import Counter
allsubs={}
for p in trans:
    Sg=gen_sub(p)
    allsubs.setdefault(len(Sg), set()).add(Sg)
for size in sorted(allsubs):
    fam=allsubs[size]
    print(f"\norder {size}: {len(fam)} distinct subgroups from transversal pairs")
    for si,Sg in enumerate(sorted(fam, key=lambda s: sorted(s))):
        hist=Counter(orders[i] for i in Sg)
        left=all(is_left_quat(G[i]) for i in Sg)
        fdH=fixdim([i for i in Sg if i!=ident])
        ninv=hist.get(2,0)
        # SU(2)-compatible iff at most one involution
        su2ok = ninv<=1
        print(f"  #{si+1}: orders {dict(sorted(hist.items()))}  involutions {ninv}  "
              f"left-quat(SU2): {left}  SU2-possible: {su2ok}  fixed-dim {fdH}")
