"""
W matrix: 5x5 operative coupling matrix and fixed-point computation.

Implements the iterative fixed-point equation:
    o(A) = sigma(W . o(A) + b(A))

Fixed-point exists if ||W|| < 1 (contraction mapping).
Spectral radius dynamics: rho(W)<1 convergence, =1 borderline, >1 divergence.

Topology presets: sequential, pipeline, recurrent, attentive, full network.

Reference:
    Paper 3: doi.org/10.5281/zenodo.18776401 (Definition 2.3, Theorem 2.1, Def 10.4)
"""

from __future__ import annotations
import math
from typing import Dict, List, Optional, Tuple
import numpy as np

MODE_NAMES = ["Operationalize", "Process", "Distribute", "Infer", "Incide"]


def sequential_topology() -> List[List[float]]:
    """Sequential (von Neumann): subdiagonal matrix."""
    return [
        [0.0, 0.0, 0.0, 0.0, 0.0],
        [1.0, 0.0, 0.0, 0.0, 0.0],
        [0.0, 1.0, 0.0, 0.0, 0.0],
        [0.0, 0.0, 1.0, 0.0, 0.0],
        [0.0, 0.0, 0.0, 1.0, 0.0],
    ]


def pipeline_topology() -> List[List[float]]:
    """Pipeline: block-diagonal with 2 parallel stages."""
    return [
        [0.0, 0.5, 0.0, 0.0, 0.0],
        [0.5, 0.0, 0.0, 0.0, 0.0],
        [0.0, 0.0, 0.3, 0.3, 0.0],
        [0.0, 0.0, 0.3, 0.0, 0.3],
        [0.0, 0.0, 0.0, 0.3, 0.0],
    ]


def recurrent_topology() -> List[List[float]]:
    """Recurrent (RNN): dense with self-loops."""
    w = [[0.0] * 5 for _ in range(5)]
    for i in range(5):
        for j in range(5):
            if i == j:
                w[i][j] = 0.4
            elif abs(i - j) <= 1:
                w[i][j] = 0.2
            else:
                w[i][j] = 0.05
    return w


def attentive_topology() -> List[List[float]]:
    """Attentive (Transformer): sparse learned weights."""
    return [
        [0.1, 0.6, 0.2, 0.05, 0.05],
        [0.5, 0.1, 0.3, 0.05, 0.05],
        [0.1, 0.4, 0.1, 0.3, 0.1],
        [0.05, 0.05, 0.5, 0.1, 0.3],
        [0.05, 0.05, 0.1, 0.6, 0.2],
    ]


def full_network_topology() -> List[List[float]]:
    """Full network: all connections equally weighted."""
    val = 0.15
    return [[val] * 5 for _ in range(5)]


TOPOLOGY_PRESETS: Dict[str, callable] = {
    "sequential": sequential_topology,
    "pipeline": pipeline_topology,
    "recurrent": recurrent_topology,
    "attentive": attentive_topology,
    "full": full_network_topology,
}


class WMatrix:
    """5x5 operative coupling matrix with fixed-point analysis."""

    def __init__(self, weights: List[List[float]]) -> None:
        self.W = np.array(weights, dtype=np.float64)
        if self.W.shape != (5, 5):
            raise ValueError("W must be 5x5")

    @classmethod
    def from_topology(cls, name: str) -> "WMatrix":
        """Create from a preset topology name."""
        if name not in TOPOLOGY_PRESETS:
            raise ValueError(f"Unknown topology: {name}. "
                           f"Choose from: {list(TOPOLOGY_PRESETS.keys())}")
        return cls(TOPOLOGY_PRESETS[name]())

    @property
    def spectral_radius(self) -> float:
        """Compute spectral radius rho(W) = max|eigenvalue|."""
        eigenvalues = np.linalg.eigvals(self.W)
        return float(max(abs(e) for e in eigenvalues))

    @property
    def is_contraction(self) -> bool:
        """Check if ||W|| < 1 (contraction mapping)."""
        return self.spectral_radius < 1.0

    @property
    def dynamics_status(self) -> str:
        """Spectral radius dynamics classification."""
        rho = self.spectral_radius
        if rho < 1.0:
            return f"CONVERGENT (rho={rho:.4f} < 1)"
        elif abs(rho - 1.0) < 1e-9:
            return f"BORDERLINE (rho={rho:.4f} ~ 1)"
        else:
            return f"DIVERGENT (rho={rho:.4f} > 1)"

    def compute_fixed_point(
        self,
        bias: Optional[List[float]] = None,
        max_iter: int = 1000,
        tol: float = 1e-10,
    ) -> Tuple[np.ndarray, int, bool]:
        """Compute fixed point via iteration.

        o* = lim o^{(n)} where o^{(n+1)} = tanh(W . o^{(n)} + b)

        Returns (fixed_point_vector, iterations, converged).
        """
        if bias is None:
            bias = [0.1] * 5
        b = np.array(bias, dtype=np.float64)

        o = np.random.rand(5) * 0.1  # Small random init
        converged = False
        for i in range(max_iter):
            o_new = np.tanh(self.W @ o + b)
            if np.max(np.abs(o_new - o)) < tol:
                o = o_new
                converged = True
                break
            o = o_new
        return o, i + 1, converged

    def __repr__(self) -> str:
        return (f"WMatrix(shape={self.W.shape}, "
                f"rho={self.spectral_radius:.4f}, "
                f"contraction={self.is_contraction})")


if __name__ == "__main__":
    print("=" * 60)
    print("W Matrix and Fixed-Point Analysis")
    print("=" * 60)

    for name in TOPOLOGY_PRESETS:
        wm = WMatrix.from_topology(name)
        fp, iters, conv = wm.compute_fixed_point()
        print(f"\n--- {name.upper()} ---")
        print(f"  Status: {wm.dynamics_status}")
        print(f"  Fixed point converged: {conv} ({iters} iterations)")
        print(f"  Fixed point: {[f'{v:.4f}' for v in fp]}")
        print(f"  Mode contributions:")
        for i, mode_name in enumerate(MODE_NAMES):
            print(f"    {mode_name:<16}: {fp[i]:.4f}")
