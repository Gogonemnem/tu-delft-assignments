import random
from project.task_list.data_for_database import TaskList


class Randomizer:
    def __init__(self):
        self.database = TaskList().data_output()

    def must_be_done_tasks_morning(self):
        "Returns a list with the tasks that must be done today."
        list_priority_today_morning = []
        for task in self.database:
            if task.priority == "must be done today" and task.preferred_time == "Morning":
                list_priority_today_morning.append(task.name)
        return list_priority_today_morning

    def must_be_done_tasks_evening(self):
        list_priority_today_evening = []
        for task in self.database:
            if task.priority == "must be done today" and task.preferred_time == "Evening":
                list_priority_today_evening.append(task.name)
        return list_priority_today_evening

    def must_be_done_tasks_afternoon(self):
        list_priority_today_afternoon = []
        for task in self.database:
            if task.priority == "must be done today" and task.preferred_time == "Afternoon":
                list_priority_today_afternoon.append(task.name)
        return list_priority_today_afternoon

    def randomize_tasks_other_morning(self):
        "Should return a list with all the tasks that are planned for today, also known as a to-do list. \
        The first tasks in this list are the tasks that must happen today. \
        The other tasks in the list have either high, normal or low priority. \
        These are in randomized order, but the tasks with high priority are 4 times more likely \
        to be added to the to-do list than the low priority tasks and the normal priority tasks \
        are twice as much more likely to get added to the to-do list than the low priority tasks."
        tasks_today_morning = []

        for task in self.must_be_done_tasks_morning():
            tasks_today_morning.append(task)

        while len(tasks_today_morning) < 3:
            dict_priority_less = dict()
            for task in self.database:
                if task.preferred_time == "Morning" or task.preferred_time == "Whole day" :
                    if task.priority == "high":
                        weight = 4
                    elif task.priority == "normal":
                        weight = 2
                    elif task.priority == "low":
                        weight = 1
                    else:
                        weight = 0
                    dict_priority_less[task.name] = weight
            list_today_morning = random.choices(list(dict_priority_less.keys()), weights=dict_priority_less.values(),k=5)

            d = dict()
            for task2 in list_today_morning:
                if task2 not in d:
                    d[task2] = 1
                else:
                    d[task2] += 1
            biggest = max(d, key=lambda k: d[k])
            if biggest not in tasks_today_morning:
                tasks_today_morning.append(biggest)
        return tasks_today_morning

    def randomize_tasks_other_evening(self):
        tasks_today_evening= []

        for task in self.must_be_done_tasks_evening():
            tasks_today_evening.append(task)

        while len(tasks_today_evening) < 3:
            dict_priority_less = dict()
            for task in self.database:
                if task.preferred_time == "Evening" or task.preferred_time == "Whole day" :
                    if task.priority == "high":
                        weight = 4
                    elif task.priority == "normal":
                        weight = 2
                    elif task.priority == "low":
                        weight = 1
                    else:
                        weight = 0
                    dict_priority_less[task.name] = weight
            list_today_morning = random.choices(list(dict_priority_less.keys()), weights=dict_priority_less.values(),k=5)

            d = dict()
            for task2 in list_today_morning:
                if task2 not in d:
                    d[task2] = 1
                else:
                    d[task2] += 1
            biggest = max(d, key=lambda k: d[k])
            if biggest not in tasks_today_evening:
                tasks_today_evening.append(biggest)
        return tasks_today_evening

    def randomize_tasks_other_afternoon(self):
        tasks_today_afternoon= []

        for task in self.must_be_done_tasks_afternoon():
            tasks_today_afternoon.append(task)

        while len(tasks_today_afternoon) < 3:
            dict_priority_less = dict()
            for task in self.database:
                if task.preferred_time == "Afternoon" or task.preferred_time == "Whole day" :
                    if task.priority == "high":
                        weight = 4
                    elif task.priority == "normal":
                        weight = 2
                    elif task.priority == "low":
                        weight = 1
                    else:
                        weight = 0
                    dict_priority_less[task.name] = weight
            list_today_morning = random.choices(list(dict_priority_less.keys()), weights=dict_priority_less.values(),k=5)

            d = dict()
            for task2 in list_today_morning:
                if task2 not in d:
                    d[task2] = 1
                else:
                    d[task2] += 1
            biggest = max(d, key=lambda k: d[k])
            if biggest not in tasks_today_afternoon:
                tasks_today_afternoon.append(biggest)
        return tasks_today_afternoon



