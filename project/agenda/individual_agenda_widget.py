import sys
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import QTime, QDateTime
from PyQt5.QtWidgets import QComboBox, QTimeEdit, QCalendarWidget, QApplication, QVBoxLayout, QFormLayout, QPushButton, \
    QMessageBox, QLineEdit, QDateTimeEdit, QRadioButton, QHBoxLayout, QWidget
from datetime import timedelta


class IndividualAgendaWidget(QtWidgets.QGroupBox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.end = None
        self.dur = None
        self.activity = None
        self.start_time = None
        self.end_time = None
        self.duration = None
        self.description = None
        self.button = None

        self.setTitle('Agenda activities can be added here')
        self.layout = QFormLayout()
        self.setLayout(self.layout)
        self.show()

        self.setup_choice()

    def setup_choice(self):
        self.end = QRadioButton('Set ending time', self)
        self.end.clicked.connect(lambda: self.layout_update(True))
        self.dur = QRadioButton('Set duration time', self)
        self.dur.clicked.connect(lambda: self.layout_update(False))

        buttons = QWidget()
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.end)
        button_layout.addWidget(self.dur)
        buttons.setLayout(button_layout)
        self.layout.addRow(buttons)

    def layout_update(self, button):
        # This ensures it remove the old forms, and will not create duplicates
        if len(self.children()) > 2:
            for widget in self.children()[2:]:
                self.layout.removeWidget(widget)

        # Type of activity
        self.activity = QComboBox(self)
        activities = ['No work', 'Work', 'Planned break', 'Do not disturb me', 'Doing task']
        for activity in activities:
            self.activity.addItem(activity)
        self.layout.addRow("Activity", self.activity)

        # Start Time
        self.start_time = QDateTimeEdit(self)
        self.start_time.setDateTime(QDateTime.currentDateTime())
        self.layout.addRow("Start time", self.start_time)

        # End Time
        if button:
            self.duration = None
            self.end_time = QDateTimeEdit(self)
            self.end_time.setDateTime(QDateTime.currentDateTime())
            self.layout.addRow("End time", self.end_time)

        # Duration
        else:
            self.end_time = None
            self.duration = QTimeEdit(self)
            self.layout.addRow("Duration", self.duration)

        # Description
        self.description = QLineEdit(self)
        self.layout.addRow("Description", self.description)

        # Add to the agenda button
        self.button = QPushButton('Add activity', self)
        self.button.clicked.connect(self.buttonclicked)
        self.button.clicked.connect(self.show_popup)
        self.layout.addWidget(self.button)

    def buttonclicked(self):
        if self.end_time:
            end_or_dur = self.end_time.dateTime().toPyDateTime()
        else:
            end_or_dur = timedelta(milliseconds=self.duration.time().msecsSinceStartOfDay())
        activity = [self.activity.currentText(),
                    self.start_time.dateTime().toPyDateTime(),
                    end_or_dur,
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
