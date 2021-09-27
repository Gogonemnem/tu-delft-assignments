import pandas as pd


class TaskList:

    def __init__(self):
        self.data = pd.DataFrame({'Task': ['Take a walk', 'Get some coffee', 'Vacuum the room', 'Do some stretching'],
                                  'Estimated time (minutes)': [30, 10, 15, 5],
                                  'Priority': ['normal', 'low', 'must be done today', 'high'],
                                  'Periodic': [True, True, False, True],
                                  'Preferred start time': ['10:00', '10:00', '14:00', '9:00'],
                                  'Preferred end time': ['17:00', '17:00', '16:00', '19:00']})

    def add_task(self, task):
        new_task = {'Task': task[0], 'Estimated time (minutes)': task[1], 'Priority': task[2],
                    'Periodic': task[3], 'Preferred start time': task[4], 'Preferred end time': task[5]}
        self.data.append(new_task, ignore_index=True)
