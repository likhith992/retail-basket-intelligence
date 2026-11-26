"""Utility functions for Retail Basket Intelligence."""

import hashlib
import time


def cache_key(dataset_name: str, thresholds: dict) -> str:
    """Generate a cache key from dataset name and thresholds.

    Used to invalidate Streamlit cache when data or settings change.
    """
    raw = f"{dataset_name}:{sorted(thresholds.items())}:{time.time() // 3600}"
    return hashlib.md5(raw.encode()).hexdigest()[:12]


def timestamp() -> str:
    """Return a human-readable timestamp for cache invalidation display."""
    return time.strftime("%Y-%m-%d %H:%M:%S")