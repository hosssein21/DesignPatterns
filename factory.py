"""
Factory Method Pattern
-----------------------
Defines an interface for creating an object, but lets subclasses (or a
central function) decide which class to instantiate. The caller doesn't
need to know the concrete class — only the common interface.

Real-world use cases:
- Choosing a payment processor (Stripe, PayPal, Crypto) at runtime
- Creating different document exporters (PDF, CSV, JSON)
- Notification systems (Email, SMS, Push)
"""

from abc import ABC, abstractmethod


class Notifier(ABC):
    @abstractmethod
    def send(self, message: str) -> None:
        ...


class EmailNotifier(Notifier):
    def send(self, message: str) -> None:
        print(f"[Email] Sending: {message}")


class SMSNotifier(Notifier):
    def send(self, message: str) -> None:
        print(f"[SMS] Sending: {message}")


class PushNotifier(Notifier):
    def send(self, message: str) -> None:
        print(f"[Push] Sending: {message}")


class NotifierFactory:
    """Factory that centralizes object creation logic."""

    _notifiers = {
        "email": EmailNotifier,
        "sms": SMSNotifier,
        "push": PushNotifier,
    }

    @classmethod
    def create(cls, channel: str) -> Notifier:
        notifier_cls = cls._notifiers.get(channel)
        if not notifier_cls:
            raise ValueError(f"Unknown channel: {channel}")
        return notifier_cls()

    @classmethod
    def register(cls, channel: str, notifier_cls: type) -> None:
        """Lets new notifier types be plugged in without editing this class."""
        cls._notifiers[channel] = notifier_cls


if __name__ == "__main__":
    for channel in ("email", "sms", "push"):
        notifier = NotifierFactory.create(channel)
        notifier.send("Your order has shipped!")

    # Extending without modifying NotifierFactory's internals directly
    class SlackNotifier(Notifier):
        def send(self, message: str) -> None:
            print(f"[Slack] Sending: {message}")

    NotifierFactory.register("slack", SlackNotifier)
    NotifierFactory.create("slack").send("Deploy finished.")
