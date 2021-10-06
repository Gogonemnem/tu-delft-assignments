import unittest
from datetime import datetime, timedelta
from project.task_list.task_list_widget import TaskListWidget
from project.randomizer.randomizer_of_tasks import randomize_tasks


class TesToDoList(unittest.TestCase):
    def test_attribute(self):
        self.to_do_list = TaskListWidget()
        self.assertTrue(hasattr(self.to_do_list, 'complete'))
        self.assertTrue(hasattr(self.to_do_list, 'ButtonGroup_task'))
        self.assertTrue(hasattr(self.to_do_list, 'ButtonGroup_remove'))
        self.assertTrue(hasattr(self.to_do_list, 'ButtonGroup_done'))
        self.assertTrue(hasattr(self.to_do_list, 'layout'))
        self.assertTrue(hasattr(self.to_do_list, 'task'))
        self.assertTrue(hasattr(self.to_do_list, 'remove'))
        self.assertTrue(hasattr(self.to_do_list, 'done'))
        self.assertTrue(hasattr(self.to_do_list, 'number_of_buttons'))

    def test_scenario(self):
        rand_task = randomize_tasks()
        self.assertEqual(rand_task[0][0], self.to_do_list.tasks[0])
        self.assertEqual(rand_task[0][0], self.to_do_list.ButtonGroup_task.button(0).text())
        self.assertTrue(len(rand_task) == len(self.to_do_list.tasks))
        self.assertTrue(len(rand_task) == len(self.to_do_list.ButtonGroup_task.buttons()))
        self.assertTrue(len(rand_task) == len(self.to_do_list.ButtonGroup_remove.buttons()))
        self.assertTrue(len(rand_task) == len(self.to_do_list.ButtonGroup_done.buttons()))

