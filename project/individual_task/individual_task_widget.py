from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QLineEdit, QCheckBox, QComboBox, QPushButton, QMessageBox, QFormLayout
from project.task_list.data_for_database import TaskList
from project.task_list.task_list_tab import TaskListTab


class TaskWidget(QtWidgets.QGroupBox):
    def __init__(self, tasklisttab, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tasklisttab = tasklisttab

        self.setTitle('Individual tasks can be added here')

        # Textbox for inserting name of the task
        self.textbox = QLineEdit(self)

        # Estimated time
        self.estimated = QComboBox(self)
        durations = [f'{x} min' for x in range(5, 35, 5)]
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

    # self.estimated.currentIndexChanged.connect(self.estimatedchange)
    # self.priority.currentIndexChanged.connect(self.prioritychange)
    # self.checkbox.stateChanged.connect(self.periodicstate)
    # self.preferred.currentIndexChanged.connect(self.preferredtime)

    # All tests to see if the buttons and sliders are connected

    # def prioritychange(self):
    #    print('Current index is', self.priority.currentText())

    # def estimatedchange(self):
    #   print('Current index is', self.estimated.currentText())

    # def periodicstate(self, state):
    #    if state == QtCore.Qt.Checked:
    #        print('Periodic')
    #    else:
    #        print('Not periodic')

    # def preferredtime(self):
    #    print('Current index is', self.preferred.currentText())

    def buttonclicked(self):
        # print(self.textbox.text())
        # print('Current index is', self.estimated.currentText())
        # print('Current index is', self.priority.currentText())
        # if self.checkbox.isChecked() == True:
        #     print('Periodic')
        # else:
        #     print('Not periodic')
        # print('Current index is', self.preferred.currentText())
        # with open('task_list_file', 'a') as file:
        #     if self.checkbox.isChecked() == True:
        #         print(
        #             self.textbox.text(),
        #             self.estimated.currentText(),
        #             self.priority.currentText(),
        #             'True',
        #             self.preferred.currentText(),
        #             sep=';',
        #             file=file
        #         )
        #     else:
        #         print(
        #             self.textbox.text(),
        #             self.estimated.currentText(),
        #             self.priority.currentText(),
        #             'False',
        #             self.preferred.currentText(),
        #             sep=';',
        #             file=file
        #         )

        task = [self.textbox.text(),
                int(self.estimated.currentText()[:-4]),
                self.priority.currentText(),
                True,
                self.preferred.currentText()]
        if self.checkbox.isChecked() is False:
            task[3] = False

        database = TaskList()
        database.add_task(task)

    def show_popup(self):
        msg = QMessageBox()
        msg.setText("Task is added to the databse")
        msg.setWindowTitle("Success!")
        msg.setWindowIcon(QtGui.QIcon('icon.png'))
        msg.setStandardButtons(QMessageBox.Ok)
        # msg.buttonClicked.connect()
        x = msg.exec()

        if x == QMessageBox.Ok:
            self.tasklisttab.refresh()





