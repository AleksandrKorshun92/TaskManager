"""
Класс TaskManager представляет собой менеджер задач, предназначенный для работы с коллекцией 
объектов типа Task.
Он предоставляет методы для загрузки, сохранения, просмотра и обработки задач, хранящихся в файле формата JSON.

### Конструктор:
Метод __init__ инициализирует экземпляр класса TaskManager, устанавливая имя файла для хранения 
задач (по умолчанию 'tasks_book.json'), пустой словарь для хранения задач и начальный идентификатор для новых задач. 
Затем вызывается метод load_tasks для загрузки существующих задач из указанного файла.

### Методы:
- load_tasks: загружает задачи из файла JSON. 
- save_tasks: сохраняет текущие задачи в файл JSON. 
- checking_for_task_availability: проверяет наличие хотя бы одной задачи. Если задач нет, выбрасывается исключение DisplayError.
- view_tasks_all: возвращает список всех активных (не выполненных) задач.
- view_tasks_category: группирует активные задачи по категориям и возвращает словарь с активными задачами.
- add_task: добавляет новую задачу в коллекцию задач. 
- task_date_check: проверяет корректность даты выполнения задачи. 
- checking_priority: проверяет, соответствует ли введенный приоритет одному из допустимых значений ("низкий", "средний", "высокий").
- checking_for_empty_data: проверяет, является ли ввод пустым. Если пользователь не ввел никаких данных, выбрасывается исключение NotInputError.
- checking_isdigit: проверяет, состоит ли ввод исключительно из цифр. Если данные содержат символы, отличные от цифр, выбрасывается исключение InvalidTaskIntError.
- checking_for_empty_id: проверяет существование задачи с указанным идентификатором. Если такой задачи нет, выбрасывается исключение InvalidIDError.
- update_task: обновляет существующую задачу новыми данными. 
- mark_task_completed: отмечает задачу с указанным идентификатором как выполненную. 
- delete_task: удаляет задачу либо по её идентификатору, либо по категории. Е
- search_tasks: выполняет поиск задач по ключевому слову, категории или статусу. 


Этот класс позволяет управлять задачами, обеспечивая их хранение, просмотр и фильтрацию по различным критериям.
"""

import json
import os
import logging
from typing import List, Dict, Optional, Any
from datetime import datetime
from Task.tasks_class import Task
from Task.lexicon import LEXICON, LEXICON_LOG
from Task.user_exception import (NotInputError, InvalidIDError, NotTaskError,
                                 DisplayError,
                                 InvalidTaskIntError, InvalidPriorityError,
                                 YearTaskError)


