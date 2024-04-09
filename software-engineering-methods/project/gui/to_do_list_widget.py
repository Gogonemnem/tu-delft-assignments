import datetime

from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QPushButton, QRadioButton, QGridLayout, QButtonGroup, QGroupBox

from project.agenda.agenda import Activity
from project.gui.agenda_widget import AgendaWidget
from project.gui.pop_up_widget import Popup, TimeDialog
from project.gui.task_list_tab import TaskListTab
from project.randomizer.time_randomizer import TimeRandomizer
from project.task_list.to_do_list import ToDoList


class ToDoListWidget(QGroupBox):
    """Visualise Task that need to be done today"""

    def __init__(self, agenda: AgendaWidget, task_list_tab: TaskListTab, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.agenda = agenda
        self.task_list_tab = task_list_tab
        self.todolist = ToDoList(self.task_list_tab.database)
        self.time_randomizer = TimeRandomizer(self.todolist, agenda)

        timer = QTimer()
        self.timers = {-1: timer, 0: self.time_randomizer.timer}

        self.setTitle("Daily to-do list")

        # Create groups for all button types
        group_names = 'group_task', 'group_doing', 'group_remove', 'group_done'
        for group_name in group_names:
            setattr(self, group_name, QButtonGroup())
        self.tuple_of_groups = tuple(getattr(self, group) for group in group_names)

        self.generate_button = QPushButton()

        self.layout = QGridLayout()
        self.layout.setColumnStretch(0, 1)
        self.setLayout(self.layout)

        self.create_to_do_list_visual()
        self.create_generator_button()
        self.initialize_timers()

        # Create a help button, to explain the daily to-do list
        self.setWhatsThis('Your daily to-do list shows all the tasks you will get today.\n'
                          'If you want to do a task earlier than planned '
                          "or don't want to do it at all, you can select the task here "
                          'and push the corresponding button.\n'
                          "Don't forget to mark a task as finished when you're done.\n"
                          "You don't need to use the daily to-do list, "
                          'because of the build-in notifications, '
                          'but it will give you a nice overview of your tasks anyway.')

    def create_to_do_list_visual(self):
        """Visualize the to do list."""
        self.todolist.status()
        for task in self.todolist.todolist:
            self.create_row(task)

    def create_row(self, task: dict):
        """Visualize a task of the todolist."""
        for i, _ in enumerate(self.tuple_of_groups[1:]):
            self.create_checkable_button(task, i + 1)

        self.create_task_select(task)
        self.color_buttons(task)

    def create_task_select(self, task: dict):
        """Visualize the selection radio button."""
        identifier = int(task['ID'])
        task_button = QRadioButton(f"Task {identifier} for today is: {task['Task']}")

        task_button.toggled.connect(lambda: self.color_buttons(task))

        self.group_task.addButton(task_button, identifier)
        self.layout.addWidget(task_button, identifier, 0)

        self.change_status_layout(task, task['Task Status'])

    def create_checkable_button(self, task: dict, group_index: int):
        """Visualize the rest of the buttons."""
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
        """Change the visual depending on the task action."""
        if status == 'Doing':
            self.doing_task_layout(task)

        elif status == 'Removed':
            self.remove_task_layout(task)

        elif status == 'Done':
            self.complete_task_layout(task)
            self.task_list_tab.refresh()

        elif status == 'Rescheduled':
            self.reschedule_task_layout(task)

    def doing_task_layout(self, task: dict):
        """Set status of task to 'Doing' and manage buttons."""

        identifier = int(task['ID'])

        self.group_task.button(identifier).setText(
            f'Doing task {identifier} for today: ' + task['Task'])
        self.group_doing.button(identifier).setText('Doing task')
        self.group_remove.button(identifier).setVisible(False)
        self.group_done.button(identifier).setVisible(True)

    def remove_task_layout(self, task: dict):
        """Set status of task to 'Removed' and remove the row."""
        identifier = int(task['ID'])

        for button_group in self.tuple_of_groups:
            self.layout.removeWidget(button_group.button(identifier))

        agenda_id = self.agenda.agenda.find_activity(task['Task'])
        if agenda_id != -1:
            self.agenda.delete_activity(agenda_id)

    def complete_task_layout(self, task: dict):
        """Set status of task to 'Done' and manage buttons."""

        identifier = int(task['ID'])

        agenda_id = self.agenda.agenda.find_activity(task['Task'])
        if agenda_id != -1:
            self.agenda.delete_activity(agenda_id)

        self.group_task.button(identifier).setText('\u2713' + 'Completed: ' + task['Task'])
        self.group_task.button(identifier).setStyleSheet("color:  rgb(100, 175, 100)")
        self.group_doing.button(identifier).setVisible(False)
        self.group_remove.button(identifier).setVisible(True)
        self.group_done.button(identifier).setVisible(False)

    def reschedule_task_layout(self, task: dict):
        """Set status of task to 'Rescheduled' and manage buttons."""
        if isinstance(task['Rescheduled Time'], str):
            time = datetime.datetime.fromisoformat(task['Rescheduled Time'])
        else:
            time = task['Rescheduled Time']

        activity = Activity('Doing Task', time, datetime.timedelta(minutes=20), task['Task'])
        if activity not in self.agenda.agenda.agenda:
            self.agenda.add_activity(activity)

        self.setup_rescheduler(task, time)

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
        """Add a button that generates a new to do list when clicked."""
        self.generate_button = QPushButton('Generate new to do list', self)
        self.layout.addWidget(self.generate_button, 99, 0, 1, 3)
        self.generate_button.clicked.connect(self.refresh)

    def refresh(self):
        """Reset the widget."""
        self.clear_widget()
        self.create_to_do_list_visual()
        self.timers = {-1: self.timers[-1], 0: self.timers[0]}
        self.initialize_timers()

    def clear_widget(self):
        """Remove the widgets."""
        for task in reversed(self.todolist.todolist):
            self.check_pop_up(2, task)

    def initialize_timers(self):
        """Start timers which check if popup can be presented."""
        self.time_randomizer.start()
        self.timers[-1].timeout.connect(self.check_randomizer_timer)
        self.timers[-1].start(5_000)

    def check_randomizer_timer(self):
        """Use timer of randomizer to check if popup can be presented and present it."""
        if self.timers[0].isActive():
            return

        self.timers[-1].stop()  # stop checking for now
        self.time_randomizer.stop()

        if self.todolist.available:
            task = self.todolist.available[0]
            choice = Popup.pop_up(task)
            self.check_pop_up(choice, task)

    def check_pop_up(self, choice, task):
        """Get the choice of the user and set the status of the task accordingly."""
        statuses = 'To Do', 'Doing', 'Removed', 'Done', 'Rescheduled', 'Another', 'Snoozed', \
                   'Skipped', 'Redo'
        status = statuses[choice]

        self.timers.pop(int(task['ID']), None)

        time = None
        if status == 'Rescheduled':
            time, okay = TimeDialog.get_time()
            if not okay:
                time = None
                status = 'To Do'

        if status == 'Redo':
            copy = task.copy()
            copy['ID'] = max(int(task['ID']) for task in self.todolist.todolist) + 1

            self.todolist.todolist.append(copy)
            self.create_row(copy)
            status = 'Done'

        self.todolist.change(task, status, time=time)
        self.change_status_layout(task, status)
        self.time_randomizer.set_timer(task)

        self.timers[-1].start(5_000)

        if status == 'Another':
            self.timers[-1].stop()

            tasks = self.todolist.available
            current_index = tasks.index(task)
            if (index := current_index + 1) >= len(tasks):
                index = 0

            task = self.todolist.available[index]
            self.check_pop_up(Popup.pop_up(task), task)

    def setup_rescheduler(self, task: dict, time: datetime.datetime):
        """Set a timer to get a popup at the rescheduled time."""
        timer = self.time_randomizer.reschedule_popup(time)
        timer.timeout.connect(lambda: self.check_pop_up(Popup.pop_up(task), task))
        self.timers[int(task['ID'])] = timer