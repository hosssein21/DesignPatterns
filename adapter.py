"""
Adapter Pattern
-----------------
Converts the interface of one class into another interface the client
expects, letting incompatible classes work together without modifying
their source code.

Real-world use cases:
- Wrapping a third-party payment SDK to match your internal interface
- Making an old legacy class work with new client code
- Adapting different data formats (XML library vs your JSON-based code)
"""

from abc import ABC, abstractmethod


# The interface your application expects
class PaymentProcessor(ABC):
    @abstractmethod
    def pay(self, amount: float) -> str:
        ...


# A third-party library with an incompatible interface you can't change
class LegacyStripeSDK:
    def make_charge(self, cents: int) -> dict:
        return {"status": "ok", "charged_cents": cents}


# The Adapter makes LegacyStripeSDK usable wherever PaymentProcessor is expected
class StripeAdapter(PaymentProcessor):
    def __init__(self, stripe_sdk: LegacyStripeSDK):
        self._sdk = stripe_sdk

    def pay(self, amount: float) -> str:
        cents = int(amount * 100)
        result = self._sdk.make_charge(cents)
        return f"Paid ${amount:.2f} via Stripe (status={result['status']})"


class PayPalSDK:
    """Another incompatible third-party interface, for contrast."""

    def send_payment(self, dollars: float) -> bool:
        return True


class PayPalAdapter(PaymentProcessor):
    def __init__(self, paypal_sdk: PayPalSDK):
        self._sdk = paypal_sdk

    def pay(self, amount: float) -> str:
        success = self._sdk.send_payment(amount)
        return f"Paid ${amount:.2f} via PayPal (success={success})"


def checkout(processor: PaymentProcessor, amount: float) -> None:
    """Client code only talks to the common PaymentProcessor interface."""
    print(processor.pay(amount))


if __name__ == "__main__":
    checkout(StripeAdapter(LegacyStripeSDK()), 49.99)
    checkout(PayPalAdapter(PayPalSDK()), 19.99)
