import datetime

from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QPushButton, QRadioButton, QGridLayout, QButtonGroup, QGroupBox, QMessageBox

from project.agenda.agenda import Activity
from project.agenda.agenda_widget import AgendaWidget
from project.randomizer.optimal_time import TimeRandomizer
from project.task_list.to_do_list import ToDoList
from project.settings.help_button import HelpButton


class TaskListWidget(QGroupBox):
    """Visualise Task that need to be done today"""

    def __init__(self, agenda: AgendaWidget, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.agenda = agenda
        self.todolist = ToDoList()
        self.time_randomizer = TimeRandomizer(self.todolist, agenda)
        # self.pop_up = PopUp()

        timer = QTimer()
        self.timers = {-1: timer, 0: self.time_randomizer.timer}

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

        # Create a help button, to explain the daily to-do list
        self.help = HelpButton()
        self.help.msg.setText('Your daily to-do list shows all the tasks you will get today.\n'
                              'If you want to do a task earlier than planned '
                              "or don't want to do it at all, you can select the task here "
                              'and push the corresponding button.\n'
                              "Don't forget to mark a task as finished when you're done.\n"
                              "You don't need to use the daily to-do list, "
                              'because of the build-in notifications, '
                              'but it will give you a nice overview of your tasks anyway.')
        self.layout.addWidget(self.help.button)

    def create_to_do_list_visual(self):
        self.todolist.status()
        for task in self.todolist.todolist:

            for i, _ in enumerate(self.tuple_of_groups[1:]):
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

        if group_index == 3:  # completed button is not yet visible
            button.setVisible(False)

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
        self.timers = {-1: self.timers[-1], 0: self.timers[0]}
        self.initialize_timers()

    def clear_widget(self):
        for task in reversed(self.todolist.todolist):
            self.check_pop_up(2, task)

    def initialize_timers(self):
        self.time_randomizer.start()
        self.timers[-1].timeout.connect(self.check_randomizer_timer)
        self.timers[-1].start(5_000)

    def check_randomizer_timer(self):
        if self.timers[0].isActive():
            return

        self.timers[-1].stop()  # stop checking for now
        self.time_randomizer.stop()

        if self.todolist.available:
            choice = self.imitate_popup()  # may be static?
            self.check_pop_up(choice)

    def check_pop_up(self, choice, task=None):
        statuses = 'To Do', 'Doing', 'Removed', 'Done', 'Rescheduled', 'Another', 'Snoozed', 'Skipped', 'Redo'
        status = statuses[choice] if choice < len(statuses) else 'Skipped'

        if not task:
            task = self.todolist.available[0]
        time = None
        self.timers.pop(int(task['ID']), None)

        # TODO: correctly set time (incorporate popup)
        if status == 'Rescheduled':
            time = datetime.datetime.now() + datetime.timedelta(minutes=1)
            self.setup_rescheduler(task, time)

            # self.agenda.add_activity(Activity())

        self.todolist.change(task, status, time=time)
        self.change_status_layout(task, status)
        self.time_randomizer.set_timer(task)

        self.timers[-1].start(5_000)

        if status == 'Another':
            task = self.todolist.available[1]
            self.check_pop_up(1, task=task)
            # self.check_pop_up(imitate_popup(), task=task)

    def setup_rescheduler(self, task: dict, time: datetime.datetime):
        timer = self.time_randomizer.reschedule_popup(time)
        timer.timeout.connect(lambda: self.imitate_popup(task))
        self.timers[int(task['ID'])] = timer

    def imitate_popup(self, task=None):
        msg = QMessageBox()
        msg.setStandardButtons(QMessageBox.Ok)
        button_clicked = msg.exec()

        if task:  # rescheduled and complete it
            self.check_pop_up(3, task)
        else:  # return the choice
            return button_clicked