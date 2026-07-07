"""Render braid words as diagrams -- ASCII text and standalone SVG."""

from .compiler import compress_word

__all__ = ["braid_diagram", "gate_summary"]

# SVG geometry
_COL = 44          # horizontal strand spacing (px)
_ROW = 44          # vertical spacing per crossing (px)
_PAD = 22          # outer margin
_GAP = 7           # half-gap in the under-strand at a crossing (px)
_STROKE = 3.0
_GOLD = "#D4AF37"  # accent for the "over" strand


def _lerp(a, b, t):
    return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)


def _subcurve(P, ta, tb):
    """The cubic Bezier ``P`` restricted to ``[ta, tb]``, as 4 control points."""
    def split_left(Q, t):
        p0, p1, p2, p3 = Q
        a, b, c = _lerp(p0, p1, t), _lerp(p1, p2, t), _lerp(p2, p3, t)
        d, e = _lerp(a, b, t), _lerp(b, c, t)
        return [p0, a, d, _lerp(d, e, t)]

    def split_right(Q, t):
        p0, p1, p2, p3 = Q
        a, b, c = _lerp(p0, p1, t), _lerp(p1, p2, t), _lerp(p2, p3, t)
        d, e = _lerp(a, b, t), _lerp(b, c, t)
        return [_lerp(d, e, t), e, c, p3]

    return split_right(split_left(P, tb), ta / tb)


def _path(P):
    return (f"M {P[0][0]:.1f} {P[0][1]:.1f} C {P[1][0]:.1f} {P[1][1]:.1f} "
            f"{P[2][0]:.1f} {P[2][1]:.1f} {P[3][0]:.1f} {P[3][1]:.1f}")


def _braid_svg(units, n_strands) -> str:
    """Standalone SVG of a braid: strands permute through each crossing; the
    under-strand is split around the crossing so the over-strand shows on top
    (theme-independent, no background fill needed)."""
    n_rows = max(len(units), 1)
    width = _PAD * 2 + (n_strands - 1) * _COL
    height = _PAD * 2 + n_rows * _ROW

    def x(pos):
        return _PAD + pos * _COL

    paths = []
    for r in range(n_rows):
        y0, y1 = _PAD + r * _ROW, _PAD + (r + 1) * _ROW
        my = (y0 + y1) / 2
        gen, sign = units[r] if r < len(units) else (None, 1)
        left = (gen - 1) if gen is not None else -1
        for pos in range(n_strands):
            if pos == left:                       # the crossing pair
                # cubic control points for the two swapping strands
                P_lr = [(x(left), y0), (x(left), my), (x(left + 1), my), (x(left + 1), y1)]
                P_rl = [(x(left + 1), y0), (x(left + 1), my), (x(left), my), (x(left), y1)]
                over, under = (P_lr, P_rl) if sign > 0 else (P_rl, P_lr)
                paths.append(f'<path d="{_path(_subcurve(under, 0.001, 0.4))}" class="under"/>')
                paths.append(f'<path d="{_path(_subcurve(under, 0.6, 0.999))}" class="under"/>')
                paths.append(f'<path d="{_path(over)}" class="over"/>')
            elif pos == left + 1:
                continue                          # drawn by the crossing above
            else:
                v = [(x(pos), y0), (x(pos), my), (x(pos), my), (x(pos), y1)]
                paths.append(f'<path d="{_path(v)}" class="strand"/>')

    css = (f".strand,.under,.over{{fill:none;stroke-width:{_STROKE};"
           "stroke-linecap:round}"
           ".strand,.under{stroke:currentColor}"
           f".over{{stroke:{_GOLD}}}"
           ":root{color:#222}"
           "@media(prefers-color-scheme:dark){:root{color:#ddd}}")
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" '
            f'height="{height}" viewBox="0 0 {width} {height}" '
            f'role="img" aria-label="braid diagram">'
            f"<style>{css}</style>" + "".join(paths) + "</svg>")


def _expand_units(word):
    """Expand ``(gen, power)`` runs into unit crossings ``(gen, sign)``."""
    units = []
    for gen, power in word:
        sign = 1 if power >= 0 else -1
        units.extend([(gen, sign)] * abs(int(power)))
    return units


def braid_diagram(word, n_strands=3, fmt="text") -> str:
    """Render a braid word as a diagram.

    ``fmt='text'`` returns ASCII art with ``n_strands`` vertical strands, one
    crossing per row. ``fmt='svg'`` returns a standalone SVG string with the
    strands actually permuting through each crossing (over/under shown by a gap in
    the under-strand). A positive ``sigma_i`` draws strand ``i`` over ``i+1``.
    """
    if fmt not in ("text", "svg"):
        raise ValueError("fmt must be 'text' or 'svg'")
    units = _expand_units(word)
    for gen, _sign in units:
        if gen + 1 > n_strands:
            raise ValueError(f"generator sigma_{gen} needs >= {gen + 1} strands, "
                             f"but n_strands={n_strands}")
    if fmt == "svg":
        return _braid_svg(units, n_strands)
    header = f"braid on {n_strands} strands ({len(units)} crossings): {compress_word(word)}"
    if not units:
        return header + "\n" + "│ " * n_strands + "  (identity)"

    rows = []
    for gen, sign in units:
        left = gen - 1                            # generator i crosses strands i-1, i
        cross = "╲╱" if sign > 0 else "╱╲"        # over / under
        cells, c = [], 0
        while c < n_strands:
            if c == left:
                cells.append(cross)
                c += 2
            else:
                cells.append("│ ")
                c += 1
        rows.append("".join(cells))
    return header + "\n" + "\n".join(rows)


def gate_summary(U) -> str:
    """A short text summary of a 2x2 gate (matrix + key properties)."""
    from .gates import gate_properties
    p = gate_properties(U)
    lines = [
        "gate:",
        f"  [{U[0,0]:+.4f}  {U[0,1]:+.4f}]",
        f"  [{U[1,0]:+.4f}  {U[1,1]:+.4f}]",
        f"  rotation angle : {p['rotation_angle']:.4f} rad "
        f"({p['rotation_angle']/3.141592653589793:.4f} pi)",
        f"  Clifford       : {p['is_clifford']}",
        f"  determinant    : {p['determinant']:+.4f}",
    ]
    return "\n".join(lines)
