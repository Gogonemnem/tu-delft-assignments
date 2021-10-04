from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QLineEdit, QCheckBox, QComboBox, QPushButton, QMessageBox, QLabel


class TaskWidget(QtWidgets.QGroupBox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setTitle('Individual tasks can be added here')

        #textbox for inserting name of the task
        self.textbox = QLineEdit(self)
        self.textbox.move(165, 40)
        self.textbox.resize(150, 20)
        self.title_textbox = QLabel("Name",self)
        self.title_textbox.move(20, 45)


        #Estimated time
        self.estimated = QComboBox(self)
        self.estimated.addItem('5 min')
        self.estimated.addItem('10 min')
        self.estimated.addItem('15 min')
        self.estimated.addItem('30 min')
        #self.estimated.currentIndexChanged.connect(self.estimatedchange)
        self.estimated.move(160, 80)
        self.estimated.resize(120, 30)
        self.title_estimated = QLabel("Estimated time",self)
        self.title_estimated.move(20, 85)


        #Priority slider
        self.priority = QComboBox(self)
        self.priority.addItem('low')
        self.priority.addItem('normal')
        self.priority.addItem('high')
        self.priority.addItem('must be done today')
        #self.priority.currentIndexChanged.connect(self.prioritychange)
        self.priority.move(160,120)
        self.priority.resize(120, 30)
        self.title_priority = QLabel("Priority",self)
        self.title_priority.move(20, 125)


        #checkbox, is it periodic or not
        self.checkbox = QCheckBox('', self)
        #self.checkbox.stateChanged.connect(self.periodicstate)
        self.checkbox.move(160, 165)
        self.title_checkbox = QLabel("Periodic",self)
        self.title_checkbox.move(20, 165)


       #Preferred time
        self.preferred = QComboBox(self)
        self.preferred.addItem('Whole day')
        self.preferred.addItem('Morning')
        self.preferred.addItem('Evening')
        self.preferred.addItem('Aternoon')
        #self.preferred.currentIndexChanged.connect(self.preferredtime)
        self.preferred.move(160, 200)
        self.preferred.resize(120, 30)
        self.title_preferred = QLabel("Preferred time",self)
        self.title_preferred.move(20, 205)


        #add to the list button
        self.button = QPushButton('Add task', self)
        self.button.move(80, 240)
        self.button.resize(150,30)
        self.button.clicked.connect(self.buttonclicked)
        self.button.clicked.connect(self.show_popup)


    #All tests to see if the buttons and sliders are connected

    #def prioritychange(self):
    #    print('Current index is', self.priority.currentText())

    #def estimatedchange(self):
    #   print('Current index is', self.estimated.currentText())

    #def periodicstate(self, state):
    #    if state == QtCore.Qt.Checked:
    #        print('Periodic')
    #    else:
    #        print('Not periodic')

    #def preferredtime(self):
    #    print('Current index is', self.preferred.currentText())

    def buttonclicked(self):
        #print(self.textbox.text())
        #print('Current index is', self.estimated.currentText())
        #print('Current index is', self.priority.currentText())
        #if self.checkbox.isChecked() == True:
        #    print('Periodic')
        #else:
        #    print('Not periodic')
        #print('Current index is', self.preferred.currentText())
        with open('task_list_file', 'a') as file:
            if self.checkbox.isChecked() == True:
                print(self.textbox.text(), self.estimated.currentText(), self.priority.currentText(), 'True', self.preferred.currentText(), sep=';', file=file)
            else:
                print(self.textbox.text(), self.estimated.currentText(), self.priority.currentText(), 'False', self.preferred.currentText(), sep=';', file=file)

    def show_popup(self):
        msg = QMessageBox()
        msg.setText("Task is added to the databse")
        msg.setWindowIcon(QtGui.QIcon('icon.png'))
        # x = msg.exec_()
