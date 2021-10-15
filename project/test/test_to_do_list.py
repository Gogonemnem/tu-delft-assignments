import unittest
from project.task_list.task_list_widget import TaskListWidget
from project.randomizer.randomizer_of_tasks import randomize_tasks


class TesToDoList(unittest.TestCase):

    def test_attribute(self):
        # MAKE TO DO LIST A LOCAL VARIABLE
        # EACH TEST SHOULD BE SEPARATE OF ITSELF
        # AND SHOULD NOT DEPEND ON ALL THE OTHER TESTS
        # I DO NOT KNOW WHETHER THIS TASK IS STILL OKAY
        # IT IS WORKING SO I WILL NOT CHANGE THE TEST MORE

        # DELETE THESE COMMENTS WHEN YOU'VE READ THEM!!
        to_do_list = TaskListWidget()
        self.assertTrue(hasattr(to_do_list, 'complete'))
        self.assertTrue(hasattr(to_do_list, 'ButtonGroup_task'))
        self.assertTrue(hasattr(to_do_list, 'ButtonGroup_remove'))
        self.assertTrue(hasattr(to_do_list, 'ButtonGroup_done'))
        self.assertTrue(hasattr(to_do_list, 'layout'))
        self.assertTrue(hasattr(to_do_list, 'task'))
        self.assertTrue(hasattr(to_do_list, 'remove'))
        self.assertTrue(hasattr(to_do_list, 'done'))
        self.assertTrue(hasattr(to_do_list, 'number_of_buttons'))

    def test_scenario(self):
        to_do_list = TaskListWidget()
        rand_task = randomize_tasks()
        self.assertEqual(rand_task[0][0], to_do_list.tasks[0])
        self.assertEqual(rand_task[0][0], to_do_list.button_group_task.button(0).text())
        self.assertTrue(len(rand_task) == len(to_do_list.tasks))
        self.assertTrue(len(rand_task) == len(to_do_list.button_group_task.buttons()))
        self.assertTrue(len(rand_task) == len(to_do_list.button_group_remove.buttons()))
        self.assertTrue(len(rand_task) == len(to_do_list.button_group_done.buttons()))
