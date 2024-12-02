"""Функция для запуска приложения"""

"""
Модуль для запуска скрипта
"""



from Task.Presenter import task_console
import logging


def setup_logging():
    """Настройка логирования."""
    logging.basicConfig(
        filename='task.log',
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
    )


if __name__ == "__main__":
    setup_logging()  # Запуск логирования

    task_console() # Запуск основной функции
