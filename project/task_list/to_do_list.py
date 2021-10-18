import os
from project.randomizer.randomizer_of_tasks import Randomizer
from pathlib import Path
folder = Path(os.getcwd())


class ToDoList:
    def __init__(self):
        self.task_todo = []
        self.task_doing = []
        self.task_done = []
        self.status()

    def status(self):
        with open(folder / "ToDoList.txt", 'r', encoding='utf-7') as file_to_do:
            for lines in file_to_do:
                if lines.split("&")[1] == "To-Do" or lines.split("&")[1] == "Snooze":
                    self.task_todo.append(lines.split("&")[0])
                elif lines.split("&")[1] == "Doing":
                    self.task_doing.append(lines.split("&")[0])
                else:
                    self.task_done.append(lines.split("&")[0])

    @staticmethod
    def execute(task, num):
        with open(folder / "ToDoList.txt", "r+", encoding='utf-7') as file_to_do:
            lines = file_to_do.readlines()
            file_to_do.seek(0)
            for i in range(len(lines)):
                if i == num:
                    file_to_do.write(task.replace("\n", "") + "&Doing" + "\n")
                else:
                    file_to_do.write(lines[i])
            file_to_do.truncate()

    @staticmethod
    def complete(task, num):
        with open(folder / "ToDoList.txt", "r+", encoding='utf-7') as file_to_do:
            lines = file_to_do.readlines()
            file_to_do.seek(0)
            for i in range(len(lines)):
                if i == num:
                    file_to_do.write(task.replace("\n", "") + "&Done" + "\n")
                else:
                    file_to_do.write(lines[i])
            file_to_do.truncate()

    @staticmethod
    def remove(num):
        with open(folder / "ToDoList.txt", "r+", encoding='utf-7') as file_to_do:
            lines = file_to_do.readlines()
            file_to_do.seek(0)
            for i in range(len(lines)):
                if not i  == num:
                    file_to_do.write(lines[i])
            file_to_do.truncate()


class CreateToDoList:
    def __init__(self):
        self.todo_list = self.list

    @staticmethod
    def list(new: bool = True):
        tasks_list = []
        if new:
            tasks_list.extend(Randomizer().randomize_tasks_other_morning())
            tasks_list.extend(Randomizer().randomize_tasks_other_afternoon())
            tasks_list.extend(Randomizer().randomize_tasks_other_evening())
            with open(folder / "ToDoList.txt", 'w', encoding='utf-7') as file_todo:
                for i in range(len(tasks_list)):
                    file_todo.writelines(tasks_list[i] + "&" + "To-Do" + '\n')
        else:
            with open(folder / "ToDoList.txt", 'r', encoding='utf-7') as file_todo:
                for line in file_todo.readlines():
                    tasks_list.append(line.split("&")[0])

        return tasks_list
