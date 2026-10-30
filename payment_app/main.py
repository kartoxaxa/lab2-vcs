"""Демонстрационное приложение системы обработки платежей."""

from logger import get_logger
from payment_app.analytics import summarize
from payment_app.gateways import (
    BelagroprombankGateway,
    BelinvestbankGateway,
    BPSberbankGateway,
    PriorbankGateway,
)
from payment_app.payment_processor import PaymentProcessor
from payment_app.storage import ResultStorage

logger = get_logger(__name__)


def main() -> None:
    gateways = [
        BelagroprombankGateway("BY_AGRO_000042"),
        PriorbankGateway("PRIOR_TEST_51Hxxxx"),
        BPSberbankGateway("BPS_SHOP_98765"),
        BelinvestbankGateway("BIW_WALLET_+375291234567"),
    ]

    processor = PaymentProcessor(gateways)

    logger.info("=== Система обработки платежей запущена ===")
    logger.info("Клиент: Иван Петрович, г. Минск, +375 (29) 123-45-67")
    logger.info("Сумма к оплате: 1500.50 BYN")

    payments = processor.pay(1500.50)
    for payment in payments:
        logger.info(payment.message)
    logger.info("Сводка по платежам: %s", summarize(payments))

    storage = ResultStorage("результаты_платежей.json")
    storage.save_payments(payments)
    logger.info("Результаты сохранены в результаты_платежей.json")

    transaction_id = next(
        (payment.transaction_id for payment in payments if payment.success), ""
    )
    if transaction_id:
        logger.info("Возврат по TX=%s", transaction_id)
        refunds = processor.refund(transaction_id)
        for refund in refunds:
            logger.info(refund.message)
        storage.save_refunds(refunds)

    logger.info("--- Платёж только через Приорбанк и Белинвестбанк ---")
    extended = PaymentProcessor([gateways[1], gateways[3]])
    for payment in extended.pay(500.00):
        logger.info(payment.message)


if __name__ == "__main__":
    main()
