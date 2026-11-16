"""Модели результатов обработки платежей."""

from dataclasses import asdict, dataclass
from typing import Any, Dict


class PaymentError(Exception):
    """Ошибка выполнения платёжной операции.

    Используется для ошибок бизнес-логики: некорректная сумма,
    пустой идентификатор транзакции, отказ шлюза.
    """


@dataclass
class PaymentResult:
    """Результат проведения платежа через конкретный шлюз."""

    gateway: str
    success: bool
    transaction_id: str
    message: str

    def to_dict(self) -> Dict[str, Any]:
        """Преобразовать результат в словарь для сериализации в JSON."""
        return asdict(self)


@dataclass
class RefundResult:
    """Результат возврата средств через конкретный шлюз."""

    gateway: str
    success: bool
    message: str

    def to_dict(self) -> Dict[str, Any]:
        """Преобразовать результат в словарь для сериализации в JSON."""
        return asdict(self)
