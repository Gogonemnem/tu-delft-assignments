import sys
from datetime import datetime, timedelta
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import QDateTime
from PyQt5.QtWidgets import QComboBox, QTimeEdit, QApplication, QFormLayout, QPushButton, \
    QMessageBox, QLineEdit, QDateTimeEdit, QRadioButton, QHBoxLayout, QWidget, QSpinBox

from project.agenda.agenda import Activity, Agenda
from project.agenda.agenda_widget import AgendaWidget


class IndividualAgendaWidget(QtWidgets.QGroupBox):
    def __init__(self, agenda_widget: AgendaWidget, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Now PyCharm knows what type these should be
        self.agenda_widget = agenda_widget
        self.create = QRadioButton()
        self.modify = QRadioButton()
        self.end = QRadioButton()
        self.dur = QRadioButton()
        self.id = QSpinBox()
        self.activity = QComboBox()
        self.start_time = QDateTimeEdit()
        self.end_time = QDateTimeEdit()
        self.duration = QTimeEdit()
        self.description = QLineEdit()
        self.button = QPushButton()

        self.setTitle('Agenda activities can be added here')
        self.layout = QFormLayout()
        self.setLayout(self.layout)
        self.show()

        self.create_or_modify()
        self.end_or_dur()

    def create_or_modify(self):
        self.create = QRadioButton('Create an activity', self)
        self.create.toggle()
        self.create.toggled.connect(self.state)
        self.modify = QRadioButton('Modify an activity', self)
        self.create.toggled.connect(self.state)

        buttons = QWidget()
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.create)
        button_layout.addWidget(self.modify)
        buttons.setLayout(button_layout)
        self.layout.addRow(buttons)

    def end_or_dur(self):
        self.end = QRadioButton('Set ending time', self)
        self.end.toggled.connect(self.state)
        self.dur = QRadioButton('Set duration time', self)
        self.dur.toggled.connect(self.state)

        buttons = QWidget()
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.end)
        button_layout.addWidget(self.dur)
        buttons.setLayout(button_layout)
        self.layout.addRow(buttons)
        self.end.toggle()

    def state(self):
        crea_or_mod = self.create.isChecked()
        end_or_dur = self.end.isChecked()
        self.layout_update(crea_or_mod, end_or_dur)

    def layout_update(self, create, end):
        # This ensures it remove the old forms, and will not create duplicates
        if len(self.children()) > 4:
            for widget in self.children()[3:]:
                self.layout.removeWidget(widget)

        if not create:
            self.id = QSpinBox(self)
            self.id.setMinimum(0)
            self.id.setMaximum(max(len(self.agenda_widget.agenda.agenda)-1, 0))
            self.layout.addRow("Id", self.id)

        # Type of activity
        self.activity = QComboBox(self)
        activities = ['No work', 'Work', 'Planned break', 'Do not disturb me', 'Doing task']
        if not create:
            activities.insert(0, '')
        for activity in activities:
            self.activity.addItem(activity)
        self.layout.addRow("Activity", self.activity)

        # Start Time
        self.start_time = QDateTimeEdit(self)
        if create:
            self.start_time.setDateTime(QDateTime.currentDateTime())
        self.layout.addRow("Start time", self.start_time)

        # End Time
        if end:
            self.duration = None
            self.end_time = QDateTimeEdit(self)
            if create:
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
        label = 'Add activity' if create else 'Modify activity'
        self.button = QPushButton(label, self)
        self.button.clicked.connect(self.buttonclicked)
        self.button.clicked.connect(self.show_popup)
        self.layout.addWidget(self.button)

    def buttonclicked(self):
        activity = self.activity.currentText()
        start_time = self.start_time.dateTime().toPyDateTime()
        summary = self.description.text()

        if self.end_time:
            end_or_dur = self.end_time.dateTime().toPyDateTime()
            start_time, end_or_dur = min(start_time, end_or_dur), max(start_time, end_or_dur)
        else:
            end_or_dur = timedelta(milliseconds=self.duration.time().msecsSinceStartOfDay())

        empty_mod = datetime.strptime('2000-01-01 00:00:00', "%Y-%m-%d %H:%M:%S")
        if self.start_time.dateTime().toPyDateTime() == empty_mod:
            start_time = None
        if end_or_dur == empty_mod or end_or_dur == timedelta():
            end_or_dur = None

        if self.create.isChecked():
            if self.end_time:
                activity1 = Activity(
                    activity, start_time, end_time=end_or_dur, summary=summary)
            else:
                activity1 = Activity(
                    activity, start_time, duration=end_or_dur, summary=summary)
            # # use this when 48-49 is merged, do not need if statements
            # activity = Activity(self.activity.currentText(),
            #                     self.start_time.dateTime().toPyDateTime(),
            #                     end_or_dur,
            #                     self.description.text()
            #                     )
            self.agenda_widget.add_activity(activity1)

        if self.modify.isChecked() and len(self.agenda_widget.agenda.agenda):

            identifier = self.id.value()
            self.agenda_widget.modify_activity(
                identifier, activity, start_time, end_or_dur, summary)

    def show_popup(self):
        msg = QMessageBox()
        msg.setText("Activity is added to the agenda")
        msg.setWindowTitle("Success!")
        msg.setWindowIcon(QtGui.QIcon('icon.png'))
        msg.setStandardButtons(QMessageBox.Ok)
        button_clicked = msg.exec()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    agenda = Agenda()
    agenda_widget = AgendaWidget(agenda)  # is not shown
    ex = IndividualAgendaWidget(agenda_widget)
    sys.exit(app.exec_())
