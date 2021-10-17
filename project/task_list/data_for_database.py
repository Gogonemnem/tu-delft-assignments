import pandas as pd
import numpy as np
#  this is the path I need to take for MacOS,
#  I will always change it to the original when committing
# path = '/Users/cristiancotovanu/Documents/GitHub/group-08/project/main/task_list_file'
path = 'task_list_file'


class TaskList:
    """This class creates and manages the dataframe with the tasks"""

    def __init__(self):
        self.data = self.add_file_data()

    def add_task(self, task):
        """Appends the new task to the dataframe and updates the external database. \
        Needs a list as input: [Task, estimated time, priority, periodic, preferred time]"""

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
        """Deletes a task from the dataframe and updates the external database. \
        Needs the index (int) of the row as input."""

        self.data = self.data.drop(index)
        self.data = self.data.reset_index(drop=True)
        self.__write_to_file()

    def edit_task(self, index, category, new_value):
        """Edits one part of the task and updates the external database \
        Needs as input: the index of the row (int), the category (str) and the new value"""

        if new_value == 'True':
            new_value = True
        elif new_value == 'False':
            new_value = False

        self.data.at[index, category] = new_value
        self.__write_to_file()

    @staticmethod
    def add_file_data():
        """Returns a dataframe of the task list database."""
        return pd.read_csv(PATH, sep='$')

    def __write_to_file(self):
        """Replaces the external database with the current dataframe."""
        self.data.to_csv(PATH, sep='$', index=False)

    def data_output(self):
        """Returns a list of objects from the class TaskObject."""
        task_object_list = []
        for i in range(len(self.data)):
            task_object_list.append(TaskObject(*self.data.iloc[i][:5]))

        return task_object_list


class TaskObject:
    """Creates an object with the attributes: \
    name, estimated time, priority, priority, periodic and preferred time"""

    def __init__(self, name, time, priority, periodic, preferred_time):
        self.name = name
        self.time = time
        self.priority = priority
        self.periodic = periodic
        self.preferred_time = preferred_time
