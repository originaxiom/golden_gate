#!/usr/bin/env python3
"""The D4-orbifold door, step 3: do the symmetries of 4_1 act on the 2T-fiber
through the OUTER involution (w in 2O\\2T)?  Method:
 - pi_1(4_1) = <a,b | r>, r = a w b^-1 w^-1, w = b a^-1 b^-1 a  (verified earlier).
 - geometric rep over Q(q)/(q^2-q+1): a->A=[[1,1],[0,1]], b->B=[[1,0],[q,1]] (faithful, discrete).
 - candidate symmetry actions phi: (a,b) -> (words U,V); phi is a homomorphism iff r(U,V)=I
   exactly in the faithful rep, and corresponds to an isometry iff (U,V) ~ (A,B) (or-pres.)
   or ~ (conj(A),conj(B)) (or-rev.) in PGL(2,C).
 - then reduce mod (sqrt-3): images in SL(2,F3); find g in GL(2,3) with g.(A3,B3).g^-1 = (U3,V3);
   det(g) square in F3* -> INNER (fiber twist inside 2T, no enhancement);
   det(g) nonsquare      -> OUTER (fiber twist by w: E6 -> E7-type wall)."""
import sympy as sp
import itertools, sys

q = sp.symbols('q')
MOD = q**2 - q + 1
def red(e): return sp.rem(sp.expand(e), MOD, q)
def rmat(M): return M.applyfunc(red)
A = sp.Matrix([[1,1],[0,1]]); B = sp.Matrix([[1,0],[q,1]])
def minv(M):
    return sp.Matrix([[M[1,1],-M[0,1]],[-M[1,0],M[0,0]]])  # det=1
def mm(*Ms):
    R = sp.eye(2)
    for M in Ms: R = rmat(R*M)
    return R
def weval(word, X, Y):
    # word: string over 'a','A','b','B' (A=a^-1 etc)
    d = {'a':X,'A':minv(X),'b':Y,'B':minv(Y)}
    R = sp.eye(2)
    for ch in word: R = rmat(R*d[ch])
    return R
RELATOR = "a" + "bABa" + "B" + "AbaB"   # a * w * b^-1 * w^-1, w = b a^-1 b^-1 a, w^-1 = A b a B -> "AbaB"? w^-1 = a^-1 b a b^-1 reversed-inverted: w=bABa -> w^-1 = A b a B
# verify relator on (A,B):
assert weval(RELATOR, A, B) == sp.eye(2), "relator check failed"
print("relator r(A,B)=I verified in the faithful rep")

# candidate symmetry actions
cands = {
 "swap  a<->b            ": ("b","a"),
 "inv   a->a^-1,b->b^-1  ": ("A","B"),
 "swapinv a->b^-1,b->a^-1": ("B","A"),
}
def is_hom(u,v):
    U = weval(u,A,B); V = weval(v,A,B)
    return weval(RELATOR, U, V) == sp.eye(2), U, V

results={}
for name,(u,v) in cands.items():
    ok,U,V = is_hom(u,v)
    if not ok:
        # try conjugating second generator by short words: phi(a)=u, phi(b)= h v h^-1
        found=None
        alph="aAbB"
        for L in range(1,5):
            for hw in itertools.product(alph, repeat=L):
                h="".join(hw)
                Vc = mm(weval(h,A,B), weval(v,A,B), minv(weval(h,A,B)))
                if weval(RELATOR, weval(u,A,B), Vc)==sp.eye(2):
                    found=(u, h+v+h.swapcase()[::-1] if False else (u,h,v)); U=weval(u,A,B); V=Vc
                    break
            if found: break
        ok = found is not None
        if ok: print(f"{name}: homomorphism after conjugating b-image by '{found[1] if isinstance(found,tuple) else found}'")
    results[name]=(ok,U,V)
    print(f"{name}: homomorphism = {ok}")

# orientation: is (U,V) conjugate to (A,B) over C (or-preserving) or to complex conjugates (or-reversing)?
# trace test: tr(UV) vs tr(AB) vs conj(tr(AB)). tr(AB) = 2+q (with q = (1+i sqrt3)/2 root of q^2-q+1)
trAB = red(sp.trace(mm(A,B)))
print("\ntr(AB) =", trAB, " (q = (1+i*sqrt3)/2; conj corresponds to q -> 1-q)")
def qconj(e):  # Galois conj q -> 1-q
    return red(sp.expand(e.subs(q,1-q)))
for name,(ok,U,V) in results.items():
    if not ok: continue
    t = red(sp.trace(mm(U,V)))
    ori = "or-PRESERVING" if t==trAB else ("or-REVERSING" if t==qconj(trAB) else "??? tr="+str(t))
    print(f"{name}: tr(phi(a)phi(b)) = {t} -> {ori}")

# mod (sqrt-3) reduction: q -> ? q=(1+sqrt-3)/2 -> (1+0)/2 = 2^-1 = 2 mod 3
A3 = sp.Matrix([[1,1],[0,1]]) % 3
B3 = sp.Matrix([[1,0],[2,1]]) % 3
def m3(*Ms):
    R = sp.eye(2)
    for M in Ms: R = (R*M) % 3
    return R
def w3(word,X,Y):
    def i3(M):
        d = (M[0,0]*M[1,1]-M[0,1]*M[1,0]) % 3
        di = 1 if d==1 else 2
        return (di*sp.Matrix([[M[1,1],-M[0,1]],[-M[1,0],M[0,0]]])) % 3
    d = {'a':X,'A':i3(X),'b':Y,'B':i3(Y)}
    R = sp.eye(2)
    for ch in word: R = (R*d[ch]) % 3
    return R
assert w3(RELATOR,A3,B3)==sp.eye(2)%3

GL23=[]
for a_ in range(3):
    for b_ in range(3):
        for c_ in range(3):
            for d_ in range(3):
                dd=(a_*d_-b_*c_)%3
                if dd!=0: GL23.append((sp.Matrix([[a_,b_],[c_,d_]]),dd))
def i3(M):
    d=(M[0,0]*M[1,1]-M[0,1]*M[1,0])%3
    di=1 if d==1 else 2
    return (di*sp.Matrix([[M[1,1],-M[0,1]],[-M[1,0],M[0,0]]]))%3

print("\nfiber-twist class (inner = twist in 2T; outer = twist by w in 2O\\2T -> E7-type wall):")
for name,(ok,U,V) in results.items():
    if not ok: continue
    U3 = w3({"b":"b","A":"A","B":"B","a":"a"}.get("x","")+"", A3,B3) # placeholder
for name,(u,v) in cands.items():
    ok,U,V = results[name]
    if not ok: continue
    U3 = w3(u, A3, B3); V3 = w3(v, A3, B3)
    dets=set()
    for g,dd in GL23:
        if (g*A3*i3(g))%3==U3 and (g*B3*i3(g))%3==V3:
            dets.add(dd)
    if not dets:
        # maybe conjugate as a PAIR to the other Aut-class? then no g exists
        verdict="NO g in GL(2,3): lands in the OTHER Aut-class of surjections"
    else:
        # det squares in F3*: {1}; nonsquares {2}
        inner = 1 in dets; outer = 2 in dets
        verdict = ("INNER (g in PSL)" if inner else "") + (" & " if inner and outer else "") + ("OUTER (g in PGL\\PSL) -> w-twist -> E7" if outer else "")
    print(f"  {name}: dets of conjugators = {dets or '{}'} -> {verdict}")
EOF_MARKER = True
