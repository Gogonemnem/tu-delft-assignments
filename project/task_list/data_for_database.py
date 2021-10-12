import pandas as pd
import numpy as np
#this is the path I need to take for MacOS,
#I will always change it to the original when commiting
#path = '/Users/cristiancotovanu/Documents/GitHub/group-08/project/main/task_list_file'
path = 'task_list_file'

class TaskList:

    def __init__(self):
        self.data = self.add_file_data()

    def add_task(self, task):
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
        self.data = self.data.drop(index)
        self.data = self.data.reset_index(drop=True)
        self.__write_to_file()

    @staticmethod
    def add_file_data():
        return pd.read_csv(path, sep='$')

    def __write_to_file(self):
        self.data.to_csv(path, sep='$', index=False)

    def data_output(self):
        task_object_list = []
        for i in range(len(self.data)):
            task_object_list.append(TaskObject(*self.data.iloc[i][:5]))

        return task_object_list


class TaskObject:

    def __init__(self, name, time, priority, periodic, preferred_time):
        self.name = name
        self.time = time
        self.priority = priority
        self.periodic = periodic
        self.preferred_time = preferred_time
