"""
Observer Pattern
------------------
Defines a one-to-many dependency between objects: when one object (the
"subject") changes state, all its registered "observers" are notified
and updated automatically.

Real-world use cases:
- Event systems / pub-sub (order placed -> notify email, inventory, analytics)
- UI frameworks (model changes -> view re-renders)
- Django/Flask signals
"""

from abc import ABC, abstractmethod


class Observer(ABC):
    @abstractmethod
    def update(self, event: str, data: dict) -> None:
        ...


class Subject:
    """The thing being observed — holds a list of observers and notifies them."""

    def __init__(self):
        self._observers: list[Observer] = []

    def subscribe(self, observer: Observer) -> None:
        self._observers.append(observer)

    def unsubscribe(self, observer: Observer) -> None:
        self._observers.remove(observer)

    def notify(self, event: str, data: dict) -> None:
        for observer in self._observers:
            observer.update(event, data)


class Order(Subject):
    """Concrete subject: an order that notifies observers on state changes."""

    def __init__(self, order_id: str):
        super().__init__()
        self.order_id = order_id
        self.status = "pending"

    def mark_paid(self):
        self.status = "paid"
        self.notify("order_paid", {"order_id": self.order_id})

    def mark_shipped(self):
        self.status = "shipped"
        self.notify("order_shipped", {"order_id": self.order_id})


class EmailNotifierObserver(Observer):
    def update(self, event: str, data: dict) -> None:
        print(f"[Email] Sending receipt for event '{event}' (order {data['order_id']})")


class InventoryObserver(Observer):
    def update(self, event: str, data: dict) -> None:
        if event == "order_paid":
            print(f"[Inventory] Reserving stock for order {data['order_id']}")


class AnalyticsObserver(Observer):
    def update(self, event: str, data: dict) -> None:
        print(f"[Analytics] Logging event '{event}' for order {data['order_id']}")


if __name__ == "__main__":
    order = Order("ORD-1001")
    order.subscribe(EmailNotifierObserver())
    order.subscribe(InventoryObserver())
    order.subscribe(AnalyticsObserver())

    order.mark_paid()
    print("---")
    order.mark_shipped()
