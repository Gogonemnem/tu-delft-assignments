from PyQt5 import QtWidgets
from project.randomizer.randomizer_of_tasks import randomize_tasks


class TaskListWidget(QtWidgets.QGroupBox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setTitle("Below you can see the to do list")
        for item in randomize_tasks():
            # self.button = QtWidgets.QPushButton(randomize_tasks(item))
            # layout = QtWidgets.QVBoxLayout()
            # layout.addWidget(self.button)
            # self.setLayout(layout)

            # purely so that pylint does not cry, delete this later!!!
            print(f'delete this statement later in task_list_widget.py {item}')

            self.button = QtWidgets.QPushButton('to do list')
            layout = QtWidgets.QVBoxLayout()
            layout.addWidget(self.button)
            self.setLayout(layout)

    # def add_task_button_to_tasklistwidget(self, randomized_list):
    #     self.randomized_list = randomize_tasks()
    #     count = 0
    #     for item in self.randomized_list:
    #         button = QtWidgets.QPushButton(item)
    #         count += 1
    #         self.layout.addWidget(button, count, 0)
