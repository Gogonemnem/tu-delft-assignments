import random
from project.task_list.data_for_database import TaskList


class Randomizer:
    def __init__(self):
        self.database = TaskList().data_output()
        self.already_chosen = []

    def hof_must_be_done_today(self, prior, pref):
        """Takes the priority and the preferred time of a certain task as input
            and returns a list with tasks with that same priority and preferred time.
            Tasks with preferred time "Whole day" can be added too."""

        if prior not in ['must be done today', 'high', 'normal', 'low']:
            raise ValueError('Priority must either be must be done today, high, normal or low.')
        if pref not in ["Morning", "Afternoon", "Evening", "Whole day"]:
            raise ValueError('Preference must either be one of the following options:'
                             'Morning, Afternoon, Evening or Whole day.')

        lst = [task.name for task in self.database
               if task.priority == prior and task.preferred_time == pref]

        for task in self.database:
            if len(lst) < 3 and task.priority == prior and task.preferred_time == "Whole day" and task.name not in lst:
                lst.append(task.name)

        return lst

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

    def returns_list_random(self, task_list, pref):
        dict_priority_less = {}
        for task in self.database:
            if len(task_list) < 3 \
                    and (task.preferred_time == pref or task.preferred_time == "Whole day") \
                    and task.name not in task_list and task.name not in self.already_chosen:
                if task.priority == "high":
                    weight = 4
                elif task.priority == "normal":
                    weight = 2
                elif task.priority == "low":
                    weight = 1
                else:
                    weight = 0
                dict_priority_less[task.name] = weight

        if not dict_priority_less:
            return None

        return random.choices(list(dict_priority_less.keys()),
                                     weights=dict_priority_less.values(), k=5)

    def adds_most_freq_to_task_list(self, task_list, pref):
        print(self.returns_list_random(task_list, pref))
        if not self.returns_list_random(task_list, pref):
            return None

        dict_counter = {}
        for task2 in self.returns_list_random(task_list, pref):
            if task2 not in dict_counter:
                dict_counter[task2] = 1
            else:
                dict_counter[task2] += 1

        biggest = max(dict_counter, key=lambda k: dict_counter[k])
        print(self.already_chosen)
        if biggest not in task_list and biggest not in self.already_chosen:
            task_list.append(biggest)
            self.already_chosen.append(biggest)
        # self.returns_list_random(task_list, pref).clear()
        dict_counter.clear()

        return task_list

    def hof_randomize_tasks_other_today(self, task_list, pref):
        while len(self.adds_most_freq_to_task_list(task_list, pref)) < 3:
            if not self.adds_most_freq_to_task_list(task_list, pref):
                break
            self.adds_most_freq_to_task_list(task_list, pref)
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


test = Randomizer()
print(test.hof_must_be_done_today("must be done today", "Morning"),
        test.returns_list_random(test.hof_must_be_done_today("must be done today", "Morning"), "Morning"),
      test.adds_most_freq_to_task_list(test.hof_must_be_done_today("must be done today", "Morning"), "Morning"))