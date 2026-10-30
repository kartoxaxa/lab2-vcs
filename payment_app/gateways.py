"""Платёжные шлюзы — конкретные реализации интерфейса IPaymentGateway."""

import uuid
from abc import ABC, abstractmethod

from payment_app.models import PaymentResult, RefundResult


class IPaymentGateway(ABC):
    """Абстрактный узел сети: единая точка взаимодействия с шлюзом."""

    display_name: str = "?"

    @abstractmethod
    def pay(self, amount: float) -> PaymentResult:
        """Провести платёж на указанную сумму."""
        ...

    @abstractmethod
    def refund(self, transaction_id: str) -> RefundResult:
        """Вернуть средства по идентификатору транзакции."""
        ...


class BelagroprombankGateway(IPaymentGateway):
    display_name = "Белагропромбанк"

    def __init__(self, merchant_id: str):
        self._merchant_id = merchant_id

    def pay(self, amount: float) -> PaymentResult:
        tx = f"BAB-{uuid.uuid4().hex[:8].upper()}"
        return PaymentResult(
            gateway=self.display_name,
            success=True,
            transaction_id=tx,
            message=(
                f"Платёж {amount:.2f} BYN через Белагропромбанк "
                f"(merchant_id={self._merchant_id}) выполнен. TX={tx}"
            ),
        )

    def refund(self, transaction_id: str) -> RefundResult:
        return RefundResult(
            gateway=self.display_name,
            success=True,
            message=f"Возврат по TX={transaction_id} через Белагропромбанк выполнен.",
        )


class PriorbankGateway(IPaymentGateway):
    display_name = "Приорбанк"

    def __init__(self, api_key: str):
        self._api_key = api_key

    def pay(self, amount: float) -> PaymentResult:
        tx = f"PRI-{uuid.uuid4().hex[:8].upper()}"
        return PaymentResult(
            gateway=self.display_name,
            success=True,
            transaction_id=tx,
            message=(
                f"Платёж {amount:.2f} BYN через Приорбанк "
                f"(key={self._api_key[:6]}...) выполнен. TX={tx}"
            ),
        )

    def refund(self, transaction_id: str) -> RefundResult:
        return RefundResult(
            gateway=self.display_name,
            success=True,
            message=f"Возврат по TX={transaction_id} через Приорбанк выполнен.",
        )


class BPSberbankGateway(IPaymentGateway):
    display_name = "БПС-Сбербанк"

    def __init__(self, shop_id: str):
        self._shop_id = shop_id

    def pay(self, amount: float) -> PaymentResult:
        tx = f"BPS-{uuid.uuid4().hex[:8].upper()}"
        return PaymentResult(
            gateway=self.display_name,
            success=True,
            transaction_id=tx,
            message=(
                f"Платёж {amount:.2f} BYN через БПС-Сбербанк "
                f"(shop_id={self._shop_id}) выполнен. TX={tx}"
            ),
        )

    def refund(self, transaction_id: str) -> RefundResult:
        return RefundResult(
            gateway=self.display_name,
            success=True,
            message=f"Возврат по TX={transaction_id} через БПС-Сбербанк выполнен.",
        )


class BelinvestbankGateway(IPaymentGateway):
    display_name = "Белинвестбанк"

    def __init__(self, wallet_id: str):
        self._wallet_id = wallet_id

    def pay(self, amount: float) -> PaymentResult:
        tx = f"BIW-{uuid.uuid4().hex[:8].upper()}"
        return PaymentResult(
            gateway=self.display_name,
            success=True,
            transaction_id=tx,
            message=(
                f"Платёж {amount:.2f} BYN через Белинвестбанк "
                f"(wallet={self._wallet_id}) выполнен. TX={tx}"
            ),
        )

    def refund(self, transaction_id: str) -> RefundResult:
        return RefundResult(
            gateway=self.display_name,
            success=True,
            message=f"Возврат по TX={transaction_id} через Белинвестбанк выполнен.",
        )
