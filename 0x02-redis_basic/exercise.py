#!/usr/bin/env python3
""" 
Redis client module and python exercise
"""
from uuid import uuid4
from functools import wraps
from typing import Any, Callable, Optional, Union

import redis

def count_calls(method: Callable) -> Callable:
    """
    Decorator takes a single method Callable argument
    returning a Callable
    """
    @wraps(method)
    def wrapper(self: Any, *args, **kwargs) -> str:
        """
        Acumulates the count for the key every time the method
        is called returning the value returned by the original method
        """
        self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """
    Stores the history of inputs and outputs for a given function
    """
    @wraps(method)
    def wrapper(self: Any, *args) -> str:
        """
        saves the input and output of every function in redis
        """
        self._redis.rpush(f'{method.__qualname__}:inputs', str(args))
        output = method(self, *args)
        self._redis.rpush(f'{method.__qualname__}:outputs', output)
        return output
    return wrapper


def replay(fn: Callable) -> None:
    """
    Display/shows the history of calls of a particular function
    """
    client = redis.Redis()
    calls = client.get(fn.__qualname__).decode('utf-8')
    inputs = [input.decode('utf-8') for input in
              client.lrange(f'{fn.__qualname__}:inputs', 0, -1)]
    outputs = [output.decode('utf-8') for output in
               client.lrange(f'{fn.__qualname__}:outputs', 0, -1)]
    print(f'{fn.__qualname__} was called {calls} times:')
    for input, output in zip(inputs, outputs):
        print(f'{fn.__qualname__}(*{input}) -> {output}')


class Cache:
    """
    redis caching class
    """
    def __init__(self) -> None:
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes,  int,  float]) -> str:
        """
        Storing data in redis with randomly generated keys
        """
        key = str(uuid4())
        client = self._redis
        client.set(key, data)
        return key

    def get(self, key: str, fn: Optional[Callable] = None) -> Any:
        """
        Get data from redis and transform into its correct data type
        """
        client = self._redis
        value = client.get(key)
        if not value:
            return
        if fn is int:
            return self.get_int(value)
        if fn is str:
            return self.get_str(value)
        if callable(fn):
            return fn(value)
        return value

    def get_str(self, data: bytes) -> str:
        """
        Transforms bytes to string
        """
        return data.decode('utf-8')

    def get_int(self, data: bytes) -> int:
        """
        Transforms redis bytes to integers
        """
        return int(data)
