#!/usr/bin/env python3
"""Countersigning the banking seat's origin-torsor claim, independently.
 T1. The four Fibonacci rules are one orbit of the Klein group acting by
     reversal-conjugation (R) and swap-conjugation (S); action free and
     transitive (no stabilizer): a K4-torsor, exactly.
 T2. All four rules generate the SAME hull language up to swap-relabelling
     (one object, four basepoints).
 T3. det M = -1 for the single tick; M^2 = [[2,1],[1,1]] = the figure-eight
     monodromy RL exactly: the object is built on the DOUBLE tick, the
     orientation-restoring one.  (Literature-standard corollary, cited not
     re-derived: the single-tick mapping torus is the GIESEKING manifold,
     non-orientable, whose orientation double cover is m004.)
 T4. The tick-arrow is NOT one of the torsor's bits: reversal/swap conjugation
     maps forward-rules to forward-rules; no K4 element inverts sigma. The
     arrow is the monoid non-surjectivity (heartbeat.py C2b), not a menu item.
"""
import itertools, sys
ok = True
def check(name, cond):
    global ok
    print(("PASS " if cond else "FAIL ") + name); ok = ok and cond

# a rule = dict on {'a','b'}. Base rule sigma: a->ab, b->a.
base = {'a':'ab','b':'a'}
def rev_conj(r):   # R . r . R  (reversal is an involution)
    return {x: r[x][::-1] for x in r}
def swap_word(w): return w.translate(str.maketrans('ab','ba'))
def swap_conj(r):  # S . r . S
    return {swap_word(x): swap_word(r[x]) for x in r}

ops = {'e': lambda r: r, 'R': rev_conj, 'S': swap_conj,
       'RS': lambda r: rev_conj(swap_conj(r))}
orbit = {k: ops[k](base) for k in ops}
def key(r): return (r['a'], r['b'])
# T1a: four distinct rules; T1b: expected menu; T1c: K4 relations; T1d: free
expected = {('ab','a'), ('ba','a'), ('b','ba'), ('b','ab')}
check("T1a: orbit has exactly 4 distinct rules", len({key(r) for r in orbit.values()}) == 4)
check("T1b: orbit = {a->ab, a->ba, b->ba, b->ab} (each with the short image on the other letter)",
      {key(r) for r in orbit.values()} == expected)
check("T1c: R and S commute and are involutions on the orbit (K4 structure)",
      key(rev_conj(rev_conj(base))) == key(base) and key(swap_conj(swap_conj(base))) == key(base)
      and key(rev_conj(swap_conj(base))) == key(swap_conj(rev_conj(base))))
check("T1d: action FREE — no nonidentity element fixes any rule (torsor, no stabilizer)",
      all(key(ops[g](orbit[h])) != key(orbit[h]) for g in ('R','S','RS') for h in orbit))

# T2: same language up to relabelling. Iterate each rule from its own growing letter.
def fixw(rule, n):
    seed = 'a' if rule['a'].startswith('a') else ('b' if rule['b'].startswith('b') else None)
    if seed is None:  # rule has no prefix-stable letter: iterate its square
        r2 = {x: ''.join(rule[c] for c in rule[x]) for x in rule}
        return fixw(r2, n)
    w = seed
    while len(w) < n: w = ''.join(rule[c] for c in w)
    return w[:n]
def factors(w, L): return {w[i:i+L] for i in range(len(w)-L+1)}
W = {k: fixw(orbit[k], 3000) for k in orbit}
lang_ok = True
for k in orbit:
    w = W[k]
    if orbit[k]['a'][0] not in 'a' and len(orbit[k]['a'])==1:  # swap-type rules live on 'b'
        pass
    # compare to base language, relabelling swapped rules back
    wcmp = swap_word(w) if key(orbit[k]) in {('b','ba'), ('b','ab')} else w
    for L in (2,5,8,11):
        if factors(wcmp, L) != factors(W['e'], L): lang_ok = False
check("T2: all four rules generate the same hull language up to swap-relabelling", lang_ok)

# T3: matrices
M  = ((1,1),(1,0))
def mm(P,Q):
    return ((P[0][0]*Q[0][0]+P[0][1]*Q[1][0], P[0][0]*Q[0][1]+P[0][1]*Q[1][1]),
            (P[1][0]*Q[0][0]+P[1][1]*Q[1][0], P[1][0]*Q[0][1]+P[1][1]*Q[1][1]))
det = lambda P: P[0][0]*P[1][1]-P[0][1]*P[1][0]
M2 = mm(M,M)
R = ((1,1),(0,1)); L = ((1,0),(1,1)); RLm = mm(R,L)
check("T3a: det(M) = -1 (each tick reverses orientation); det(M^2)=+1", det(M)==-1 and det(M2)==1)
check("T3b: M^2 = [[2,1],[1,1]] = RL, the figure-eight monodromy, exactly", M2 == ((2,1),(1,1)) and RLm == ((2,1),(1,1)))

# T4: no K4 element maps sigma to an INVERSE-direction rule. All four orbit rules
# are positive substitutions (images in the positive monoid); sigma^{-1} is not
# (needs b^-1 a, heartbeat.py C1). So the arrow is outside the torsor's menu.
check("T4: all four orbit rules are positive (forward) substitutions — the arrow is not a torsor bit",
      all(set(r['a']+r['b']) <= set('ab') for r in orbit.values()))

print("\nOVERALL:", "ALL PASS" if ok else "SOMETHING FAILED")
sys.exit(0 if ok else 1)
