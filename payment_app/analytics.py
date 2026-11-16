"""Аналитика по результатам платежей."""

from typing import Dict, Iterable, List

from logger import get_logger
from payment_app.models import PaymentResult

logger = get_logger(__name__)


def summarize(payments: Iterable[PaymentResult]) -> Dict[str, object]:
    """Собрать сводку по списку результатов платежей.

    Args:
        payments: результаты платежей по всем шлюзам.

    Returns:
        Словарь с общим числом платежей, числом успешных и неуспешных
        операций и списком задействованных шлюзов.
    """
    items: List[PaymentResult] = list(payments)
    successful = [item for item in items if item.success]
    gateways = sorted({item.gateway for item in items})
    logger.debug(
        "Сводка: всего %d, успешно %d, шлюзов %d",
        len(items),
        len(successful),
        len(gateways),
    )

    return {
        "total": len(items),
        "successful": len(successful),
        "failed": len(items) - len(successful),
        "gateways": gateways,
    }
