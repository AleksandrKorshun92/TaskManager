"""
Функция для отображения главного меню приложения.

Меню содержит следующие пункты:
1. Показать задачи
2. Добавить задачу
3. Изменить задачу
4. Удалить задачу
5. Найти задачу
6. Выход из программы
"""

from Task.lexicon import LEXICON


def print_main_menu():
    print(f"\n {LEXICON['main_menu']} \n")
    print(LEXICON['display_tasks'])
    print(LEXICON['add_task'])
    print(LEXICON['update_status'])
    print(LEXICON['delete_tasks'])
    print(LEXICON['search_tasks'])
    print(f"{LEXICON['exit_menu']}\n")
