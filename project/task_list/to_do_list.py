
class ToDoList:
    def __init__(self):
        self.task_todo = []
        self.task_doing = []
        self.task_done = []
        self.status()

    def status(self):
        file = open("ToDoList.txt", 'r')
        for lines in file:
            self.task_todo.append(lines)
        file.close()
        file2 = open("DoingList.txt", 'r')
        for lines in file2:
            self.task_doing.append(lines)
        file2.close()
        file3 = open("DoneList.txt", 'r')
        for lines in file3:
            self.task_done.append(lines)
        file3.close()

    @staticmethod
    def execute(task):
        file = open("DoingList.txt", 'a')
        file.writelines(task)
        file.close()
        file2 = open("ToDoList.txt", 'r')
        lines = file2.readlines()
        file2.close()
        file2 = open("ToDoList.txt", 'w')
        for line in lines:
            if not task == line:
                file2.writelines(line)
        file2.close()

    @staticmethod
    def complete(task):
        file = open("DoneList.txt", 'a')
        file.writelines(task)
        file.close()
        file2 = open("Doinglist.txt", 'r')
        lines = file2.readlines()
        file2.close()
        file2 = open("Doinglist.txt", 'w')
        for line in lines:
            if not task == line:
                file2.writelines(line)
        file2.close()

    @staticmethod
    def remove(task):
        file = open("ToDoList.txt", 'r')
        lines = file.readlines()
        file.close()
        file = open("ToDoList.txt", 'w')

        for line in lines:
            if not task == line.replace("\n", ""):
                file.writelines(line)
        file.close()

    def todo(self):
        return self.task_todo

    def doing(self):
        return self.task_doing

    def done(self):
        return self.task_done
