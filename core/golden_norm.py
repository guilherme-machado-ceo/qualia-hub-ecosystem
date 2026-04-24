"""
Golden-weighted norm and significance vector.

Implements f(A) = sqrt(sum phi^(k-1) * [f_rho_k(A)]^2)
and the complete expression Pi(A) = (sum ...)^(1/(2*pi)).

Maximum value: f_max ~ 5.236 (when all f_rho_k = 1).

Reference:
    Paper 3: doi.org/10.5281/zenodo.18776401 (Definitions 5.1, 5.2, 6.1)
"""

from __future__ import annotations
import math
from typing import List, Tuple
import numpy as np

PHI = (1.0 + math.sqrt(5.0)) / 2.0  # Golden ratio ~1.618034
PI = math.pi
NUM_RELATIONS = 6


def golden_weights() -> List[float]:
    """Return the 6 golden weights [phi^0, phi^1, ..., phi^5]."""
    return [PHI ** k for k in range(NUM_RELATIONS)]


def golden_norm(significance: List[float]) -> float:
    """Compute the golden norm f(A).

    f(A) = sqrt(sum_{k=1}^{6} phi^(k-1) * [f_rho_k(A)]^2)

    Args:
        significance: List of 6 values f_rho_k in [0, 1].

    Returns:
        Golden-weighted norm value (max ~ 5.236).
    """
    if len(significance) != NUM_RELATIONS:
        raise ValueError(
            f"Expected {NUM_RELATIONS} relations, got {len(significance)}"
        )
    weights = golden_weights()
    total = sum(w * s ** 2 for w, s in zip(weights, significance))
    return math.sqrt(total)


def max_golden_norm() -> float:
    """Maximum possible value of f(A) when all f_rho_k = 1.

    f_max = sqrt((phi^6 - 1) / (phi - 1)) ~ 5.236
    """
    return math.sqrt((PHI ** 6 - 1) / (PHI - 1))


def complete_expression(significance: List[float]) -> float:
    """Compute the complete pi*sqrt expression.

    Pi(A) = (sum_{k=1}^{6} phi^(k-1) * [f_rho_k(A)]^2)^(1/(2*pi))

    The exponent 1/(2*pi) is the inverse of a full circle in radians.
    Significance = golden-weighted evaluation raised to inverse of rotation.
    """
    if len(significance) != NUM_RELATIONS:
        raise ValueError(
            f"Expected {NUM_RELATIONS} relations, got {len(significance)}"
        )
    weights = golden_weights()
    total = sum(w * s ** 2 for w, s in zip(weights, significance))
    return total ** (1.0 / (2.0 * PI))


def normalize_significance(significance: List[float]) -> List[float]:
    """Normalize significance vector to [0, 1] range.

    Enforces monotonicity: f_rho_j <= f_rho_i for j > i.
    """
    result = [max(0.0, min(1.0, s)) for s in significance]
    # Enforce monotonicity (implication chain requires deeper <= shallower)
    for i in range(1, len(result)):
        result[i] = min(result[i], result[i - 1])
    return result


def significance_angle(a: List[float], b: List[float]) -> float:
    """Compute the significance angle theta between two profiles.

    cos(theta) = (a . b) / (||a|| * ||b||) using golden weights.

    Analogous to Fubini-Study angle on the real projective space.
    """
    if len(a) != len(b):
        raise ValueError("Profiles must have same length")
    weights = golden_weights()
    dot = sum(w * ai * bi for w, ai, bi in zip(weights, a, b))
    norm_a = golden_norm(a)
    norm_b = golden_norm(b)
    if norm_a < 1e-15 or norm_b < 1e-15:
        return float("inf")
    cos_theta = dot / (norm_a * norm_b)
    cos_theta = max(-1.0, min(1.0, cos_theta))
    return math.acos(cos_theta)


class SignificanceVector:
    """Represents a 6-dimensional significance profile f_vec(A)."""

    NAMES = [
        "rho_1_similitude",
        "rho_2_homology",
        "rho_3_equivalence",
        "rho_4_symmetry",
        "rho_5_equilibrium",
        "rho_6_compensation",
    ]

    def __init__(self, values: List[float], label: str = "") -> None:
        if len(values) != NUM_RELATIONS:
            raise ValueError(f"Expected {NUM_RELATIONS} values")
        self.values = normalize_significance(values[:])
        self.label = label

    @property
    def golden_norm(self) -> float:
        return golden_norm(self.values)

    @property
    def pi_radical(self) -> float:
        return complete_expression(self.values)

    @property
    def is_consistent(self) -> bool:
        """Check if the profile respects the implication chain."""
        return all(
            self.values[i] <= self.values[i - 1] + 1e-9
            for i in range(1, NUM_RELATIONS)
        )

    def binary_profile(self, threshold: float = 0.5) -> Tuple[int, ...]:
        """Convert to binary profile (analogous to lattice element)."""
        return tuple(1 if v >= threshold else 0 for v in self.values)

    def __repr__(self) -> str:
        vals = ", ".join(f"{v:.3f}" for v in self.values)
        return f"SignificanceVector([{vals}], gn={self.golden_norm:.4f})"


if __name__ == "__main__":
    print("=" * 60)
    print("Golden Norm and Significance Vector demo")
    print("=" * 60)

    weights = golden_weights()
    print(f"\nGolden weights: {[f'{w:.3f}' for w in weights]}")
    print(f"Maximum golden norm: {max_golden_norm():.6f}")

    # Test profiles
    profiles = [
        ([1.0, 1.0, 1.0, 1.0, 1.0, 1.0], "Plenitude"),
        ([1.0, 0.8, 0.6, 0.4, 0.3, 0.1], "Typical algorithm"),
        ([0.9, 0.3, 0.3, 0.7, 0.2, 0.5], "Anomalous (Shor)"),
        ([0.0, 0.0, 0.0, 0.0, 0.0, 0.0], "Semiotic void"),
    ]
    print(f"\n{'Profile':<20} | {'f(A)':>8} | {'Pi(A)':>8} | {'Consistent':>10}")
    print("  " + "-" * 54)
    for vals, label in profiles:
        sv = SignificanceVector(vals, label)
        print(
            f"  {label:<20} | {sv.golden_norm:>8.4f} "
            f"| {sv.pi_radical:>8.4f} | {str(sv.is_consistent):>10}"
        )

    # Significance angle
    a = SignificanceVector([1.0, 0.9, 0.7, 0.5, 0.3, 0.1])
    b = SignificanceVector([0.8, 0.7, 0.6, 0.4, 0.2, 0.1])
    theta = significance_angle(a.values, b.values)
    print(f"\nSignificance angle between profiles: {math.degrees(theta):.2f} deg")
