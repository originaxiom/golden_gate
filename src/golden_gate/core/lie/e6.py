"""Exact Chevalley E6 -- the integer-structure-constant Lie algebra e6 (result: ported).

Ported from origin-axiom B351 (``frontier/B351_exact_e6_chevalley/exact_e6.py``), the
first part of the {4,8}-integrability program. Everything here is **exact** (python
ints / :class:`fractions.Fraction`; no floats):

* the 72 roots of E6 by height induction from the Bourbaki Cartan matrix (chain
  1-3-4-5-6, node 2 on node 4);
* the 78-dim algebra ``{h_1..h_6} + {e_alpha}`` with integer structure constants built
  from a Frenkel-Kac / Kac asymmetry 2-cocycle ``eps`` (bimultiplicative,
  ``eps(a,b)eps(b,a) = (-1)^{(a,b)}``, ``eps(r,r) = -1`` on roots), which makes Jacobi a
  *theorem* of the construction -- and it is verified anyway, exactly, over all 76,076
  basis triples (:func:`jacobi_residual_count` returns 0);
* the principal ``sl2`` ``(e, h, f)``, ``h = sum c_i h_i`` with ``c = 2 A^{-1} 1 =
  (16,22,30,42,30,16)``;
* the exponent decomposition: ``ker(ad e)`` has ad-h weights ``{2,8,10,14,16,22} = 2 x
  {1,4,5,7,8,11}`` (the E6 exponents), i.e. ``e6 = (+)_i Sym^{2 m_i}`` as an sl2-module;
* the diagram involution ``theta`` (Dynkin flip 1<->6, 3<->5): an automorphism,
  ``theta^2 = id``, fixed subalgebra dim 52 (= f4), (-1)-eigenspace dim 26 (= e6/f4), and
  it acts on the six highest-weight lines by ``(-1)^{m+1}`` -- +1 on the F4 exponents
  ``{1,5,7,11}``, -1 on the escape sector ``{4,8}``.

This is exact Lie theory / low-dimensional topology machinery; it makes no physics
claim. It is stdlib-only (``fractions``) and imports nothing else in the package.
"""

from fractions import Fraction
from itertools import combinations

# --- (i) the E6 root system (Bourbaki labels) ----------------------------------------
# Cartan matrix: chain 1-3-4-5-6, node 2 attached to node 4.
_EDGES = [(1, 3), (3, 4), (4, 5), (5, 6), (2, 4)]
A = [[2 if i == j else 0 for j in range(6)] for i in range(6)]
for i, j in _EDGES:
    A[i - 1][j - 1] = A[j - 1][i - 1] = -1

SIGMA = {0: 5, 5: 0, 2: 4, 4: 2, 1: 1, 3: 3}          # the diagram flip 1<->6, 3<->5


def _pair(a, b):
    """(a, b) in the root lattice (simple-root coords; norm-2 normalization)."""
    return sum(a[i] * A[i][j] * b[j] for i in range(6) for j in range(6))


def positive_roots():
    """Height induction: gamma = beta + alpha_i is a root iff (beta, alpha_i) = -1
    (simply-laced, beta != alpha_i). Returns the positives sorted by height."""
    simples = [tuple(1 if k == i else 0 for k in range(6)) for i in range(6)]
    roots = set(simples)
    frontier_set = set(simples)
    while frontier_set:
        new = set()
        for b in frontier_set:
            for i, s in enumerate(simples):
                if _pair(b, s) == -1:
                    g = tuple(b[k] + s[k] for k in range(6))
                    if g not in roots:
                        new.add(g)
        roots |= new
        frontier_set = new
    return sorted(roots, key=lambda r: (sum(r), r))


POS = positive_roots()
ROOTS = POS + [tuple(-x for x in r) for r in POS]
NROOTS = len(ROOTS)                                    # 72
RIDX = {r: k for k, r in enumerate(ROOTS)}

# --- (ii) the asymmetry cocycle and the exact bracket table --------------------------
# B_ii = 1, B_ij = A_ij mod 2 for i < j, else 0  =>  eps(a,b) = (-1)^{a.B.b} is
# bimultiplicative with eps(a,b)eps(b,a) = (-1)^{(a,b)} and eps(r,r) = -1 on roots.
_B = [[1 if i == j else (A[i][j] % 2 if i < j else 0) for j in range(6)] for i in range(6)]


