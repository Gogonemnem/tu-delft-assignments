import pandas as pd


class TaskList:

    def __init__(self):
        self.data = pd.DataFrame({'Task': [],
                                  'Estimated time (minutes)': [],
                                  'Priority': [],
                                  'Periodic': [],
                                  'Preferred time': [],
                                  'Delete task': [],
                                  'Edit task': []})
        self.add_file_data()

    def __add_task(self, task):
        new_task = {'Task': task[0], 'Estimated time (minutes)': task[1], 'Priority': task[2],
                    'Periodic': task[3], 'Preferred time': task[4], 'Delete task': None, 'Edit task': None}
        self.data = self.data.append(new_task, ignore_index=True)

    def delete_task(self, index):
        self.data = self.data.drop(index)
        self.data = self.data.reset_index(drop=True)

        with open('task_list_file', 'r') as file:
            lines = file.readlines()
        with open('task_list_file', 'w') as file:
            count = 0
            for line in lines:
                if count != index:
                    file.write(line)
                count += 1

    def add_file_data(self):
        with open('task_list_file', 'r') as file:
            for line in file:
                new_line = line.strip().split(';')
                self.__add_task(new_line)

    def write_to_file(self, task):
        with open('task_list_file', 'a') as file:
            print(*task, sep=';', file=file)

        self.__add_task(task)

    def data_output(self):
        data_dict = dict()
        for i in range(len(self.data)):
            data_dict[self.data.iloc[i][0]] = list(self.data.iloc[i][1:5])

        return data_dict

