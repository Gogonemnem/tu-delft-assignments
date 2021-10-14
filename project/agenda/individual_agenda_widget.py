import sys
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import QTime
from PyQt5.QtWidgets import QComboBox, QTimeEdit, QCalendarWidget, QApplication, QVBoxLayout, QFormLayout, QPushButton, \
    QMessageBox


class IndividualAgendaWidget(QtWidgets.QGroupBox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setTitle('Agenda activities can be added here')

        # Type of activity
        self.activity = QComboBox(self)
        activities = ['No work', 'Work', 'Planned break', 'Do not disturb me', 'Doing task']
        for activity in activities:
            self.activity.addItem(activity)

        # Start Time
        self.start_time = QTimeEdit(self)
        self.start_time.setTime(QTime.currentTime())

        # End Time
        self.end_time = QTimeEdit(self)
        self.end_time.setTime(QTime.currentTime())

        # Date
        self.date = QCalendarWidget(self)
        self.date.setGridVisible(True)

        # Add to the agenda button
        self.button = QPushButton('Add activity', self)
        self.button.clicked.connect(self.buttonclicked)
        self.button.clicked.connect(self.show_popup)

        # vbox = QVBoxLayout()
        # vbox.addWidget(self.activity)
        # vbox.addWidget(self.start_time)
        # vbox.addWidget(self.end_time)
        # vbox.addWidget(self.date)
        # vbox.addStretch()
        layout = QFormLayout()
        layout.addRow("Activity", self.activity)
        layout.addRow("Start time", self.start_time)
        layout.addRow("End time", self.end_time)
        layout.addRow("Date", self.date)
        layout.addWidget(self.button)
        self.setLayout(layout)
        self.show()

    def buttonclicked(self):
        activity = [self.activity.currentText(),
                    self.start_time.time(),
                    self.end_time.time(),
                    self.date.selectedDate()]
        print(activity)

    def show_popup(self):
        msg = QMessageBox()
        msg.setText("Activity is added to the agenda")
        msg.setWindowTitle("Success!")
        msg.setWindowIcon(QtGui.QIcon('icon.png'))
        msg.setStandardButtons(QMessageBox.Ok)
        button_clicked = msg.exec()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = IndividualAgendaWidget()
    sys.exit(app.exec_())