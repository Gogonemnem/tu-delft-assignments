import random
from project.task_list.data_for_database import TaskList


class Randomizer:
    def __init__(self):
        self.database = TaskList().data_output()
        self.already_chosen = []
        self.dict_counter = {}
        self.lst_random = []
        self.biggest = "key"
        self.lst = []
        self.dict_priority_less = {}

    def hof_must_be_done_today(self, pref):
        """Takes the priority and the preferred time of a certain task as input
            and returns a list with tasks with that same priority and preferred time.
            Tasks with preferred time "Whole day" can be added too."""
        print(self.lst)
        self.lst = [task.name for task in self.database if task.priority == "must be done today"
                    and task.preferred_time == pref]
        # print(self.lst)

        for task in self.database:
            if len(self.lst) < 3 and task.priority == "must be done today" \
                    and task.preferred_time == "Whole day" \
                    and task.name not in self.lst and task.name not in self.already_chosen:
                self.lst.append(task.name)
                self.already_chosen.append(task.name)

        # print(self.lst)

    def returns_list_random(self, pref):
        """"Returns a randomized list of tasks for the given preferred part of the day.
        The tasks with a higher priority are more likely to appear in the list and may appear multiple times."""
        self.dict_priority_less.clear()
        weight = 0
        if len(self.lst) < 3:
            for task in self.database:
                if (task.preferred_time == pref or task.preferred_time == "Whole day") \
                        and task.name not in self.lst and task.name not in self.already_chosen:
                    if task.priority == "high":
                        weight = 4
                    elif task.priority == "normal":
                        weight = 2
                    elif task.priority == "low":
                        weight = 1
                    self.dict_priority_less[task.name] = weight

        if not self.dict_priority_less:
            return None

        self.lst_random = random.choices(list(self.dict_priority_less.keys()), weights=self.dict_priority_less.values(), k=5)
        # print(self.lst_random)

    def most_freq(self):
        """"Returns the task that appears most often in the randomized list.
        When there are multiple tasks that appear the most often, the first task that appears will be returned."""
        self.dict_counter.clear()
        if not self.lst_random:
            return

        for task_name in self.lst_random:
            if task_name not in self.dict_counter:
                self.dict_counter[task_name] = 1
            else:
                self.dict_counter[task_name] += 1

        self.biggest = max(self.dict_counter, key=lambda k: self.dict_counter[k])
        # print(self.biggest)

    def adds_most_freq_to_task_list(self):
        """"Adds the task that appears most often to the task list for the given part of the day."""
        if self.biggest not in self.lst \
                and self.biggest not in self.already_chosen:
            self.lst.append(self.biggest)
            self.already_chosen.append(self.biggest)
            # print(self.lst)
            # print(self.already_chosen)

    def hof_randomize_tasks_other_today(self, pref):
        """"Returns the task list for the given part of the day."""
        self.hof_must_be_done_today(pref)
        while self.lst and len(self.lst) < 3:
            self.returns_list_random(pref)
            if not self.dict_priority_less:
                break
            self.most_freq()
            self.adds_most_freq_to_task_list()
            # print(self.lst)
        # print(self.lst)
        return self.lst

    # def randomize_tasks_other_morning(self):
    #     return self.hof_randomize_tasks_other_today("Morning")
    #
    # def randomize_tasks_other_afternoon(self):
    #     return self.hof_randomize_tasks_other_today("Afternoon")
    #
    # def randomize_tasks_other_evening(self):
    #     return self.hof_randomize_tasks_other_today("Evening")

    def randomize_tasks(self):
        print(self.hof_randomize_tasks_other_today("Morning"),
              self.hof_randomize_tasks_other_today("Afternoon"),
              self.hof_randomize_tasks_other_today("Evening"))


test = Randomizer()
# print(test.randomize_tasks_other_morning())
# print(test.randomize_tasks_other_afternoon())
# print(test.randomize_tasks_other_evening())
test.randomize_tasks()


# def hof_randomize_tasks_other_today(self, task_list, pref):
    #     """Returns a randomized list of tasks to be done during the preferred time."""
    #
    #     dict_priority_less = {}
    #     while len(task_list) < 3:
    #         for task in self.database:
    #             if len(task_list) < 3 \
    #                 and (task.preferred_time == pref or task.preferred_time == "Whole day") \
    #                     and (task.name not in task_list and task.name not in self.already_chosen):
    #                 if task.priority == "high":
    #                     weight = 4
    #                 elif task.priority == "normal":
    #                     weight = 2
    #                 elif task.priority == "low":
    #                     weight = 1
    #                 else:
    #                     weight = 0
    #                 dict_priority_less[task.name] = weight
    #         if not dict_priority_less:
    #             break
    #         list_random = random.choices(list(dict_priority_less.keys()),
    #                                         weights=dict_priority_less.values(), k=5)
    #
    #
    #         dict_counter = {}
    #         for task2 in list_random:
    #             if task2 not in dict_counter:
    #                 dict_counter[task2] = 1
    #             else:
    #                 dict_counter[task2] += 1
    #         biggest = max(dict_counter, key=lambda k: dict_counter[k])
    #         if biggest not in task_list and biggest not in self.already_chosen:
    #             task_list.append(biggest)
    #             self.already_chosen.append(biggest)
    #         dict_priority_less.clear()
    #         list_random.clear()
    #         dict_counter.clear()
    #     return task_list