""" 
Данный модуль содержит функцию task_console, которая запускает консольное интерфейс для 
взаимодействия с задачами пользователя.

Эта функция представляет собой главный цикл программы, который отображает 
меню для пользователя, позволяя ему просматривать, добавлять, удалять, менять и искать задачи.
Она включает обработку пользовательского ввода, а также обработку 
ошибок, связанных с введенными данными, таких как отсутствие ввода, неверный 
формат или недопустимые значения.

В рамках этой функции выполняются следующие операции:
1. Отображение основного меню и ожидание выбора пользователя.
2. Вывод на экран всех незавершенных задач или с разбивкой по категориям. 
3. Добавление новой задачи с запросом названия, описания, категории, срока, приоритета.
4. Изменение задачи по идентификатору или изменения статуса задачи.
5. Удаление задачи по идентификатору или удаление категории задач.
6. Поиск задач по заданному критерию, категориям или статусу выполнения.
7. Выход из программы.

При возникновении ошибок они логируются, и пользователю предоставляется обратная связь о причине сбоя.
Все действия записываются в лог для последующего анализа.

Это функция является основным интерфейсом для работы с библиотекой и обеспечивает пользователю 
доступ ко всем основным операциям управления задачами.
"""

import logging
from Task.TaskManager import TaskManager
from Task.lexicon import LEXICON, LEXICON_LOG
import Task.View as view
from Task.user_exception import (NotInputError, InvalidIDError, NotTaskError,
                                 DisplayError,
                                 InvalidTaskIntError, InvalidPriorityError,
                                 YearTaskError)


