from PyQt5.QtWidgets import QPushButton, QCheckBox, QRadioButton, QGridLayout, QButtonGroup, QGroupBox
from project.randomizer.randomizer_of_tasks import randomize_tasks


class TaskListWidget(QGroupBox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setTitle("Below you can see the to do list")
        i = 0
        layout = QGridLayout()


        for item in randomize_tasks():
            # self.button = QtWidgets.QPushButton(randomize_tasks(item))
            # layout = QtWidgets.QVBoxLayout()
            # layout.addWidget(self.button)
            # self.setLayout(layout)

            # purely so that pylint does not cry, delete this later!!!
            print(f'delete this statement later in task_list_widget.py {item}')

            self.button = QRadioButton(f'Button {i + 1}', self)
            self.button.setText(f'The item is {item}')
            self.button.setMinimumWidth(450)
            self.remove = QPushButton(f'Button {i + 1}', self)
            self.remove.setText('Remove task')
            self.remove.setMaximumWidth(100)
            self.remove.setStyleSheet("background-color:  rgb(225, 75, 75)")
            self.done = QPushButton(f'Button {i + 1}', self)
            self.done.setText('Task completed')
            self.done.setMaximumWidth(100)
            self.done.setStyleSheet("background-color: rgb(100, 175, 100)")
            self.snooze = QPushButton(f'Button {i + 1}', self)
            self.snooze.setText('Snooze task')
            self.snooze.setMaximumWidth(100)
            self.snooze.setStyleSheet("background-color: rgb(175, 175, 175)")

            layout.addWidget(self.button, i, 0)
            layout.addWidget(self.remove, i, 1)
            layout.addWidget(self.done, i, 2)
            layout.addWidget(self.snooze, i, 3)
            self.setLayout(layout)
            i += 1

    # def add_task_button_to_tasklistwidget(self, randomized_list):
    #     self.randomized_list = randomize_tasks()
    #     count = 0
    #     for item in self.randomized_list:
    #         button = QtWidgets.QPushButton(item)
    #         count += 1
    #         self.layout.addWidget(button, count, 0)
