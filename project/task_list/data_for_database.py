import pandas as pd


class TaskList:

    def __init__(self):
        self.data = self.add_file_data()

    def add_task(self, task):
        new_task = {'Task': task[0], 'Estimated time (minutes)': task[1], 'Priority': task[2],
                    'Periodic': task[3], 'Preferred time': task[4], 'Delete task': None, 'Edit task': None}
        self.data = self.data.append(new_task, ignore_index=True)
        self.__write_to_file()

    def delete_task(self, index):
        self.data = self.data.drop(index)
        self.data = self.data.reset_index(drop=True)
        self.__write_to_file()

    @staticmethod
    def add_file_data():
        return pd.read_csv('task_list_file', sep='$')

    def __write_to_file(self):
        self.data.to_csv('task_list_file', sep='$', index=False)

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
