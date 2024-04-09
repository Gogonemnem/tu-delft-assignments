import os

import numpy as np
import pandas as pd

# Creates an absolute path, that works on different computers
absolute_path = os.path.abspath(__file__)
fileDirectory = os.path.dirname(absolute_path)
parent = os.path.dirname(fileDirectory)
path = os.path.join(parent, 'main', 'task_list_file')


class TaskList:
    """This class creates and manages the dataframe with the tasks"""

    def __init__(self, file=path):
        self.file = file
        self.data = self.add_file_data(file)

    def add_task(self, task):
        """Append the new task to the dataframe and updates the external database.

         Parameters: Task, estimated time, priority, periodic, preferred time.
         """

        new_task = {
            'Task': task[0],
            'Estimated time (minutes)': task[1],
            'Priority': task[2],
            'Periodic': task[3],
            'Preferred time': task[4],
            'Delete task': np.nan,
            'Edit task': np.nan
        }
        self.data = self.data.append(new_task, ignore_index=True)
        self.__write_to_file()

    def delete_task(self, index):
        """Delete a task from the dataframe and update the external database.

        Parameter: the index (int) of the row as input.
        """

        self.data = self.data.drop(index)
        self.data = self.data.reset_index(drop=True)
        self.__write_to_file()

    def delete_task_periodic(self, title):
        """Delete a task from the database if task is not periodic and update the external database.

        Parameter: the name (str) of the task as input.
        """

        if (self.data[self.data.Task == title].Periodic == 'not periodic').bool():
            index = self.data.index[self.data.Task == title][0]
            self.delete_task(index)

    def edit_task(self, index, category, new_value):
        """Edit one part of the task and updates the external database.

        Parameters: the index of the row (int), the category (str) and the new value.
        """

        self.data.at[index, category] = new_value
        self.__write_to_file()

    @staticmethod
    def add_file_data(file):
        """Return a dataframe of the task list database."""
        return pd.read_csv(file, sep='$')

    def __write_to_file(self):
        """Replace the external database with the current dataframe.

        This function must be used after every addition of the dataframe.
        """
        self.data.to_csv(self.file, sep='$', index=False)

    def data_output(self):
        """Return a list of objects from the class TaskObject."""
        task_object_list = []
        for i in range(len(self.data)):
            task_object_list.append(TaskObject(*self.data.iloc[i][:5]))

        return task_object_list


class TaskObject:
    """This class represents tasks.

    Attributes: name, estimated time, priority, priority, periodic and preferred time.
    """

    def __init__(self, name, time, priority, periodic, preferred_time):
        self.name = name
        self.time = time
        self.priority = priority
        self.periodic = periodic
        self.preferred_time = preferred_time