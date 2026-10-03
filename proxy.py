"""
Proxy Pattern
---------------
Provides a surrogate/placeholder object that controls access to another
object. The proxy implements the same interface as the real object, so
clients can't tell the difference — but the proxy can add caching,
access control, lazy loading, or logging around the real calls.

Real-world use cases:
- Lazy-loading an expensive resource (image, DB connection) only when needed
- Caching proxy in front of a slow/expensive API call
- Access-control proxy that checks permissions before delegating
"""

from abc import ABC, abstractmethod
import time


class DataFetcher(ABC):
    @abstractmethod
    def fetch(self, query: str) -> str:
        ...


class RealDataFetcher(DataFetcher):
    """Simulates an expensive remote/database call."""

    def fetch(self, query: str) -> str:
        time.sleep(1)  # pretend this is slow
        return f"Result for '{query}'"


class CachingProxy(DataFetcher):
    """Proxy that adds a transparent cache in front of the real fetcher."""

    def __init__(self, real_fetcher: DataFetcher):
        self._real_fetcher = real_fetcher
        self._cache = {}

    def fetch(self, query: str) -> str:
        if query in self._cache:
            print(f"[Proxy] Cache hit for '{query}'")
            return self._cache[query]

        print(f"[Proxy] Cache miss for '{query}' — calling real fetcher")
        result = self._real_fetcher.fetch(query)
        self._cache[query] = result
        return result


class AccessControlProxy(DataFetcher):
    """Proxy that enforces permission checks before delegating."""

    def __init__(self, real_fetcher: DataFetcher, user_is_admin: bool):
        self._real_fetcher = real_fetcher
        self._user_is_admin = user_is_admin

    def fetch(self, query: str) -> str:
        if not self._user_is_admin:
            raise PermissionError("Only admins can fetch data.")
        return self._real_fetcher.fetch(query)


if __name__ == "__main__":
    proxy = CachingProxy(RealDataFetcher())

    start = time.time()
    print(proxy.fetch("users"))        # slow — cache miss
    print(f"Took {time.time() - start:.2f}s")

    start = time.time()
    print(proxy.fetch("users"))        # instant — cache hit
    print(f"Took {time.time() - start:.2f}s")

    guarded = AccessControlProxy(RealDataFetcher(), user_is_admin=False)
    try:
        guarded.fetch("secrets")
    except PermissionError as e:
        print(f"Blocked: {e}")
