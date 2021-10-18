from PyQt5.QtWidgets import QPushButton, QRadioButton, QGridLayout, QButtonGroup, QGroupBox
from project.task_list.to_do_list import ToDoList, CreateToDoList


class TaskListWidget(QGroupBox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setTitle("Daily to-do list")
        self.complete = 0

        self.group_task = QButtonGroup()
        self.group_remove = QButtonGroup()
        self.group_done = QButtonGroup()
        self.group_doing = QButtonGroup()
        self.tasks = CreateToDoList.list(new=True)

        self.layout = QGridLayout()
        self.setLayout(self.layout)

        for i, item in enumerate(self.tasks):
            self.task = self.create_task_select(i, item)
            self.remove = self.create_remove_button(i)
            self.doing = self.create_doing_button(i)
            self.done = self.create_done_button(i)

            self.color_buttons(i)

        # self.length_list = len(self.group_task.buttons())

    def removed(self, index):
        """Remove task from to-do list."""
        task_button = self.group_task.button(index)
        if task_button.isChecked():
            ToDoList.remove(task_button.text().replace(
                f'Task {index + 1} for today is: ', ''), self.group_task.id(self.group_task.checkedButton()))
            self.group_task.button(index).setVisible(False)
            self.group_done.button(index).setVisible(False)
            self.group_remove.button(index).setVisible(False)
            self.group_doing.button(index).setVisible(False)

    def ongoing(self, index):
        """Set status of task to "Doing"."""
        task_button = self.group_task.button(index)
        if task_button.isChecked():
            new_text = task_button.text().replace(f'Task {index + 1} for today is: ', '')
            ToDoList.execute(new_text, index)
            self.group_remove.button(index).setVisible(False)
            self.group_done.button(index).setVisible(True)

    def completed(self, index):
        """Set status of task to "Done"."""
        task_button = self.group_task.button(index)
        if task_button.isChecked():
            old_text = f'Task {index + 1} for today is: '
            ToDoList.complete(task_button.text().replace(old_text, ''), index)

            selected_task = self.group_task.button(index)
            selected_doing = self.group_doing.button(index)
            selected_done = self.group_done.button(index)
            # selected_remove = self.group_remove.button(index)

            selected_task.setDisabled(True)
            selected_doing.setVisible(False)
            selected_done.setVisible(False)

            # ## Do we want this?????
            # ## If so, selected_task may not be disabled!
            # selected_remove.setVisible(True)

            selected_task.setStyleSheet("color:  rgb(100, 175, 100)")
            selected_task.setText(
                selected_task.text().replace(old_text, '\u2713' + 'Completed: '))
            # selected_done.setStyleSheet("background-color:  rgb(175, 175, 175)")

            # ## Personal taste Question: Do we want to reorder the tasks?
            # ## I actually like it staying in order like this
            # ## This will also make our code a bit shorter
            #
            # self.group_task.removeButton(selected_task)
            # self.group_doing.removeButton(selected_doing)
            # self.group_done.removeButton(selected_done)
            # self.group_remove.removeButton(selected_remove)
            #
            # self.layout.addWidget(selected_task, self.length_list + self.complete, 0)
            # self.layout.addWidget(selected_doing, self.length_list + self.complete, 1)
            # self.layout.addWidget(selected_done, self.length_list + self.complete, 2)
            self.complete += 1

    def create_task_select(self, index, item):
        """Visualize the selection radio button"""
        task = QRadioButton()

        task.setText(f'Task {index + 1} for today is: {item}')
        task.setMinimumWidth(450)

        task.toggled.connect(lambda: self.color_buttons(index))

        self.group_task.addButton(task, index)
        self.layout.addWidget(task, index, 0)

        return task

    def create_remove_button(self, index):
        """Visualize the selection remove button"""
        remove = QPushButton()

        remove.setText('Remove task')
        remove.setCheckable(True)
        remove.setMaximumWidth(100)

        remove.clicked.connect(lambda: self.removed(index))

        self.group_remove.addButton(remove, index)
        self.layout.addWidget(remove, index, 2)

        return remove

    def create_doing_button(self, index):
        """Visualize the selection doing button"""
        doing = QPushButton()

        doing.setText('Do task')
        doing.setCheckable(True)
        doing.setMaximumWidth(100)

        doing.clicked.connect(lambda: self.ongoing(index))

        self.group_doing.addButton(doing, index)
        self.layout.addWidget(doing, index, 1)

        return doing

    def create_done_button(self, index):
        """Visualize the selection done button"""
        done = QPushButton()

        done.setText('Task completed')
        done.setCheckable(True)
        done.setVisible(False)
        done.setMaximumWidth(100)

        done.clicked.connect(lambda: self.completed(index))

        self.group_done.addButton(done, index)
        self.layout.addWidget(done, index, 2)

        return done

    def color_buttons(self, index):
        """Color selected task and accompanying buttons."""

        selected_remove = self.group_remove.button(index)
        selected_done = self.group_done.button(index)
        selected_doing = self.group_doing.button(index)

        is_checked = self.group_task.button(index).isChecked()

        selected_remove.setEnabled(is_checked)
        selected_done.setEnabled(is_checked)
        selected_doing.setEnabled(is_checked)

        if is_checked:
            selected_remove.setStyleSheet("background-color:  rgb(225, 75, 75)")
            selected_done.setStyleSheet("background-color:  rgb(100, 175, 100)")
            selected_doing.setStyleSheet("background-color:  rgb(40, 125, 175)")

        else:
            selected_remove.setStyleSheet("background-color:  rgb(225, 175, 175)")
            selected_done.setStyleSheet("background-color:  rgb(200, 225, 200)")
            selected_doing.setStyleSheet("background-color:  rgb(50, 200, 255)")
