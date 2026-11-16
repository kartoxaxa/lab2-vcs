"""Тесты модуля аналитики."""

from payment_app.analytics import summarize
from payment_app.models import PaymentResult


def test_summarize_counts_results():
    """Сводка корректно считает успешные, неуспешные платежи и шлюзы."""
    payments = [
        PaymentResult("Банк A", True, "TX-1", "ok"),
        PaymentResult("Банк B", True, "TX-2", "ok"),
        PaymentResult("Банк A", False, "", "error"),
    ]

    summary = summarize(payments)

    assert summary["total"] == 3
    assert summary["successful"] == 2
    assert summary["failed"] == 1
    assert summary["gateways"] == ["Банк A", "Банк B"]


def test_summarize_empty_list():
    """Сводка по пустому списку содержит нули и пустой список шлюзов."""
    summary = summarize([])

    assert summary == {"total": 0, "successful": 0, "failed": 0, "gateways": []}
