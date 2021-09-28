import pandas as pd


class TaskList:

    def __init__(self):
        self.data = pd.DataFrame({'Task': ['Take a walk', 'Get some coffee', 'Vacuum the room', 'Do some stretching'],
                                  'Estimated time (minutes)': [30, 10, 15, 5],
                                  'Priority': ['normal', 'low', 'must be done today', 'high'],
                                  'Periodic': [True, True, False, True],
                                  'Preferred time': ['Whole day', 'Morning', 'Afternoon', 'Whole day'],
                                  'Delete task': [None, None, None, None],
                                  'Edit task': [None, None, None, None]})

    def add_task(self, task):
        new_task = {'Task': task[0], 'Estimated time (minutes)': task[1], 'Priority': task[2],
                    'Periodic': task[3], 'Preferred time': task[4], 'Delete task': None, 'Edit task': None}
        self.data = self.data.append(new_task, ignore_index=True)

    def delete_task(self, index):
        self.data = self.data.drop(index)
        self.data = self.data.reset_index(drop=True)
