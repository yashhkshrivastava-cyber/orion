"""Indian geography helpers backed by bharatpin (India Post 2026 pincode dataset)."""

from functools import lru_cache

import bharatpin


@lru_cache(maxsize=1)
def get_all_states():
    """Return all Indian states and union territories."""
    return sorted(bharatpin.get_all_states())


@lru_cache(maxsize=128)
def get_cities_for_state(state):
    """
    Return districts for a state, used as the city dropdown options.

    India has no single official city list; districts are the standard
    admin division below state and map well to how addresses are recorded.
    """
    if not state:
        return []
    districts = bharatpin.get_districts_by_state(state)
    return sorted(districts) if districts else []