def eps(a, b):
    return -1 if sum(a[i] * _B[i][j] * b[j] for i in range(6) for j in range(6)) % 2 else 1


# Basis: 0..5 = h_1..h_6 (simple coroots); 6..77 = e_alpha, alpha = ROOTS[k-6].
DIM = 6 + NROOTS


def _add(vec, idx, coef):
    if coef:
        vec[idx] = vec.get(idx, 0) + coef
        if vec[idx] == 0:
            del vec[idx]


def _bracket_basis(i, j):
    """[basis_i, basis_j] as a sparse dict {index: int}."""
    out = {}
    if i < 6 and j < 6:
        return out                                             # [h, h] = 0
    if i < 6:                                                  # [h_i, e_b] = (alpha_i, b) e_b
        b = ROOTS[j - 6]
        _add(out, j, _pair(tuple(1 if k == i else 0 for k in range(6)), b))
        return out
    if j < 6:
        for k, c in _bracket_basis(j, i).items():
            _add(out, k, -c)
        return out
    a, b = ROOTS[i - 6], ROOTS[j - 6]
    s = tuple(a[k] + b[k] for k in range(6))
    if all(x == 0 for x in s):
        # [e_a, e_-a] = eps(a,-a) h_a = -h_a. The sign is FORCED by Jacobi given the
        # cocycle: with +h_a the mixed triples (e_a, e_-a, e_b), (a,b) = -1, violate
        # Jacobi by exactly 2 e_b (1440 triples fail, found by the exact enumeration
        # below -- the same trap the first cross-session attempt hit).
        for k in range(6):
            _add(out, k, -a[k])
        return out
    if s in RIDX:                                              # [e_a, e_b] = eps(a,b) e_{a+b}
        _add(out, 6 + RIDX[s], eps(a, b))
    return out


BRACKET = {(i, j): _bracket_basis(i, j) for i in range(DIM) for j in range(DIM)}


def brk(x, y):
    """Bracket of sparse vectors {idx: Fraction/int}."""
    out = {}
    for i, ci in x.items():
        for j, cj in y.items():
            for k, c in BRACKET[(i, j)].items():
                _add(out, k, ci * cj * c)
    return out


def antisymmetry_holds():
    return all(
        all(BRACKET[(j, i)].get(k, 0) == -c for k, c in BRACKET[(i, j)].items())
        and len(BRACKET[(j, i)]) == len(BRACKET[(i, j)])
        for i in range(DIM) for j in range(DIM)
    )


def jacobi_residual_count():
    """Number of basis triples violating Jacobi (exact integer arithmetic). Must be 0."""
    bad = 0
    basis = [{i: 1} for i in range(DIM)]
    for i, j, k in combinations(range(DIM), 3):
        out = {}
        for term in (brk(basis[i], BRACKET[(j, k)]), brk(basis[j], BRACKET[(k, i)]),
                     brk(basis[k], BRACKET[(i, j)])):
            for idx, c in term.items():
                _add(out, idx, c)
        if out:
            bad += 1
    return bad


# --- (iii) the principal sl2 ----------------------------------------------------------
def _cartan_inverse_times(v):
    """Exact A^{-1} v via Gaussian elimination over Fractions."""
    M = [[Fraction(A[i][j]) for j in range(6)] + [Fraction(v[i])] for i in range(6)]
    for col in range(6):
        p = next(r for r in range(col, 6) if M[r][col] != 0)
        M[col], M[p] = M[p], M[col]
        M[col] = [x / M[col][col] for x in M[col]]
        for r in range(6):
            if r != col and M[r][col]:
                M[r] = [xr - M[r][col] * xc for xr, xc in zip(M[r], M[col])]
    return [M[r][6] for r in range(6)]


PRINCIPAL_C = [2 * x for x in _cartan_inverse_times([1] * 6)]   # = (16,22,30,42,30,16)


def principal_sl2():
    e = {6 + RIDX[tuple(1 if k == i else 0 for k in range(6))]: 1 for i in range(6)}
    # f carries -c_i: with [e_a, e_-a] = -h_a the Chevalley f_i is -e_{-alpha_i}.
    f = {6 + RIDX[tuple(-1 if k == i else 0 for k in range(6))]: -int(PRINCIPAL_C[i])
         for i in range(6)}
    h = {i: int(PRINCIPAL_C[i]) for i in range(6)}
    return e, h, f


