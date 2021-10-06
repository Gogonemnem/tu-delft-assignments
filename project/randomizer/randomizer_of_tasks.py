import random
from project.task_list.data_for_database import TaskList


def randomize_tasks():
    database = TaskList()
    dictionary_object = database.data.to_dict()
    list_priority_low = []
    list_priority_normal = []
    list_priority_today = []
    list_priority_high = []
    total_list = []
    for task in dictionary_object['Task']:
        if dictionary_object['Priority'][task] == 'high':
            list_priority_high.append(dictionary_object['Task'][task])
        elif dictionary_object['Priority'][task] == 'must be done today':
            list_priority_today.append(dictionary_object['Task'][task])
        elif dictionary_object['Priority'][task] == 'normal':
            list_priority_normal.append(dictionary_object['Task'][task])
        elif dictionary_object['Priority'][task] == 'low':
            list_priority_low.append(dictionary_object['Task'][task])

    # Gonem deleted (weights=None, cum_weights=None)
    # I even think the k can be left empty too, but I'm not sure
    high = random.choices(list_priority_high, k=len(list_priority_high))
    today = random.choices(list_priority_today, k=len(list_priority_today))
    normal = random.choices(list_priority_normal, k=len(list_priority_normal))
    low = random.choices(list_priority_low, k=len(list_priority_low))
    total_list.extend([high, today, normal, low])
    # print(total_list)
    return total_list
