from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QLineEdit, QCheckBox, QComboBox, QPushButton, QMessageBox, QFormLayout
from project.task_list.data_for_database import TaskList
from project.task_list.task_list_tab import TaskListTab


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
        self.checkbox = QCheckBox('', self)

        # Preferred time
        self.preferred = QComboBox(self)
        day_parts = ['Whole day', 'Morning', 'Afternoon', 'Evening']
        for day_part in day_parts:
            self.preferred.addItem(day_part)

        # Add to the list button
        self.button = QPushButton('Add task', self)
        self.button.clicked.connect(self.buttonclicked)
        self.button.clicked.connect(self.show_popup)

        # Layout
        layout = QFormLayout()
        layout.addRow("Name", self.textbox)
        layout.addRow("Estimated time", self.estimated)
        layout.addRow("Priority", self.priority)
        layout.addRow("Periodic", self.checkbox)
        layout.addRow("Preferred time", self.preferred)
        layout.addWidget(self.button)
        self.setLayout(layout)

    def buttonclicked(self):
        task = [self.textbox.text(),
                int(self.estimated.currentText().split()[0]),
                self.priority.currentText(),
                self.checkbox.isChecked(),
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
