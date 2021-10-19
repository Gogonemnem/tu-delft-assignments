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
        """Check status of all tasks in To-Do list file."""

        with open(folder / "ToDoList.txt", 'r', encoding='utf-7') as file_to_do:
            for lines in file_to_do:
                if lines.split("&")[1] == "To-Do" or lines.split("&")[1] == "Snooze" or\
                        lines.split("&")[1] == "Reschedule":
                    self.task_todo.append(lines.split("&")[0])
                elif lines.split("&")[1] == "Doing":
                    self.task_doing.append(lines.split("&")[0])
                else:
                    self.task_done.append(lines.split("&")[0])

    @staticmethod
    def change(task, num, status):
        """Change status of task [task] with id [num] from to-do list to status [status]."""

        with open(folder / "ToDoList.txt", "r+", encoding='utf-7') as file_to_do:
            lines = file_to_do.readlines()
            file_to_do.seek(0)
            for i in range(len(lines)):
                if lines[i].split("&")[1] == str(num):
                    file_to_do.write(task.replace("\n", "") + "&" + str(num) + "&" + status + "\n")
                else:
                    file_to_do.write(lines[i])
            file_to_do.truncate()


class CreateToDoList:
    def __init__(self):
        self.todo_list = self.list

    @staticmethod
    def list(new: bool = True):
        """Create to-do list from the randomizer if new is true and \n
         and based on the status of all tasks when the new is false. """

        tasks_list = []
        if new:
            tasks_list.extend(Randomizer().randomize_tasks_other_morning())
            tasks_list.extend(Randomizer().randomize_tasks_other_afternoon())
            tasks_list.extend(Randomizer().randomize_tasks_other_evening())
            with open(folder / "ToDoList.txt", 'w', encoding='utf-7') as file_todo:
                for i in range(len(tasks_list)):
                    file_todo.writelines(tasks_list[i] + "&" + str(i) + "&" + "To-Do" + '\n')
        else:
            with open(folder / "ToDoList.txt", 'r+', encoding='utf-7') as file_todo:
                lines = file_todo.readlines()
                file_todo.seek(0)
                i = 0
                file_todo.truncate()
                for line in lines:
                    if "Removed" not in line and "Done" not in line:
                        tasks_list.append(line.split("&")[0])
                        file_todo.write(line.split("&")[0] + "&" + str(i) + "&" + line.split("&")[2])
                        i += 1
                    else:
                        file_todo.write(line.split("&")[0] + "&" +
                                        str(int(line.split("&")[1]) + 100) +
                                        "&" + line.split("&")[2])
        return tasks_list
