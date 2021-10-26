import random
from project.task_list.data_for_database import TaskList


class Randomizer:
    def __init__(self):
        self.database = TaskList().data_output()
        self.lst = []
        self.already_chosen = []
        self.dict_priority_less = {}
        self.lst_random = []
        self.dict_counter = {}
        self.biggest = "key"

    def hof_must_be_done_today(self, pref):
        """Takes the priority and the preferred time of a certain task as input
            and creates a list with tasks with that same priority and preferred time.
            Tasks with preferred time "Whole day" can be added too."""
        self.lst = [task.name for task in self.database if task.priority == "must be done today"
                    and task.preferred_time == pref]

        # Add task to task list and to a list that records which
        # tasks have already been chosen if the conditions hold.
        for task in self.database:
            if len(self.lst) < 3 and task.priority == "must be done today" \
                    and task.preferred_time == "Whole day" \
                    and task.name not in self.lst and task.name not in self.already_chosen:
                self.lst.append(task.name)
                self.already_chosen.append(task.name)

    def creates_list_random(self, pref):
        """"Creates a randomized list of tasks for the given preferred part of the day.
        The tasks with a higher priority are more likely to appear in the list and may appear multiple times."""
        self.dict_priority_less.clear()
        weight = 0

        # Add task to dictionary if the conditions hold.
        # The value in the key-value pair is the priority
        # of the task expressed as an integer.
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

        # Create a list with random tasks for the given part of the day.
        # The tasks in this list are not necessary unique (yet).
        self.lst_random = random.choices(list(self.dict_priority_less.keys()), weights=self.dict_priority_less.values(),
                                         k=5)

    def most_freq(self):
        """"Detects the task that appears most often in the randomized list.
        When there are multiple tasks that appear the most often,
        the first task that appears will be detected as the biggest."""
        self.dict_counter.clear()
        if not self.lst_random:
            return

        # Add every task from randomized list to dictionary.
        # The value of the key-value pair is the number of
        # occurrences the task appears in the randomized list.
        for task_name in self.lst_random:
            if task_name not in self.dict_counter:
                self.dict_counter[task_name] = 1
            else:
                self.dict_counter[task_name] += 1

        # Contains the task that has the biggest amount of occurrences.
        self.biggest = max(self.dict_counter, key=lambda k: self.dict_counter[k])

    def adds_most_freq_to_task_list(self):
        """"Adds the task that appears most often to the
        task list for the given part of the day."""
        if self.biggest not in self.lst \
                and self.biggest not in self.already_chosen:
            self.lst.append(self.biggest)

            # Add task to already chosen list if the periodicity isn't several times a day.
            # This way the task will appear at the most once a day in the to-do list.
            for task in self.database:
                if task.name == self.biggest and task.periodic != "several times a day":
                    self.already_chosen.append(self.biggest)

    def hof_randomize_tasks_other_today(self, pref):
        """"Returns the task list for the given part of the day."""
        self.hof_must_be_done_today(pref)

        # Keep adding tasks to task list while the list contains fewer
        # than three tasks and there are still tasks available to add.
        while len(self.lst) < 3:
            self.creates_list_random(pref)
            if not self.dict_priority_less:
                break
            self.most_freq()
            self.adds_most_freq_to_task_list()
        return self.lst

    def randomize_tasks_other_morning(self):
        """Returns a randomized list of tasks for the morning."""
        return self.hof_randomize_tasks_other_today("Morning")

    def randomize_tasks_other_afternoon(self):
        """Returns a randomized list of tasks for the afternoon."""
        return self.hof_randomize_tasks_other_today("Afternoon")

    def randomize_tasks_other_evening(self):
        """Returns a randomized list of tasks for the evening."""
        return self.hof_randomize_tasks_other_today("Evening")
