"""
64-profile Boolean lattice {0,1}^6.

Implements the Boolean lattice structure for significance profiles:
- Meet (AND): sigma AND tau (intersection)
- Join (OR): sigma OR tau (union)
- Complement (NOT): NOT sigma

Anomaly degree: alpha(sigma) = sum max(0, sigma_k - sigma_{k-1})
alpha = 0 -> consistent profile
alpha > 0 -> anomaly detected

Reference:
    Paper 3: doi.org/10.5281/zenodo.18776401 (Definitions 4.1-4.4, Theorem 4.1)
    Paper 2: doi.org/10.5281/zenodo.18776462 (Theorem 2.2, isomorphism with 6-qubit basis)
"""

from __future__ import annotations
from typing import Dict, FrozenSet, Iterator, List, Optional, Tuple
from itertools import product


NUM_DIMS = 6
TOTAL_PROFILES = 2 ** NUM_DIMS  # 64


def generate_all_profiles() -> List[Tuple[int, ...]]:
    """Generate all 64 binary profiles {0,1}^6."""
    return list(product([0, 1], repeat=NUM_DIMS))


def meet(a: Tuple[int, ...], b: Tuple[int, ...]) -> Tuple[int, ...]:
    """Boolean meet (AND): sigma AND tau."""
    return tuple(min(ai, bi) for ai, bi in zip(a, b))


def join(a: Tuple[int, ...], b: Tuple[int, ...]) -> Tuple[int, ...]:
    """Boolean join (OR): sigma OR tau."""
    return tuple(max(ai, bi) for ai, bi in zip(a, b))


def complement(a: Tuple[int, ...]) -> Tuple[int, ...]:
    """Boolean complement (NOT): NOT sigma."""
    return tuple(1 - ai for ai in a)


def hamming_distance(a: Tuple[int, ...], b: Tuple[int, ...]) -> int:
    """Hamming distance between two profiles."""
    return sum(ai != bi for ai, bi in zip(a, b))


def anomaly_degree(sigma: Tuple[int, ...]) -> int:
    """Compute anomaly degree alpha(sigma).

    alpha(sigma) = sum_{k=2}^{6} max(0, sigma_k - sigma_{k-1})

    alpha = 0: consistent profile (respects implication chain)
    alpha > 0: anomaly detected (chain violation)
    """
    return sum(max(0, sigma[k] - sigma[k - 1]) for k in range(1, NUM_DIMS))


def is_consistent(sigma: Tuple[int, ...]) -> bool:
    """Check if profile is consistent (respects implication chain).

    sigma is consistent iff: for all k in 2..6:
        sigma_k = 1 implies sigma_{k-1} = 1
    """
    return all(
        sigma[k] <= sigma[k - 1]
        for k in range(1, NUM_DIMS)
    )


def classify_profile(sigma: Tuple[int, ...]) -> str:
    """Classify a profile by its active relations."""
    names = {
        (0, 0, 0, 0, 0, 0): "Semiotic Void",
        (1, 0, 0, 0, 0, 0): "Appearance",
        (1, 1, 0, 0, 0, 0): "Correspondence",
        (1, 1, 1, 0, 0, 0): "Interchange",
        (1, 1, 1, 1, 0, 0): "Mirroring",
        (1, 1, 1, 1, 1, 0): "Stability",
        (1, 1, 1, 1, 1, 1): "Plenitude",
    }
    return names.get(sigma, "ANOMALOUS")


def lattice_statistics() -> Dict:
    """Compute statistics for the full 64-profile lattice."""
    all_profiles = generate_all_profiles()
    consistent = [p for p in all_profiles if is_consistent(p)]
    anomalous = [p for p in all_profiles if not is_consistent(p)]

    # Anomaly degree distribution
    degree_dist: Dict[int, int] = {}
    for p in anomalous:
        d = anomaly_degree(p)
        degree_dist[d] = degree_dist.get(d, 0) + 1

    return {
        "total": TOTAL_PROFILES,
        "consistent": len(consistent),
        "anomalous": len(anomalous),
        "consistent_profiles": consistent,
        "anomaly_degree_distribution": degree_dist,
    }


def find_anomaly_neighbors(
    sigma: Tuple[int, ...],
    max_distance: int = 2,
) -> List[Tuple[int, Tuple[int, ...]]]:
    """Find nearest consistent profiles to an anomalous one.

    Returns list of (distance, profile) sorted by distance.
    """
    all_profiles = generate_all_profiles()
    neighbors = []
    for p in all_profiles:
        if is_consistent(p):
            d = hamming_distance(sigma, p)
            if d <= max_distance:
                neighbors.append((d, p))
    neighbors.sort()
    return neighbors


if __name__ == "__main__":
    print("=" * 60)
    print("64-Profile Boolean Lattice Demo")
    print("=" * 60)

    stats = lattice_statistics()
    print(f"\nTotal profiles: {stats['total']}")
    print(f"Consistent: {stats['consistent']}")
    print(f"Anomalous: {stats['anomalous']}")

    print("\n7 Consistent profiles:")
    for p in stats["consistent_profiles"]:
        name = classify_profile(p)
        print(f"  {p} -> {name}")

    print(f"\nAnomaly degree distribution:")
    for degree, count in sorted(stats["anomaly_degree_distribution"].items()):
        print(f"  degree={degree}: {count} profiles")

    # Demo operations
    a = (1, 1, 0, 0, 0, 0)
    b = (1, 0, 1, 0, 0, 0)  # anomalous
    print(f"\nOperations demo:")
    print(f"  a = {a} (Correspondence)")
    print(f"  b = {b} (Anomalous)")
    print(f"  meet(a,b) = {meet(a, b)}")
    print(f"  join(a,b) = {join(a, b)}")
    print(f"  complement(a) = {complement(a)}")
    print(f"  hamming(a,b) = {hamming_distance(a, b)}")
    print(f"  anomaly_degree(b) = {anomaly_degree(b)}")

    # Find nearest consistent for anomalous profile
    neighbors = find_anomaly_neighbors(b)
    print(f"\nNearest consistent profiles to {b}:")
    for dist, profile in neighbors[:5]:
        print(f"  distance={dist}: {profile} ({classify_profile(profile)})")
