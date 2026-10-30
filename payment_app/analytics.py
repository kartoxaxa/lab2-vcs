"""Аналитика по результатам платежей."""

from typing import Dict, Iterable, List

from payment_app.models import PaymentResult


def summarize(payments: Iterable[PaymentResult]) -> Dict[str, object]:
    """Собрать сводку по списку результатов платежей."""
    items: List[PaymentResult] = list(payments)
    successful = [item for item in items if item.success]

    return {
        "total": len(items),
        "successful": len(successful),
        "failed": len(items) - len(successful),
        "gateways": sorted({item.gateway for item in items}),
    }
