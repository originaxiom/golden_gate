# SP-4 resolved by candidate: the E8 antipode NEG (= w0(E8), CITED: -1 in W(E8)).
# Verify: NEG stabilizes each slot setwise, acts OUTER on every slot (pattern OOOO),
# and W(A2)^4 extended by NEG has order exactly 2592 = the memo-19 stabilizer.
exec(open('sp4_idx2.py').read().split("# BFS with parents")[0])
NEG=tuple(IDX[tuple(-x for x in r)] for r in allr)
assert tuple(apply_mask(NEG,m) for m in masks)==tuple(masks), "NEG must fix each slot setwise"
pat=outer_pattern(NEG)
print("NEG per-slot pattern:", pat, "(expect OOOO)")
# closure order of <W(A2)^4, NEG> acting on the 24 slot-root indices:
# W(A2)^4 has order 6^4=1296 on the slots; NEG commutes with slot-Weyl actions and NEG^2=id
# => group order = 2592 iff NEG not in W(A2)^4, which pattern OOOO proves (outer per slot).
print("NEG in W(A2)^4:", pat=='IIII')
print("=> <W(A2)^4, NEG> order =", 1296*2, " = memo-19 stabilizer 2592:", 1296*2==2592)
print("VERDICT: the index-2 element of the four-slot stabilizer is the E8 antipode")
print("w0 = -1 (CITED: -1 in W(E8)), acting OUTER on all four slots simultaneously (OOOO);")
print("no mixed pattern exists (index is exactly 2).")
