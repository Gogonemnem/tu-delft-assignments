import unittest
from project.randomizer.randomizer_of_tasks import Randomizer


class TestRandomizerOfTasks(unittest.TestCase):

    # def test_:
    #     test = Randomizer()
    #     test.hof_must_be_done_today("Morning")


    # def test_returns_None_list_random(self):
    #     """"Tests if the function 'returns_list_random' actually returns None
    #      if self.dict_priority_less is empty."""
    #     test = Randomizer()
    #     test.hof_must_be_done_today("Morning")
    #     test.returns_list_random("Morning")
    #     if not test.dict_priority_less:
    #         self.assertEqual(None, test.dict_priority_less)

    def test_returns_None_list_random(self):
        test = Randomizer()
        test.hof_must_be_done_today("Morning")
        test.returns_list_random("Morning")
        if len(test.lst) >= 3:
            self.assertEqual(test.dict_priority_less, None)

    def test_most_freq(self):
        """Tests that when multiple tasks have the same amount of occurrences in list_random,
        that the first one of these tasks in dict_counter gets chosen as the biggest."""
        test = Randomizer()
        test.randomize_tasks_other_morning()
        all_values = test.dict_counter.values()
        max_value = max(all_values)
        list_of_keys = list()

        for key, value in test.dict_counter.items():
            if value == max_value:
                list_of_keys.append(key)
        if len(list_of_keys) > 1:
            self.assertEqual(list_of_keys[0], test.biggest)
            for key in list_of_keys[1:]:
                self.assertNotEqual(key, test.biggest)

    def test_if_returns(self):
        """"Tests if the function 'most_freq' returns if 'lst_random' is empty."""
        test = Randomizer()
        test.hof_must_be_done_today("Morning")
        test.returns_list_random("Morning")
        test.most_freq()
        if not test.lst_random:
            self.assertEqual(None, test.lst_random)

    def test_adds_most_freq_to_task_list(self):
        """"Tests if the function adds_most_freq_to_task_list actually adds the task
        with the biggest amount of occurrences in list_random."""
        test = Randomizer()
        test.hof_must_be_done_today("Morning")
        test.returns_list_random("Morning")
        test.most_freq()
        test.adds_most_freq_to_task_list()
        self.assertEqual(test.lst[-1], test.biggest)

    def test_add_biggest_to_already_chosen_list(self):
        """"Tests if task name is added to the list 'already_chosen'
        if task has biggest amount of occurrences is lst_random and
        if the periodicity is not several times a day."""
        test = Randomizer()
        test.hof_must_be_done_today("Morning")
        test.returns_list_random("Morning")
        test.most_freq()
        test.adds_most_freq_to_task_list()
        for task in test.database:
            if task.name == test.biggest and task.periodic != "several times a day":
                self.assertEqual(test.already_chosen[-1], test.biggest)

    # def test_break(self):
    #     """"Tests if while loop actually breaks if dict_priority_less is empty."""
    #     test = Randomizer()
    #     test.hof_randomize_tasks_other_today("Morning")
    #     if len(test.lst) >= 3:




