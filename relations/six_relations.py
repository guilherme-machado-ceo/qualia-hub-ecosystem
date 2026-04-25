"""
The six significance relations rho_1 through rho_6.

Each relation evaluates a different depth of connection between algorithms:
    rho_6 (Compensacao) => rho_5 (Equilibrio) => rho_4 (Simetria)
        => rho_3 (Equivalencia) => rho_2 (Homologia) => rho_1 (Similitude)

Properties:
    rho_1: Reflexive, Symmetric, NOT transitive (sorites)
    rho_2: Reflexive, NOT symmetric, Transitive
    rho_3: Reflexive, Symmetric, Transitive (equivalence relation)
    rho_4: Reflexive, Symmetric, Transitive (group orbits)
    rho_5: Symmetric, NOT reflexive, NOT transitive
    rho_6: Symmetric, NOT reflexive, NOT transitive

Reference:
    Paper 3: doi.org/10.5281/zenodo.18776401 (Definitions 3.1-3.6, Theorem 3.1)
"""

from __future__ import annotations
import math
from typing import Callable, Dict, List, Tuple
from dataclasses import dataclass


@dataclass
class RelationProperties:
    """Formal properties of a binary relation."""
    reflexive: bool
    symmetric: bool
    transitive: bool


# Properties of each relation
RELATION_PROPERTIES: Dict[int, RelationProperties] = {
    1: RelationProperties(reflexive=True, symmetric=True, transitive=False),
    2: RelationProperties(reflexive=True, symmetric=False, transitive=True),
    3: RelationProperties(reflexive=True, symmetric=True, transitive=True),
    4: RelationProperties(reflexive=True, symmetric=True, transitive=True),
    5: RelationProperties(reflexive=False, symmetric=True, transitive=False),
    6: RelationProperties(reflexive=False, symmetric=True, transitive=False),
}


def rho1_similitude(x: List[float], y: List[float], eps: float = 0.1) -> float:
    """rho_1: Similitude - surface-level similarity.

    x rho_1 y iff d(phi(x), phi(y)) < epsilon
    Reflexive, symmetric, NOT transitive (sorites paradox).
    Maps to: Gestalt proximity, lexical similarity, Peircean iconic relation.

    Args:
        x, y: Feature vectors to compare.
        eps: Tolerance threshold.

    Returns:
        Similarity score in [0, 1].
    """
    if len(x) != len(y):
        return 0.0
    diff = sum((a - b) ** 2 for a, b in zip(x, y))
    dist = math.sqrt(diff / max(len(x), 1))
    score = max(0.0, 1.0 - dist / eps)
    return min(1.0, score)


def rho2_homology(
    x_struct: Dict[str, object],
    y_struct: Dict[str, object],
) -> float:
    """rho_2: Homology - structural correspondence.

    x rho_2 y iff exists isomorphism h: Struct(x) ~ Struct(y)
    Reflexive, NOT symmetric in general, transitive.
    Maps to: topological correspondence, structural design patterns.

    Args:
        x_struct, y_struct: Structural descriptors as dicts.

    Returns:
        Homology score in [0, 1].
    """
    if not x_struct or not y_struct:
        return 0.0
    keys_x = set(x_struct.keys())
    keys_y = set(y_struct.keys())
    common = keys_x & keys_y
    total = keys_x | keys_y
    if not total:
        return 0.0
    # Jaccard-like structural similarity
    structural_score = len(common) / len(total)
    # Value agreement on common keys
    value_scores = []
    for k in common:
        vx = x_struct[k]
        vy = y_struct[k]
        if isinstance(vx, (int, float)) and isinstance(vy, (int, float)):
            max_v = max(abs(vx), abs(vy), 1e-9)
            value_scores.append(1.0 - abs(vx - vy) / max_v)
        elif vx == vy:
            value_scores.append(1.0)
    value_score = sum(value_scores) / max(len(value_scores), 1)
    return 0.6 * structural_score + 0.4 * value_score


def rho3_equivalence(
    x_behavior: List[float],
    y_behavior: List[float],
    contexts: List[Callable],
) -> float:
    """rho_3: Equivalence - functional interchangeability.

    x rho_3 y iff for all C in contexts: C[x] ~= C[y]
    Reflexive, symmetric, transitive (proper equivalence relation).
    Maps to: Liskov substitution, semantic equivalence.

    Args:
        x_behavior, y_behavior: Behavioral profiles.
        contexts: List of context functions C_i.

    Returns:
        Equivalence score in [0, 1].
    """
    if len(x_behavior) != len(y_behavior):
        return 0.0
    total_diff = 0.0
    for c in contexts:
        cx = [c(xi) for xi in x_behavior]
        cy = [c(yi) for yi in y_behavior]
        total_diff += sum(abs(a - b) for a, b in zip(cx, cy))
    max_diff = len(contexts) * len(x_behavior) * 2.0
    if max_diff < 1e-9:
        return 1.0
    return max(0.0, 1.0 - total_diff / max_diff)


def rho4_symmetry(
    x: List[float],
    y: List[float],
    tolerance: float = 0.01,
) -> float:
    """rho_4: Symmetry - transformational invariance.

    x rho_4 y iff exists T in G: T(x)=y AND T^-1(y)=x
    Reflexive, symmetric, transitive (classes = group orbits).
    Maps to: Noether theorem, group theory, invariance.

    Returns:
        Symmetry score in [0, 1].
    """
    if len(x) != len(y):
        return 0.0
    # Check if y can be obtained from x by a simple transformation
    # Test: reflection, rotation, scaling
    n = len(x)

    # Test reflection
    reflected = x[::-1]
    ref_score = sum(1.0 - min(abs(a - b) / max(abs(a), abs(b), 1e-9), 1.0)
                    for a, b in zip(reflected, y)) / n

    # Test negation
    negated = [-v for v in x]
    neg_score = sum(1.0 - min(abs(a - b) / max(abs(a), abs(b), 1e-9), 1.0)
                    for a, b in zip(negated, y)) / n

    # Test cyclic rotation
    best_rot = 0.0
    for shift in range(1, n):
        rotated = x[shift:] + x[:shift]
        rot_score = sum(1.0 - min(abs(a - b) / max(abs(a), abs(b), 1e-9), 1.0)
                        for a, b in zip(rotated, y)) / n
        best_rot = max(best_rot, rot_score)

    return max(ref_score, neg_score, best_rot)


def rho5_equilibrium(
    x_potential: float,
    y_potential: float,
    dynamic_tolerance: float = 0.1,
) -> float:
    """rho_5: Equilibrium - potential balance.

    x rho_5 y iff Phi(x) + Phi(y) = 0 (static)
    OR d/dt[Phi(x) + Phi(y)] = 0 (dynamic)
    NOT reflexive, symmetric, NOT transitive.
    Maps to: Nash equilibrium, visual balance, potential theory.

    Returns:
        Equilibrium score in [0, 1].
    """
    total = abs(x_potential + y_potential)
    magnitude = abs(x_potential) + abs(y_potential)
    if magnitude < 1e-9:
        return 1.0
    ratio = total / magnitude
    score = max(0.0, 1.0 - ratio / dynamic_tolerance)
    return min(1.0, score)


def rho6_compensation(
    x_delta: float,
    y_delta: float,
    x_omega: float,
    y_omega: float,
    combined_omega: float,
) -> float:
    """rho_6: Compensation - complementarity with emergence.

    x rho_6 y iff:
        1) delta(x) = -delta(y) (complementarity)
        2) Omega(x + y) > Omega(x) + Omega(y) (emergence)
    NOT reflexive, symmetric, NOT transitive.
    Maps to: Hegelian synthesis, musical counterpoint, ecological mutualism.

    Args:
        x_delta, y_delta: Changes/transformations.
        x_omega, y_omega: Individual complexity measures.
        combined_omega: Combined complexity measure.

    Returns:
        Compensation score in [0, 1].
    """
    # Complementarity: deltas should be opposite
    complementarity_score = max(0.0, 1.0 - abs(x_delta + y_delta) /
                                max(abs(x_delta), abs(y_delta), 1e-9))
    # Emergence: combined should exceed sum
    expected = x_omega + y_omega
    if expected < 1e-9:
        emergence_score = 1.0
    else:
        emergence_ratio = combined_omega / expected
        emergence_score = max(0.0, min(1.0, emergence_ratio - 1.0))

    return 0.5 * complementarity_score + 0.5 * emergence_score


def evaluate_all_relations(
    x: List[float],
    y: List[float],
) -> Dict[str, float]:
    """Evaluate all 6 relations between two profiles at once.

    Returns dict with scores for rho_1 through rho_6.
    """
    x_sum = sum(x) if x else 0.0
    y_sum = sum(y) if y else 0.0
    x_mean = x_sum / max(len(x), 1)
    y_mean = y_sum / max(len(y), 1)
    identity = lambda v: v  # noqa: E731
    square = lambda v: v * v  # noqa: E731

    return {
        "rho_1_similitude": rho1_similitude(x, y),
        "rho_2_homology": rho2_homology(
            {"mean": x_mean, "sum": x_sum, "len": len(x)},
            {"mean": y_mean, "sum": y_sum, "len": len(y)},
        ),
        "rho_3_equivalence": rho3_equivalence(x, y, [identity, square]),
        "rho_4_symmetry": rho4_symmetry(x, y),
        "rho_5_equilibrium": rho5_equilibrium(x_sum, -y_sum),
        "rho_6_compensation": rho6_compensation(
            x_mean, -y_mean,
            math.sqrt(sum(v**2 for v in x)),
            math.sqrt(sum(v**2 for v in y)),
            math.sqrt(sum((a+b)**2 for a, b in zip(x, y))),
        ),
    }


if __name__ == "__main__":
    print("=" * 60)
    print("Six Significance Relations Demo")
    print("=" * 60)

    # Show properties
    print("\nFormal properties:")
    print(f"  {'Rel':<6} | {'Reflex':>6} | {'Sym':>6} | {'Trans':>6}")
    print("  " + "-" * 32)
    names = {1: "rho_1", 2: "rho_2", 3: "rho_3",
             4: "rho_4", 5: "rho_5", 6: "rho_6"}
    for k, p in RELATION_PROPERTIES.items():
        print(f"  {names[k]:<6} | {str(p.reflexive):>6} "
              f"| {str(p.symmetric):>6} | {str(p.transitive):>6}")

    # Evaluate relations between profiles
    profiles = {
        "Algorithm_A": [0.9, 0.8, 0.7, 0.5, 0.3, 0.1],
        "Algorithm_B": [0.85, 0.75, 0.65, 0.45, 0.25, 0.1],
        "Algorithm_C": [0.3, 0.5, 0.8, 0.9, 0.7, 0.5],
    }

    pairs = [("Algorithm_A", "Algorithm_B"),
             ("Algorithm_A", "Algorithm_C"),
             ("Algorithm_B", "Algorithm_C")]

    for name_a, name_b in pairs:
        scores = evaluate_all_relations(profiles[name_a], profiles[name_b])
        print(f"\n{name_a} vs {name_b}:")
        for rel, score in scores.items():
            print(f"  {rel:<24}: {score:.4f}")
