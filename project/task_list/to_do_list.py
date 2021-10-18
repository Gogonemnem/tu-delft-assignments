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
                self.task_todo.append(lines)
        with open(folder / "DoingList.txt", 'r', encoding='utf-7') as file_doing:
            for lines in file_doing:
                self.task_doing.append(lines)
        with open(folder / "DoneList.txt", 'r', encoding='utf-7') as file_done:
            for lines in file_done:
                self.task_done.append(lines)

    @staticmethod
    def execute(task):
        with open(folder / "DoingList.txt", 'a', encoding='utf-7') as file_doing:
            file_doing.writelines(task)
            file_doing.truncate()

        with open(folder / "ToDoList.txt", "r+", encoding='utf-7') as file_to_do:
            lines = file_to_do.readlines()
            file_to_do.seek(0)
            for i in lines:
                if not i.replace("\n", "") == task.replace("\n", ""):

                    file_to_do.write(i)
            file_to_do.truncate()

    @staticmethod
    def complete(task):
        with open(folder / "DoneList.txt", 'a', encoding='utf-7') as file_done:
            file_done.writelines(task)
        with open(folder / "Doinglist.txt", "r+", encoding='utf-7') as file_doing:
            lines = file_doing.readlines()
            file_doing.seek(0)
            for i in lines:
                if not i.replace("\n", "") == task.replace("\n", ""):

                    file_doing.write(i)
            file_doing.truncate()

    @staticmethod
    def remove(task):
        with open(folder / "Doinglist.txt", "r+", encoding='utf-7') as file_to_do:
            lines = file_to_do.readlines()
            file_to_do.seek(0)
            for i in lines:
                if not i.replace("\n", "") == task.replace("\n", ""):
                    file_to_do.write(i)
            file_to_do.truncate()


class CreateToDoList:
    def __init__(self):
        self.todo_list = self.list()

    @staticmethod
    def list(new: bool = True):
        tasks_list = []
        if new:
            tasks_list.extend(Randomizer().randomize_tasks_other_morning())
            tasks_list.extend(Randomizer().randomize_tasks_other_afternoon())
            tasks_list.extend(Randomizer().randomize_tasks_other_evening())
            with open(folder / "ToDoList.txt", 'w', encoding='utf-7') as file_todo:
                for i in range(len(tasks_list)):
                    file_todo.writelines(tasks_list[i] + '\n')
            with open(folder / "DoingList.txt", 'w', encoding='utf-7') as file_doing:
                file_doing.close()
            with open(folder / "DoneList.txt", 'w', encoding='utf-7') as file_done:
                file_done.close()
        else:
            print("Geen nieuwe lijst")
            with open(folder / "ToDoList.txt", 'r', encoding='utf-7') as file_todo:
                for line in file_todo.readlines():
                    print(line)
                    tasks_list.append(line)

        return tasks_list