def _vec_eq(x, y):
    return all(x.get(k, 0) == y.get(k, 0) for k in set(x) | set(y))


def _scale(x, c):
    return {k: c * v for k, v in x.items()}


def principal_relations_hold():
    e, h, f = principal_sl2()
    return (_vec_eq(brk(h, e), _scale(e, 2)) and _vec_eq(brk(h, f), _scale(f, -2))
            and _vec_eq(brk(e, f), h))


# --- (iv) the exponent decomposition --------------------------------------------------
def _ad_matrix(x):
    """ad(x) as a dense DIM x DIM matrix of Fractions."""
    M = [[Fraction(0)] * DIM for _ in range(DIM)]
    for j in range(DIM):
        for k, c in brk(x, {j: 1}).items():
            M[k][j] += c
    return M


def _nullspace(M):
    """Exact nullspace basis of a DIM x DIM Fraction matrix (Gauss)."""
    m = [row[:] for row in M]
    n = DIM
    piv_of_col, r = {}, 0
    for c in range(n):
        p = next((i for i in range(r, n) if m[i][c] != 0), None)
        if p is None:
            continue
        m[r], m[p] = m[p], m[r]
        m[r] = [x / m[r][c] for x in m[r]]
        for i in range(n):
            if i != r and m[i][c]:
                m[i] = [xi - m[i][c] * xr for xi, xr in zip(m[i], m[r])]
        piv_of_col[c] = r
        r += 1
    free = [c for c in range(n) if c not in piv_of_col]
    basis = []
    for fc in free:
        v = {fc: Fraction(1)}
        for c, rr in piv_of_col.items():
            if m[rr][fc]:
                v[c] = -m[rr][fc]
        basis.append(v)
    return basis


def exponent_weights():
    """ad-h weights of ker(ad e): must be {2,8,10,14,16,22} = 2 x exponents."""
    e, h, f = principal_sl2()
    kern = _nullspace(_ad_matrix(e))
    weights = []
    for v in kern:
        hv = brk(h, v)
        pivot = next(iter(v))
        w = hv.get(pivot, 0) / v[pivot]
        assert _vec_eq(hv, _scale(v, w)), "kernel vector is not an ad-h eigenvector"
        weights.append(int(w))
    return sorted(weights)


EXPONENTS = [1, 4, 5, 7, 8, 11]

# --- (v)/(vi) the diagram involution theta --------------------------------------------
def _chain_expressions():
    """For each positive root, a recorded (i, beta) with gamma = alpha_i + beta and
    e_gamma = eps(alpha_i, beta) [e_i, e_beta] (true by the bracket table)."""
    chain = {}
    for g in POS:
        if sum(g) == 1:
            continue
        for i in range(6):
            s = tuple(1 if k == i else 0 for k in range(6))
            b = tuple(g[k] - s[k] for k in range(6))
            if b in RIDX:
                chain[g] = (i, b)
                break
        else:
            raise RuntimeError("no chain decomposition for %s" % (g,))
    return chain


_CHAIN = _chain_expressions()


def theta_map():
    """theta on the basis, as sparse vectors. Generators: h_i -> h_sigma(i),
    e_{alpha_i} -> e_{alpha_sigma(i)}, e_{-alpha_i} -> e_{-alpha_sigma(i)}; propagated
    up the recorded bracket chains (an automorphism must satisfy
    theta e_gamma = eps(alpha_i, beta) [theta e_i, theta e_beta])."""
    th = {}
    for i in range(6):
        th[i] = {SIGMA[i]: 1}
    for i in range(6):
        s = tuple(1 if k == i else 0 for k in range(6))
        ss = tuple(1 if k == SIGMA[i] else 0 for k in range(6))
        th[6 + RIDX[s]] = {6 + RIDX[ss]: 1}
        th[6 + RIDX[tuple(-x for x in s)]] = {6 + RIDX[tuple(-x for x in ss)]: 1}
    for g in POS:
        if sum(g) == 1:
            continue
        i, b = _CHAIN[g]
        s = tuple(1 if k == i else 0 for k in range(6))
        img = _scale(brk(th[6 + RIDX[s]], th[6 + RIDX[b]]), eps(s, b))
        th[6 + RIDX[g]] = img
        neg_img = _scale(brk(th[6 + RIDX[tuple(-x for x in s)]],
                             th[6 + RIDX[tuple(-x for x in b)]]), eps(s, b))
        th[6 + RIDX[tuple(-x for x in g)]] = neg_img
    return th


