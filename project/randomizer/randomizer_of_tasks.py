import random
import csv
from project.task_list.data_for_database import TaskList


class Randomizer:
    def __init__(self):
        self.database = TaskList().data_output()
        self.already_chosen = []

    #Takes the priority and the preferred time of a certain task as input
    #and returns a list with tasks with that same priority and preferred time.
    #Tasks with preferred time "Whole day" can be added too.
    def hof_must_be_done_today(self, prior, pref):
        lst = [task.name for task in self.database
               if task.priority == prior and task.preferred_time == pref]
        for task in self.database:
            if len(lst) < 3 and task.priority == prior and task.preferred_time == "Whole day" \
                    and (task.name not in lst or task.name not in self.already_chosen):
                lst.append(task.name)
        return lst

    #Returns a randomized list of tasks to be done during the preferred time.
    def hof_randomize_tasks_other_today(self, task_list, pref):
        dict_priority_less = {}
        while len(task_list) < 3:
            for task in self.database:
                if len(task_list) < 3 \
                    and (task.preferred_time == pref or task.preferred_time == "Whole day") \
                        and (task.name not in task_list or task.name not in self.already_chosen):
                    if task.priority == "high":
                        weight = 4
                    elif task.priority == "normal":
                        weight = 2
                    elif task.priority == "low":
                        weight = 1
                    else:
                        weight = 0
                    dict_priority_less[task.name] = weight
            list_random = random.choices(list(dict_priority_less.keys()),
                                            weights=dict_priority_less.values(), k=5)

            dict_counter = {}
            for task2 in list_random:
                if task2 not in dict_counter:
                    dict_counter[task2] = 1
                else:
                    dict_counter[task2] += 1
            biggest = max(dict_counter, key=lambda k: dict_counter[k])
            if biggest not in task_list and biggest not in self.already_chosen:
                task_list.append(biggest)
                self.already_chosen.append(biggest)
        return task_list

    def randomize_tasks_other_morning(self):
        return self.hof_randomize_tasks_other_today(
            self.hof_must_be_done_today("must be done today", "Morning"), "Morning")

    def randomize_tasks_other_afternoon(self):
        return self.hof_randomize_tasks_other_today(
            self.hof_must_be_done_today("must be done today", "Afternoon"), "Afternoon")

    def randomize_tasks_other_evening(self):
        return self.hof_randomize_tasks_other_today(
            self.hof_must_be_done_today("must be done today", "Evening"), "Evening")

    def write_lists_to_file(self):
        with open('file.csv', 'a', newline='') as file:
            header = ['Morning', 'Afternoon', 'Evening']
            writer = csv.DictWriter(file, fieldnames=header)
            writer.writeheader()
            writer.writerow({'Morning': self.randomize_tasks_other_morning(),
                             'Afternoon': self.randomize_tasks_other_afternoon(),
                             'Evening': self.randomize_tasks_other_evening()})


test = Randomizer()
test.write_lists_to_file()