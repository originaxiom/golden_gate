"""Compile a target single-qubit gate into a Fibonacci-anyon braid word.

Two methods:

* ``brute_force`` -- breadth-first search over braid words (the four unit
  generators ``sigma1^+-1, sigma2^+-1``), pruning immediate inverse pairs and
  deduplicating gates already seen. General; the workhorse for short words.
* ``golden`` -- approximate the target by powers of the golden gate ``G`` and a
  short brute-force refinement. Best when the target lies near ``G``'s rotation
  axis; documented as a special-case optimization, not a general optimum.

Honest note on prior art: exact/asymptotically-optimal Fibonacci-anyon synthesis
is a mature literature (Kliuchnikov-Bocharov-Svore; Kliuchnikov-Yard's exact
synthesis over Z[phi]). This module is a clean, practical compiler, not a novel
algorithm.
"""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass, field

import numpy as np

from .braiding import evaluate_braid, sigma1, sigma1_inv, sigma2, sigma2_inv
from .gates import gate_fidelity, golden_gate

# the four unit generators, as (gen, power) with their matrices
_UNITS = [((1, 1), sigma1()), ((1, -1), sigma1_inv()),
          ((2, 1), sigma2()), ((2, -1), sigma2_inv())]
_INVERSE = {(1, 1): (1, -1), (1, -1): (1, 1), (2, 1): (2, -1), (2, -1): (2, 1)}


@dataclass
class CompilationResult:
    word: list = field(default_factory=list)     # list[(gen, power)] unit steps
    gate: np.ndarray = None
    fidelity: float = 0.0
    length: int = 0                               # number of crossings
    error: float = 1.0                            # 1 - fidelity

    def __repr__(self):
        return (f"CompilationResult(length={self.length}, "
                f"fidelity={self.fidelity:.6f}, word={compress_word(self.word)})")


def compress_word(word):
    """Collapse a unit-step word to ``(gen, power)`` runs, e.g. [(1,1),(1,1)] -> [(1,2)]."""
    out = []
    for gen, p in word:
        if out and out[-1][0] == gen:
            out[-1] = (gen, out[-1][1] + p)
            if out[-1][1] == 0:
                out.pop()
        else:
            out.append((gen, p))
    return out


def _key(U, ndigits=6):
    return tuple(np.round([U[0, 0], U[0, 1], U[1, 0], U[1, 1]], ndigits).view(float))


def _result(word, target):
    U = evaluate_braid(word) if word else np.eye(2, dtype=complex)
    fid = gate_fidelity(U, target)
    return CompilationResult(word=list(word), gate=U, fidelity=fid,
                             length=len(word), error=1.0 - fid)


def brute_force(target, max_length=14, tolerance=1e-3):
    """BFS over braid words; return the first word with fidelity >= 1 - tolerance,
    else the best found within ``max_length``."""
    best = _result([], target)
    if best.fidelity >= 1 - tolerance:
        return best
    seen = {_key(np.eye(2, dtype=complex))}
    frontier = deque([([], np.eye(2, dtype=complex), None)])
    while frontier:
        word, U, last = frontier.popleft()
        if len(word) >= max_length:
            continue
        for step, M in _UNITS:
            if last is not None and step == _INVERSE[last]:
                continue                          # prune immediate cancellation
            nU = U @ M
            k = _key(nU)
            if k in seen:
                continue
            seen.add(k)
            nword = word + [step]
            fid = gate_fidelity(nU, target)
            if fid > best.fidelity:
                best = CompilationResult(word=list(nword), gate=nU, fidelity=fid,
                                         length=len(nword), error=1.0 - fid)
                if fid >= 1 - tolerance:
                    return best
            frontier.append((nword, nU, step))
    return best


def golden(target, max_power=40, tolerance=1e-3, refine=6):
    """Approximate ``target`` by a power of the golden gate, then a short
    brute-force refinement of the residual."""
    G = golden_gate()
    best = _result([], target)
    word_word = golden_word()
    U = np.eye(2, dtype=complex)
    acc_word = []
    for n in range(1, max_power + 1):
        U = U @ G
        acc_word = acc_word + word_word
        fid = gate_fidelity(U, target)
        if fid > best.fidelity:
            best = CompilationResult(word=list(acc_word), gate=U, fidelity=fid,
                                     length=len(acc_word), error=1.0 - fid)
            if fid >= 1 - tolerance:
                return best
    # refine: brute-force the residual target' = target * U_best^-1 to `refine` length
    if best.fidelity < 1 - tolerance and best.word:
        residual = target @ np.linalg.inv(best.gate)
        r = brute_force(residual, max_length=refine, tolerance=tolerance)
        combined = r.word + best.word
        cand = _result(combined, target)
        if cand.fidelity > best.fidelity:
            best = cand
    return best


def golden_word():
    from .gates import golden_gate_word
    return golden_gate_word()


_METHODS = {"brute_force": brute_force, "golden": golden}


def compile_gate(target, max_length=14, tolerance=1e-3, method="brute_force"):
    """Compile ``target`` (a 2x2 unitary) into a braid word.

    Parameters
    ----------
    target : np.ndarray        2x2 unitary to approximate.
    max_length : int           max braid word length (brute_force).
    tolerance : float          required error ``1 - fidelity``.
    method : str               'brute_force' or 'golden'.
    """
    if method not in _METHODS:
        raise ValueError(f"method must be one of {sorted(_METHODS)}, got {method!r}")
    if method == "brute_force":
        return brute_force(target, max_length=max_length, tolerance=tolerance)
    return golden(target, tolerance=tolerance)
