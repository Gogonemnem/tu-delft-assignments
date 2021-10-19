import unittest
from project.randomizer.randomizer_of_tasks import Randomizer


class TestRandomizerOfTasks(unittest.TestCase):
    def test_values(self):
        #Make sure value errors are raised when input not equal to one of the priorities
        #or preferences.
        self.assertRaises(ValueError, Randomizer.hof_must_be_done_today(), prior=5)
        self.assertRaises(ValueError, Randomizer.hof_must_be_done_today(), prior=-1)
        self.assertRaises(ValueError, Randomizer.hof_must_be_done_today(), prior='yes')
        self.assertRaises(ValueError, Randomizer.hof_must_be_done_today(), prior=True)
        self.assertRaises(ValueError, Randomizer.hof_must_be_done_today(), pref='today')
        self.assertRaises(ValueError, Randomizer.hof_must_be_done_today(), pref=1)

    def test_biggest_in_dict_counter(self):
        #Make sure if multiple tasks have the same amount of occurrences in list_random,
        #that the first one of these tasks in dict_counter gets chosen.



    def test_same_task(self):
        pass
