#!/usr/bin/env python3
"""THE GIESEKING FIRST BEAT — the object's own antilinear element, explicit.

m004 is the orientation double cover of the Gieseking manifold: the fig-8 monodromy
[[2,1],[1,1]] is the SQUARE of the orientation-reversing Fibonacci map (det -1).
So Gamma_G = <Gamma, w> with w acting ANTIHOLOMORPHICALLY: M -> W conj(M) W^{-1}
(conj = the Galois q -> 1-q = complex conjugation on Q(sqrt-3) entries).

Compute, exactly over Q(q)/(q^2-q+1):
 1. fiber generators x = A B^{-1}, y = A^{-1} B (kernel of exponent sum; CITED as the
    fig-8 fiber F2); check tr[x,y] = -2 (the fiber boundary is parabolic).
 2. the monodromy = conjugation by the meridian A: find A x A^{-1}, A y A^{-1} as
    WORDS in x,y (exact matrix match) => the H1 monodromy matrix; verify det 1,
    trace 3 ([[2,1],[1,1]]-class).
 3. THE BEAT: search antiholomorphic W with W conj(x) W^{-1} = w1(x,y),
    W conj(y) W^{-1} = w2(x,y) for short words (w1,w2) with H1 det -1, and
    W conj(W) projectively in Gamma matching (meridian x fiber). Verify
    beat^2 = monodromy on H1: F^2 = [[2,1],[1,1]].
"""
import itertools
from fractions import Fraction as F

ZERO=(F(0),F(0)); ONE=(F(1),F(0)); QQ=(F(0),F(1))
def fadd(u,v): return (u[0]+v[0], u[1]+v[1])
def fsub(u,v): return (u[0]-v[0], u[1]-v[1])
def fneg(u): return (-u[0],-u[1])
def fmul(u,v):
    a=u[0]*v[0]; b=u[0]*v[1]+u[1]*v[0]; c=u[1]*v[1]
    return (a-c, b+c)
def finv(u):
    x,y=u; n=x*x+x*y+y*y
    return ((x+y)/n, -y/n)
def fbar(u):  # Galois q -> 1-q  (= complex conjugation on Q(sqrt-3))
    x,y=u
    return (x+y, -y)
def frat(r): return (F(r),F(0))

def mm(A,B):
    return [[fadd(fmul(A[0][0],B[0][0]),fmul(A[0][1],B[1][0])), fadd(fmul(A[0][0],B[0][1]),fmul(A[0][1],B[1][1]))],
            [fadd(fmul(A[1][0],B[0][0]),fmul(A[1][1],B[1][0])), fadd(fmul(A[1][0],B[0][1]),fmul(A[1][1],B[1][1]))]]
def minv2(A):
    d=fsub(fmul(A[0][0],A[1][1]),fmul(A[0][1],A[1][0]))
    di=finv(d)
    return [[fmul(di,A[1][1]),fmul(di,fneg(A[0][1]))],[fmul(di,fneg(A[1][0])),fmul(di,A[0][0])]]
def mbar(A): return [[fbar(A[0][0]),fbar(A[0][1])],[fbar(A[1][0]),fbar(A[1][1])]]
def tr(A): return fadd(A[0][0],A[1][1])
def det(A): return fsub(fmul(A[0][0],A[1][1]),fmul(A[0][1],A[1][0]))
def meq(A,B): return A[0][0]==B[0][0] and A[0][1]==B[0][1] and A[1][0]==B[1][0] and A[1][1]==B[1][1]
def proj_eq(A,B):
    """A = lambda B for scalar lambda (projective equality)."""
    for i in range(2):
        for j in range(2):
            if B[i][j]!=ZERO:
                lam=fmul(A[i][j],finv(B[i][j]))
                if lam==ZERO: return None
                lb=[[fmul(lam,B[0][0]),fmul(lam,B[0][1])],[fmul(lam,B[1][0]),fmul(lam,B[1][1])]]
                return lam if meq(A,lb) else None
    return None

A=[[ONE,ONE],[ZERO,ONE]]
B=[[ONE,ZERO],[QQ,ONE]]
Ai=minv2(A); Bi=minv2(B)
x=mm(A,Bi); y=mm(Ai,B)
xi=minv2(x); yi=minv2(y)
comm=mm(mm(x,y),mm(xi,yi))
print("fiber x=AB^-1, y=A^-1B:  tr x =",tr(x)," tr y =",tr(y)," tr xy =",tr(mm(x,y)))
print("tr [x,y] =",tr(comm)," (fiber boundary parabolic: expect -2 up to sign)")

GENW={'x':x,'X':xi,'y':y,'Y':yi}
def wordmat(w):
    M=[[ONE,ZERO],[ZERO,ONE]]
    for ch in w: M=mm(M,GENW[ch])
    return M
def h1(w):
    return (w.count('x')-w.count('X'), w.count('y')-w.count('Y'))
words=['']
for L in range(1,6):
    for t in itertools.product('xXyY',repeat=L):
        w=''.join(t)
        if any(w[i]+w[i+1] in ('xX','Xx','yY','Yy') for i in range(len(w)-1)): continue
        words.append(w)
words=[w for w in words if w]

# 2. the monodromy: conj by A as words in x,y
psi={}
for gname,g in (('x',x),('y',y)):
    tgt=mm(mm(A,g),Ai)
    hit=[w for w in words if meq(wordmat(w),tgt)]
    assert hit, f"monodromy image of {gname} not found in short words"
    psi[gname]=hit[0]
    print(f"monodromy: A {gname} A^-1 = {hit[0]}")
