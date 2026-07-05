"""Visualization smoke tests -- render without error, sane shape."""

from golden_gate.demo import knots as K
from golden_gate.demo import visualize as V


def test_identity_diagram():
    out = V.braid_diagram([])
    assert "identity" in out


def test_golden_gate_diagram_has_four_crossings():
    word = K.knot_braid("figure_eight")
    out = V.braid_diagram(word)
    # 4 unit crossings -> header + 4 rows
    body = out.splitlines()[1:]
    assert len(body) == 4
    assert "4 crossings" in out


def test_all_named_knots_render():
    for name in K.KNOT_BRAIDS:
        out = V.braid_diagram(K.knot_braid(name))
        assert isinstance(out, str) and out


def test_gate_summary():
    from golden_gate.demo import gates as G
    s = V.gate_summary(G.golden_gate())
    assert "rotation angle" in s and "Clifford" in s


def test_bad_format_rejected():
    import pytest
    with pytest.raises(ValueError):
        V.braid_diagram([(1, 1)], fmt="png")


def test_too_few_strands_rejected():
    import pytest
    with pytest.raises(ValueError):
        V.braid_diagram([(2, 1)], n_strands=2)   # sigma_2 needs >= 3 strands
    with pytest.raises(ValueError):
        V.braid_diagram([(2, 1)], n_strands=2, fmt="svg")


def test_svg_is_well_formed():
    import xml.dom.minidom as MD
    svg = V.braid_diagram(K.knot_braid("figure_eight"), fmt="svg")
    MD.parseString(svg)                          # raises if not well-formed XML
    assert svg.startswith("<svg") and svg.rstrip().endswith("</svg>")
    assert svg.count('class="over"') == 4        # one over-strand per crossing


def test_svg_identity_is_valid():
    import xml.dom.minidom as MD
    svg = V.braid_diagram([], fmt="svg")
    MD.parseString(svg)
    assert svg.count('class="over"') == 0