def _apply(mapping, x):
    out = {}
    for i, c in x.items():
        for k, v in mapping[i].items():
            _add(out, k, c * v)
    return out


def theta_checks():
    """(is_automorphism, is_involution, dim_fixed, dim_minus)."""
    th = theta_map()
    auto = all(
        _vec_eq(_apply(th, BRACKET[(i, j)]), brk(th[i], th[j]))
        for i in range(DIM) for j in range(DIM)
    )
    invol = all(_vec_eq(_apply(th, th[i]), {i: 1}) for i in range(DIM))
    # eigenspace dims of the (exact, entries in {0, +-1}) matrix of theta
    fixed = minus = 0
    seen = set()
    for i in range(DIM):
        if i in seen:
            continue
        img = th[i]
        if _vec_eq(img, {i: 1}):
            fixed += 1
            seen.add(i)
        elif _vec_eq(img, {i: -1}):
            minus += 1
            seen.add(i)
        else:
            j = next(iter(img))
            # theta permutes basis lines in +-1 pairs off the diagonal blocks
            fixed += 1
            minus += 1
            seen.add(i)
            seen.add(j)
            assert _vec_eq(_apply(th, img), {i: 1}), "not an order-2 pairing"
    return auto, invol, fixed, minus


def theta_commutes_with_principal_sl2():
    th = theta_map()
    e, h, f = principal_sl2()
    return all(_vec_eq(_apply(th, x), x) for x in (e, h, f))


def theta_signs_on_exponent_lines():
    """theta eigenvalue on each 1-dim highest-weight line, keyed by exponent m.
    Expected: (-1)^{m+1} -- i.e. +1 on the F4 exponents {1,5,7,11}, -1 on {4,8}."""
    th = theta_map()
    e, h, f = principal_sl2()
    kern = _nullspace(_ad_matrix(e))
    out = {}
    for v in kern:
        pivot = next(iter(v))
        w = int(brk(h, v).get(pivot, 0) / v[pivot])
        m = w // 2
        tv = _apply(th, v)
        pivot_ratio = tv.get(pivot, 0) / v[pivot]
        assert _vec_eq(tv, _scale(v, pivot_ratio)), "theta does not preserve the line"
        out[m] = int(pivot_ratio)
    return out


def run_all():
    r = {}
    r["n_positive_roots"] = len(POS)
    r["antisymmetry"] = antisymmetry_holds()
    r["jacobi_violations"] = jacobi_residual_count()
    r["principal_c"] = [int(x) for x in PRINCIPAL_C]
    r["principal_relations"] = principal_relations_hold()
    r["exponent_weights"] = exponent_weights()
    auto, invol, fixed, minus = theta_checks()
    r["theta_automorphism"] = auto
    r["theta_involution"] = invol
    r["theta_fixed_dim"] = fixed
    r["theta_minus_dim"] = minus
    r["theta_commutes_principal"] = theta_commutes_with_principal_sl2()
    r["theta_signs"] = theta_signs_on_exponent_lines()
    return r


if __name__ == "__main__":
    r = run_all()
    print("exact Chevalley e6 (ported from origin-axiom B351)\n")
    print("(i)   positive roots:", r["n_positive_roots"], "(expect 36)")
    print("(ii)  antisymmetry:", r["antisymmetry"], "| Jacobi violations:",
          r["jacobi_violations"], "(expect 0, exact integers, all 76,076 triples)")
    print("(iii) principal c = 2 A^-1 1 =", r["principal_c"],
          "| sl2 relations exact:", r["principal_relations"])
    print("(iv)  ad-h weights on ker(ad e):", r["exponent_weights"],
          "(expect 2x exponents {1,4,5,7,8,11})")
    print("(v)   theta: automorphism", r["theta_automorphism"], "| involution",
          r["theta_involution"], "| dim fixed", r["theta_fixed_dim"],
          "(f4 = 52) | dim -1:", r["theta_minus_dim"], "(26)")
    print("(vi)  theta commutes with principal sl2:", r["theta_commutes_principal"])
    print("      theta signs on exponent lines:", r["theta_signs"],
          "(expect (-1)^{m+1}: +1 on {1,5,7,11}, -1 on {4,8})")
