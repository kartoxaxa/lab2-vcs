"""Тесты координатора платежей."""

from payment_app.gateways import IPaymentGateway
from payment_app.models import PaymentResult, RefundResult
from payment_app.payment_processor import PaymentProcessor


class FakeGateway(IPaymentGateway):
    """Тестовый шлюз, который умеет имитировать отказ."""

    display_name = "Fake"

    def __init__(self, fail: bool = False) -> None:
        """Создать шлюз; fail=True заставляет методы выбрасывать RuntimeError."""
        self.fail = fail
        self.pay_calls = 0
        self.refund_calls = 0

    def pay(self, amount: float) -> PaymentResult:
        """Вернуть результат платежа или имитировать отказ шлюза."""
        self.pay_calls += 1
        if self.fail:
            raise RuntimeError("шлюз недоступен")
        return PaymentResult("Fake", True, "FAKE-1", f"Оплата {amount:.2f}")

    def refund(self, transaction_id: str) -> RefundResult:
        """Вернуть результат возврата или имитировать отказ шлюза."""
        self.refund_calls += 1
        if self.fail:
            raise RuntimeError("шлюз недоступен")
        return RefundResult("Fake", True, f"Возврат {transaction_id}")


def test_processor_calls_all_gateways():
    """Координатор вызывает каждый шлюз ровно один раз."""
    first = FakeGateway()
    second = FakeGateway()

    results = PaymentProcessor([first, second]).pay(10.0)

    assert len(results) == 2
    assert first.pay_calls == 1
    assert second.pay_calls == 1


def test_processor_handles_gateway_failure():
    """Сбой шлюза превращается в результат success=False, а не в исключение."""
    results = PaymentProcessor([FakeGateway(fail=True)]).pay(10.0)

    assert len(results) == 1
    assert results[0].success is False
    assert "шлюз недоступен" in results[0].message


def test_processor_does_not_depend_on_concrete_gateways():
    """Без шлюзов координатор возвращает пустые списки результатов."""
    processor = PaymentProcessor([])

    assert not processor.pay(1.0)
    assert not processor.refund("TX")
