"""Тесты файлового хранилища."""

import json

from payment_app.models import PaymentResult
from payment_app.storage import ResultStorage


def test_save_and_load(tmp_path):
    path = tmp_path / "results.json"
    storage = ResultStorage(path)

    storage.save_payments([PaymentResult("Тест", True, "TX-1", "Оплата прошла")])
    storage.save_refunds([])

    data = storage.load()
    assert data["payments"][0]["transaction_id"] == "TX-1"
    assert data["refunds"] == []
    assert json.loads(path.read_text(encoding="utf-8"))["payments"][0]["success"] is True
