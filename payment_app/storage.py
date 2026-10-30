"""Сохранение результатов платежей в JSON."""

import json
from pathlib import Path
from typing import Any, Dict, List

from payment_app.models import PaymentResult, RefundResult


class ResultStorage:
    """Простое файловое хранилище результатов."""

    def __init__(self, path: str | Path):
        self._path = Path(path)

    def save_payments(self, payments: List[PaymentResult]) -> None:
        self._write({"payments": [item.to_dict() for item in payments]})

    def save_refunds(self, refunds: List[RefundResult]) -> None:
        self._write({"refunds": [item.to_dict() for item in refunds]})

    def load(self) -> Dict[str, Any]:
        if not self._path.exists():
            return {}
        with self._path.open("r", encoding="utf-8") as stream:
            return json.load(stream)

    def _write(self, payload: Dict[str, Any]) -> None:
        data = self.load()
        data.update(payload)
        self._path.parent.mkdir(parents=True, exist_ok=True)
        with self._path.open("w", encoding="utf-8") as stream:
            json.dump(data, stream, ensure_ascii=False, indent=2)
