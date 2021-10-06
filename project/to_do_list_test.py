import unittest
from PyQt5.QtWidgets import QWidget, QApplication
import sys
from project.randomizer.randomizer_of_tasks import randomize_tasks
from project.task_list.task_list_widget import TaskListWidget


class CallGroupBox:
    def __init__(self):
        app = QApplication(sys.argv)
        self.window = TaskListWidget()
        self.text = self.window.task.text()
        self.buttons_task = self.window.ButtonGroup_task.buttons()
        self.buttons_done = self.window.ButtonGroup_done.buttons()
        self.buttons_remove = self.window.ButtonGroup_remove.buttons()


class TesToDoList(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.to_do_list = CallGroupBox().window

    def test_attribute(self):
        self.assertTrue(hasattr(self.to_do_list, 'completed'))
        self.assertTrue(hasattr(self.to_do_list, 'select'))
        self.assertTrue(hasattr(self.to_do_list, 'removed'))
        self.assertTrue(hasattr(self.to_do_list, 'ButtonGroup_task'))
        self.assertTrue(hasattr(self.to_do_list, 'ButtonGroup_done'))
        self.assertTrue(hasattr(self.to_do_list, 'ButtonGroup_remove'))
        self.assertTrue(hasattr(self.to_do_list, 'complete'))
        self.assertTrue(hasattr(self.to_do_list, 'tasks'))
        self.assertTrue(hasattr(self.to_do_list, 'task'))
        self.assertTrue(hasattr(self.to_do_list, 'done'))
        self.assertTrue(hasattr(self.to_do_list, 'remove'))
        self.assertTrue(hasattr(self.to_do_list, 'layout'))

    def test_scenario(self):
        rand_task = randomize_tasks()
        text = CallGroupBox().text.replace(f'Task {len(rand_task)} for today is: ', "")
        self.assertEqual(rand_task[0][0], self.to_do_list.tasks[0])
        self.assertEqual(rand_task[-1][-1], text)
        self.assertTrue(len(rand_task) == len(self.to_do_list.tasks))
        self.assertTrue(len(rand_task) == len(CallGroupBox().buttons_task))
        self.assertTrue(len(rand_task) == len(CallGroupBox().buttons_done))
        self.assertTrue(len(rand_task) == len(CallGroupBox().buttons_remove))
