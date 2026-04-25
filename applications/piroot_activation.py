"""
PiRoot as a machine learning activation function.

PiRoot(x) = sign(x) * |x|^(1/pi)

Key properties:
- Infinite gradient at 0 (amplifies weak signals)
- Gradient compression for large values
- 3 fixed points: {-1, 0, 1}
- Surjective: R -> R

Potential application: amplify gradients in barren plateau regions
of variational quantum circuits (Paper 2, Open Problem 3).

Reference:
    Paper 3: doi.org/10.5281/zenodo.18776401 (Definition 11.3, Proposition 11.1)
    Paper 2: doi.org/10.5281/zenodo.18776462 (barren plateaus note)
"""

from __future__ import annotations
import math
from typing import List, Tuple
import numpy as np

PI = math.pi
PI_INV = 1.0 / PI


class PiRootLayer:
    """PiRoot activation layer for neural networks."""

    def __init__(self, trainable_bias: bool = False) -> None:
        self.bias = 0.0
        self.trainable_bias = trainable_bias

    def forward(self, x: np.ndarray) -> np.ndarray:
        """Forward pass: PiRoot(x) = sign(x) * |x|^(1/pi)."""
        return np.sign(x) * np.abs(x) ** PI_INV

    def gradient(self, x: np.ndarray) -> np.ndarray:
        """Backward pass gradient.

        d/dx PiRoot(x) = (1/pi) * |x|^((1-pi)/pi)
        """
        abs_x = np.abs(x)
        safe_x = np.where(abs_x < 1e-15, 1e-15, abs_x)
        return PI_INV * safe_x ** ((1.0 - PI) / PI)

    def __call__(self, x: np.ndarray) -> np.ndarray:
        return self.forward(x)


def compare_activations(
    x_values: List[float],
) -> List[dict]:
    """Compare PiRoot with standard activation functions.

    Returns list of dicts with values for PiRoot, ReLU, sigmoid, tanh.
    """
    results = []
    for x in x_values:
        piroot = math.copysign(abs(x) ** PI_INV, x)
        relu = max(0.0, x)
        sigmoid = 1.0 / (1.0 + math.exp(-x))
        tanh = math.tanh(x)
        piroot_grad = PI_INV * max(abs(x), 1e-15) ** ((1.0 - PI) / PI) if x != 0 else float("inf")
        relu_grad = 1.0 if x > 0 else 0.0
        sig_grad = sigmoid * (1.0 - sigmoid)
        tanh_grad = 1.0 - tanh ** 2

        results.append({
            "x": x,
            "PiRoot": piroot,
            "ReLU": relu,
            "sigmoid": sigmoid,
            "tanh": tanh,
            "PiRoot_grad": piroot_grad,
            "ReLU_grad": relu_grad,
            "sigmoid_grad": sig_grad,
            "tanh_grad": tanh_grad,
        })
    return results


def barren_plateau_analysis() -> dict:
    """Analyze PiRoot behavior in barren plateau regions.

    In barren plateaus, gradients are exponentially small in the
    number of qubits n: grad ~ O(2^{-n}).

    PiRoot amplifies small gradients by factor (1/pi) * |x|^((1-pi)/pi).
    As x -> 0: |gradient| -> infinity, potentially counteracting the plateau.
    """
    analysis = {
        "description": (
            "PiRoot has infinite gradient sensitivity at x=0, which could "
            "amplify exponentially vanishing gradients in variational circuits. "
            "This is speculative (Paper 2, Open Problem 3) and requires "
            "empirical validation."
        ),
        "small_gradient_amplification": [],
    }
    for log_x in range(-10, -1):
        x = 10.0 ** log_x
        piroot_grad = PI_INV * x ** ((1.0 - PI) / PI)
        amplification = piroot_grad  # vs identity gradient = 1
        analysis["small_gradient_amplification"].append({
            "x": x,
            "x_exp": log_x,
            "PiRoot_gradient": piroot_grad,
            "amplification_vs_identity": amplification,
        })
    return analysis


if __name__ == "__main__":
    print("=" * 60)
    print("PiRoot Activation Function Analysis")
    print("=" * 60)

    # Activation comparison
    print("\nActivation function comparison:")
    results = compare_activations([0.001, 0.01, 0.1, 0.5, 1.0, 2.0, 5.0, 10.0])
    print(f"  {'x':>8} | {'PiRoot':>8} | {'ReLU':>8} | {'sigm':>8} "
          f"| {'tanh':>8} | {'PiRoot_g':>10}")
    print("  " + "-" * 56)
    for r in results:
        pg = f"{r['PiRoot_grad']:.2f}" if r["PiRoot_grad"] < 1000 else "inf"
        print(f"  {r['x']:>8.3f} | {r['PiRoot']:>8.4f} | {r['ReLU']:>8.4f} "
              f"| {r['sigmoid']:>8.4f} | {r['tanh']:>8.4f} | {pg:>10}")

    # Barren plateau analysis
    print("\nBarren plateau gradient amplification:")
    bp = barren_plateau_analysis()
    for entry in bp["small_gradient_amplification"]:
        print(f"  x=10^{entry['x_exp']:<3} : "
              f"PiRoot_grad={entry['PiRoot_gradient']:>12.2f} "
              f"(amplification={entry['amplification_vs_identity']:>12.2f}x)")

    # Fixed points
    print("\nFixed points of PiRoot: -1, 0, 1")
    layer = PiRootLayer()
    for fp in [-1.0, 0.0, 1.0]:
        result = layer.forward(np.array([fp]))[0]
        print(f"  PiRoot({fp}) = {result:.6f}")

    # Note about barren plateaus
    print(f"\nBarren plateau note:")
    print(f"  {bp['description']}")
