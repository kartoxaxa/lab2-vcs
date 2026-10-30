"""Тесты конкретных реализаций платёжных шлюзов."""

import pytest

from payment_app.gateways import (
    BelagroprombankGateway,
    BelinvestbankGateway,
    BPSberbankGateway,
    PriorbankGateway,
)


@pytest.fixture(
    params=[
        BelagroprombankGateway("BY_AGRO_000042"),
        PriorbankGateway("PRIOR_TEST_51Hxxxx"),
        BPSberbankGateway("BPS_SHOP_98765"),
        BelinvestbankGateway("BIW_WALLET_+375291234567"),
    ]
)
def gateway(request):
    return request.param


def test_pay_returns_success(gateway):
    result = gateway.pay(100.0)

    assert result.success is True
    assert result.gateway == gateway.display_name
    assert result.transaction_id
    assert "100.00 BYN" in result.message


def test_refund_returns_success(gateway):
    result = gateway.refund("TEST-TX-0001")

    assert result.success is True
    assert result.gateway == gateway.display_name
    assert "TEST-TX-0001" in result.message