M_h1=[[0,0],[0,0]]
(M_h1[0][0],M_h1[1][0])=h1(psi['x'])
(M_h1[0][1],M_h1[1][1])=h1(psi['y'])
dM=M_h1[0][0]*M_h1[1][1]-M_h1[0][1]*M_h1[1][0]
tM=M_h1[0][0]+M_h1[1][1]
print(f"monodromy H1 matrix {M_h1}, det {dM}, trace {tM}  (expect det 1, trace 3)")
assert dM==1 and tM==3

# 3. THE BEAT: search (w1,w2) short, H1 det -1, solve W from the antiholomorphic
#    intertwining W conj(g) = wi(g) W, then demand W conj(W) projectively = A^{\pm1} * fiber word.
xb=mbar(x); yb=mbar(y)
def solve_W(t1,t2):
    """W xb = t1 W and W yb = t2 W: linear in W's 4 entries; return basis of solutions."""
    rowsys=[]
    for (Mb,T) in ((xb,t1),(yb,t2)):
        # W Mb - T W = 0: entry (i,j): sum_k W[i][k] Mb[k][j] - T[i][k] W[k][j] = 0
        for i in range(2):
            for j in range(2):
                coef={ (i2,j2):ZERO for i2 in range(2) for j2 in range(2)}
                for k in range(2):
                    coef[(i,k)]=fadd(coef[(i,k)],Mb[k][j])
                    coef[(k,j)]=fsub(coef[(k,j)],T[i][k])
                rowsys.append([coef[(0,0)],coef[(0,1)],coef[(1,0)],coef[(1,1)]])
    # nullspace over the field
    Mx=[r[:] for r in rowsys]; nrow=len(Mx); piv=[]; r=0
    for c in range(4):
        pr=next((i for i in range(r,nrow) if Mx[i][c]!=ZERO), None)
        if pr is None: continue
        Mx[r],Mx[pr]=Mx[pr],Mx[r]
        inv=finv(Mx[r][c]); Mx[r]=[fmul(inv,v) for v in Mx[r]]
        for i in range(nrow):
            if i!=r and Mx[i][c]!=ZERO:
                f_=Mx[i][c]; Mx[i]=[fsub(a,fmul(f_,b)) for a,b in zip(Mx[i],Mx[r])]
        piv.append(c); r+=1
    free=[c for c in range(4) if c not in piv]
    outs=[]
    for fc in free:
        v=[ZERO]*4; v[fc]=ONE
        for i,c in enumerate(piv): v[c]=fneg(Mx[i][fc])
        outs.append([[v[0],v[1]],[v[2],v[3]]])
    return outs

fiberwords=['']+[w for w in words if len(w)<=3]
mer=[('A',A),('Ai',Ai)]
found=[]
cand_words=[w for w in words if len(w)<=3]
for w1 in cand_words:
    for w2 in cand_words:
        a11,a21=h1(w1); a12,a22=h1(w2)
        if a11*a22-a12*a21!=-1: continue     # beat must reverse orientation on H1
        # beat^2 on H1 must equal the monodromy H1 matrix
        Bm=[[a11,a12],[a21,a22]]
        B2=[[Bm[0][0]*Bm[0][0]+Bm[0][1]*Bm[1][0], Bm[0][0]*Bm[0][1]+Bm[0][1]*Bm[1][1]],
            [Bm[1][0]*Bm[0][0]+Bm[1][1]*Bm[1][0], Bm[1][0]*Bm[0][1]+Bm[1][1]*Bm[1][1]]]
        if B2!=M_h1: continue
        t1=wordmat(w1); t2=wordmat(w2)
        for W in solve_W(t1,t2):
            if det(W)==ZERO: continue
            WWb=mm(W,mbar(W))
            for mname,Mm in mer:
                for fw in fiberwords:
                    tgt=mm(Mm,wordmat(fw)) if fw else Mm
                    lam=proj_eq(WWb,tgt)
                    if lam is not None:
                        found.append((w1,w2,W,mname,fw,lam))
print(f"\nbeat solutions found: {len(found)}")
for w1,w2,W,mname,fw,lam in found[:4]:
    print(f"  beat: x -> {w1}, y -> {w2};  W conj(W) ~ {mname}{('*'+fw) if fw else ''} (scalar {lam})")
    print(f"     W = {W}  det W = {det(W)}")
if found:
    w1,w2,W,mname,fw,lam=found[0]
    # final verification of the chosen beat, all exact:
    ok1=meq(mm(mm(W,xb),minv2(W)), wordmat(w1))
    ok2=meq(mm(mm(W,yb),minv2(W)), wordmat(w2))
    a11,a21=h1(w1); a12,a22=h1(w2)
    print(f"  VERIFY: intertwining exact: {ok1 and ok2}; H1(beat) = [[{a11},{a12}],[{a21},{a22}]] "
          f"det {a11*a22-a12*a21} (Fibonacci class, det -1); beat^2 H1 = monodromy H1: True")
    print("  => Gamma_G = <Gamma, w>, w antiholomorphic, w^2 = meridian x fiber:")
    print("     THE OBJECT'S OWN FIRST BEAT = (Galois conjugation) o (Fibonacci step),")
    print("     and m004's monodromy (the tick^2) is its square.")
