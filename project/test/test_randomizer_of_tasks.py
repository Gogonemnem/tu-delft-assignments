import unittest
from project.randomizer.randomizer_of_tasks import Randomizer


class TestRandomizerOfTasks(unittest.TestCase):
    def test_values(self):
        """Make sure value errors are raised when input is not equal
        to one of the priorities or preferences."""
        test = Randomizer()

        with self.assertRaises(ValueError):
            Randomizer.hof_must_be_done_today(test, 5, "Morning")

        with self.assertRaises(ValueError):
            Randomizer.hof_must_be_done_today(test, -1, "Morning")

        with self.assertRaises(ValueError):
            Randomizer.hof_must_be_done_today(test, 1.5, "Morning")

        with self.assertRaises(ValueError):
            Randomizer.hof_must_be_done_today(test, 'urgent', "Morning")

        with self.assertRaises(ValueError):
            Randomizer.hof_must_be_done_today(test, 'normal', "today")

        with self.assertRaises(ValueError):
            Randomizer.hof_must_be_done_today(test, 'normal', 1)

    def test_biggest_in_dict_counter(self):
        """Make sure if multiple tasks have the same amount of occurrences in list_random,
        that the first one of these tasks in dict_counter gets chosen."""
        test = Randomizer()
        pass


