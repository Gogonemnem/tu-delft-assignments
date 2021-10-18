import unittest
from project.randomizer.randomizer_of_tasks import Randomizer


class TestRandomizeroOfTasks(unittest.TestCase):
    def test_values(self):
        #Make sure value errors are raised when input not equal to one of the priorities
        #or preferrences.
        self.assertRaises(ValueError, Randomizer.hof_must_be_done_today(), prior='today')
        self.assertRaises(ValueError, Randomizer.hof_must_be_done_today(), prior='tomorrow')
        self.assertRaises(ValueError, Randomizer.hof_must_be_done_today(), prior=1)
        self.assertRaises(ValueError, Randomizer.hof_must_be_done_today(), prior=-1)
        self.assertRaises(ValueError, Randomizer.hof_must_be_done_today(), prior=True)
        self.assertRaises(ValueError, Randomizer.hof_must_be_done_today(), prior=False)