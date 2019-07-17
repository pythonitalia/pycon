from abc import ABC, abstractmethod


class PaymentProvider(ABC):
    """
    Generic interface for a payment provider.
    """

    @classmethod
    @abstractmethod
    def setup(cls):
        """
        Called when the payments app is ready
        """
        pass

    @abstractmethod
    def charge(self, *, order, payload):
        """
        Execute the payment
        """
        pass
