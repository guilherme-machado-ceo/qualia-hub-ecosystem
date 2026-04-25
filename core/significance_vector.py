"""
Significance vector management and operations.

Provides high-level operations on 6-dimensional significance profiles
including comparison, combination, and semiring operations.

Reference:
    Paper 3: doi.org/10.5281/zenodo.18776401 (Chapters 5, 7, 8)
"""

from __future__ import annotations
import math
from typing import List, Optional, Tuple
from core.golden_norm import (
    golden_norm,
    golden_weights,
    normalize_significance,
    complete_expression,
)


class SignificanceProfile:
    """Full significance profile with algebraic operations.

    Supports semiring operations:
    - Addition (point-wise max): a + b
    - Multiplication (point-wise product): a * b
    - Zero: all-zeros profile
    - One: all-ones profile
    """

    ZERO = [0.0] * 6
    ONE = [1.0] * 6

    def __init__(self, values: List[float], name: str = "A") -> None:
        if len(values) != 6:
            raise ValueError("Profile must have exactly 6 dimensions")
        self.values = normalize_significance(values[:])
        self.name = name

    @property
    def f_norm(self) -> float:
        """Golden-weighted norm f(A)."""
        return golden_norm(self.values)

    @property
    def pi_value(self) -> float:
        """Complete pi*sqrt expression Pi(A)."""
        return complete_expression(self.values)

    @property
    def binary(self) -> Tuple[int, ...]:
        """Binary representation (threshold=0.5)."""
        return tuple(1 if v >= 0.5 else 0 for v in self.values)

    def add(self, other: SignificanceProfile) -> SignificanceProfile:
        """Semiring addition: point-wise maximum."""
        result = [max(a, b) for a, b in zip(self.values, other.values)]
        return SignificanceProfile(result, f"{self.name}+{other.name}")

    def multiply(self, other: SignificanceProfile) -> SignificanceProfile:
        """Semiring multiplication: point-wise product."""
        result = [a * b for a, b in zip(self.values, other.values)]
        return SignificanceProfile(result, f"{self.name}*{other.name}")

    @staticmethod
    def zero() -> SignificanceProfile:
        return SignificanceProfile(SignificanceProfile.ZERO[:], "0")

    @staticmethod
    def one() -> SignificanceProfile:
        return SignificanceProfile(SignificanceProfile.ONE[:], "1")

    def dominates(self, other: SignificanceProfile) -> bool:
        """Check if self dominates other component-wise."""
        return all(a >= b - 1e-9 for a, b in zip(self.values, other.values))

    def depth(self) -> int:
        """Return the depth of active relations (count of non-zero)."""
        return sum(1 for v in self.values if v > 1e-9)

    def describe(self) -> str:
        """Human-readable description of the profile."""
        labels = ["Similaridade", "Homologia", "Equivalencia",
                   "Simetria", "Equilibrio", "Compensacao"]
        active = []
        for i, v in enumerate(self.values):
            if v >= 0.5:
                active.append(labels[i])
        if not active:
            return "Vazio semiotico (nenhuma relacao ativa)"
        return "Relacoes ativas: " + ", ".join(active)

    def __repr__(self) -> str:
        vals = ", ".join(f"{v:.2f}" for v in self.values)
        return f"Profile({self.name}: [{vals}], f={self.f_norm:.3f})"


if __name__ == "__main__":
    print("=" * 60)
    print("Significance Profile Operations")
    print("=" * 60)

    # Create example profiles
    p1 = SignificanceProfile([0.95, 0.85, 0.7, 0.6, 0.3, 0.2], "Shor")
    p2 = SignificanceProfile([0.9, 0.75, 0.5, 0.7, 0.6, 0.9], "VQE")
    p3 = SignificanceProfile([0.7, 0.8, 0.5, 0.6, 0.7, 0.7], "QAOA")

    for p in [p1, p2, p3]:
        print(f"\n{p}")
        print(f"  Pi(A) = {p.pi_value:.6f}")
        print(f"  Binary: {p.binary}")
        print(f"  Depth: {p.depth()}")
        print(f"  {p.describe()}")

    # Semiring operations
    print("\n--- Semiring Operations ---")
    z = SignificanceProfile.zero()
    o = SignificanceProfile.one()
    print(f"Zero: {z}")
    print(f"One:  {o}")

    s = p1.add(p2)
    print(f"\nShor + VQE: {s}")
    m = p1.multiply(p2)
    print(f"Shor * VQE: {m}")

    print(f"\nShor dominates VQE? {p1.dominates(p2)}")
    print(f"Shor dominates QAOA? {p1.dominates(p3)}")
