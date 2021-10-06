import pandas as pd
import numpy as np
import unittest
from project.task_list.data_for_database import TaskList, TaskObject


class TestDatabase(unittest.TestCase):

    def test_delete_task(self):
        task_list = TaskList()
        task_list.delete_task(1)
        remaining_task = pd.DataFrame({
                                    'Task': ['Take a walk'],
                                    'Estimated time (minutes)': [30],
                                    'Priority': ['normal'],
                                    'Periodic': [True],
                                    'Preferred time': ['Whole day'],
                                    'Delete task': [np.nan],
                                    'Edit task:': [np.nan]})
        task = ['Get some coffee', 10, 'low', True, 'Morning']

        try:
            self.assertEqual(task_list.data.iloc[0][0], remaining_task.iloc[0][0])
            self.assertEqual(task_list.data.iloc[0][3], remaining_task.iloc[0][3])
            self.assertEqual(len(task_list.data), len(remaining_task))
        finally:
            task_list.add_task(task)

            try:
                self.assertEqual(len(task_list.data), 2)
                self.assertEqual(task_list.data.iloc[1][0], task[0])
                self.assertEqual(task_list.data.iloc[1][4], task[4])
            finally:
                pass

    def test_data_output(self):
        task_list = TaskList()
        object_list = task_list.data_output()

        self.assertIsInstance(object_list[0], TaskObject)
        self.assertIsInstance(object_list[1], TaskObject)
        self.assertEqual(object_list[0].name, 'Take a walk')
        self.assertEqual(object_list[1].time, 10)
        self.assertEqual(object_list[1].priority, 'low')
        self.assertTrue(object_list[0].periodic)
        self.assertEqual(len(object_list), len(task_list.data))
