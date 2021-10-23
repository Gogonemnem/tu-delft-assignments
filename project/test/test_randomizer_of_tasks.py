import unittest
from project.randomizer.randomizer_of_tasks import Randomizer


class TestRandomizerOfTasks(unittest.TestCase):

    def test_adds_most_freq_to_task_list(self):
        """"Tests if the function adds_most_freq_to_task_list actually adds the task
        with the biggest amount of occurrences in list_random."""
        test = Randomizer()
        test.hof_must_be_done_today("Morning")
        test.returns_list_random("Morning")
        test.most_freq()
        test.adds_most_freq_to_task_list()
        self.assertEqual(test.lst[-1], test.biggest)

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





