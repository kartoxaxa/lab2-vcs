"""Сохранение результатов платежей в JSON."""

import json
from pathlib import Path
from typing import Any, Dict, List

from logger import get_logger
from payment_app.models import PaymentResult, RefundResult

logger = get_logger(__name__)


class ResultStorage:
    """Простое файловое хранилище результатов."""

    def __init__(self, path: str | Path) -> None:
        """Задать путь к JSON-файлу с результатами.

        Args:
            path: путь к файлу или каталог с файлом результатов.
        """
        self._path = Path(path)
        logger.debug("Хранилище результатов: %s", self._path)

    def save_payments(self, payments: List[PaymentResult]) -> None:
        """Сохранить результаты платежей в файл.

        Args:
            payments: список результатов платежей.
        """
        logger.info("Сохранение %d платежей в %s", len(payments), self._path)
        self._write({"payments": [item.to_dict() for item in payments]})

    def save_refunds(self, refunds: List[RefundResult]) -> None:
        """Сохранить результаты возвратов в файл.

        Args:
            refunds: список результатов возврата.
        """
        logger.info("Сохранение %d возвратов в %s", len(refunds), self._path)
        self._write({"refunds": [item.to_dict() for item in refunds]})

    def load(self) -> Dict[str, Any]:
        """Прочитать сохранённые результаты.

        Returns:
            Словарь с ключами payments и refunds или пустой словарь,
            если файл ещё не создан.
        """
        if not self._path.exists():
            logger.debug("Файл %s не найден, возвращены пустые данные", self._path)
            return {}
        with self._path.open("r", encoding="utf-8") as stream:
            return json.load(stream)

    def _write(self, payload: Dict[str, Any]) -> None:
        """Дописать раздел payload в JSON-файл результатов."""
        data = self.load()
        data.update(payload)
        self._path.parent.mkdir(parents=True, exist_ok=True)
        with self._path.open("w", encoding="utf-8") as stream:
            json.dump(data, stream, ensure_ascii=False, indent=2)
