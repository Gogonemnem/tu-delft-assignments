import sys
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import QTime, QDateTime
from PyQt5.QtWidgets import QComboBox, QTimeEdit, QCalendarWidget, QApplication, QVBoxLayout, QFormLayout, QPushButton, \
    QMessageBox, QLineEdit, QDateTimeEdit
from datetime import timedelta


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
        self.start_time = QDateTimeEdit(self)
        self.start_time.setDateTime(QDateTime.currentDateTime())

        # End Time
        self.end_time = QDateTimeEdit(self)
        self.end_time.setDateTime(QDateTime.currentDateTime())

        # # Date
        # self.date = QCalendarWidget(self)
        # self.date.setGridVisible(True)

        # Duration
        self.duration = QTimeEdit(self)
        self.end_time.setTime(QTime.currentTime())

        # Description
        self.description = QLineEdit(self)

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
        # layout.addRow("Date", self.date)
        layout.addRow("Duration", self.duration)
        layout.addRow("Description", self.description)
        layout.addWidget(self.button)
        self.setLayout(layout)
        self.show()

    def buttonclicked(self):
        activity = [self.activity.currentText(),
                    self.start_time.dateTime().toPyDateTime(),
                    self.end_time.dateTime().toPyDateTime(),
                    # self.date.selectedDate(),
                    timedelta(milliseconds=self.duration.time().msecsSinceStartOfDay()),
                    self.description.text()
                    ]
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
