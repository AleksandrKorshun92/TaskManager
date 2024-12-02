""" 
Данный модуль содержит функцию для взаимодействия с пользователем для получения данных 
и ввывод информции

В рамках функций выполняются следующие операции:
1. Отображение меню 
2. Получения данных от пользователя по выбору пункта меню
3. Получения данных от пользователя для передачи в другие функции (id и тд)
4. Вывод пользователю информацию о задачах
"""

from typing import Dict, List, Any
from Task.lexicon import LEXICON


def menu() -> int:
    print(f"\n{LEXICON.get('main_menu')[0]}")
    for i in range(1, len(LEXICON.get('main_menu'))):
        print(f"\t{i}.{LEXICON.get('main_menu')[i]}")
    while True:
        select = input(LEXICON['choice_menu'])
        if select.isdigit() and 0 < int(select) < int(
                len(LEXICON.get('main_menu'))):
            return int(select)
        else:
            raise ValueError("Неверный выбор ")


def print_message(message: str):
    print('\n' + '=' * len(message))
    print(message)
    print('=' * len(message) + '\n')


def input_user(message: str) -> str:
    return input(message)


def actions_with_tasks(message: str) -> Dict[str, Any]:
    new: Dict[str, Any] = {}
    for key, value in message.items():
        new[key] = input(value)
    return new


def show_tasks(tasks_shows: List[Any], message: str = None):
    if message:
        print('=' * 30)
        print(' ' * 15 + message)
    for task in tasks_shows:
        print(
            f"ID: {task.id}, Название: {task.title}, Описание: {task.description}, "
            f"Категория: {task.category}, Срок выполнения: {task.due_date}, "
            f"Приоритет: {task.priority}, Статус: {task.status} \n")
