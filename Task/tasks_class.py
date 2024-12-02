"""
Класс Task предназначен для представления задач, которые могут иметь различные характеристики: 
- идентификатор (id)
- название (title)
- описание (description)
- категория (category)
- срок выполнения (due_date)
- приоритет (priority)
- статус (status).

Конструктор класса (__init__) принимает все необходимые параметры для создания новой задачи.
Метод mark_completed() изменяет статус задачи на "Выполнена". 
Метод to_dict() возвращает словарь, содержащий все данные задачи, а статический метод from_task_in_dict()
создает новый объект Task, используя данные из переданного словаря.

Класс может использоваться в приложениях для управления задачами, 
где требуется отслеживать их выполнение, сортировку по категориям и приоритетам, 
а также изменение статуса.
"""

from typing import Dict


class Task:
    def __init__(self, book_id: int, title: str, description: str,
                 category: str,
                 due_date: str, priority: str):
        self.id = book_id
        self.title = title
        self.description = description
        self.category = category
        self.due_date = due_date
        self.priority = priority
        self.status = 'Не выполнена'

    def mark_completed(self):
        self.status = 'Выполнена'

    def to_dict(self) -> Dict[str, str]:
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "category": self.category,
            "due_date": self.due_date,
            "priority": self.priority,
            "status": self.status
        }

    @staticmethod
    def from_task_in_dict(data: Dict[str, str]) -> 'Task':
        task = Task(data['id'], data['title'], data['description'],
                    data['category'],
                    data['due_date'], data['priority'])
        task.status = data['status']
        return task
