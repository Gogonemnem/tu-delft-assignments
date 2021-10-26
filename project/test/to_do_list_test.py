import unittest
from project.task_list.task_list_widget import ToDoList


class TesToDoList(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.random, self.to_do_list = ToDoList().create_todolist(output=True)
        self.todo = ToDoList()

    def test_attribute(self):
        """Check all attributes of class To do list"""
        self.assertTrue(hasattr(self.todo, 'available'))
        self.assertTrue(hasattr(self.todo, 'is_completed'))
        self.assertTrue(hasattr(self.todo, 'status'))
        self.assertTrue(hasattr(self.todo, 'create_todolist'))
        self.assertTrue(hasattr(self.todo, 'change'))
        self.assertTrue(hasattr(self.todo, 'read_file'))
        self.assertTrue(hasattr(self.todo, 'write_to_file'))
        self.assertTrue(hasattr(self.todo, 'todolist'))
        self.assertIsInstance(self.todo.todolist, list)

    def test_new_list(self):
        """Check if input from randomizer is correctly interpreted"""
        self.assertTrue(len(self.random) == 9)
        self.assertIsInstance(self.random, list)
        self.assertTrue(len(self.to_do_list) == 9)
        self.assertIsInstance(self.to_do_list, list)
        self.assertTrue(len(self.todo.available) == 9)
        self.assertIsInstance(self.todo.available, list)

        for i, task in enumerate(self.to_do_list):
            self.assertEqual(self.to_do_list[i]["Task"], self.random[i])

    def test_change_status(self):
        """Check if changes made to the to do list are correctly adjusted"""
        self.todo.change(self.to_do_list[5], "Done")
        self.todo.change(self.to_do_list[6], "Doing")
        self.todo.change(self.to_do_list[2], "Rescheduled")
        self.todo.change(self.to_do_list[8], "Rescheduled")
        self.todo.change(self.to_do_list[3], "Doing")
        self.todo.change(self.to_do_list[0], "Done")

        self.to_do_list[5]["Task Status"] = "Done"
        self.to_do_list[6]["Task Status"] = "Doing"
        self.to_do_list[2]["Task Status"] = "Rescheduled"
        self.to_do_list[2]["Rescheduled Time"] = ""
        self.to_do_list[8]["Task Status"] = "Rescheduled"
        self.to_do_list[8]["Rescheduled Time"] = ""
        self.to_do_list[3]["Task Status"] = "Doing"
        self.to_do_list[0]["Task Status"] = "Done"

        self.assertEqual(self.todo.read_file(output=True)[5], self.to_do_list[5])
        self.assertEqual(self.todo.read_file(output=True)[6], self.to_do_list[6])
        self.assertEqual(self.todo.read_file(output=True)[2], self.to_do_list[2])
        self.assertEqual(self.todo.read_file(output=True)[8], self.to_do_list[8])
        self.assertEqual(self.todo.read_file(output=True)[3], self.to_do_list[3])
        self.assertEqual(self.todo.read_file(output=True)[0], self.to_do_list[0])
