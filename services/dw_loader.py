from typing import Dict

from dw.registry import DW_SYNC


def run_dw_load(table_name: str) -> Dict[str, int]:
    sync_fn = DW_SYNC.get(table_name)
    if sync_fn is None:
        raise ValueError(f"No DW load configured for '{table_name}'.")
    return sync_fn()
