import unittest
import pandas as pd
import numpy as np
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
        self.assertEqual(object_list[0].preferred_time, 'Whole day')
        self.assertEqual(len(object_list), len(task_list.data))

    def test_task_object(self):
        task_object = TaskObject('Water the plants', 5, 'high', False, 'Whole day')
        attributes = ['name', 'time', 'priority', 'periodic', 'preferred_time']

        for attribute in attributes:
            self.assertTrue(hasattr(task_object, attribute))

    def test_edit_task(self):
        task_list = TaskList()
        categories = ['Task', 'Estimated time (minutes)', 'Priority', 'Periodic', 'Preferred time']
        original_values = ['Take a walk', 30, 'normal', True, 'Whole day']
        new_values = ['Take a very long walk', 5, 'high', False, 'Afternoon']

        # test the original values
        for i in range(len(original_values)):
            self.assertEqual(task_list.data.iloc[0][i], original_values[i])

        # edit the task
        for i in range(len(categories)):
            task_list.edit_task(0, categories[i], new_values[i])

        # test if the tasks are changed
        for i in range(len(categories)):
            self.assertEqual(task_list.data.iloc[0][i], new_values[i])

        # change it back
        for i in range(len(categories)):
            task_list.edit_task(0, categories[i], original_values[i])

        # test if the change back worked
        for i in range(len(original_values)):
            self.assertEqual(task_list.data.iloc[0][i], original_values[i])

    def test_create_dataframe(self):
        database = TaskList.add_file_data()
        task_list = TaskList()

        self.assertIsInstance(database, pd.DataFrame)
        self.assertIsInstance(task_list.data, pd.DataFrame)
        self.assertTrue(hasattr(task_list, 'data'))
