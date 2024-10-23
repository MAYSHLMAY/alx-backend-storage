#!/usr/bin/env python3
""" Redis Module """

from functools import wraps
import redis
import requests
from typing import Callable

# Initialize Redis connection
redis_ = redis.Redis()

def count_requests(method: Callable[[str], str]) -> Callable[[str], str]:
    """ Decorator for counting requests and caching HTML responses """
    @wraps(method)
    def wrapper(url: str) -> str:
        # Increment the request count for the given URL
        redis_.incr(f"count:{url}")
        
        # Attempt to retrieve the cached HTML content
        cached_html = redis_.get(f"cached:{url}")
        if cached_html:
            return cached_html.decode('utf-8')
        
        # If not cached, make a request to get the HTML
        try:
            html = method(url)
            # Store the HTML in cache with an expiration time of 10 seconds
            redis_.setex(f"cached:{url}", 10, html)
            return html
        except requests.RequestException as e:
            # Handle request exceptions (optional)
            print(f"Error fetching {url}: {e}")
            return ""  # Or raise an exception depending on your use case

    return wrapper

@count_requests
def get_page(url: str) -> str:
    """ Obtain the HTML content of a URL """
    response = requests.get(url)
    response.raise_for_status()  # Raise an error for bad responses
    return response.text
