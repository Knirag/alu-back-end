#!/usr/bin/env python3
"""
This module provides a `Cache` class for interacting with a Redis NoSQL data store.
It offers functionalities to store, retrieve, and track method calls within the cache object.
"""

import uuid
import redis
from functools import wraps
from typing import Any, Callable, Union


def track_calls(method: Callable) -> Callable:
    """
    Decorator that keeps track of the number of times a method within the `Cache` class is called.
    Increments a dedicated Redis key associated with the method's qualified name for call counting.
    """

    @wraps(method)
    def wrapper(self, *args, **kwargs) -> Any:
        """
        Inner wrapper function that verifies a valid Redis connection before incrementing the call counter
        and invoking the wrapped method.
        """
        if isinstance(self._redis, redis.Redis):
            self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)

    return wrapper


def record_call_history(method: Callable) -> Callable:
    """
    Decorator that tracks the call history of a method within the `Cache` class.
    Stores method inputs and outputs in separate Redis lists using keys derived from the method's qualified name.
    """

    @wraps(method)
    def wrapper(self, *args, **kwargs) -> Any:
        """
        Inner wrapper function that retrieves the method's output, stores the corresponding inputs and output
        in Redis if a valid connection exists, and finally returns the output.
        """
        input_key = f"{method.__qualname__}:inputs"
        output_key = f"{method.__qualname__}:outputs"
        if isinstance(self._redis, redis.Redis):
            self._redis.rpush(input_key, str(args))
            output = method(self, *args, **kwargs)
            self._redis.rpush(output_key, output)
        else:
            output = method(self, *args, **kwargs)
        return output

    return wrapper


def display_call_history(fn: Callable) -> None:
    """
    Analyzes the call history of a method decorated with `record_call_history`.
    Extracts method call count, inputs, and outputs from associated Redis keys,
    and presents the information if a valid connection and call data exist.
    """

    if not fn or not hasattr(fn, "__self__"):
        return

    redis_store = getattr(fn.__self__, "_redis", None)
    if not isinstance(redis_store, redis.Redis):
        return

    function_name = fn.__qualname__
    input_key = f"{function_name}:inputs"
    output_key = f"{function_name}:outputs"
    call_count = 0
    if redis_store.exists(function_name) != 0:
        call_count = int(redis_store.get(function_name))

    print(f"{function_name} was called {call_count} times:")
    call_inputs = redis_store.lrange(input_key, 0, -1)
    call_outputs = redis_store.lrange(output_key, 0, -1)
    for input_data, output_data in zip(call_inputs, call_outputs):
        print(f"{function_name}(*{input_data.decode('utf-8')}) -> {output_data.decode('utf-8')}")


class Cache:
    """
    Represents a cache object for interacting with a Redis NoSQL data store.
    Provides methods for storing data (`store`), retrieving data (`get`, `get_str`, `get_int`),
    and analyzing method call history (`display_call_history`).
    """

    def __init__(self) -> None:
        """
        Initializes a `Cache` instance and establishes a connection to the Redis data store.
        Clears any existing data within the connected Redis database.
        """
        self._redis = redis.Redis()
        self._redis.flushdb(True)

        @record_call_history
    @track_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Stores a value in the Redis data store and returns the generated key for retrieval.
        Utilizes `uuid.uuid4()` to create a unique key for the stored data.
        """
        data_key = str(uuid.uuid4())
        self._redis.set(data_key, data)
        return data_key

    def get(
        self,
        key: str,
        fn: Callable = None,
    ) -> Union[str, bytes, int, float]:
        """
        Retrieves a value from the Redis data store using the provided key.
        Optionally applies a transformation function (`fn`) to the retrieved data before returning it.
        """
        data = self._redis.get(key)
        return fn(data) if fn is not None else data

    def get_str(self, key: str) -> str:
        """
        Retrieves a value from the Redis data store using the provided key and ensures it's decoded as a string.
        """
        return self.get(key, lambda x: x.decode("utf-8"))

    def get_int(self, key: str) -> int:
        """
        Retrieves a value from the Redis data store using the provided key and ensures it's converted to an integer.
        """
        return self.get(key, lambda x: int(x))
