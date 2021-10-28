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
        for atribute in [self.random, self.to_do_list, self.todo.available]:
            self.assertTrue(len(atribute) == 9)
            self.assertIsInstance(atribute, list)

    def test_task_in_new_list(self):
        """Check if all task from randomizer are in to do list in the right order"""
        for i, task in enumerate(self.to_do_list):
            self.assertEqual(self.to_do_list[i]["Task"], self.random[i])

    def test_change_status(self):
        """Check if changes made to the to do list are correctly adjusted"""
        # Change status in to do list
        self.todo.change(self.to_do_list[5], "Done")
        self.todo.change(self.to_do_list[6], "Doing")
        self.todo.change(self.to_do_list[2], "Rescheduled")
        self.todo.change(self.to_do_list[8], "Rescheduled")
        self.todo.change(self.to_do_list[3], "Doing")
        self.todo.change(self.to_do_list[0], "Done")
        self.todo.change(self.to_do_list[1], "Done")

        self.assertTrue(len(self.todo.available) == 4)

    def test_invalid_change_status(self):
        """When Task is set to "Rescheduled" or "Done" it can not be changed to "Doing or 'Done'"""
        self.todo.change(self.to_do_list[8], "Rescheduled")
        self.todo.change(self.to_do_list[0], "Done")
        self.todo.change(self.to_do_list[8], "Doing")
        self.todo.change(self.to_do_list[8], "Done")
        self.todo.change(self.to_do_list[0], "Doing")

        self.assertTrue(len(self.todo.available) == 7)

    def test_change_status_source(self):
        """Make local changes in test to compare to to do list"""
        self.random, self.to_do_list = ToDoList().create_todolist(output=True)
        self.todo = ToDoList()
        self.todo.change(self.to_do_list[5], "Done")
        self.todo.change(self.to_do_list[6], "Doing")
        self.todo.change(self.to_do_list[2], "Rescheduled")
        self.todo.change(self.to_do_list[8], "Rescheduled")
        self.todo.change(self.to_do_list[3], "Doing")
        self.todo.change(self.to_do_list[0], "Done")
        self.todo.change(self.to_do_list[1], "Done")

        self.to_do_list[5]["Task Status"] = "Done"
        self.to_do_list[6]["Task Status"] = "Doing"
        self.to_do_list[2]["Task Status"] = "Rescheduled"
        self.to_do_list[2]["Rescheduled Time"] = ""
        self.to_do_list[8]["Task Status"] = "Rescheduled"
        self.to_do_list[8]["Rescheduled Time"] = ""
        self.to_do_list[3]["Task Status"] = "Doing"
        self.to_do_list[0]["Task Status"] = "Done"
        self.to_do_list[1]["Task Status"] = "Done"

        # Compare local changes with to do list
        read_from_file = []
        for i in range(9):
            read_from_file.append(self.todo.read_file(output=True)[i])

        self.assertEqual(read_from_file, self.to_do_list)

    def test_empty_list(self):
        """Set status of all tasks to "Done" and check if new is created"""
        for i in range(len(self.todo.todolist)):
            self.assertEqual(self.todo.is_completed(), False)
            self.todo.change(self.todo.todolist[i], "Done")
        self.assertEqual(self.todo.is_completed(), True)
