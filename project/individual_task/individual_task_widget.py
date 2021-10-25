from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QLineEdit, QComboBox, QPushButton, QMessageBox, QFormLayout
from project.task_list.data_for_database import TaskList
from project.task_list.task_list_tab import TaskListTab
from project.settings.help_button import HelpButton


class TaskWidget(QtWidgets.QGroupBox):
    def __init__(self, task_list_tab: TaskListTab, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.task_list_tab = task_list_tab

        self.setTitle('Individual tasks can be added here')

        # Textbox for inserting name of the task
        self.textbox = QLineEdit(self)

        # Estimated time
        self.estimated = QComboBox(self)
        durations = [f'{x} minutes' for x in range(5, 35, 5)]
        for duration in durations:
            self.estimated.addItem(duration)

        # Priority slider
        self.priority = QComboBox(self)
        priorities = ['low', 'normal', 'high', 'must be done today']
        for priority in priorities:
            self.priority.addItem(priority)

        # Checkbox, is it periodic or not
        self.periodic = QComboBox(self)
        periodic = ['max once a day', 'several times a day', 'not periodic']
        for period in periodic:
            self.periodic.addItem(period)

        # Preferred time
        self.preferred = QComboBox(self)
        day_parts = ['Whole day', 'Morning', 'Afternoon', 'Evening']
        for day_part in day_parts:
            self.preferred.addItem(day_part)

        # Add to the list button
        self.button = QPushButton('Add task', self)
        self.button.clicked.connect(self.buttonclicked)
        self.button.clicked.connect(self.show_popup)

        # Help button
        self.help = HelpButton()
        self.help.msg.setText('You can add a new task to the database here.\n'
                              'Fill in a name for the task and select your preferences.\n'
                              'When done, you click: "Add task"\n'
                              'and go to the Task list tab to see the result.\n')

        # Layout
        layout = QFormLayout()
        layout.addRow("Name", self.textbox)
        layout.addRow("Estimated time", self.estimated)
        layout.addRow("Priority", self.priority)
        layout.addRow("Periodic", self.periodic)
        layout.addRow("Preferred time", self.preferred)
        layout.addWidget(self.button)
        layout.addWidget(self.help.button)
        self.setLayout(layout)

    def buttonclicked(self):
        task = [self.textbox.text(),
                int(self.estimated.currentText().split()[0]),
                self.priority.currentText(),
                self.periodic.currentText(),
                self.preferred.currentText()]

        database = TaskList()
        database.add_task(task)

    def show_popup(self):
        msg = QMessageBox()
        msg.setText("Task is added to the databse")
        msg.setWindowTitle("Success!")
        msg.setWindowIcon(QtGui.QIcon('icon.png'))
        msg.setStandardButtons(QMessageBox.Ok)
        msg.buttonClicked.connect(self.task_list_tab.refresh)
        button_clicked = msg.exec()

        if button_clicked == 1024:
            self.task_list_tab.refresh()
