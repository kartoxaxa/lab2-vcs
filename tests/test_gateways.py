"""Тесты конкретных реализаций платёжных шлюзов."""

# pylint: disable=redefined-outer-name  # имя фикстуры совпадает с параметром теста

import pytest

from payment_app.gateways import (
    BelagroprombankGateway,
    BelinvestbankGateway,
    BPSberbankGateway,
    PriorbankGateway,
)
from payment_app.models import PaymentError


@pytest.fixture(
    params=[
        BelagroprombankGateway("BY_AGRO_000042"),
        PriorbankGateway("PRIOR_TEST_51Hxxxx"),
        BPSberbankGateway("BPS_SHOP_98765"),
        BelinvestbankGateway("BIW_WALLET_+375291234567"),
    ]
)
def gateway_instance(request):
    """Вернуть по очереди экземпляр каждого конкретного шлюза."""
    return request.param


def test_pay_returns_success(gateway_instance):
    """Платёж через любой шлюз завершается успешно и возвращает TX."""
    result = gateway_instance.pay(100.0)

    assert result.success is True
    assert result.gateway == gateway_instance.display_name
    assert result.transaction_id
    assert "100.00 BYN" in result.message


def test_refund_returns_success(gateway_instance):
    """Возврат через любой шлюз завершается успешно и содержит TX."""
    result = gateway_instance.refund("TEST-TX-0001")

    assert result.success is True
    assert result.gateway == gateway_instance.display_name
    assert "TEST-TX-0001" in result.message


def test_pay_rejects_non_positive_amount(gateway_instance):
    """Платёж на неположительную сумму отклоняется с PaymentError."""
    with pytest.raises(PaymentError, match="положительной"):
        gateway_instance.pay(0)
