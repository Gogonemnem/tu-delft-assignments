import unittest
from project.randomizer.randomizer_of_tasks import Randomizer


class TestRandomizerOfTasks(unittest.TestCase):

    def test_returns_list_random(self):
        pass

    def test_most_freq(self):
        """Tests that when multiple tasks have the same amount of occurrences in list_random,
        that the first one of these tasks in dict_counter gets chosen."""
        test = Randomizer()
        pass

    def test_adds_most_freq_to_task_list(self):
        """"Tests if the function adds_most_freq_to_task_list actually adds the task
        with the biggest amount of occurrences in list_random."""
        test = Randomizer()
        task_list = test.hof_must_be_done_today("Morning")
        test.most_freq()
        test.adds_most_freq_to_task_list(task_list)
        self.assertEqual(task_list[-1], test.biggest)

    def test_



