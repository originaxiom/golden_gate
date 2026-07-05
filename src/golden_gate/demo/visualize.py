"""Render braid words as diagrams (text for now; SVG is a later addition)."""

from .compiler import compress_word


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
    crossing per row (top to bottom = left to right in the word). A positive
    ``sigma_i`` crossing is drawn ``\\ /`` (strand i over i+1); a negative one
    ``/ \\`` (under).
    """
    if fmt != "text":
        raise ValueError("only fmt='text' is supported in v0.1")
    units = _expand_units(word)
    header = "braid on %d strands (%d crossings): %s" % (
        n_strands, len(units), compress_word(word))
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
