from PyQt5.QtWidgets import QPushButton, QRadioButton, QGridLayout, QButtonGroup, QGroupBox
# from project.randomizer.randomizer_of_tasks import Randomizer


class TaskListWidget(QGroupBox):
    def __init__(self,  *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setTitle("Daily to-do list")
        i = 0
        self.complete = 0
        self.layout = QGridLayout()
        self.ButtonGroup_task = QButtonGroup()
        self.ButtonGroup_remove = QButtonGroup()
        self.ButtonGroup_done = QButtonGroup()
        self.tasks = []
        # for cat in Randomizer.randomize_tasks():
        #     for task in cat:
        #         self.tasks.append(task)

        for item in self.tasks:
            self.task = QRadioButton(f'Button {i + 1}', self)
            self.task.setText(f'Task {i + 1} for today is: {item}')
            self.task.setMinimumWidth(450)
            self.ButtonGroup_task.addButton(self.task, i)
            self.remove = QPushButton(f'Button {i + 1}', self)
            self.remove.setText('Remove task')
            self.remove.setCheckable(True)
            self.remove.setMaximumWidth(100)
            self.ButtonGroup_remove.addButton(self.remove, i)
            self.done = QPushButton(f'Button {i + 1}', self)
            self.done.setText('Task completed')
            self.done.setCheckable(True)
            self.done.setMaximumWidth(100)
            self.ButtonGroup_done.addButton(self.done, i)
            self.layout.addWidget(self.task, i, 0)
            self.layout.addWidget(self.remove, i, 1)
            self.layout.addWidget(self.done, i, 2)
            self.setLayout(self.layout)
            i += 1

        self.number_of_buttons = len(self.ButtonGroup_task.buttons())
        self.ButtonGroup_task.buttonClicked.connect(lambda: self.select())
        self.ButtonGroup_remove.buttonClicked.connect(lambda: self.removed())
        self.ButtonGroup_done.buttonClicked.connect(lambda: self.completed())
        self.select()

    def select(self):
        for i in range(self.number_of_buttons):
            if not self.ButtonGroup_task.button(i) is None:
                if i == self.ButtonGroup_task.id(self.ButtonGroup_task.checkedButton()):
                    selected_remove = self.ButtonGroup_remove.button(i)
                    selected_remove.setDisabled(False)
                    selected_remove.setStyleSheet("background-color:  rgb(225, 75, 75)")
                    selected_done = self.ButtonGroup_done.button(i)
                    selected_done.setDisabled(False)
                    selected_done.setStyleSheet("background-color:  rgb(100, 175, 100)")

                else:
                    selected_remove = self.ButtonGroup_remove.button(i)
                    selected_remove.setDisabled(True)
                    selected_remove.setStyleSheet("background-color:  rgb(225, 175, 175)")
                    selected_done = self.ButtonGroup_done.button(i)
                    selected_done.setDisabled(True)
                    selected_done.setStyleSheet("background-color:  rgb(200, 225, 200)")

    def removed(self):
        for i in range(self.number_of_buttons):
            if i == self.ButtonGroup_task.id(self.ButtonGroup_task.checkedButton()):
                self.ButtonGroup_task.button(i).setVisible(False)
                self.ButtonGroup_done.button(i).setVisible(False)
                self.ButtonGroup_remove.button(i).setVisible(False)

    def completed(self):
        for i in range(self.number_of_buttons):
            if i == self.ButtonGroup_task.id(self.ButtonGroup_task.checkedButton()):
                selected_task = self.ButtonGroup_task.button(i)
                selected_task.setStyleSheet("color:  rgb(100, 175, 100)")
                selected_task.setText(u'\u2713' + 'Completed:' + selected_task.text().replace(
                    f'Task {i + 1} for today is:', ''))
                selected_remove = self.ButtonGroup_remove.button(i)
                selected_remove.setDisabled(True)
                selected_remove.setStyleSheet("background-color:  rgb(175, 175, 175)")
                selected_done = self.ButtonGroup_done.button(i)
                selected_done.setStyleSheet("background-color:  rgb(175, 175, 175)")
                self.ButtonGroup_remove.removeButton(self.ButtonGroup_remove.button(i))
                self.ButtonGroup_task.removeButton(self.ButtonGroup_task.button(i))
                self.ButtonGroup_done.removeButton(self.ButtonGroup_done.button(i))
                self.layout.addWidget(selected_task, self.number_of_buttons + self.complete, 0)
                self.layout.addWidget(selected_remove, self.number_of_buttons + self.complete, 1)
                self.layout.addWidget(selected_done, self.number_of_buttons + self.complete, 2)
                self.setLayout(self.layout)
                self.complete += 1
