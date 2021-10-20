import os
import csv
from project.randomizer.randomizer_of_tasks import Randomizer

absolute_path = os.path.abspath(__file__)
fileDirectory = os.path.dirname(absolute_path)
parent = os.path.dirname(fileDirectory)
path = os.path.join(parent, 'main', 'todolist')


class ToDoList:
    def __init__(self):
        self.todolist: list[dict] = []
        self.status()

    def status(self):
        """Check status of all tasks in To-Do list file."""
        self.read_file()

        not_completed = [task for task in self.todolist if task['Task Status'] != 'Done']

        if not not_completed:
            self.create_todolist()

    def create_todolist(self):
        self.empty_lists()

        randomizer = Randomizer()
        lst = [
            *randomizer.randomize_tasks_other_morning(),
            *randomizer.randomize_tasks_other_afternoon(),
            *randomizer.randomize_tasks_other_evening()
        ]
        for i, task in enumerate(lst):
            self.todolist.append({'Task': task, 'ID': i + 1, 'Task Status': 'To-Do'})

    def empty_lists(self):
        self.todolist = []

    def read_file(self):
        with open(path, encoding='utf-8') as file_to_do:
            if file_to_do.readline() == 'Task&ID&Task Status':
                fieldnames = None
            else:
                fieldnames = ['Task', 'ID', 'Task Status']
            csv_reader = csv.DictReader(file_to_do, fieldnames=fieldnames, delimiter='&')
            self.todolist = list(csv_reader)

    def change(self, identifier, status):
        """Change status of task [task] with id [indentifier] from to-do list to status [status]."""
        pos = next((i for i, item in enumerate(self.todolist) if int(item["ID"]) == identifier), None)
        self.todolist[pos]['Task Status'] = status
        self.write_to_file()

    def remove_task(self, identifier):
        pos = next((i for i, item in enumerate(self.todolist) if int(item["ID"]) == identifier), None)
        self.todolist.pop(pos)
        self.write_to_file()

    def write_to_file(self):
        with open(path, 'w', encoding='utf-8') as file_to_do:
            csv_writer = csv.DictWriter(file_to_do, ['Task', 'ID', 'Task Status'], delimiter='&')
            csv_writer.writeheader()
            csv_writer.writerows(self.todolist)


def main():
    todolist = ToDoList()
    print(todolist.todolist)
    todolist.remove_task(0)


if __name__ == '__main__':
    main()
