import csv
import os

from project.randomizer.queue_randomizer import QueueRandomizer
from project.task_list.data_for_database import TaskList

absolute_path = os.path.abspath(__file__)
fileDirectory = os.path.dirname(absolute_path)
parent = os.path.dirname(fileDirectory)
path = os.path.join(parent, 'main', 'todolist')


class ToDoList:
    column_names = ['Task', 'ID', 'Task Status', 'Rescheduled Time']
    delimiter = '&'

    def __init__(self, tasklist: TaskList):
        self.tasklist = tasklist
        self.todolist: list[dict] = []
        self.status()

    @property
    def available(self):
        """Return list of task id's that are able to be scheduled."""

        return [task for task in self.todolist
                if task['Task Status'] not in ('Done', 'Rescheduled', 'Skipped')]

    def is_completed(self) -> bool:

        next_task = next((task for task in self.todolist if task['Task Status'] != 'Done'), None)
        return not next_task

    def status(self):
        """Check status of all tasks in To-Do list file."""

        self.read_file()

        if self.is_completed():
            self.create_todolist()
            self.write_to_file()

    def create_todolist(self, output=False):
        """Generate a new to-do list."""
        self.todolist = []

        randomizer = QueueRandomizer(self.tasklist)
        lst = [
            *randomizer.randomize_tasks_other_morning(),
            *randomizer.randomize_tasks_other_afternoon(),
            *randomizer.randomize_tasks_other_evening()
        ]

        for i, task in enumerate(lst):
            self.todolist.append(
                {'Task': task, 'ID': str(i + 1), 'Task Status': 'To-Do', 'Rescheduled Time': ''})

        self.write_to_file()

        if output:
            return lst, self.todolist

        return None

    def change(self, task: dict, status: str, time=None):
        """Change status of task [task] from to-do list to status [status]."""

        if task not in self.todolist:
            return

        index = self.todolist.index(task)
        self.todolist[index]['Task Status'] = status

        if status == 'Removed':
            self.todolist.pop(index)

        elif status == 'Rescheduled':
            task['Rescheduled Time'] = time

        elif status == 'Done':
            database = self.tasklist
            database.delete_task_periodic(task['Task'])

        self.write_to_file()

    def read_file(self, output=False):
        """Read the file contents transforming it to a list of tasks."""

        with open(path, encoding='utf-8') as file_to_do:
            if file_to_do.readline() == ToDoList.delimiter.join(ToDoList.column_names):
                fieldnames = None
            else:
                fieldnames = ToDoList.column_names

            csv_reader = csv.DictReader(file_to_do, fieldnames, delimiter=ToDoList.delimiter)
            self.todolist = list(csv_reader)

        if output:
            return self.todolist

        return None

    def write_to_file(self):
        """Write the list of tasks to the file."""

        with open(path, 'w', encoding='utf-8') as file_to_do:
            csv_writer = csv.DictWriter(
                file_to_do, ToDoList.column_names, delimiter=ToDoList.delimiter)
            csv_writer.writeheader()
            csv_writer.writerows(self.todolist)
