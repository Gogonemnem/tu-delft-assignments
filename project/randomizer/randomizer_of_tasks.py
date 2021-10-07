import random
from project.task_list.data_for_database import TaskList
from project.task_list.data_for_database import TaskObject
from project.task_list.database_task_list import TaskListDatabase
from project.agenda.agenda import Agenda
from project.agenda.agenda import Activity


class Randomizer:
    def __init__(self):
        self.database = TaskList().data_output()

    def randomize_tasks(self):
        list_priority_today = []
        for task in self.database:
            if task.priority == "must be done today":
                list_priority_today.append(task.name)
        return list_priority_today

    def randomize_tasks_other(self):
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
            print(list_today)
            print(d)
            if max(d) not in tasks_today:
                tasks_today.append(max(d))
        print(tasks_today)
        return tasks_today

# class RandomizedTasks:
#     def __init__(self, database, agenda):
#         self.database = database
#         self.agenda = agenda
#
#     def add_randomized_tasks_must_today(self):
#         for task in Randomizer.randomize_tasks_today():
#             pref = self.database.data_output()[task][-1]
#             duration = self.database.data_output()[task][1]
#             while task not in self.agenda.today():
#                 for i in range(len(self.agenda.today())):
#                     if vars(i+1)['start_time'] - vars(i)['end_time'] >= duration:
#                         if pref == "Morning" and vars(i)['start_time'] >= 6 and vars(i+1)['end_time'] < 12:
#                             self.agenda.today().append(task)
#                         elif pref == "Afternoon" and vars(i)['start_time'] >= 12 and vars(i+1)['end_time'] < 18:
#                             self.agenda.today().append(task)
#                         elif pref == "Evening" and vars(i)['start_time'] >= 18 and vars(i+1)['end_time'] < 24:
#                             self.agenda.today().append(task)
#                         elif pref == "Whole day":
#                             self.agenda.today().append(task)
#                         elif pref == "Mor + Aft" and vars(i)['start_time'] >= 6 and vars(i+1)['end_time'] < 18:
#                             self.agenda.today().append(task)
#                         elif pref == "Mor + Eve" and 6 <= vars(i)['start_time'] < 12 and 18 <= vars(i+1)['start_time'] < 24:
#                             self.agenda.today().append(task)
#                         elif pref == "Aft + Eve" and 12 <= vars(i)['start_time'] and vars(i+1)['end_time'] < 24:
#                             self.agenda.today().append(task)
#                 return self.agenda.today()

test = Randomizer()
test.randomize_tasks_other()




