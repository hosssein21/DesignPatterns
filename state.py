"""
State Pattern
---------------
Lets an object alter its behavior when its internal state changes —
the object appears to change its class. Replaces big if/elif chains
checking a status field with small state objects that each know what
transitions and behaviors are valid for that state.

Real-world use cases:
- Order lifecycle (pending -> paid -> shipped -> delivered/cancelled)
- Document workflow (draft -> review -> published)
- Traffic light / media player (playing -> paused -> stopped)
"""

from abc import ABC, abstractmethod


class OrderState(ABC):
    @abstractmethod
    def pay(self, order: "Order") -> None:
        ...

    @abstractmethod
    def ship(self, order: "Order") -> None:
        ...

    @abstractmethod
    def cancel(self, order: "Order") -> None:
        ...


class PendingState(OrderState):
    def pay(self, order: "Order") -> None:
        print("Payment received — moving to Paid.")
        order.state = PaidState()

    def ship(self, order: "Order") -> None:
        print("Cannot ship — order hasn't been paid yet.")

    def cancel(self, order: "Order") -> None:
        print("Order cancelled before payment.")
        order.state = CancelledState()


class PaidState(OrderState):
    def pay(self, order: "Order") -> None:
        print("Already paid.")

    def ship(self, order: "Order") -> None:
        print("Shipping order — moving to Shipped.")
        order.state = ShippedState()

    def cancel(self, order: "Order") -> None:
        print("Refunding and cancelling paid order.")
        order.state = CancelledState()


class ShippedState(OrderState):
    def pay(self, order: "Order") -> None:
        print("Already paid.")

    def ship(self, order: "Order") -> None:
        print("Already shipped.")

    def cancel(self, order: "Order") -> None:
        print("Cannot cancel — order already shipped.")


class CancelledState(OrderState):
    def pay(self, order: "Order") -> None:
        print("Cannot pay — order is cancelled.")

    def ship(self, order: "Order") -> None:
        print("Cannot ship — order is cancelled.")

    def cancel(self, order: "Order") -> None:
        print("Already cancelled.")


class Order:
    """Context object — delegates all behavior to its current state."""

    def __init__(self):
        self.state: OrderState = PendingState()

    def pay(self):
        self.state.pay(self)

    def ship(self):
        self.state.ship(self)

    def cancel(self):
        self.state.cancel(self)


if __name__ == "__main__":
    order = Order()
    order.ship()    # blocked — not paid yet
    order.pay()     # pending -> paid
    order.pay()     # already paid
    order.ship()    # paid -> shipped
    order.cancel()  # blocked — already shipped
