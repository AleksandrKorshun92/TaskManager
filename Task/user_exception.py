"""
Модуль содержит различные пользовательские исключения, связанные с обработкой задач
"""


class TaskError(Exception):
    """Базовый класс для всех ошибок, связанных с задачами."""
    pass


class InvalidTaskIntError(TaskError):
    """Ошибка, возникающая при передаче строки вместо числового значения."""

    def __init__(self, num: str) -> None:
        super().__init__()
        self.num = num

    def __str__(self) -> str:
        return f"Должна быть цифра, а не строка - {self.num}"


class YearTaskError(TaskError):
    """Ошибка, возникающая при неправильном указании года."""

    def __init__(self) -> None:
        super().__init__()

    def __str__(self) -> str:
        return f"Срок выполнения не может быть в прошлом."


class NotInputError(TaskError):
    """Ошибка, возникающая при отсутствии введенных данных (пустые поля)."""

    def __init__(self) -> None:
        super().__init__()

    def __str__(self) -> str:
        return f"Ошибка ввода данных (пустые поля)"


class NotTaskError(TaskError):
    """Ошибка, возникающая при отсутствии задачи по переданным данным."""

    def __init__(self) -> None:
        super().__init__()

    def __str__(self) -> str:
        return f"Такая задача не найдена"


class DisplayError(TaskError):
    """Ошибка, возникающая при загрузке задач."""

    def __init__(self) -> None:
        super().__init__()

    def __str__(self) -> str:
        return f"Книга задач пустая (надо сделать больше новых задач)"


class InvalidIDError(TaskError):
    """Ошибка, возникающая при передаче неверного ID."""

    def __init__(self, book_id: int) -> None:
        super().__init__()
        self.book_id = book_id

    def __str__(self) -> str:
        return f"Задача не найдена с id - {self.book_id}"


class InvalidPriorityError(TaskError):
    """Ошибка, возникающая при передаче приоритета, кторого нет"""

    def __init__(self, data: int) -> None:
        super().__init__()
        self.data = data

    def __str__(self) -> str:
        return f"Такого приоритета нет - {self.data}"
