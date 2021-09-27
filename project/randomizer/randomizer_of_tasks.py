import random
from project.task_list.data_for_database import TaskList


def randomize_tasks():
    database = TaskList()
    dictionaryObject = database.data.to_dict()
    list_priority_low = []
    list_priority_normal = []
    list_priority_today = []
    list_priority_high = []
    total_list = []
    for task in dictionaryObject['Task']:
        if dictionaryObject['Priority'][task] == 'high':
            list_priority_high.append(dictionaryObject['Task'][task])
        elif dictionaryObject['Priority'][task] == 'must be done today':
            list_priority_today.append(dictionaryObject['Task'][task])
        elif dictionaryObject['Priority'][task] == 'normal':
            list_priority_normal.append(dictionaryObject['Task'][task])
        elif dictionaryObject['Priority'][task] == 'low':
            list_priority_low.append(dictionaryObject['Task'][task])
    high = random.choices(list_priority_high, weights=None, cum_weights=None, k=len(list_priority_high))
    today = random.choices(list_priority_today, weights=None, cum_weights=None, k=len(list_priority_today))
    normal = random.choices(list_priority_normal, weights=None, cum_weights=None, k=len(list_priority_normal))
    low = random.choices(list_priority_low, weights=None, cum_weights=None, k=len(list_priority_low))
    total_list.extend([high, today, normal, low])
    print(total_list)
    return total_list

