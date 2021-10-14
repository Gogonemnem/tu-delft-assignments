import random
from project.task_list.data_for_database import TaskList

already_chosen = []

class Randomizer:
    def __init__(self):
        self.database = TaskList().data_output()

    def hof_must_be_done_today(self, prior, pref):
        lst = [task.name for task in self.database if task.priority == prior and task.preferred_time == pref]
        for task in self.database:
            if len(lst) < 3 and task.priority == prior and task.preferred_time == "Whole day" and task.name not in already_chosen:
                lst.append(task.name)
                already_chosen.append(task.name)
        return lst

    def must_be_done_tasks_morning(self):
        return self.hof_must_be_done_today("must be done today", "Morning")

    def must_be_done_tasks_afternoon(self):
        return self.hof_must_be_done_today("must be done today", "Afternoon")

    def must_be_done_tasks_evening(self):
        return self.hof_must_be_done_today("must be done today", "Evening")

    def hof_randomize_tasks_other_today(self, task_list, pref):
        # print(len(task_list))
        while len(task_list) < 3:
            dict_priority_less = dict()
            for task in self.database:
                if (task.preferred_time == pref or (task.preferred_time == "Whole day" and task.name not in already_chosen)):
                    if task.priority == "high":
                        weight = 4
                    elif task.priority == "normal":
                        weight = 2
                    elif task.priority == "low":
                        weight = 1
                    else:
                        weight = 0
                    dict_priority_less[task.name] = weight
                    already_chosen.append(task.name)
            list_random = random.choices(list(dict_priority_less.keys()), weights=dict_priority_less.values(),
                                                k=5)
            # print(list_random)
            d = dict()
            for task2 in list_random:
                if task2 not in d:
                    d[task2] = 1
                else:
                    d[task2] += 1
            biggest = max(d, key=lambda k: d[k])
            if biggest not in task_list:
                task_list.append(biggest)
            return task_list

    def randomize_tasks_other_morning(self):
        return self.hof_randomize_tasks_other_today(self.must_be_done_tasks_morning(), "Morning")

    def randomize_tasks_other_afternoon(self):
        return self.hof_randomize_tasks_other_today(self.must_be_done_tasks_afternoon(), "Afternoon")

    def randomize_tasks_other_evening(self):
        return self.hof_randomize_tasks_other_today(self.must_be_done_tasks_evening(), "Evening")


test = Randomizer()
# print(test.must_be_done_tasks_afternoon())
# print(test.must_be_done_tasks_afternoon())
print(test.randomize_tasks_other_evening())
