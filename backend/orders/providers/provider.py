from abc import ABC, abstractmethod


class PaymentProvider(ABC):
    """
    Generic interface for a payment provider.
    """
    @abstractmethod
    def charge(self, *, order, token):
        """
        Execute the payment
        """
        pass
