import hashlib
import json
from typing import Any


def make_cache_key(prefix: str, data: Any) -> str:
    """
    Generate a cache key by hashing the provided data with a given prefix.

    The data is serialized to JSON (with sorted keys for consistency),
    then hashed using MD5 to produce a compact identifier.

    Args:
        prefix (str): A prefix to namespace the key (e.g., the agent or purpose).
        data (Any): The data to hash (must be JSON-serializable).

    Returns:
        str: The generated cache key in the format "{prefix}:{hash}".
    """
    raw = json.dumps(data, sort_keys=True)
    hash_digest = hashlib.md5(raw.encode()).hexdigest()
    return f"{prefix}:{hash_digest}"