def task_console():
    logging.info(LEXICON_LOG['start_console'])
    # Создаем экземпляр класса записной книжки названием - tasks_book.json)
    task_manager = TaskManager(filename='tasks_book.json')

    # запуск цикла основного меню
    while True:
        logging.info(LEXICON_LOG['run_main_menu'])

        try:
            choice = view.menu()
            match choice:
                case 1:  # Показать список задач
                    logging.info(LEXICON_LOG['display_tasks'])
                    try:
                        choice_view = view.input_user(LEXICON['choice_veiw'])
                        # производим проверку на наличия задач, на введенные данные
                        task_manager.checking_for_task_availability()
                        task_manager.checking_for_empty_data(choice_view)
                        task_manager.checking_isdigit(choice_view)
                        if choice_view == "1":
                            # Получаем и выводим все активные задачи (status - Не выполнена)
                            tasks_shows = task_manager.view_tasks_all()
                            view.print_message(LEXICON['tasks_display_true'])
                            view.show_tasks(tasks_shows)

                        if choice_view == "2":
                            # Получаем и выводим по категориям все активные задачи (status - Не выполнена)
                            tasks_shows = task_manager.view_tasks_category()
                            view.print_message(LEXICON['tasks_display_true'])
                            for key, value in tasks_shows.items():
                                view.show_tasks(value, key)
                        logging.info(LEXICON_LOG['tasks_display_true'])
                    except (NotInputError, ValueError, DisplayError,
                            InvalidTaskIntError) as e:
                        # Выводим информацию в логи и пользователю в зависимости от вида ошибок
                        logging.error(
                            f"{LEXICON_LOG['task_display_error']} {e}")
                        print(e)

                case 2:  # Добавление задачи
                    logging.info(LEXICON_LOG['add_task'])
                    # Запрашиваем у пользователя данные
                    new_task = view.actions_with_tasks(LEXICON['new_task'])

                    try:
                        # производим проверку корректность данных от пользователя (пустое название, формат даты, выбор приоритета)
                        task_manager.checking_for_empty_data(
                            new_task.get('title'))
                        task_manager.task_date_check(new_task.get("due_date"))
                        task_manager.checking_priority(
                            new_task.get('priority'))
                        # добавляем новую задачу
                        view.print_message(task_manager.add_task(**new_task))
                        logging.info(LEXICON_LOG['task_add_true'])

                    except (NotInputError, YearTaskError, ValueError,
                            InvalidPriorityError) as e:
                        # Выводим информацию в логи и пользователю в зависимости от ошибок
                        logging.error(f"{LEXICON_LOG['task_add_error']} {e}")
                        print(e)

                case 3:  # Изменения задачи
                    logging.info(LEXICON_LOG['update_task'])
                    try:
                        task_id = view.input_user(LEXICON['update_task_id'])
                        # производим проверку корректность данных от пользователя (отсутсвие пустых данных, наличия задачи с id)
                        task_manager.checking_for_empty_data(task_id)
                        task_manager.checking_for_empty_id(task_id)
                        choice_update = view.input_user(
                            LEXICON['choice_update'])
                        task_manager.checking_for_empty_data(choice_update)
                        if choice_update == "1":
                            # производим изменение задачи по id
                            update_data = view.actions_with_tasks(
                                LEXICON['update_task'])
                            print(
                                task_manager.update_task(task_id, update_data))

                        if choice_update == '2':
                            # производим изменение статуса задачи по id
                            print(task_manager.mark_task_completed(task_id))
                        logging.info(LEXICON_LOG['task_update_true'])
                    except (
                    InvalidIDError, NotInputError, InvalidTaskIntError) as e:
                        # Выводим информацию в логи и пользователю в зависимости от ошибок
                        logging.error(
                            f"{LEXICON_LOG['task_update_error']} {e}")
                        print(e)

                case 4:  # Удаление задачи
                    logging.info(LEXICON_LOG['delete_task'])
                    try:
                        task_date = view.actions_with_tasks(
                            LEXICON['delete_tasks_data'])
                        # проверка ввел пользователь id (если есть удаление по id)
                        if task_date.get('task_id'):
                            task_manager.checking_for_empty_id(
                                task_date.get('task_id'))
                        # производим удаление по полученным данным (id или category)
                        print(task_manager.delete_task(**task_date))
                        logging.info(LEXICON_LOG['delete_tasks_true'])
                    except (NotInputError, InvalidIDError) as e:
                        # Выводим информацию в логи и пользователю в зависимости от ошибок
                        logging.error(
                            f"{LEXICON_LOG['delete_task_error']} {e}")
                        print(e)

                case 5:  # Поиск задачи
                    logging.info(LEXICON_LOG['search_tasks'])
                    try:
                        # Запрашиваем у пользователя данные для выбора раздела поиска
                        choice_search = view.input_user(
                            LEXICON['choice_search'])
                        task_manager.checking_for_empty_data(choice_search)
                        if choice_search == "1":
                            # Поиск по ключевому слову
                            search_data = view.input_user(
                                LEXICON['search_tasks_keyword'])
                            result = task_manager.search_tasks(search_data)
                        if choice_search == "2":
                            # Поиск по категории
                            search_category = view.input_user(
                                LEXICON['search_tasks_category'])
                            result = task_manager.search_tasks(
                                category=search_category)
                        if choice_search == "3":
                            # Поиск по статусу
                            search_status = view.input_user(
                                LEXICON['search_tasks_status'])
                            result = task_manager.search_tasks(
                                status=search_status)

                        # Выводим задачи, которые найдены
                        view.print_message(LEXICON['search_tasks_true'])
                        view.show_tasks(result)
                        logging.info(LEXICON_LOG['search_tasks_true'])
                    except (
                    NotTaskError, NotInputError, InvalidTaskIntError) as e:
                        # Выводим информацию в логи и пользователю в зависимости от ошибок
                        logging.error(
                            f"{LEXICON_LOG['search_tasks_error']} {e}")
                        print(e)

                case 6:  # Завершение работы приложения
                    logging.info(LEXICON_LOG['exit_menu'])
                    print(f"{LEXICON['exit']} \n")
                    break

        except (ValueError, NotInputError) as e:
            # Выводим информацию в логи и пользователю в зависимости от ошибок
            logging.error(f"{LEXICON_LOG['exit_error']} {e}")
            print(e)


if __name__ == "__main__":
    # Настройка логирования (cохраняются в файл "task.log").
    logging.basicConfig(
        filename='task.log',
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
    )

    task_console()
