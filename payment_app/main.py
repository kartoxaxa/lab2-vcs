"""Демонстрационное приложение системы обработки платежей."""

from payment_app.gateways import (
    BelagroprombankGateway,
    BelinvestbankGateway,
    BPSberbankGateway,
    PriorbankGateway,
)
from payment_app.payment_processor import PaymentProcessor
from payment_app.storage import ResultStorage


def main() -> None:
    gateways = [
        BelagroprombankGateway("BY_AGRO_000042"),
        PriorbankGateway("PRIOR_TEST_51Hxxxx"),
        BPSberbankGateway("BPS_SHOP_98765"),
        BelinvestbankGateway("BIW_WALLET_+375291234567"),
    ]

    processor = PaymentProcessor(gateways)

    print("=== Система обработки платежей запущена ===")
    print("Клиент: Иван Петрович, г. Минск, +375 (29) 123-45-67")
    print("Сумма к оплате: 1500.50 BYN")

    payments = processor.pay(1500.50)
    for payment in payments:
        print(payment.message)

    storage = ResultStorage("результаты_платежей.json")
    storage.save_payments(payments)
    print("Результаты сохранены в результаты_платежей.json")

    transaction_id = next(
        (payment.transaction_id for payment in payments if payment.success), ""
    )
    if transaction_id:
        print(f"Возврат по TX={transaction_id}")
        refunds = processor.refund(transaction_id)
        for refund in refunds:
            print(refund.message)
        storage.save_refunds(refunds)

    print("--- Платёж только через Приорбанк и Белинвестбанк ---")
    extended = PaymentProcessor([gateways[1], gateways[3]])
    for payment in extended.pay(500.00):
        print(payment.message)


if __name__ == "__main__":
    main()
