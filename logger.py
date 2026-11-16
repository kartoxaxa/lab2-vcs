"""Настройка логирования приложения."""

import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path

_CONSOLE_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
_FILE_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s:%(lineno)d | %(message)s"


def _configure_root(log_dir: str) -> None:
    """Настроить корневой логгер один раз: консоль и файл с ротацией."""
    root = logging.getLogger()
    if root.handlers:
        return

    root.setLevel(logging.DEBUG)

    console = logging.StreamHandler(stream=sys.stdout)
    console.setLevel(logging.INFO)
    console.setFormatter(logging.Formatter(_CONSOLE_FORMAT, "%H:%M:%S"))

    directory = Path(log_dir)
    directory.mkdir(parents=True, exist_ok=True)
    file_handler = RotatingFileHandler(
        directory / "application.log",
        maxBytes=1024 * 1024,
        backupCount=3,
        encoding="utf-8",
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(logging.Formatter(_FILE_FORMAT))

    root.addHandler(console)
    root.addHandler(file_handler)


def get_logger(name: str = "payment_app", log_dir: str = "logs") -> logging.Logger:
    """Вернуть логгер модуля, при первом вызове настроив обработчики.

    Args:
        name: имя логгера, обычно __name__ модуля.
        log_dir: каталог для файла журнала.

    Returns:
        Настроенный логгер с выводом в консоль (INFO) и файл (DEBUG).
    """
    _configure_root(log_dir)
    return logging.getLogger(name)
