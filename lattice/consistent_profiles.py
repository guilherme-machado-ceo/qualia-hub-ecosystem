"""
7 consistent profiles and consistency projection.

Consistent profiles form initial segments of {1,2,...,6}:
  Level 0: (0,0,0,0,0,0) - Semiotic Void
  Level 1: (1,0,0,0,0,0) - Appearance
  Level 2: (1,1,0,0,0,0) - Correspondence
  Level 3: (1,1,1,0,0,0) - Interchange
  Level 4: (1,1,1,1,0,0) - Mirroring
  Level 5: (1,1,1,1,1,0) - Stability
  Level 6: (1,1,1,1,1,1) - Plenitude

Consistency projection: map any profile to its closest consistent
profile by truncating at the first violation.

Reference:
    Paper 3: doi.org/10.5281/zenodo.18776401 (Theorem 4.1)
    Paper 2: doi.org/10.5281/zenodo.18776462 (Definition 2.5, consistent subspace)
"""

from __future__ import annotations
from typing import Dict, List, Optional, Tuple


# The 7 consistent profiles
CONSISTENT_PROFILES: List[Tuple[int, ...]] = [
    (0, 0, 0, 0, 0, 0),  # Level 0: Semiotic Void
    (1, 0, 0, 0, 0, 0),  # Level 1: Appearance
    (1, 1, 0, 0, 0, 0),  # Level 2: Correspondence
    (1, 1, 1, 0, 0, 0),  # Level 3: Interchange
    (1, 1, 1, 1, 0, 0),  # Level 4: Mirroring
    (1, 1, 1, 1, 1, 0),  # Level 5: Stability
    (1, 1, 1, 1, 1, 1),  # Level 6: Plenitude
]

LEVEL_NAMES: Dict[int, str] = {
    0: "Semiotic Void",
    1: "Appearance",
    2: "Correspondence",
    3: "Interchange",
    4: "Mirroring",
    5: "Stability",
    6: "Plenitude",
}

RELATION_NAMES = [
    "rho_1_similitude",
    "rho_2_homology",
    "rho_3_equivalence",
    "rho_4_symmetry",
    "rho_5_equilibrium",
    "rho_6_compensation",
]


def consistency_projection(sigma: Tuple[int, ...]) -> Tuple[int, ...]:
    """Project any profile onto the consistent subspace.

    Truncates at the first chain violation: if sigma_k=1 but sigma_{k-1}=0,
    set sigma_k and all deeper relations to 0.
    """
    result = list(sigma)
    for k in range(1, 6):
        if result[k] > result[k - 1]:
            # Violation: truncate here
            for j in range(k, 6):
                result[j] = 0
            break
    return tuple(result)


def get_level(sigma: Tuple[int, ...]) -> int:
    """Get the consistency level (0-6) of a profile.

    Returns -1 if inconsistent.
    """
    for level, cp in enumerate(CONSISTENT_PROFILES):
        if sigma == cp:
            return level
    return -1


def active_relations(sigma: Tuple[int, ...]) -> List[str]:
    """Get list of active relation names for a consistent profile."""
    return [RELATION_NAMES[i] for i in range(6) if sigma[i] == 1]


def level_from_count(count: int) -> Tuple[int, ...]:
    """Get the consistent profile with exactly `count` active relations."""
    if count < 0 or count > 6:
        raise ValueError("Count must be between 0 and 6")
    return CONSISTENT_PROFILES[count]


def profile_distance_to_consistent(sigma: Tuple[int, ...]) -> int:
    """Compute Hamming distance to the closest consistent profile."""
    projected = consistency_projection(sigma)
    return sum(a != b for a, b in zip(sigma, projected))


def compare_profiles(
    a: Tuple[int, ...],
    b: Tuple[int, ...],
) -> Dict:
    """Compare two profiles in detail."""
    level_a = get_level(a)
    level_b = get_level(b)
    return {
        "profile_a": a,
        "profile_b": b,
        "level_a": level_a,
        "level_b": level_b,
        "name_a": LEVEL_NAMES.get(level_a, "Anomalous"),
        "name_b": LEVEL_NAMES.get(level_b, "Anomalous"),
        "consistent_a": level_a >= 0,
        "consistent_b": level_b >= 0,
        "a_implies_b": all(ai >= bi for ai, bi in zip(a, b)),
        "b_implies_a": all(bi >= ai for ai, bi in zip(a, b)),
    }


if __name__ == "__main__":
    print("=" * 60)
    print("7 Consistent Profiles")
    print("=" * 60)

    print("\nAll consistent profiles:")
    print(f"  {'Level':>5} | {'Profile':<20} | {'Name':<16} | Active Relations")
    print("  " + "-" * 70)
    for level, profile in enumerate(CONSISTENT_PROFILES):
        active = active_relations(profile)
        active_str = ", ".join(r.split("_")[0] + "_" + r.split("_")[1][:3]
                               for r in active) if active else "none"
        print(f"  {level:>5} | {str(profile):<20} | "
              f"{LEVEL_NAMES[level]:<16} | {active_str}")

    # Test projection
    test_profiles = [
        (1, 0, 1, 0, 0, 0),  # Anomalous: rho_3 active but rho_2 inactive
        (0, 1, 1, 1, 0, 0),  # Anomalous: rho_2 active but rho_1 inactive
        (1, 1, 1, 0, 1, 0),  # Anomalous: rho_5 active but rho_4 inactive
        (1, 1, 0, 1, 0, 0),  # Anomalous: rho_4 active but rho_3 inactive
    ]

    print("\nConsistency projection:")
    for sigma in test_profiles:
        projected = consistency_projection(sigma)
        dist = profile_distance_to_consistent(sigma)
        print(f"  {sigma} -> {projected} "
              f"({LEVEL_NAMES.get(get_level(projected), '?')}) "
              f"dist={dist}")

    # Compare profiles
    print("\nProfile comparison:")
    comp = compare_profiles((1, 1, 0, 0, 0, 0), (1, 1, 1, 1, 0, 0))
    print(f"  Correspondence vs Mirroring:")
    print(f"    Correspondence implies Mirroring: {comp['a_implies_b']}")
    print(f"    Mirroring implies Correspondence: {comp['b_implies_a']}")
