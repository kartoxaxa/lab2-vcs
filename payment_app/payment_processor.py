"""Основной модуль обработки платежей.

Модуль не импортирует конкретные шлюзы: он знает только об абстракции
IPaymentGateway, что обеспечивает слабую связность (принцип Open/Closed).
"""

from typing import Iterable, List

from logger import get_logger
from payment_app.gateways import IPaymentGateway
from payment_app.models import PaymentError, PaymentResult, RefundResult

logger = get_logger(__name__)


class PaymentProcessor:
    """Координатор, работающий с произвольным набором шлюзов."""

    def __init__(self, gateways: Iterable[IPaymentGateway]) -> None:
        """Сохранить набор шлюзов для проведения операций.

        Args:
            gateways: любая коллекция объектов IPaymentGateway.
        """
        self._gateways: List[IPaymentGateway] = list(gateways)
        logger.info("Создан обработчик платежей: шлюзов %d", len(self._gateways))

    def pay(self, amount: float) -> List[PaymentResult]:
        """Провести платёж через все шлюзы.

        Сбой одного шлюза не прерывает обработку остальных: ошибка
        логируется, а в результат добавляется запись success=False.

        Args:
            amount: сумма платежа в BYN.

        Returns:
            Список результатов по каждому шлюзу.
        """
        logger.info(
            "Запуск платежа на сумму %.2f BYN через %d шлюзов",
            amount,
            len(self._gateways),
        )
        results: List[PaymentResult] = []
        for gateway in self._gateways:
            try:
                results.append(gateway.pay(amount))
            except (PaymentError, ValueError, RuntimeError) as error:
                logger.error(
                    "Шлюз %s: ошибка платежа: %s",
                    gateway.display_name,
                    error,
                    exc_info=True,
                )
                results.append(
                    PaymentResult(
                        gateway=gateway.display_name,
                        success=False,
                        transaction_id="",
                        message=f"Ошибка при оплате: {error}",
                    )
                )
        successful = sum(1 for result in results if result.success)
        logger.debug("Платёж завершён: успешно %d из %d", successful, len(results))
        return results

    def refund(self, transaction_id: str) -> List[RefundResult]:
        """Вернуть средства по транзакции через все шлюзы.

        Args:
            transaction_id: идентификатор исходной транзакции.

        Returns:
            Список результатов возврата по каждому шлюзу.
        """
        logger.info(
            "Запуск возврата по TX=%s через %d шлюзов",
            transaction_id,
            len(self._gateways),
        )
        results: List[RefundResult] = []
        for gateway in self._gateways:
            try:
                results.append(gateway.refund(transaction_id))
            except (PaymentError, ValueError, RuntimeError) as error:
                logger.error(
                    "Шлюз %s: ошибка возврата: %s",
                    gateway.display_name,
                    error,
                    exc_info=True,
                )
                results.append(
                    RefundResult(
                        gateway=gateway.display_name,
                        success=False,
                        message=f"Ошибка при возврате: {error}",
                    )
                )
        logger.debug("Возврат завершён: результатов %d", len(results))
        return results
