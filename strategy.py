"""
Strategy Pattern
------------------
Defines a family of interchangeable algorithms, encapsulates each one,
and lets the client pick which one to use at runtime — without
changing the code that uses it.

Real-world use cases:
- Different discount/pricing rules
- Different sorting/compression algorithms chosen at runtime
- Different payment or shipping-cost calculation methods
"""

from abc import ABC, abstractmethod


class DiscountStrategy(ABC):
    @abstractmethod
    def apply(self, total: float) -> float:
        ...


class NoDiscount(DiscountStrategy):
    def apply(self, total: float) -> float:
        return total


class PercentageDiscount(DiscountStrategy):
    def __init__(self, percent: float):
        self.percent = percent

    def apply(self, total: float) -> float:
        return total * (1 - self.percent / 100)


class FlatAmountDiscount(DiscountStrategy):
    def __init__(self, amount: float):
        self.amount = amount

    def apply(self, total: float) -> float:
        return max(0.0, total - self.amount)


class ShoppingCart:
    """Context: holds a reference to a strategy and delegates to it."""

    def __init__(self, strategy: DiscountStrategy = None):
        self.items: list[float] = []
        self.strategy = strategy or NoDiscount()

    def add_item(self, price: float):
        self.items.append(price)

    def set_strategy(self, strategy: DiscountStrategy):
        self.strategy = strategy

    def total(self) -> float:
        subtotal = sum(self.items)
        return self.strategy.apply(subtotal)


if __name__ == "__main__":
    cart = ShoppingCart()
    cart.add_item(50)
    cart.add_item(30)

    print(f"No discount: ${cart.total():.2f}")

    cart.set_strategy(PercentageDiscount(10))
    print(f"10% off: ${cart.total():.2f}")

    cart.set_strategy(FlatAmountDiscount(15))
    print(f"$15 off: ${cart.total():.2f}")
