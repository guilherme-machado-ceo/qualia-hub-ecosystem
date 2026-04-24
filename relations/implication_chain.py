"""
Implication chain validation: rho_6 => rho_5 => ... => rho_1.

Checks if a significance profile respects the monotonicity constraint
implied by the chain: f_rho_j <= f_rho_i for j > i.

Reference:
    Paper 3: doi.org/10.5281/zenodo.18776401 (Theorem 3.1)
"""

from __future__ import annotations
from typing import Dict, List, Optional, Tuple


def check_implication_chain(values: List[float]) -> Dict:
    """Check if a profile violates the implication chain.

    The chain rho_6 => rho_5 => ... => rho_1 implies:
    f_rho_6 <= f_rho_5 <= f_rho_4 <= f_rho_3 <= f_rho_2 <= f_rho_1

    Args:
        values: List of 6 relation scores [rho_1, ..., rho_6].

    Returns:
        Dict with 'valid' (bool), 'violations' (list of violation details).
    """
    violations = []
    for i in range(1, 6):
        if values[i] > values[i - 1] + 1e-9:
            violations.append({
                "position": i,
                "from": f"rho_{i}",
                "to": f"rho_{i + 1}",
                "value_from": values[i - 1],
                "value_to": values[i],
                "excess": values[i] - values[i - 1],
            })

    return {
        "valid": len(violations) == 0,
        "violations": violations,
        "profile": values,
    }


def fix_chain_violations(values: List[float]) -> List[float]:
    """Fix chain violations by enforcing monotonicity.

    For each violation, clamp the deeper relation to not exceed
    the shallower one.
    """
    result = values[:]
    for i in range(1, 6):
        if result[i] > result[i - 1]:
            result[i] = result[i - 1]
    return result


def chain_depth(values: List[float], threshold: float = 0.5) -> int:
    """Compute the chain depth: how deep the implication chain goes.

    Returns the number of consecutive active relations starting from rho_1.
    """
    depth = 0
    for v in values:
        if v >= threshold:
            depth += 1
        else:
            break
    return depth


def chain_completeness(values: List[float]) -> float:
    """Compute how completely the chain is filled.

    Returns ratio of active relations to total (6).
    """
    active = sum(1 for v in values if v >= 0.5)
    return active / 6.0


def validate_paper_profiles() -> Dict[str, Dict]:
    """Validate profiles from the papers against the implication chain.

    Paper 3 profiles for quantum algorithms:
    - Shor: [0.9, 0.85, 0.3, 0.7, 0.2, 0.5] -> rho_4 > rho_3 VIOLATION
    - Grover: [0.95, 0.6, 0.7, 0.9, 0.3, 0.2] -> rho_4 > rho_3 VIOLATION
    - VQE: [0.7, 0.8, 0.5, 0.6, 0.7, 0.9] -> rho_3 > rho_2 VIOLATION
    - QAOA: [0.6, 0.75, 0.4, 0.5, 0.6, 0.7] -> rho_6 > rho_5 VIOLATION
    """
    paper_profiles = {
        "Shor": [0.9, 0.85, 0.3, 0.7, 0.2, 0.5],
        "Grover": [0.95, 0.6, 0.7, 0.9, 0.3, 0.2],
        "VQE": [0.7, 0.8, 0.5, 0.6, 0.7, 0.9],
        "QAOA": [0.6, 0.75, 0.4, 0.5, 0.6, 0.7],
    }
    results = {}
    for name, profile in paper_profiles.items():
        check = check_implication_chain(profile)
        check["chain_depth"] = chain_depth(profile)
        check["completeness"] = chain_completeness(profile)
        check["fixed"] = fix_chain_violations(profile)
        results[name] = check
    return results


if __name__ == "__main__":
    print("=" * 60)
    print("Implication Chain Validation")
    print("=" * 60)

    print("\nChain: rho_6 => rho_5 => rho_4 => rho_3 => rho_2 => rho_1")
    print("Constraint: f(rho_i) >= f(rho_j) for i < j\n")

    # Validate paper profiles
    results = validate_paper_profiles()
    for name, info in results.items():
        status = "VALID" if info["valid"] else "VIOLATED"
        print(f"--- {name}: {status} ---")
        print(f"  Profile: {[f'{v:.2f}' for v in info['profile']]}")
        print(f"  Chain depth: {info['chain_depth']} / 6")
        print(f"  Completeness: {info['completeness']:.1%}")
        if info["violations"]:
            print(f"  Violations ({len(info['violations'])}):")
            for v in info["violations"]:
                print(f"    {v['from']}={v['value_from']:.2f} < "
                      f"{v['to']}={v['value_to']:.2f} "
                      f"(excess={v['excess']:.2f})")
            print(f"  Fixed: {[f'{v:.2f}' for v in info['fixed']]}")
        print()
