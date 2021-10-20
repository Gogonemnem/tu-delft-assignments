from PyQt5.QtWidgets import QPushButton, QRadioButton, QGridLayout, QButtonGroup, QGroupBox

from project.randomizer.optimal_time import TimeRandomizer
from project.task_list.to_do_list import ToDoList


class TaskListWidget(QGroupBox):
    """Visualise Task that need to be done today"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.todolist = ToDoList()
        # self.time_randomizer = TimeRandomizer(self.todolist.todolist)

        self.setTitle("Daily to-do list")

        # Create groups for all button types
        self.group_task = QButtonGroup()
        self.group_remove = QButtonGroup()
        self.group_done = QButtonGroup()
        self.group_doing = QButtonGroup()

        self.layout = QGridLayout()
        self.setLayout(self.layout)

        self.create_to_do_list_visual()

        self.generate_new = QPushButton('Generate new to do list', self)
        self.layout.addWidget(self.generate_new, 99, 0, 1, 3)
        self.generate_new.clicked.connect(self.refresh)

    def create_to_do_list_visual(self):
        self.todolist.status()
        for task in self.todolist.todolist:
            # identifier = int(task['ID'])

            self.create_remove_button(task)
            self.create_doing_button(task)
            self.create_done_button(task)
            self.create_task_select(task)

            self.color_buttons(task)

    def removed(self, task: dict):
        """Remove task from to-do list."""
        identifier = int(task['ID'])
        self.todolist.change(task, 'Removed')
        self.layout.removeWidget(self.group_task.button(identifier))
        self.layout.removeWidget(self.group_done.button(identifier))
        self.layout.removeWidget(self.group_remove.button(identifier))
        self.layout.removeWidget(self.group_doing.button(identifier))

    def ongoing(self, task: dict):
        """Set status of task to "Doing"."""
        identifier = int(task['ID'])
        task_button = self.group_task.button(identifier)

        task_button.setText(f'Doing task {identifier} for today: ' + task['Task'])

        self.todolist.change(task, "Doing")
        self.group_doing.button(identifier).setText('Doing task')
        self.group_remove.button(identifier).setVisible(False)
        self.group_done.button(identifier).setVisible(True)

    def completed(self, task: dict):
        """Set status of task to "Done"."""
        identifier = int(task['ID'])
        task_button = self.group_task.button(identifier)
        task_button.setText('\u2713' + 'Completed: ' + task['Task'])
        self.todolist.change(task, "Done")

        selected_task = self.group_task.button(identifier)
        selected_doing = self.group_doing.button(identifier)
        selected_done = self.group_done.button(identifier)
        selected_remove = self.group_remove.button(identifier)

        selected_doing.setVisible(False)
        selected_done.setVisible(False)
        selected_remove.setVisible(True)

        selected_task.setStyleSheet("color:  rgb(100, 175, 100)")

    def create_task_select(self, task: dict):
        """Visualize the selection radio button"""
        identifier = int(task['ID'])
        text = f"Task {identifier} for today is: {task['Task']}"
        task_button = QRadioButton(text, self)
        task_button.setMinimumWidth(450)

        task_button.toggled.connect(lambda: self.color_buttons(task))

        self.group_task.addButton(task_button, identifier)
        self.layout.addWidget(task_button, identifier, 0)

        if task['Task Status'] == 'Done':
            self.completed(task)
        elif task['Task Status'] == 'Doing':
            self.ongoing(task)

        return task

    def create_remove_button(self, task: dict):
        """Visualize the selection remove button"""

        remove = QPushButton('Remove task', self)
        remove.setCheckable(True)
        remove.setMaximumWidth(100)

        remove.clicked.connect(lambda: self.removed(task))

        identifier = int(task['ID'])
        self.group_remove.addButton(remove, identifier)
        self.layout.addWidget(remove, identifier, 2)

        return remove

    def create_doing_button(self, task: dict):
        """Visualize the selection doing button"""

        doing = QPushButton('Do task', self)
        doing.setCheckable(True)
        doing.setMaximumWidth(100)

        doing.clicked.connect(lambda: self.ongoing(task))

        identifier = int(task['ID'])
        self.group_doing.addButton(doing, identifier)
        self.layout.addWidget(doing, identifier, 1)

        return doing

    def create_done_button(self, task: dict):
        """Visualize the selection done button"""

        done = QPushButton('Task completed', self)
        done.setCheckable(True)
        done.setVisible(False)
        done.setMaximumWidth(100)

        done.clicked.connect(lambda: self.completed(task))

        identifier = int(task['ID'])
        self.group_done.addButton(done, identifier)
        self.layout.addWidget(done, identifier, 2)

        return done

    def color_buttons(self, task: dict):
        """Color selected task and accompanying buttons."""
        identifier = int(task['ID'])

        selected_remove = self.group_remove.button(identifier)
        selected_done = self.group_done.button(identifier)
        selected_doing = self.group_doing.button(identifier)

        is_checked = self.group_task.button(identifier).isChecked()

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

    def refresh(self):
        self.clear_widget()
        self.create_to_do_list_visual()

    def clear_widget(self):
        for item in reversed(self.todolist.todolist):
            self.removed(item)
