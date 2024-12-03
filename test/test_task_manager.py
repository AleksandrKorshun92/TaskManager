
"""
Модуль содержит тесты (pytest) для классов Task и TaskManager, которые проверяют функциональность системы 
управления задачами. 

В модуле реализованы следующие тесты:
- тестирование создания задачи (test_task_creation_valid). 
Тестирует создания задачи с определенными параметрами и проверяет корректность

- добавление новой задачи (test_add_task)
Тестирует метод добавления задачи в систему.

-удаление задачи (test_delete_task)
Проверка удаления задачи из списка задач. 

- изменение статуса на выполнено задачи (test_mark_task_completed)

- поиск задач (test_search_tasks)
Тестирует поиск задач по ключевому слову. 

После завершения всех тестов файл с данными задач удаляется, чтобы избежать загрязнения данных 
при последующих запусках тестов.
"""


import os
from Task.tasks_class import Task
from Task.TaskManager import TaskManager

FILENAME = "test_tasks.json" # название файла для записи задач

# Тест для класса Task

# Cоздание задачи
def test_task_creation_valid():
    task = Task('1', "Test Task", "This is a test task", "Work", "2023-12-31", "High")
    assert task.title == "Test Task"

    assert task.description == "This is a test task"
    assert task.category == "Work"
    assert task.due_date == "2023-12-31"
    assert task.priority == "High"
    assert task.status == 'Не выполнена'


# Тесты для класса TaskManager

# Добавление задачи
def test_add_task():
    task_manager = TaskManager(FILENAME)
    initial_count = len(task_manager.tasks)
    task_manager.add_task("New Task", "Task description", "Personal", "2023-11-30", "высокий")
    assert len(task_manager.tasks) == initial_count + 1
    assert task_manager.tasks[1].title == "New Task"


# Удаление задачи
def test_delete_task():
    task_manager = TaskManager(FILENAME)
    task_manager.add_task("Task to delete", "Description", "Personal", "2023-11-30", "высокий")
    task_id = task_manager.tasks[2].id
    task_manager.delete_task(task_id=str(task_id))
    assert not any(task.id == task_id for task in task_manager.tasks.values())


# Изменение статуса задачи
def test_mark_task_completed():
    task_manager = TaskManager(FILENAME)
    task_manager.add_task("Task to complete", "Description", "Work", "2023-11-30", "высокий")
    task_id = task_manager.tasks[1].id
    task_manager.mark_task_completed(task_id)
    assert any(task.id == task_id and task.status == "Выполнена" for task in task_manager.tasks.values())


# Поиск задачи
def test_search_tasks():
    task_manager = TaskManager(FILENAME)
    task_manager.add_task("Search Task", "Find me", "Misc", "2023-11-30", "высокий")
    results = task_manager.search_tasks(keyword="Find")
    try: 
        assert len(results) == 1
        assert results[0].title == "Search Task"
    
    finally:
    # Удаление файла JSON после тестирования
        if os.path.exists(FILENAME):
            os.remove(FILENAME)