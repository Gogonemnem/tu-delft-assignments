import unittest
from project.randomizer.randomizer_of_tasks import Randomizer


class TestRandomizerOfTasks(unittest.TestCase):

    def test_most_freq(self):
        """Tests that when multiple tasks have the same amount of occurrences in list_random,
        that the first one of these tasks in dict_counter gets chosen as the biggest."""
        test = Randomizer()
        task_list = test.hof_must_be_done_today("Morning")
        test.returns_list_random(task_list, "Morning")
        test.most_freq()
        all_values = test.dict_counter.values()
        max_value = max(all_values)
        list_of_keys = list()
        #Iterate over all the items in dictionary to find keys with max value
        for key, value in test.dict_counter.items():
            if value == max_value:
                list_of_keys.append(key)
        if len(list_of_keys) > 1:
            self.assertEqual(list_of_keys[0], test.biggest)
            for key in list_of_keys[1:]:
                self.assertNotEqual(key, test.biggest)

    def test_adds_most_freq_to_task_list(self):
        """"Tests if the function adds_most_freq_to_task_list actually adds the task
        with the biggest amount of occurrences in list_random."""
        test = Randomizer()
        task_list = test.hof_must_be_done_today("Morning")
        test.most_freq()
        test.adds_most_freq_to_task_list(task_list)
        self.assertEqual(task_list[-1], test.biggest)

    # def test_hof_randomize_tasks_other_today(self):
    #     """"Tests if the while loop in the function hof_randomize_tasks_other_today breaks
    #     when the condition does no longer hold."""
    #     test = Randomizer()
    #     pref = "Morning"
    #     task_list = test.hof_must_be_done_today(pref)
    #     test.returns_list_random(pref)
    #     test.most_freq()
    #     test.hof_randomize_tasks_other_today(task_list)
    #     self.assertLessEqual(len(), 3)

    def test_


