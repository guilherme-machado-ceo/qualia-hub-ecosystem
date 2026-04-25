"""
pi-radical operator and PiRoot activation function.

Implements Pi(A) = [f(A)]^(1/pi) and its iterative convergence.
Also implements PiRoot(x) = sign(x) * |x|^(1/pi) as a neural network
activation function.

Reference:
    Paper 2: doi.org/10.5281/zenodo.18776462
    Paper 3: doi.org/10.5281/zenodo.18776401
"""

from __future__ import annotations
import math
from typing import List, Tuple, Optional
import numpy as np

PI = math.pi
PI_INV = 1.0 / PI  # ~0.31831


class PiRadical:
    """The pi-radical operator Pi(A) = [f(A)]^(1/pi).

    Key properties:
    - Convergence: lim Pi^n(A) = 1 for all f(A) > 0
    - Super-exponential with geometric ratio 1/pi
    - Irrationality: if f(A) in Q+, f(A) != 0,1, then Pi(A) not in Q
    - Fixed points: x in {-1, 0, 1}
    """

    def __init__(self, f_value: float) -> None:
        if f_value <= 0:
            raise ValueError("f(A) must be positive")
        self.f_value = f_value

    def evaluate(self) -> float:
        """Compute Pi(A) = [f(A)]^(1/pi)."""
        return self.f_value ** PI_INV

    def iterate(self, n: int) -> List[float]:
        """Compute iterative convergence Pi^n(A) = f(A)^(1/pi^n).

        After ~5 iterations, result is essentially 1.0.
        Returns list of values [Pi^1(A), Pi^2(A), ..., Pi^n(A)].
        """
        if n < 1:
            raise ValueError("n must be >= 1")
        values = []
        exponent = PI_INV
        for i in range(n):
            val = self.f_value ** exponent
            values.append(val)
            exponent = exponent / PI
        return values

    def converge(self, tol: float = 1e-10, max_iter: int = 20) -> Tuple[List[float], int]:
        """Iterate until |Pi^n(A) - 1| < tol.

        Returns (list_of_values, iterations_taken).
        """
        values = []
        for i in range(max_iter):
            val = self.f_value ** (PI_INV ** (i + 1))
            values.append(val)
            if abs(val - 1.0) < tol:
                return values, i + 1
        return values, max_iter

    def hermeneutic_information(self) -> float:
        """Total hermeneutic information = |f(A) - 1|.

        Measures total interpretive distance from unity.
        """
        return abs(self.f_value - 1.0)


class PiRootActivation:
    """PiRoot as a neural network activation function.

    PiRoot(x) = sign(x) * |x|^(1/pi)

    Properties:
    - Domain/Range: R -> R (surjective)
    - Strictly monotone increasing
    - Infinite sensitivity near 0 (gradient -> +inf)
    - Compression of large values (gradient -> 0+)
    - Fixed points: {-1, 0, 1}

    Gradient: d/dx PiRoot(x) = (1/pi) * |x|^((1-pi)/pi)
    """

    FIXED_POINTS = [-1.0, 0.0, 1.0]

    @staticmethod
    def forward(x: float | np.ndarray) -> float | np.ndarray:
        """Compute PiRoot(x) = sign(x) * |x|^(1/pi)."""
        x_arr = np.asarray(x, dtype=np.float64)
        result = np.sign(x_arr) * np.abs(x_arr) ** PI_INV
        if np.isscalar(x):
            return float(result)
        return result

    @staticmethod
    def gradient(x: float | np.ndarray) -> float | np.ndarray:
        """Compute gradient: (1/pi) * |x|^((1-pi)/pi).

        As x -> 0+: gradient -> +inf (amplifies weak signals).
        As x -> +inf: gradient -> 0+ (compresses strong signals).
        """
        x_arr = np.asarray(x, dtype=np.float64)
        abs_x = np.abs(x_arr)
        # Handle x=0 by returning a large finite value
        safe_x = np.where(abs_x < 1e-15, 1e-15, abs_x)
        grad = PI_INV * safe_x ** ((1.0 - PI) / PI)
        if np.isscalar(x):
            return float(grad)
        return grad

    @staticmethod
    def compare_with_other_activations(
        x: float
    ) -> dict:
        """Compare PiRoot with ReLU, sigmoid, and tanh at a given x."""
        relu = max(0.0, x)
        sigmoid = 1.0 / (1.0 + math.exp(-x))
        tanh = math.tanh(x)
        piroot = PiRootActivation.forward(x)
        return {
            "x": x,
            "PiRoot": piroot,
            "ReLU": relu,
            "sigmoid": sigmoid,
            "tanh": tanh,
        }


def golden_weight(k: int) -> float:
    """Return the golden weight phi^(k-1) for position k (1-indexed).

    phi = (1 + sqrt(5)) / 2 ~ 1.618034
    Weights: [1.0, 1.618, 2.618, 4.236, 6.854, 11.090]
    """
    phi = (1.0 + math.sqrt(5.0)) / 2.0
    return phi ** (k - 1)


if __name__ == "__main__":
    print("=" * 60)
    print("pi-radical operator demo")
    print("=" * 60)

    # Test PiRadical convergence
    test_values = [0.1, 1.0, 2.0, 5.0, 282.17, 1000.0]
    print("\nConvergence Pi^n(A) -> 1:")
    print(f"  {'f(A)':>8} | {'Pi(A)':>8} | {'Pi^5(A)':>10} | {'iters':>5}")
    print("  " + "-" * 42)
    for fv in test_values:
        pr = PiRadical(fv)
        vals = pr.iterate(5)
        conv_vals, iters = pr.converge()
        print(f"  {fv:>8.2f} | {vals[0]:>8.5f} | {vals[4]:>10.8f} | {iters:>5}")

    # Test PiRoot
    print("\nPiRoot activation comparison:")
    print(f"  {'x':>6} | {'PiRoot':>8} | {'ReLU':>8} | {'sigmoid':>8} | {'tanh':>8}")
    print("  " + "-" * 44)
    for x_val in [0.1, 0.5, 1.0, 2.0, 5.0, 10.0]:
        c = PiRootActivation.compare_with_other_activations(x_val)
        print(
            f"  {c['x']:>6.1f} | {c['PiRoot']:>8.4f} | {c['ReLU']:>8.4f} "
            f"| {c['sigmoid']:>8.4f} | {c['tanh']:>8.4f}"
        )

    # Test golden weights
    print("\nGolden weights for 6 positions:")
    for k in range(1, 7):
        print(f"  w_{k} = phi^{k-1} = {golden_weight(k):.6f}")

    print("\nFixed points of PiRoot:", PiRootActivation.FIXED_POINTS)
