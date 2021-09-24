from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QLineEdit, QCheckBox, QHBoxLayout, QComboBox


class TaskWidget(QtWidgets.QGroupBox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setTitle('Individual tasks can be added here')

        #textbox for inserting name of the task
        self.textbox = QLineEdit(self)
        self.textbox.move(200, 40)
        self.textbox.resize(200, 20)
        #self.title_textbox =

        #Estimated time
        self.estimated = QComboBox(self)
        self.estimated.addItem('5 min')
        self.estimated.addItem('10 min')
        self.estimated.addItem('15 min')
        self.estimated.currentIndexChanged.connect(self.estimatedchange)
        self.estimated.move(200, 80)
        # self.title_estimated =

        #Priority slider
        self.priority = QComboBox(self)
        self.priority.addItem('high')
        self.priority.addItem('normal')
        self.priority.addItem('low')
        self.priority.currentIndexChanged.connect(self.prioritychange)
        self.priority.move(200,120)
        # self.title_priority =

        #checkbox, is it periodic or not
        self.checkbox = QCheckBox('', self)
        self.checkbox.stateChanged.connect(self.periodicstate)
        self.checkbox.move(200, 160)
        #self.title_checkbox =






        #add to the list button
        self.button = QtWidgets.QPushButton('individual task input')
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.button)
        self.setLayout(layout)



    def periodicstate(self, state):
        if state == QtCore.Qt.Checked:
            print('Checked')
        else:
            print('Unchecked')

    def prioritychange(self):
        print('Current index is', self.priority.currentText())

    def estimatedchange(self):
        print('Current index is', self.estimated.currentText())
