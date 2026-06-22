from cachetools import TTLCache
import hashlib
import json
from typing import Any

# Cache up to 256 unique queries; expire after 10 minutes
_cache: TTLCache = TTLCache(maxsize=256, ttl=600)

def make_cache_key(req_dict: dict) -> str:
    """Generate a deterministic cache key from the request body."""
    canonical = json.dumps(req_dict, sort_keys=True)
    return hashlib.md5(canonical.encode()).hexdigest()

def get_cached(key: str) -> Any:
    return _cache.get(key)

def set_cached(key: str, value: Any):
    _cache[key] = value