class TaskManager:
    def __init__(self, filename: str = 'tasks_book.json') -> None:
        """
        Инициализация экземпляра класса TaskManager.

        :param filename: Имя файла для хранения данных о задачах. По умолчанию 'tasks_book.json'.
        """
        self.filename: str = filename
        self.tasks: dict = {}
        self.next_id: int = 1
        self.load_tasks()

    def load_tasks(self) -> None:
        """
        Загружает книги из файла JSON.

        Метод пытается открыть указанный файл и загрузить данные о книгах в словарь tasks.
        Если файл не существует или возникает ошибка,записывает сообщение об ошибке в лог и 
        выводит сообщение пользователю.
        """
        try:
            if os.path.exists(self.filename):
                with open(self.filename, 'r', encoding='utf-8') as f:
                    data: List[Dict[str, Any]] = json.load(f)
                    for task_data in data:
                        task = Task.from_task_in_dict(task_data)
                        self.tasks[task.id] = task
                        if task.id >= self.next_id:
                            self.next_id = task.id + 1
            logging.info(LEXICON_LOG['load_task_book'])
        except (IOError, FileNotFoundError, json.JSONDecodeError) as e:
            logging.error(f"{LEXICON_LOG['error_load_task_book']} {e}")
            print(LEXICON['error_load_task_book'])

    def save_tasks(self):
        """
        Сохраняет задачи в файл JSON.

        Метод открывает файл для записи и сериализует данные о задачах из словаря tasks в формате JSON.
        Если при сохранении возникает ошибка, она записывается в лог и выводится сообщение об ошибке.
        """
        try:
            with open(self.filename, 'w', encoding='utf-8') as f:
                data: List[Dict[str, Any]] = [task.to_dict() for task in
                                              self.tasks.values()]
                json.dump(data, f, ensure_ascii=False, indent=4)
                logging.info(LEXICON_LOG['save_tasks'])
        except OSError as e:
            logging.error(f"{LEXICON_LOG['error_save_tasks']} {e}")
            print(LEXICON['error_save_tasks'])
        except Exception as e:
            logging.error(f"{LEXICON_LOG['error_save_tasks']} {e}")
            print(LEXICON['error_save_tasks'])

    def checking_for_task_availability(self):
        """ функция для проверки наличия задач
        
        :raises DisplayError: Если нет задач.
        """
        if not self.tasks:
            raise DisplayError

    def view_tasks_all(self) -> List[Task]:
        """ Просмотр всех текущих задач
        
        :return: Список активных задач.
        """

        tasks_book = [task for task in self.tasks.values() if
                      task.status == 'Не выполнена']
        return tasks_book

    def view_tasks_category(self) -> Dict[str, Task]:
        """ Просмотр задач по категориям
        :return: Словарь активных задач с разбивкой по категориям.
        """

        category = [task.category for task in self.tasks.values() if
                    task.status == "Не выполнена"]
        tasks_book = {}
        for key in category:
            tasks_book[key] = [task for task in self.tasks.values() if
                               task.category == key]
        return tasks_book

    def add_task(self, title: str, description: str, category: str,
                 due_date: str, priority: str) -> str:
        """
        Добавление новой задачи.

        :param title: Название задачи.
        :param description: Описание задачи.
        :param category: Категория задачи.
        :param due_date: Дата выполнения задачи.
        :param priority: Приоритет задачи.
        :return: Сообщение об успешном добавлении задачи.
        """
        task = Task(self.next_id, title, description, category, due_date,
                    priority)
        self.tasks[self.next_id] = task
        self.next_id += 1
        self.save_tasks()
        return f"{LEXICON['task_add_true']} {task.title}\n"

    def task_date_check(self, data: str):
        """ Функция для проверки даты задач
        
        :raises ValueError: Если ошибка в формате даты.
        :raises YearTaskError: Если ошибка в периоде задачи (ранее текущей даты).
        """
        try:
            parsed_date = datetime.strptime(data, '%Y-%m-%d')
        except ValueError as e:
            raise ValueError("Ошибка в формате даты")
        if parsed_date < datetime.now():
            raise YearTaskError

    def checking_priority(self, data: Optional[str]):
        """ Функция для проверки веденного приоритета
        
        :param data: Данные от пользовтеля.
        :raises InvalidPriorityError: Если выбран не правильный приоритет
        """
        if data.lower() not in ["низкий", "средний", "высокий"]:
            raise InvalidPriorityError(data)

    def checking_for_empty_data(self, data: Optional[str]):
        """ Функция для проверки введенных данных пользователем на пустоту
        
        :param data: Данные от пользовтеля.
        :raises NotInputError: Если пуступает пустая строка.
        """
        if not data:
            raise NotInputError

    def checking_isdigit(self, data: Optional[str]):
        """ Функция для проверки введенных данных на наличия цифр
        
        :param data: Данные от пользовтеля.
        :raises InvalidTaskIntError: Если данные не являются числом.
        """
        if not data.isdigit():
            raise InvalidTaskIntError(data)

    def checking_for_empty_id(self, task_id: str):
        """ Функция для проверки наличия задачи по id
        
        :param task_id: ID задачи.
        :raises InvalidIDError: Если задачи с id нет.
        """
        task_id = int(task_id)
        if task_id not in self.tasks:
            raise InvalidIDError(task_id)

    def update_task(self, task_id: Optional[str],
                    update_data: Dict[str, str] = None) -> str:
        """ Функция для изменения задачи на новые данные
        
        :param task_id: ID задачи.
        :param update_data: Новые данные для обновления задачи.
        :return: возвращает данные по успешному обновлению задачи
        """

        task_id = int(task_id)
        update_task = self.tasks.get(task_id).to_dict()
        for key, value in update_data.items():
            if not value:
                continue
            update_task[key] = update_data[key]
        new_task = Task.from_task_in_dict(update_task)
        self.tasks[task_id] = new_task
        self.save_tasks()
        return f"{LEXICON['task_update_true']} {new_task.id} c названием - {new_task.title}"

    def mark_task_completed(self, task_id: str) -> str:
        """
        Отметка задачи как выполненной по заданному идентификатору.

        :param task_id: Идентификатор задачи, статус которой нужно изменить..
        :return: Сообщение об успешном обновлении статуса задачи.
        """

        current_task: Task = self.tasks[int(task_id)]
        current_task.mark_completed()
        self.save_tasks()
        return (
            f"{LEXICON['task_update_status_true']} {current_task.id} c названием - {current_task.title} обновлен на - {current_task.status}")

    def delete_task(self, task_id: Optional[str] = None,
                    category: Optional[str] = None) -> str:
        """ Удаление задачи по идентификатору или категории 
        
        :param task_id: Идентификатор задачи, которую нужно удалить. Должен быть строкой, 
                        которая будет преобразована в целое число.
        :param category: Категория задач, которые нужно удалить.             
        :return: Сообщение об успешном удалении задачи.
        """
        if task_id.isdigit():
            task_id = int(task_id)
            removed_task = self.tasks.pop(task_id)
            self.save_tasks()
            return f"{LEXICON['delete_tasks_true_id']} {removed_task.id} c названием - {removed_task.title}"
        elif category:
            removed_list_category = [task for task in self.tasks.values() if
                                     task.category == category]
            for task in removed_list_category:
                self.tasks.pop(task.id)
            self.save_tasks()
            return f"{LEXICON['delete_tasks_true_category']} {category}"

    def search_tasks(self, keyword: Optional[str] = None,
                     category: Optional[str] = None,
                     status: Optional[str] = None) -> List[Task]:
        """ Поиск задач по ключевым словам, категории или статусу выполнения 
        
        :param keyword: Строка, содержащая поисковый запрос. Используется для поиска по названию или описанию.
        :param category: Строка, данные категории.
        :param status: Строка, данные статуса.
        :raises NotTaskError: Если не найдено ни одной книги по заданному запросу.
        :return: Список найденных книг.
        """

        results: List[Task] = []
        if keyword:
            keyword = keyword.lower()
            results = [task for task in self.tasks.values()
                       if
                       keyword in task.title.lower() or keyword in task.description.lower()]
        if category:
            results = [task for task in self.tasks.values() if
                       task.category.lower() == category.lower()]
        if status:
            results = [task for task in self.tasks.values() if
                       task.status.lower() == status.lower()]

        if not results:
            raise NotTaskError

        return results
