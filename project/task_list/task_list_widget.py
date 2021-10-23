import datetime

from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QPushButton, QRadioButton, QGridLayout, QButtonGroup, QGroupBox, QMessageBox

from project.agenda.agenda import Activity
from project.agenda.agenda_widget import AgendaWidget
from project.randomizer.optimal_time import TimeRandomizer
from project.task_list.to_do_list import ToDoList


class TaskListWidget(QGroupBox):
    """Visualise Task that need to be done today"""

    def __init__(self, agenda: AgendaWidget, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.agenda = agenda
        self.todolist = ToDoList()
        self.time_randomizer = TimeRandomizer(self.todolist, agenda)
        # self.pop_up = PopUp()

        timer = QTimer()
        timer.timeout.connect(self.check_randomizer_timer)
        self.timers = [timer, self.time_randomizer.timer]

        self.setTitle("Daily to-do list")

        # Create groups for all button types
        self.group_task = QButtonGroup()
        self.group_remove = QButtonGroup()
        self.group_done = QButtonGroup()
        self.group_doing = QButtonGroup()
        self.tuple_of_groups = self.group_task, self.group_doing, self.group_remove, self.group_done

        self.generate_button = QPushButton()

        self.layout = QGridLayout()
        self.layout.setColumnStretch(0, 1)
        self.setLayout(self.layout)

        self.create_to_do_list_visual()
        self.create_generator_button()
        self.initialize_timers()

    def create_to_do_list_visual(self):
        self.todolist.status()
        for task in self.todolist.todolist:

            for i, button_group in enumerate(self.tuple_of_groups[1:]):
                self.create_checkable_button(task, i + 1)

            self.create_task_select(task)
            self.color_buttons(task)

    def create_task_select(self, task: dict):
        """Visualize the selection radio button"""
        identifier = int(task['ID'])
        task_button = QRadioButton(f"Task {identifier} for today is: {task['Task']}")

        task_button.toggled.connect(lambda: self.color_buttons(task))

        self.group_task.addButton(task_button, identifier)
        self.layout.addWidget(task_button, identifier, 0)

        self.change_status_layout(task, task['Task Status'])

    def create_checkable_button(self, task: dict, group_index: int):
        labels = None, 'Do task', 'Remove task', 'Task completed'

        identifier = int(task['ID'])
        label = labels[group_index]

        button = QPushButton(label)
        button.setCheckable(True)
        button.setMinimumWidth(100)

        button.clicked.connect(lambda: self.check_pop_up(group_index, task))

        self.tuple_of_groups[group_index].addButton(button, identifier)
        self.layout.addWidget(button, identifier, min(group_index, 2))

    def change_status_layout(self, task: dict, status: str):
        if status == 'Doing':
            self.doing_task_layout(task)

        elif status == 'Removed':
            self.remove_task_layout(task)

        elif status == 'Done':
            self.complete_task_layout(task)

    def doing_task_layout(self, task: dict):
        """Set status of task to "Doing"."""

        identifier = int(task['ID'])

        self.group_task.button(identifier).setText(f'Doing task {identifier} for today: ' + task['Task'])
        self.group_doing.button(identifier).setText('Doing task')
        self.group_remove.button(identifier).setVisible(False)
        self.group_done.button(identifier).setVisible(True)

    def remove_task_layout(self, task: dict):

        identifier = int(task['ID'])

        for button_group in self.tuple_of_groups:
            self.layout.removeWidget(button_group.button(identifier))

    def complete_task_layout(self, task: dict):
        """Set status of task to "Done"."""

        identifier = int(task['ID'])

        self.group_task.button(identifier).setText('\u2713' + 'Completed: ' + task['Task'])
        self.group_task.button(identifier).setStyleSheet("color:  rgb(100, 175, 100)")
        self.group_doing.button(identifier).setVisible(False)
        self.group_remove.button(identifier).setVisible(True)
        self.group_done.button(identifier).setVisible(False)

    def color_buttons(self, task: dict):
        """Color selected task and accompanying buttons."""
        colors = (((50, 200, 255), (225, 175, 175), (200, 225, 200)),  # when not selected
                  ((40, 125, 175), (225, 75, 75), (100, 175, 100)))  # selected

        identifier = int(task['ID'])
        is_checked = self.group_task.button(identifier).isChecked()

        for i, button_group in enumerate(self.tuple_of_groups[1:]):
            button_group.button(identifier).setEnabled(is_checked)

            color = colors[is_checked][i]
            button_group.button(identifier).setStyleSheet("background-color:  rgb" + str(color))

    def create_generator_button(self):
        self.generate_button = QPushButton('Generate new to do list', self)
        self.layout.addWidget(self.generate_button, 99, 0, 1, 3)
        self.generate_button.clicked.connect(self.refresh)

    def refresh(self):
        self.clear_widget()
        self.create_to_do_list_visual()
        self.timers[0].stop()
        self.initialize_timers()

    def clear_widget(self):
        for task in reversed(self.todolist.todolist):
            self.check_pop_up(2, task)

    def initialize_timers(self):
        self.time_randomizer.start()
        self.timers[0].start(1_000)

    def check_randomizer_timer(self):
        if self.timers[1].isActive():
            return

        self.timers[0].stop()  # stop checking for now
        self.time_randomizer.stop()

        if self.todolist.available:
            choice = imitate_popup()  # may be static?
            self.check_pop_up(choice)

    def check_pop_up(self, choice, task=None):
        statuses = 'To Do', 'Doing', 'Removed', 'Done', 'Rescheduled', 'Another', 'Snoozed', 'Skipped', 'Redo'
        status = statuses[choice] if choice < len(statuses) else 'Rescheduled'

        if not task:
            task = self.todolist.available[0]

        # self.todolist.change(task, status, time='14:55')
        self.change_status_layout(task, status)
        self.time_randomizer.set_timer(task)

        self.timers[0].start(5_000)

        if status == 'Rescheduled':
            time = (datetime.datetime.now() + datetime.timedelta(minutes=1)).time().isoformat()
            self.todolist.change(task, status, time=time)
            timer = self.time_randomizer.reschedule_popup(task)
            timer.timeout.connect(imitate_reschedule)
            timer.timeout.connect(lambda: self.timers.remove(timer))
            self.timers.append(timer)

            # self.agenda.add_activity(Activity())

        elif status == 'Another':
            task = self.todolist.available[1]
            self.check_pop_up(1, task=task)
            # self.check_pop_up(imitate_popup(), task=task)


def imitate_popup() -> int:
    msg = QMessageBox()
    msg.setStandardButtons(QMessageBox.Ok)
    button_clicked = msg.exec()

    return button_clicked


def imitate_reschedule():
    msg = QMessageBox()
    msg.setText('Rescheduled task')
    msg.setStandardButtons(QMessageBox.Ok)
    button_clicked = msg.exec()

    # return button_clicked
