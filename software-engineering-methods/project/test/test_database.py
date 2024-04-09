import os
import unittest

import numpy as np
import pandas as pd

from project.task_list.data_for_database import TaskList, TaskObject

absolute_path = os.path.abspath(__file__)
fileDirectory = os.path.dirname(absolute_path)
path = os.path.join(fileDirectory, 'task_list_file_test')


class TestDatabase(unittest.TestCase):

    def test_delete_task(self):
        # Create a TaskList object
        task_list = TaskList(file=path)

        # Delete the task with index 1
        task_list.delete_task(1)

        # Create a dataframe for the remaining task
        remaining_task = pd.DataFrame({
            'Task': ['Take a walk'],
            'Estimated time (minutes)': [30],
            'Priority': ['normal'],
            'Periodic': ['max once a day'],
            'Preferred time': ['Whole day'],
            'Delete task': [np.nan],
            'Edit task:': [np.nan]})

        # Create the input for the deleted task, to restore the file
        task = ['Get some coffee', 10, 'low', 'several times a day', 'Morning']

        # Check if the task is really deleted, and if it was the right one
        # try and finally is used, because if these tests fail,
        # the database should still be restored to it's former version.
        try:
            self.assertEqual(task_list.data.iloc[0][0], remaining_task.iloc[0][0])
            self.assertEqual(task_list.data.iloc[0][3], remaining_task.iloc[0][3])
            self.assertEqual(len(task_list.data), len(remaining_task))
        finally:
            # Add the deleted task again
            task_list.add_task(task)

            try:
                # Check if the task is added
                self.assertEqual(len(task_list.data), 2)
                self.assertEqual(task_list.data.iloc[1][0], task[0])
                self.assertEqual(task_list.data.iloc[1][4], task[4])
            finally:
                pass

    def test_delete_periodic_task(self):
        # Create a new database
        task_list = TaskList(file=path)

        # Add a new task that is not periodic
        task = ['Water the plants', 5, 'high', 'not periodic', 'Whole day']
        task_list.add_task(task)

        # Check if the task is really added
        categories = ['Task', 'Estimated time (minutes)', 'Priority', 'Periodic', 'Preferred time']
        self.assertEqual(3, len(task_list.data))
        for i, element in enumerate(task):
            self.assertEqual(element, task_list.data.iloc[2][categories[i]])

        # Try the delete if not periodic function on all the tasks
        title = ['Take a walk', 'Get some coffee', 'Water the plants']
        for tsk in title:
            task_list.delete_task_periodic(tsk)

        # Check if only the last task is deleted
        self.assertEqual(2, len(task_list.data))
        self.assertEqual(task_list.data.iloc[0][0], 'Take a walk')
        self.assertEqual(task_list.data.iloc[1][0], 'Get some coffee')

    def test_data_output(self):
        # Checks the output of the data output function
        task_list = TaskList(file=path)
        object_list = task_list.data_output()

        self.assertIsInstance(object_list[0], TaskObject)
        self.assertIsInstance(object_list[1], TaskObject)
        self.assertEqual(object_list[0].name, 'Take a walk')
        self.assertEqual(object_list[1].time, 10)
        self.assertEqual(object_list[1].priority, 'low')
        self.assertEqual(object_list[0].periodic, 'max once a day')
        self.assertEqual(object_list[0].preferred_time, 'Whole day')
        self.assertEqual(len(object_list), len(task_list.data))

    def test_task_object(self):
        # Tests the attributes of the TaskObject class
        task_object = TaskObject('Water the plants', 5, 'high', 'not periodic', 'Whole day')
        attributes = ['name', 'time', 'priority', 'periodic', 'preferred_time']

        for attribute in attributes:
            self.assertTrue(hasattr(task_object, attribute))

    def test_edit_task(self):
        task_list = TaskList(file=path)
        categories = ['Task', 'Estimated time (minutes)', 'Priority', 'Periodic', 'Preferred time']
        original_values = ['Take a walk', 30, 'normal', 'max once a day', 'Whole day']
        new_values = ['Take a very long walk', 5, 'high', 'not periodic', 'Afternoon']

        # Test the original values
        for i, value in enumerate(original_values):
            self.assertEqual(task_list.data.iloc[0][i], value)

        # Edit the task, test if changed, revert back
        for i, category in enumerate(categories):
            task_list.edit_task(0, category, new_values[i])
            self.assertEqual(task_list.data.iloc[0][i], new_values[i])
            task_list.edit_task(0, category, original_values[i])

        # Test if the change back worked
        for i, value in enumerate(original_values):
            self.assertEqual(task_list.data.iloc[0][i], value)

    def test_create_dataframe(self):
        # Tests is the TaskList class creates panda DataFrames
        database = TaskList.add_file_data(path)
        task_list = TaskList(file=path)

        self.assertIsInstance(database, pd.DataFrame)
        self.assertIsInstance(task_list.data, pd.DataFrame)
        self.assertTrue(hasattr(task_list, 'data'))