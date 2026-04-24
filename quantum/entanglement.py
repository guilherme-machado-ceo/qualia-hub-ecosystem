"""
Entanglement as rho_6 and quantum information measures.

Implements:
- f_rho6(A,B) = S(rho_A) / ln(d) (entanglement as compensation)
- Von Neumann entropy: S(rho) = -Tr(rho * ln(rho))
- Quantum mutual information: I(A:B) = S(rho_A) + S(rho_B) - S(rho_AB)
- Concurrence for 2-qubit states

Reference:
    Paper 2: doi.org/10.5281/zenodo.18776462 (Propositions 3.1, 3.2)
"""

from __future__ import annotations
import math
from typing import Dict, List, Optional, Tuple
import numpy as np


def von_neumann_entropy(rho: np.ndarray) -> float:
    """Compute Von Neumann entropy S(rho) = -sum lambda_i * ln(lambda_i).

    Args:
        rho: Density matrix (Hermitian, positive semidefinite, trace=1).

    Returns:
        Entropy in nats (natural units).
    """
    eigenvalues = np.linalg.eigvalsh(rho)
    # Remove near-zero eigenvalues to avoid log(0)
    eigenvalues = eigenvalues[eigenvalues > 1e-12]
    eigenvalues = eigenvalues / np.sum(eigenvalues)  # Re-normalize
    entropy = -np.sum(eigenvalues * np.log(eigenvalues))
    return float(entropy)


def purity(rho: np.ndarray) -> float:
    """Compute purity Tr(rho^2). Range: [1/d, 1].

    purity = 1 for pure states, 1/d for maximally mixed.
    """
    return float(np.real(np.trace(rho @ rho)))


def mutual_information(
    rho_a: np.ndarray,
    rho_b: np.ndarray,
    rho_ab: np.ndarray,
) -> float:
    """Compute quantum mutual information I(A:B).

    I(A:B) = S(rho_A) + S(rho_B) - S(rho_AB)

    I > 0 for entangled states, I = 0 for separable states.
    """
    sa = von_neumann_entropy(rho_a)
    sb = von_neumann_entropy(rho_b)
    sab = von_neumann_entropy(rho_ab)
    return sa + sb - sab


def entanglement_as_rho6(rho_ab: np.ndarray, dim_a: int, dim_b: int) -> float:
    """Compute entanglement measure as rho_6 significance.

    f_rho6(A,B) = S(rho_A) / ln(d) where d = min(dim_A, dim_B).

    Range: 0 (separable) to 1 (maximally entangled).
    """
    # Compute reduced density matrix rho_A = Tr_B(rho_AB)
    rho_reshaped = rho_ab.reshape(dim_a, dim_b, dim_a, dim_b)
    rho_a = np.trace(rho_reshaped, axis1=1, axis2=3)
    rho_a = rho_a / np.trace(rho_a)  # Normalize

    s_a = von_neumann_entropy(rho_a)
    d = min(dim_a, dim_b)
    if d <= 1:
        return 0.0
    return min(1.0, s_a / math.log(d))


def concurrence_two_qubit(rho: np.ndarray) -> float:
    """Compute concurrence for a 2-qubit density matrix.

    C = max(0, lambda_1 - lambda_2 - lambda_3 - lambda_4)
    where lambda_i are square roots of eigenvalues of rho * tilde(rho)
    in decreasing order.

    Range: [0, 1] where 0 = separable, 1 = maximally entangled.
    """
    if rho.shape != (4, 4):
        raise ValueError("Expected 4x4 density matrix for 2-qubit system")

    # Pauli Y matrix
    sigma_y = np.array([[0, -1j], [1j, 0]])

    # Compute tilde(rho) = (sigma_y x sigma_y) * rho* * (sigma_y x sigma_y)
    sy_sy = np.kron(sigma_y, sigma_y)
    rho_conj = np.conj(rho)
    rho_tilde = sy_sy @ rho_conj @ sy_sy

    # Compute R = rho * rho_tilde
    R = rho @ rho_tilde

    # Eigenvalues of R
    eigvals = np.linalg.eigvals(R)
    eigvals = np.real(eigvals)
    eigvals = np.sort(eigvals)[::-1]

    # Square roots (take absolute to handle numerical errors)
    sqrt_eigvals = np.sqrt(np.maximum(eigvals, 0))

    # Concurrence
    C = sqrt_eigvals[0] - sqrt_eigvals[1] - sqrt_eigvals[2] - sqrt_eigvals[3]
    return float(max(0.0, C))


def bell_state(rho_type: str = "phi_plus") -> np.ndarray:
    """Generate a Bell state density matrix.

    Types:
    - phi_plus: (|00> + |11>) / sqrt(2)
    - phi_minus: (|00> - |11>) / sqrt(2)
    - psi_plus: (|01> + |10>) / sqrt(2)
    - psi_minus: (|01> - |10>) / sqrt(2)
    """
    states = {
        "phi_plus": np.array([1, 0, 0, 1]) / math.sqrt(2),
        "phi_minus": np.array([1, 0, 0, -1]) / math.sqrt(2),
        "psi_plus": np.array([0, 1, 1, 0]) / math.sqrt(2),
        "psi_minus": np.array([0, 1, -1, 0]) / math.sqrt(2),
    }
    psi = states.get(rho_type, states["phi_plus"])
    return np.outer(psi, psi.conj())


def separable_state() -> np.ndarray:
    """Generate a separable 2-qubit state |00>."""
    psi = np.array([1, 0, 0, 0], dtype=np.complex128)
    return np.outer(psi, psi.conj())


if __name__ == "__main__":
    print("=" * 60)
    print("Quantum Entanglement as rho_6")
    print("=" * 60)

    # Bell state analysis
    print("\nBell state |Phi+> = (|00> + |11>)/sqrt(2):")
    rho_bell = bell_state("phi_plus")
    print(f"  Purity: {purity(rho_bell):.6f} (1.0 = pure)")
    print(f"  Entanglement (rho_6): {entanglement_as_rho6(rho_bell, 2, 2):.6f}")
    print(f"  Concurrence: {concurrence_two_qubit(rho_bell):.6f}")

    # Reduced density matrices
    rho_reshaped = rho_bell.reshape(2, 2, 2, 2)
    rho_a = np.trace(rho_reshaped, axis1=1, axis2=3)
    rho_a = rho_a / np.trace(rho_a)
    print(f"  S(rho_A) = {von_neumann_entropy(rho_a):.6f} (max = ln2 = {math.log(2):.6f})")

    # Separable state
    print("\nSeparable state |00>:")
    rho_sep = separable_state()
    print(f"  Purity: {purity(rho_sep):.6f}")
    print(f"  Entanglement (rho_6): {entanglement_as_rho6(rho_sep, 2, 2):.6f}")
    print(f"  Concurrence: {concurrence_two_qubit(rho_sep):.6f}")

    # All 4 Bell states
    print("\nAll Bell states comparison:")
    print(f"  {'State':<12} | {'Purity':>8} | {'rho_6':>8} | {'Concurrence':>11}")
    print("  " + "-" * 46)
    for name in ["phi_plus", "phi_minus", "psi_plus", "psi_minus"]:
        rho = bell_state(name)
        r6 = entanglement_as_rho6(rho, 2, 2)
        c = concurrence_two_qubit(rho)
        p = purity(rho)
        print(f"  {name:<12} | {p:>8.4f} | {r6:>8.4f} | {c:>11.6f}")
