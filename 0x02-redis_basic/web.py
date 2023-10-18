#!/usr/bin/env python3
"""
Function uses the requests module to obtain the,
HTML content of a particular URL and returns it
"""
import redis
import requests
from functools import wraps
from typing import Callable


def track_get_page(fn: Callable) -> Callable:
    """
    Decorator counts how many times
    a URL/page is accessed
    """
    @wraps(fn)
    def wrapper(url: str) -> str:
        """
        verifies if a url's data is cached
        tracks how many times get_page is called
        """
        client = redis.Redis()
        client.incr(f'count:{url}')
        cached_page = client.get(f'{url}')
        if cached_page:
            return cached_page.decode('utf-8')
        response = fn(url)
        client.set(f'{url}', response, 10)
        return response
    return wrapper


@track_get_page
def get_page(url: str) -> str:
    """
    Makes a http request retuning HTML content of url
    """
    response = requests.get(url)
    return response.text
