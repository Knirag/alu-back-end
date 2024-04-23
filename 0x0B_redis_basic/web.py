#!/usr/bin/env python3
"""
This module provides utilities for data caching and request tracking using Redis.
"""

import redis
import requests
from functools import wraps
from typing import Callable


redis_store = redis.Redis()
"""
A central Redis instance used for data caching and request tracking.
"""


def cache_data(method: Callable) -> Callable:
    """
    Decorator function that caches the output of a wrapped function
    utilizing Redis for efficient data storage and retrieval.
    """

    @wraps(method)
    def wrapper(url: str) -> str:
        """
        Inner wrapper function that handles caching logic and invocation
        of the wrapped function.

        Tracks the number of requests made to a specific URL using a dedicated
        Redis key and caches the retrieved data for a configurable time period.
        """
        redis_store.incr(f"count:{url}")
        cached_result = redis_store.get(f"result:{url}")
        if cached_result:
            return cached_result.decode("utf-8")

        result = method(url)
        redis_store.set(f"count:{url}", 0)
        redis_store.setex(f"result:{url}", 10, result)
        return result

    return wrapper


@cache_data
def fetch_page(url: str) -> str:
    """
    Fetches the content of a given URL, leverages caching for improved
    performance, and tracks request count using Redis.

    Returns the content of the URL as a string after potentially retrieving
    it from the cache or making a fresh request.
    """
    return requests.get(url).text
