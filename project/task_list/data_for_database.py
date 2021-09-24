def database():
    import pandas as pd
    data = pd.DataFrame({'Task': ['Take a walk', 'Get some coffee', 'Vacuum the room', 'Do some stretching'],
                         'Estimated time (minutes)': [30, 10, 15, 5],
                         'Priority': ['normal', 'low', 'must be done today', 'high'],
                         'Periodic': [True, True, False, True],
                         'Preferred start time': ['10:00', '10:00', '14:00', '9:00'],
                         'Preferred end time': ['17:00', '17:00', '16:00', '20:00']})

    return data
