import sys
from datetime import datetime, timedelta
from PyQt5 import QtWidgets, QtGui, sip
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
        self.delete = QRadioButton()
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

        self.crea_mod_del()

    def keep_old_widgets(self, count):
        """Remove widgets which will be recreated when selecting an option on the screen"""
        if len(self.children()) > count:
            for widget in self.children()[:count - 1:-1]:
                self.layout.removeWidget(widget)
                sip.delete(widget)
                # del widget

    def calculate_keep_widgets(self):
        """Determine how many widgets should be kept with each option"""
        widgets = 2
        if self.delete.isChecked():
            widgets += 1
        elif self.end.isChecked() or self.dur.isChecked():
            if self.create.isChecked():
                widgets += 1
            elif self.modify.isChecked():
                widgets += 3
        return widgets

    def crea_mod_del(self):
        """Show three options the user can use to manipulate the agenda
        with creating an activity as the default option"""
        self.create = QRadioButton('Create an activity', self)
        self.modify = QRadioButton('Modify an activity', self)
        self.delete = QRadioButton('Delete an activity', self)

        self.create.toggled.connect(self.first_stage)
        self.modify.toggled.connect(self.first_stage)
        self.delete.toggled.connect(self.first_stage)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.create)
        button_layout.addWidget(self.modify)
        button_layout.addWidget(self.delete)

        buttons = QWidget()
        buttons.setLayout(button_layout)
        self.layout.addRow(buttons)

        self.create.toggle()

    def first_stage(self):
        """Show the next option depending on the three options"""
        self.keep_old_widgets(2)
        if self.create.isChecked():
            self.end_or_dur()
        elif self.modify.isChecked():
            self.end_or_dur()
        else:
            self.layout_id()
            self.second_stage()

    def end_or_dur(self):
        """Show two options the user can use to specify the activity
        with relaying the end time as the default option"""
        self.end = QRadioButton('Set ending time', self)
        self.dur = QRadioButton('Set duration time', self)

        self.end.toggled.connect(self.second_stage)
        self.dur.toggled.connect(self.second_stage)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.end)
        button_layout.addWidget(self.dur)

        buttons = QWidget()
        buttons.setLayout(button_layout)
        self.layout.addRow(buttons)

        if self.modify.isChecked():
            self.layout_id()

        self.end.toggle()

    def second_stage(self):
        """Show the form depending on the two options"""
        count = self.calculate_keep_widgets()
        self.keep_old_widgets(count)

        if not self.delete.isChecked():
            self.layout_activity()
            self.layout_start_time()
            if self.end.isChecked():
                self.layout_end_time()
            else:
                self.layout_duration()
            self.layout_description()
        self.layout_button()

    def layout_id(self):
        """Show the option to choose the id"""
        self.id = QSpinBox(self)
        self.id.setMinimum(0)
        self.id.setMaximum(max(len(self.agenda_widget.agenda.agenda) - 1, 0))
        self.layout.addRow("Id", self.id)

    def layout_activity(self):
        """Show the option to choose the activity"""
        self.activity = QComboBox(self)
        activities = ['No work', 'Work', 'Planned break', 'Do not disturb me', 'Doing task']
        if self.modify.isChecked():
            activities.insert(0, '')
        for activity in activities:
            self.activity.addItem(activity)
        self.layout.addRow("Activity", self.activity)

    def layout_start_time(self):
        """Show the option to choose the starting time"""
        self.start_time = QDateTimeEdit(self)
        if self.create.isChecked():
            self.start_time.setDateTime(QDateTime.currentDateTime())
        self.layout.addRow("Start time", self.start_time)

    def layout_end_time(self):
        """Show the option to choose the ending time
        while setting the duration automatically to None"""
        self.duration = None
        self.end_time = QDateTimeEdit(self)
        if self.create.isChecked():
            self.end_time.setDateTime(QDateTime.currentDateTime())
        self.layout.addRow("End time", self.end_time)

    def layout_duration(self):
        """Show the option to choose the duration of the task
        while setting the ending time automatically to None"""
        self.end_time = None
        self.duration = QTimeEdit(self)
        self.layout.addRow("Duration", self.duration)

    def layout_description(self):
        """Show the option to give a short description of the task"""
        self.description = QLineEdit(self)
        self.layout.addRow("Description", self.description)

    def layout_button(self):
        """Show the button to add, modify or delete the activity in the agenda"""
        if self.create.isChecked():
            label = 'Add activity'
            self.button = QPushButton(label, self)
            self.button.clicked.connect(self.click_create)
        elif self.modify.isChecked():
            label = 'Modify activity'
            self.button = QPushButton(label, self)
            self.button.clicked.connect(self.click_modify)
        else:
            label = 'Delete activity'
            self.button = QPushButton(label, self)
            self.button.clicked.connect(self.click_delete)

        self.layout.addWidget(self.button)

    def click_create(self):
        """Add the activity to the agenda widget"""
        activity, start_time, end_or_dur, summary = self.read_data()
        activity1 = Activity(activity, start_time, end_or_dur, summary)

        self.agenda_widget.add_activity(activity1)
        text = "Activity is added to the agenda"
        self.show_popup(text)

    def click_modify(self):
        """Modify the activity in the agenda widget"""
        activity, start_time, end_or_dur, summary = self.read_data()

        if len(self.agenda_widget.agenda.agenda):
            identifier = self.id.value()
            self.agenda_widget.modify_activity(
                identifier, activity, start_time, end_or_dur, summary)
        text = "Activity is modified"
        self.show_popup(text)

    def click_delete(self):
        """Delete the activity from the agenda widget"""
        if len(self.agenda_widget.agenda.agenda):
            identifier = self.id.value()
            self.agenda_widget.delete_activity(identifier)
        text = "Activity is deleted from the agenda"
        self.show_popup(text)

    def show_popup(self, text):
        """Show that the manipulation was a success and what modification was done"""
        msg = QMessageBox()
        msg.setText(text)
        msg.setWindowTitle("Success!")
        msg.setWindowIcon(QtGui.QIcon('icon.png'))
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec()
        self.first_stage()
        self.create.click()

    def read_data(self):
        """Turn the data of the form into correct types for the Activity class"""
        activity = self.activity.currentText()
        start_time = self.start_time.dateTime().toPyDateTime()
        summary = self.description.text()

        if self.end_time:
            end_or_dur = self.end_time.dateTime().toPyDateTime()
            start_time, end_or_dur = min(start_time, end_or_dur), max(start_time, end_or_dur)
        else:
            end_or_dur = timedelta(milliseconds=self.duration.time().msecsSinceStartOfDay())

        empty_mod = datetime.strptime('2000-01-01 00:00:00', "%Y-%m-%d %H:%M:%S")
        if start_time == empty_mod:
            start_time = None
        if end_or_dur == empty_mod or end_or_dur == timedelta():
            end_or_dur = None

        return activity, start_time, end_or_dur, summary


def main():
    app = QApplication(sys.argv)

    agenda = Agenda()
    agenda_widget1 = AgendaWidget(agenda)  # is not shown
    widget = IndividualAgendaWidget(agenda_widget1)
    widget.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
