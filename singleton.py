"""
Singleton Pattern
------------------
Ensures a class has only ONE instance and provides a global access point to it.

Real-world use cases:
- Database connection pools
- Configuration managers
- Logging objects
- Caches
"""

import threading


class Singleton:
    """Thread-safe Singleton using double-checked locking."""

    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            with cls._lock:
                # Double-checked locking: check again inside the lock
                # in case two threads passed the first check simultaneously.
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, value=None):
        # __init__ runs every time Singleton() is called, even on the
        # same instance, so guard against re-initializing.
        if not hasattr(self, "_initialized"):
            self.value = value
            self._initialized = True


class ConfigManager(Singleton):
    """Practical example: a single shared app configuration object."""

    def __init__(self, settings: dict = None):
        super().__init__()
        if not hasattr(self, "settings"):
            self.settings = settings or {}

    def set(self, key, value):
        self.settings[key] = value

    def get(self, key):
        return self.settings.get(key)


if __name__ == "__main__":
    config1 = ConfigManager({"debug": True})
    config2 = ConfigManager({"debug": False})  # ignored — instance already exists

    config1.set("env", "production")

    print(config1 is config2)          # True — same object
    print(config2.get("env"))          # "production" — shared state
    print(config1.get("debug"))        # True — first init wins
