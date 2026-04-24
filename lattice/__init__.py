"""Lattice module: 64-profile Boolean lattice and consistent profiles."""
from lattice.profile_lattice import (
    generate_all_profiles, meet, join, complement,
    hamming_distance, anomaly_degree, is_consistent,
    lattice_statistics,
)
from lattice.consistent_profiles import (
    CONSISTENT_PROFILES, consistency_projection,
    get_level, active_relations, LEVEL_NAMES,
)
