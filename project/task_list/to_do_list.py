import os
import csv
from project.randomizer.randomizer_of_tasks import Randomizer

absolute_path = os.path.abspath(__file__)
fileDirectory = os.path.dirname(absolute_path)
parent = os.path.dirname(fileDirectory)
path = os.path.join(parent, 'main', 'todolist')


class ToDoList:

    column_names = ['Task', 'ID', 'Task Status', 'Rescheduled Time']
    delimiter = '&'

    def __init__(self):
        self.todolist: list[dict] = []
        self.status()

    @property
    def available(self):
        """Return list of task id's that are able to be scheduled"""

        return [task for task in self.todolist if task['Task Status'] not in ('Done', 'Rescheduled')]

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
        """Generates a new to-do list"""
        self.todolist = []

        randomizer = Randomizer()
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

        self.write_to_file()

    def read_file(self, output=False):
        """Reads the file contents transforming it to a list of tasks"""

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
        """Writes the list of tasks to the file"""

        with open(path, 'w', encoding='utf-8') as file_to_do:
            csv_writer = csv.DictWriter(file_to_do, ToDoList.column_names, delimiter=ToDoList.delimiter)
            csv_writer.writeheader()
            csv_writer.writerows(self.todolist)


def main():
    todolist = ToDoList()
    print(todolist.todolist)
    # todolist.change()


if __name__ == '__main__':
    main()
