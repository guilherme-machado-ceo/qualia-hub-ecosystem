"""
Quantum significance profiles and measurement.

Implements quantum extensions of the profile framework:
- Quantum significance profiles with superposition
- Measurement as evaluation (Born rule)
- Consistency projection onto 7-element consistent subspace
- Significance as observable (Hermitian operator)

Reference:
    Paper 2: doi.org/10.5281/zenodo.18776462 (Definitions 4.1-4.6)
    Paper 3: doi.org/10.5281/zenodo.18776401 (Definition 11.3)
"""

from __future__ import annotations
import math
from typing import Dict, List, Optional, Tuple
import numpy as np

NUM_RELATIONS = 6
TOTAL_PROFILES = 64
CONSISTENT_COUNT = 7

# The 7 consistent profiles (initial segments)
CONSISTENT_PROFILES = [
    (0, 0, 0, 0, 0, 0),
    (1, 0, 0, 0, 0, 0),
    (1, 1, 0, 0, 0, 0),
    (1, 1, 1, 0, 0, 0),
    (1, 1, 1, 1, 0, 0),
    (1, 1, 1, 1, 1, 0),
    (1, 1, 1, 1, 1, 1),
]


class QuantumSignificanceProfile:
    """Quantum significance profile: superposition over 64 basis states.

    |sigma>_q = sum_{sigma in {0,1}^6} alpha_sigma |sigma>

    Measurement collapses to a classical profile with probability |alpha|^2.
    """

    def __init__(self, amplitudes: Optional[np.ndarray] = None) -> None:
        if amplitudes is None:
            # Default: uniform superposition over consistent profiles
            self.amplitudes = np.zeros(TOTAL_PROFILES, dtype=np.complex128)
            for cp in CONSISTENT_PROFILES:
                idx = self._profile_to_index(cp)
                self.amplitudes[idx] = 1.0 / math.sqrt(CONSISTENT_COUNT)
        else:
            self.amplitudes = np.array(amplitudes, dtype=np.complex128)
            if len(self.amplitudes) != TOTAL_PROFILES:
                raise ValueError(f"Expected {TOTAL_PROFILES} amplitudes")
        self._normalize()

    def _normalize(self) -> None:
        norm = np.sqrt(np.sum(np.abs(self.amplitudes) ** 2))
        if norm > 1e-15:
            self.amplitudes /= norm

    @staticmethod
    def _profile_to_index(sigma: Tuple[int, ...]) -> int:
        idx = 0
        for i, b in enumerate(sigma):
            idx |= (b << (NUM_RELATIONS - 1 - i))
        return idx

    @staticmethod
    def _index_to_profile(idx: int) -> Tuple[int, ...]:
        return tuple((idx >> (NUM_RELATIONS - 1 - i)) & 1 for i in range(NUM_RELATIONS))

    @property
    def probabilities(self) -> np.ndarray:
        """Born rule: P(sigma) = |alpha_sigma|^2."""
        return np.abs(self.amplitudes) ** 2

    def measure(self) -> Tuple[int, ...]:
        """Perform measurement: collapse to classical profile."""
        probs = self.probabilities
        idx = np.random.choice(TOTAL_PROFILES, p=probs)
        return self._index_to_profile(idx)

    def expected_profile(self) -> List[float]:
        """Compute expected (average) profile <sigma_k>."""
        probs = self.probabilities
        expected = []
        for k in range(NUM_RELATIONS):
            exp_val = 0.0
            for idx in range(TOTAL_PROFILES):
                profile = self._index_to_profile(idx)
                exp_val += probs[idx] * profile[k]
            expected.append(exp_val)
        return expected

    @property
    def consistency_probability(self) -> float:
        """P(profile is consistent) = sum |alpha_sigma|^2 for sigma in Sigma_C."""
        total = 0.0
        for cp in CONSISTENT_PROFILES:
            idx = self._profile_to_index(cp)
            total += self.probabilities[idx]
        return total

    def consistency_project(self) -> "QuantumSignificanceProfile":
        """Project onto the consistent subspace Sigma_C (dim=7).

        P_C = sum_{sigma in Sigma_C} |sigma><sigma|
        |sigma>_C = P_C |sigma>_q / ||P_C |sigma>_q||
        """
        projected = np.zeros(TOTAL_PROFILES, dtype=np.complex128)
        for cp in CONSISTENT_PROFILES:
            idx = self._profile_to_index(cp)
            projected[idx] = self.amplitudes[idx]
        return QuantumSignificanceProfile(projected)

    @property
    def uncertainty(self) -> float:
        """Uncertainty Var(Pi_hat) in significance measurement.

        Var = sum p(sigma) * Pi(sigma)^2 - (sum p(sigma) * Pi(sigma))^2
        Using PiRoot as the significance observable.
        """
        probs = self.probabilities
        mean = 0.0
        mean_sq = 0.0
        for idx in range(TOTAL_PROFILES):
            profile = self._index_to_profile(idx)
            p = probs[idx]
            if p < 1e-15:
                continue
            # Compute Pi(sigma) as weighted count
            pi_val = sum(1.0 for b in profile if b == 1)
            mean += p * pi_val
            mean_sq += p * pi_val ** 2
        return mean_sq - mean ** 2

    @property
    def is_deterministic(self) -> bool:
        """Check if profile is a single basis state (zero uncertainty)."""
        return np.sum(self.probabilities > 0.999) == 1


if __name__ == "__main__":
    print("=" * 60)
    print("Quantum Significance Profiles")
    print("=" * 60)

    # Create default profile (consistent superposition)
    qsp = QuantumSignificanceProfile()
    print(f"\nDefault: uniform superposition over 7 consistent profiles")
    print(f"  Consistency probability: {qsp.consistency_probability:.4f}")
    print(f"  Expected profile: {[f'{v:.3f}' for v in qsp.expected_profile()]}")
    print(f"  Uncertainty: {qsp.uncertainty:.4f}")
    print(f"  Is deterministic: {qsp.is_deterministic}")

    # Perform measurements
    print(f"\n  5 measurements:")
    for _ in range(5):
        result = qsp.measure()
        print(f"    {result}")

    # Create a profile with anomaly (inconsistent superposition)
    anomalous = np.zeros(64, dtype=np.complex128)
    # Put amplitude on an inconsistent profile
    anomalous[QuantumSignificanceProfile._profile_to_index((1, 0, 1, 0, 0, 0))] = 0.7
    anomalous[QuantumSignificanceProfile._profile_to_index((1, 1, 0, 0, 0, 0))] = 0.7
    qsp_anom = QuantumSignificanceProfile(anomalous)
    print(f"\nAnomalous profile:")
    print(f"  Consistency probability: {qsp_anom.consistency_probability:.4f}")
    print(f"  Expected profile: {[f'{v:.3f}' for v in qsp_anom.expected_profile()]}")
    print(f"  Uncertainty: {qsp_anom.uncertainty:.4f}")

    # Consistency projection
    projected = qsp_anom.consistency_project()
    print(f"\nAfter consistency projection:")
    print(f"  Consistency probability: {projected.consistency_probability:.4f}")
    print(f"  Expected profile: {[f'{v:.3f}' for v in projected.expected_profile()]}")
