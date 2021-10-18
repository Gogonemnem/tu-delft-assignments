from PyQt5.QtWidgets import QPushButton, QRadioButton, QGridLayout, QButtonGroup, QGroupBox
from project.task_list.to_do_list import ToDoList, CreateToDoList


class TaskListWidget(QGroupBox):
    def __init__(self,  *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setTitle("Daily to-do list")
        i = 0
        self.complete = 0
        self.layout = QGridLayout()
        self.group_task = QButtonGroup()
        self.group_remove = QButtonGroup()
        self.group_done = QButtonGroup()
        self.group_doing = QButtonGroup()
        self.tasks = CreateToDoList.list(new=False)

        for item in self.tasks:
            self.task = QRadioButton(f'Button {i + 1}', self)
            self.task.setText(f'Task {i + 1} for today is: {item}')
            self.task.setMinimumWidth(450)
            self.group_task.addButton(self.task, i)
            self.remove = QPushButton(f'Button {i + 1}', self)
            self.remove.setText('Remove task')
            self.remove.setCheckable(True)
            self.remove.setMaximumWidth(100)
            self.group_remove.addButton(self.remove, i)
            self.doing = QPushButton(f'Button {i + 1}', self)
            self.doing.setText('Do task')
            self.doing.setCheckable(True)
            self.doing.setMaximumWidth(100)
            self.group_doing.addButton(self.doing, i)
            self.done = QPushButton(f'Button {i + 1}', self)
            self.done.setText('Task completed')
            self.done.setCheckable(True)
            self.done.setVisible(False)
            self.done.setMaximumWidth(100)
            self.group_done.addButton(self.done, i)
            self.layout.addWidget(self.task, i, 0)
            self.layout.addWidget(self.doing, i, 1)
            self.layout.addWidget(self.remove, i, 2)
            self.layout.addWidget(self.done, i, 2)
            self.setLayout(self.layout)
            i += 1

        self.length_list = len(self.group_task.buttons())
        self.group_task.buttonClicked.connect(self.select)
        self.group_remove.buttonClicked.connect(self.removed)
        self.group_done.buttonClicked.connect(self.completed)
        self.group_doing.buttonClicked.connect(self.ongoing)
        self.select()

    def select(self):
        """Visualise selected task and accompanying buttons."""

        for i in range(self.length_list):
            if not self.group_task.button(i) is None and\
                    i == self.group_task.id(self.group_task.checkedButton()):
                selected_remove = self.group_remove.button(i)
                selected_remove.setDisabled(False)
                selected_remove.setStyleSheet("background-color:  rgb(225, 75, 75)")
                selected_done = self.group_done.button(i)
                selected_done.setDisabled(False)
                selected_done.setStyleSheet("background-color:  rgb(100, 175, 100)")
                selected_doing = self.group_doing.button(i)
                selected_doing.setDisabled(False)
                selected_doing.setStyleSheet("background-color:  rgb(40, 125, 175)")

            elif not self.group_task.button(i) is None:
                selected_remove = self.group_remove.button(i)
                selected_remove.setDisabled(True)
                selected_remove.setStyleSheet("background-color:  rgb(225, 175, 175)")
                selected_done = self.group_done.button(i)
                selected_done.setDisabled(True)
                selected_done.setStyleSheet("background-color:  rgb(200, 225, 200)")
                selected_doing = self.group_doing.button(i)
                selected_doing.setDisabled(True)
                selected_doing.setStyleSheet("background-color:  rgb(50, 200, 255)")

    def removed(self):
        """Remove task from to-do list."""

        for i in range(self.length_list):
            if i == self.group_task.id(self.group_task.checkedButton()):
                ToDoList.remove(self.group_task.checkedButton().text().replace(
                    f'Task {i + 1} for today is: ', ''), self.group_task.id(self.group_task.checkedButton()))
                self.group_task.button(i).setVisible(False)
                self.group_done.button(i).setVisible(False)
                self.group_remove.button(i).setVisible(False)
                self.group_doing.button(i).setVisible(False)

    def ongoing(self):
        """Set status of task to "Doing"."""

        for i in range(self.length_list):
            if i == self.group_doing.id(self.group_doing.checkedButton()):
                ToDoList.execute(self.group_task.checkedButton().text().replace(
                    f'Task {i + 1} for today is: ', ''), self.group_task.id(self.group_task.checkedButton()))
                self.group_remove.button(i).setVisible(False)
                self.group_done.button(i).setVisible(True)

    def completed(self):
        """Set status of task to "Done"."""

        for i in range(self.length_list):
            if i == self.group_task.id(self.group_task.checkedButton()):
                ToDoList.complete(self.group_task.checkedButton().text().replace(
                    f'Task {i + 1} for today is: ', ''), self.group_task.id(self.group_task.checkedButton()))
                selected_task = self.group_task.button(i)
                selected_task.setDisabled(True)
                selected_task.setStyleSheet("color:  rgb(100, 175, 100)")
                selected_task.setText('\u2713' + 'Completed:' + selected_task.text().replace(
                    f'Task {i + 1} for today is: ', ''))
                selected_doing = self.group_doing.button(i)
                selected_doing.setVisible(False)
                selected_done = self.group_done.button(i)
                selected_done.setStyleSheet("background-color:  rgb(175, 175, 175)")
                selected_done.setVisible(False)
                self.group_remove.removeButton(self.group_remove.button(i))
                self.group_task.removeButton(self.group_task.button(i))
                self.group_done.removeButton(self.group_done.button(i))
                self.group_doing.removeButton(self.group_doing.button(i))
                self.layout.addWidget(selected_task, self.length_list + self.complete, 0)
                self.layout.addWidget(selected_doing, self.length_list + self.complete, 1)
                self.layout.addWidget(selected_done, self.length_list + self.complete, 2)
                self.setLayout(self.layout)
                self.complete += 1
