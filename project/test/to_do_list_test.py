import unittest
from PyQt5.QtWidgets import QApplication
import sys
from project.randomizer.randomizer_of_tasks import Randomizer
from project.task_list.task_list_widget import ToDoList


class TesToDoList(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.to_do_list = ToDoList().todolist

    def test_attribute(self):
        self.assertTrue(hasattr(self.to_do_list, 'status'))
        self.assertTrue(hasattr(self.to_do_list, 'todolist'))
        self.assertTrue(hasattr(self.to_do_list, 'available'))
        self.assertTrue(hasattr(self.to_do_list, 'create_todolist'))
        self.assertTrue(hasattr(self.to_do_list, 'change'))
        self.assertTrue(hasattr(self.to_do_list, 'read_file'))
        self.assertTrue(hasattr(self.to_do_list, 'write_to_file'))

    def test_scenario(self):
        randomizer = Randomizer()
        lst = [
            *randomizer.randomize_tasks_other_morning(),
            *randomizer.randomize_tasks_other_afternoon(),
            *randomizer.randomize_tasks_other_evening()
        ]

        print(self.to_do_list)
        # for task, status in enumerate(self.to_do_list):
        #     self.assertEqual(self.to_do_list["Task"])


    def test_read_write(self):
        print("test voor lezen schrijven maken")
