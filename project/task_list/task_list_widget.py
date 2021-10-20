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
        self.complete = 0

        # Create groups for all button types
        self.group_task = QButtonGroup()
        self.group_remove = QButtonGroup()
        self.group_done = QButtonGroup()
        self.group_doing = QButtonGroup()

        # self.group_task = []
        # self.group_remove = []
        # self.group_done = []
        # self.group_doing = []

        self.layout = QGridLayout()
        self.setLayout(self.layout)

        self.create_to_do_list_visual()

        self.generate_new = QPushButton('Generate new to do list', self)
        self.layout.addWidget(self.generate_new, 99, 0, 1, 3)
        self.generate_new.clicked.connect(self.refresh)

    def create_to_do_list_visual(self):
        self.todolist.status()
        for task in self.todolist.todolist:
            identifier = int(task['ID'])

            self.create_remove_button(identifier)
            self.create_doing_button(identifier)
            self.create_done_button(identifier)
            self.create_task_select(identifier, task['Task'])

            self.color_buttons(identifier)

    def removed(self, identifier):
        """Remove task from to-do list."""
        self.todolist.remove_task(identifier)
        self.layout.removeWidget(self.group_task.button(identifier))
        self.layout.removeWidget(self.group_done.button(identifier))
        self.layout.removeWidget(self.group_remove.button(identifier))
        self.layout.removeWidget(self.group_doing.button(identifier))

    def ongoing(self, identifier):
        """Set status of task to "Doing"."""
        task_button = self.group_task.button(identifier)

        task = next((item for item in self.todolist.todolist if int(item["ID"]) == identifier), None)
        task_button.setText(f'Doing task {identifier} for today: ' + task['Task'])

        self.todolist.change(identifier, "Doing")
        self.group_doing.button(identifier).setText('Doing task')
        self.group_remove.button(identifier).setVisible(False)
        self.group_done.button(identifier).setVisible(True)

    def completed(self, identifier):
        """Set status of task to "Done"."""
        task_button = self.group_task.button(identifier)
        task = next((item for item in self.todolist.todolist if int(item["ID"]) == identifier), None)
        task_button.setText('\u2713' + 'Completed: ' + task['Task'])
        self.todolist.change(identifier, "Done")

        selected_task = self.group_task.button(identifier)
        selected_doing = self.group_doing.button(identifier)
        selected_done = self.group_done.button(identifier)
        selected_remove = self.group_remove.button(identifier)

        selected_doing.setVisible(False)
        selected_done.setVisible(False)
        selected_remove.setVisible(True)

        selected_task.setStyleSheet("color:  rgb(100, 175, 100)")
        self.complete += 1

    def create_task_select(self, identifier, item):
        """Visualize the selection radio button"""
        index = next((i for i, item in enumerate(self.todolist.todolist) if int(item["ID"]) == identifier), None)

        text = f'Task {identifier} for today is: {item}'
        task = QRadioButton(text, self)
        task.setMinimumWidth(450)

        task.toggled.connect(lambda: self.color_buttons(identifier))

        self.group_task.addButton(task, identifier)
        self.layout.addWidget(task, identifier, 0)

        task = self.todolist.todolist[index]

        if task['Task Status'] == 'Done':
            self.completed(identifier)
        elif task['Task Status'] == 'Doing':
            self.ongoing(identifier)

        return task

    def create_remove_button(self, identifier):
        """Visualize the selection remove button"""
        remove = QPushButton('Remove task', self)
        remove.setCheckable(True)
        remove.setMaximumWidth(100)

        remove.clicked.connect(lambda: self.removed(identifier))

        self.group_remove.addButton(remove, identifier)
        self.layout.addWidget(remove, identifier, 2)

        return remove

    def create_doing_button(self, identifier):
        """Visualize the selection doing button"""
        doing = QPushButton('Do task', self)
        doing.setCheckable(True)
        doing.setMaximumWidth(100)

        doing.clicked.connect(lambda: self.ongoing(identifier))

        self.group_doing.addButton(doing, identifier)
        self.layout.addWidget(doing, identifier, 1)

        return doing

    def create_done_button(self, identifier):
        """Visualize the selection done button"""
        done = QPushButton('Task completed', self)
        done.setCheckable(True)
        done.setVisible(False)
        done.setMaximumWidth(100)

        done.clicked.connect(lambda: self.completed(identifier))

        self.group_done.addButton(done, identifier)
        self.layout.addWidget(done, identifier, 2)

        return done

    def color_buttons(self, identifier):
        """Color selected task and accompanying buttons."""

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
        for item in self.group_task.buttons():
            identifier = self.group_task.id(item)
            self.removed(identifier)
