import random
from project.task_list.data_for_database import TaskList


class Randomizer:
    def __init__(self):
        self.database = TaskList().data_output()

    def randomize_tasks(self):
        "Returns a list with the tasks that must be done today."
        list_priority_today = []
        for task in self.database:
            if task.priority == "must be done today":
                list_priority_today.append(task.name)
        return list_priority_today

    def randomize_tasks_other(self):
        "Should return a list with all the tasks that are planned for today, also known as a to-do list. \
        The first tasks in this list are the tasks that must happen today. \
        The other tasks in the list have either high, normal or low priority. \
        These are in randomized order, but the tasks with high priority are 4 times more likely \
        to be added to the to-do list than the low priority tasks and the normal priority tasks \
        are twice as much more likely to get added to the to-do list than the low priority tasks."
        tasks_today = []
        for task1 in self.randomize_tasks():
            tasks_today.append(task1)

        while len(tasks_today) < 9:
            dict_priority_less = dict()
            for task in self.database:
                if task.priority == "high":
                    weight = 4
                elif task.priority == "normal":
                    weight = 2
                elif task.priority == "low":
                    weight = 1
                else:
                    weight = 0
                dict_priority_less[task.name] = weight
            list_today = random.choices(list(dict_priority_less.keys()), weights=dict_priority_less.values(),
                                  k=5)

            d = dict()
            for task2 in list_today:
                if task2 not in d:
                    d[task2] = 1
                else:
                    d[task2] += 1
            biggest = max(d, key=lambda k: d[k])
            if biggest not in tasks_today:
                tasks_today.append(biggest)
        return tasks_today


test = Randomizer()
test.randomize_tasks_other()




