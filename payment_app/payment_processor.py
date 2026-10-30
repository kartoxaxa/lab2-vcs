"""Основной модуль обработки платежей.

Модуль не импортирует конкретные шлюзы: он знает только об абстракции
IPaymentGateway, что обеспечивает слабую связность (принцип Open/Closed).
"""

from typing import Iterable, List

from payment_app.gateways import IPaymentGateway
from payment_app.models import PaymentResult, RefundResult


class PaymentProcessor:
    """Координатор, работающий с произвольным набором шлюзов."""

    def __init__(self, gateways: Iterable[IPaymentGateway]):
        self._gateways: List[IPaymentGateway] = list(gateways)

    def pay(self, amount: float) -> List[PaymentResult]:
        results: List[PaymentResult] = []
        for gateway in self._gateways:
            try:
                results.append(gateway.pay(amount))
            except Exception as error:  # изоляция сбоя одного узла сети
                results.append(
                    PaymentResult(
                        gateway=gateway.display_name,
                        success=False,
                        transaction_id="",
                        message=f"Ошибка при оплате: {error}",
                    )
                )
        return results

    def refund(self, transaction_id: str) -> List[RefundResult]:
        results: List[RefundResult] = []
        for gateway in self._gateways:
            try:
                results.append(gateway.refund(transaction_id))
            except Exception as error:
                results.append(
                    RefundResult(
                        gateway=gateway.display_name,
                        success=False,
                        message=f"Ошибка при возврате: {error}",
                    )
                )
        return results
