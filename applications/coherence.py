"""
Coherence function and semiring operations.

Implements:
- Coherence: Coh(A,B) = f(A) . f(B) (golden-weighted dot product)
- Cauchy-Schwarz inequality: Coh(A,B)^2 <= Coh(A,A) * Coh(B,B)
- Commutative semiring (Alg, +, *, 0, 1)

Reference:
    Paper 3: doi.org/10.5281/zenodo.18776401 (Theorem 7.1, Theorem 8.2)
"""

from __future__ import annotations
import math
from typing import Dict, List, Optional, Tuple
import numpy as np

PHI = (1.0 + math.sqrt(5.0)) / 2.0


def golden_weights() -> List[float]:
    return [PHI ** k for k in range(6)]


def coherence(a: List[float], b: List[float]) -> float:
    """Compute coherence Coh(A,B) = sum phi^k * f_k(A) * f_k(B).

    Golden-weighted dot product between two significance profiles.
    """
    if len(a) != len(b):
        raise ValueError("Profiles must have same length")
    weights = golden_weights()
    return sum(w * ai * bi for w, ai, bi in zip(weights, a, b))


def self_coherence(a: List[float]) -> float:
    """Coh(A,A) = golden norm squared."""
    return coherence(a, a)


def cauchy_schwarz_check(a: List[float], b: List[float]) -> Dict:
    """Verify Cauchy-Schwarz: Coh(A,B)^2 <= Coh(A,A) * Coh(B,B).

    Equality holds iff profiles are proportional.
    """
    cab = coherence(a, b)
    caa = self_coherence(a)
    cbb = self_coherence(b)
    lhs = cab ** 2
    rhs = caa * cbb
    is_equal = abs(lhs - rhs) < 1e-9
    return {
        "Coh(A,B)": cab,
        "Coh(A,A)": caa,
        "Coh(B,B)": cbb,
        "Coh(A,B)^2": lhs,
        "Coh(A,A)*Coh(B,B)": rhs,
        "inequality_holds": lhs <= rhs + 1e-9,
        "equality": is_equal,
    }


class SemiringProfile:
    """Profile with semiring operations.

    (Alg, +, *, 0, 1) forms a commutative semiring:
    - (Alg, +, 0): commutative monoid (addition = point-wise max)
    - (Alg, *, 1): commutative monoid (multiplication = point-wise product)
    - * distributes over +
    - 0 is absorbing for *
    """

    def __init__(self, values: List[float], name: str = "A") -> None:
        if len(values) != 6:
            raise ValueError("Expected 6 values")
        self.values = [max(0.0, min(1.0, v)) for v in values]
        self.name = name

    def __add__(self, other: "SemiringProfile") -> "SemiringProfile":
        """Semiring addition: point-wise maximum."""
        result = [max(a, b) for a, b in zip(self.values, other.values)]
        return SemiringProfile(result, f"{self.name}+{other.name}")

    def __mul__(self, other: "SemiringProfile") -> "SemiringProfile":
        """Semiring multiplication: point-wise product."""
        result = [a * b for a, b in zip(self.values, other.values)]
        return SemiringProfile(result, f"{self.name}*{other.name}")

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, SemiringProfile):
            return NotImplemented
        return all(abs(a - b) < 1e-9 for a, b in zip(self.values, other.values))

    def __repr__(self) -> str:
        vals = ", ".join(f"{v:.2f}" for v in self.values)
        return f"Semiring({self.name}: [{vals}])"

    def coherence_with(self, other: "SemiringProfile") -> float:
        return coherence(self.values, other.values)


@staticmethod
def semiring_zero() -> "SemiringProfile":
    return SemiringProfile([0.0] * 6, "0")


@staticmethod
def semiring_one() -> "SemiringProfile":
    return SemiringProfile([1.0] * 6, "1")


if __name__ == "__main__":
    print("=" * 60)
    print("Coherence and Semiring Operations")
    print("=" * 60)

    # Coherence examples
    profiles = {
        "Plenitude": [1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
        "Stability": [1.0, 1.0, 1.0, 1.0, 1.0, 0.0],
        "Interchange": [1.0, 1.0, 1.0, 0.0, 0.0, 0.0],
        "Appearance": [1.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    }

    names = list(profiles.keys())
    print(f"\nCoherence matrix:")
    header = f"  {'':<14}" + "".join(f"| {n:<14}" for n in names)
    print(header)
    print("  " + "-" * len(header))
    for n1 in names:
        row = f"  {n1:<14}"
        for n2 in names:
            c = coherence(profiles[n1], profiles[n2])
            row += f"| {c:>14.4f}"
        print(row)

    # Cauchy-Schwarz verification
    print(f"\nCauchy-Schwarz checks:")
    pairs = [("Plenitude", "Stability"), ("Interchange", "Appearance")]
    for n1, n2 in pairs:
        cs = cauchy_schwarz_check(profiles[n1], profiles[n2])
        print(f"  {n1} vs {n2}: inequality={cs['inequality_holds']}, "
              f"equality={cs['equality']}")

    # Semiring operations
    print(f"\nSemiring operations:")
    a = SemiringProfile([0.8, 0.6, 0.4, 0.3, 0.2, 0.1], "A")
    b = SemiringProfile([0.5, 0.7, 0.3, 0.5, 0.1, 0.0], "B")
    z = SemiringProfile([0.0] * 6, "0")
    o = SemiringProfile([1.0] * 6, "1")

    print(f"  {a}")
    print(f"  {b}")
    print(f"  A + B = {a + b}")
    print(f"  A * B = {a * b}")
    print(f"  A * 0 = {a * z}")
    print(f"  A * 1 = {a * o}")
    print(f"  A + 0 = {a + z}")
    print(f"  Distributive: A*(B+0) == A*B + A*0? {(a * (b + z)) == (a * b + a * z)}")
