"""
Decorator Pattern
-------------------
Attaches additional responsibilities to an object dynamically, by
wrapping it, without modifying its class. A flexible alternative to
subclassing for extending behavior.

Real-world use cases:
- Adding logging/caching/auth checks around a service call
- Coffee-shop style "add-ons" (milk, sugar, whipped cream) on a base item
- Python's own @decorator syntax (functions wrapping functions)
"""

from abc import ABC, abstractmethod


class Coffee(ABC):
    @abstractmethod
    def cost(self) -> float:
        ...

    @abstractmethod
    def description(self) -> str:
        ...


class SimpleCoffee(Coffee):
    def cost(self) -> float:
        return 2.0

    def description(self) -> str:
        return "Coffee"


class CoffeeDecorator(Coffee):
    """Base decorator: wraps a Coffee and delegates by default."""

    def __init__(self, coffee: Coffee):
        self._coffee = coffee

    def cost(self) -> float:
        return self._coffee.cost()

    def description(self) -> str:
        return self._coffee.description()


class MilkDecorator(CoffeeDecorator):
    def cost(self) -> float:
        return self._coffee.cost() + 0.5

    def description(self) -> str:
        return self._coffee.description() + " + Milk"


class SugarDecorator(CoffeeDecorator):
    def cost(self) -> float:
        return self._coffee.cost() + 0.2

    def description(self) -> str:
        return self._coffee.description() + " + Sugar"


class WhippedCreamDecorator(CoffeeDecorator):
    def cost(self) -> float:
        return self._coffee.cost() + 0.7

    def description(self) -> str:
        return self._coffee.description() + " + Whipped Cream"


if __name__ == "__main__":
    order = SimpleCoffee()
    order = MilkDecorator(order)
    order = SugarDecorator(order)
    order = WhippedCreamDecorator(order)

    print(f"{order.description()} = ${order.cost():.2f}")
    # Coffee + Milk + Sugar + Whipped Cream = $3.40

    # Bonus: Python's built-in function decorators are the same idea,
    # just applied to functions instead of objects.
    def logged(func):
        def wrapper(*args, **kwargs):
            print(f"Calling {func.__name__}{args}")
            return func(*args, **kwargs)
        return wrapper

    @logged
    def add(a, b):
        return a + b

    add(2, 3)
