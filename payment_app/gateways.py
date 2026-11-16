"""Платёжные шлюзы — конкретные реализации интерфейса IPaymentGateway."""

import uuid
from abc import ABC, abstractmethod

from logger import get_logger
from payment_app.models import PaymentError, PaymentResult, RefundResult

logger = get_logger(__name__)


class IPaymentGateway(ABC):
    """Абстрактный платёжный шлюз: единая точка взаимодействия."""

    display_name: str = "?"

    @abstractmethod
    def pay(self, amount: float) -> PaymentResult:
        """Провести платёж на указанную сумму."""

    @abstractmethod
    def refund(self, transaction_id: str) -> RefundResult:
        """Вернуть средства по идентификатору транзакции."""


class UuidGateway(IPaymentGateway):
    """Базовый шлюз: UUID-транзакция, маскирование учётных данных, логирование.

    Конкретные шлюзы отличаются только названием, префиксом транзакции
    и именем учётных данных, поэтому вся логика вынесена в этот класс.
    """

    prefix: str = "GEN"
    credential_name: str = "credential"

    def __init__(self, credential: str) -> None:
        """Сохранить учётные данные шлюза (merchant_id, ключ API, shop_id).

        Args:
            credential: идентификатор продавца или ключ доступа.
        """
        self._credential = credential

    @property
    def _masked_credential(self) -> str:
        """Вернуть учётные данные без секретной части (для журнала)."""
        if len(self._credential) <= 6:
            return "***"
        return f"{self._credential[:6]}..."

    def pay(self, amount: float) -> PaymentResult:
        """Провести платёж и вернуть результат операции.

        Args:
            amount: сумма платежа в BYN.

        Returns:
            Результат успешного платежа с идентификатором транзакции.

        Raises:
            PaymentError: если сумма не положительная.
        """
        if amount <= 0:
            raise PaymentError("Сумма платежа должна быть положительной")
        transaction_id = f"{self.prefix}-{uuid.uuid4().hex[:8].upper()}"
        logger.info(
            "Платёж %.2f BYN через %s (%s=%s)",
            amount,
            self.display_name,
            self.credential_name,
            self._masked_credential,
        )
        return PaymentResult(
            gateway=self.display_name,
            success=True,
            transaction_id=transaction_id,
            message=(
                f"Платёж {amount:.2f} BYN через {self.display_name} "
                f"({self.credential_name}={self._masked_credential}) выполнен. "
                f"TX={transaction_id}"
            ),
        )

    def refund(self, transaction_id: str) -> RefundResult:
        """Вернуть средства по идентификатору транзакции.

        Args:
            transaction_id: идентификатор исходной транзакции.

        Returns:
            Результат возврата средств.

        Raises:
            PaymentError: если идентификатор транзакции пустой.
        """
        if not transaction_id:
            raise PaymentError("Идентификатор транзакции не может быть пустым")
        logger.info("Возврат по TX=%s через %s", transaction_id, self.display_name)
        return RefundResult(
            gateway=self.display_name,
            success=True,
            message=f"Возврат по TX={transaction_id} через {self.display_name} выполнен.",
        )


class BelagroprombankGateway(UuidGateway):
    """Шлюз Белагропромбанка."""

    display_name = "Белагропромбанк"
    prefix = "BAB"
    credential_name = "merchant_id"


class PriorbankGateway(UuidGateway):
    """Шлюз Приорбанка."""

    display_name = "Приорбанк"
    prefix = "PRI"
    credential_name = "key"


class BPSberbankGateway(UuidGateway):
    """Шлюз БПС-Сбербанк."""

    display_name = "БПС-Сбербанк"
    prefix = "BPS"
    credential_name = "shop_id"


class BelinvestbankGateway(UuidGateway):
    """Шлюз Белинвестбанка."""

    display_name = "Белинвестбанк"
    prefix = "BIW"
    credential_name = "wallet"
