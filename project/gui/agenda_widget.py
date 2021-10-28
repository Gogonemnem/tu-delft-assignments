from datetime import datetime, timedelta

import pandas as pd
import plotly.express as px
from PyQt5 import QtWidgets, QtWebEngineWidgets
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QWidget, QHBoxLayout

from project.agenda.agenda import Agenda


class AgendaWidget(QtWidgets.QGroupBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.agenda = Agenda()
        self.setTitle("The agenda can be seen below")

        # This shows the figure
        self.browser = QtWebEngineWidgets.QWebEngineView(self)

        # Buttons for showing/updating and stop updating
        self.buttons_widget = QWidget()
        self.buttons_layout = QHBoxLayout(self.buttons_widget)
        self.update_button = QtWidgets.QPushButton('Show && Update Agenda', self)
        self.stop_button = QtWidgets.QPushButton('Stop Updating Agenda', self)
        self.buttons_layout.addWidget(self.update_button)
        self.buttons_layout.addWidget(self.stop_button)
        self.buttons_widget.setFixedHeight(40)

        # Creates a help button, which explains what the agenda does.
        self.setWhatsThis(
            'This widget shows your personal agenda. '
            'To show and update the agenda, press the top left button '
            'and to stop updating it again, press the button next to it.\n'
            'You can add new activities to the agenda, with the widget at '
            'the bottom left side of the agenda.\n'
            'You can use the agenda, for example, to let Breaksum know when you have time '
            'to get a new task or when you do not want to be disturbed.\n'
            'The agenda will delete the activities when they are done '
            'and you can not import your external agenda. '
            'You have to add activities manually.')

        # Main layout
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.buttons_widget)
        layout.addWidget(self.browser)

        # Update the figure after a timer goes off and connect the corresponding buttons
        self.timer = QTimer()
        self.timer.timeout.connect(self.show_graph)
        self.update_button.clicked.connect(self.start)
        self.stop_button.clicked.connect(self.stop)
        self.resize(1000, 800)

    def start(self):
        """Initiate refreshing the agenda each minute with corresponding button settings."""
        self.timer.start(60000)
        self.show_graph()
        self.update_button.setEnabled(False)
        self.stop_button.setEnabled(True)

    def stop(self):
        """Stop refreshing the agenda with corresponding button settings."""
        self.timer.stop()
        self.update_button.setEnabled(True)
        self.stop_button.setEnabled(False)

    def show_graph(self):
        """Draw the graph with agenda activities using plotly express."""
        df, x_range = self.get_agenda_data()

        # Plot the figure
        fig = px.timeline(
            df, x_start="start_time", x_end="end_time", y="activity", color="ID", range_x=x_range,
            hover_data=['activity', 'start_time', 'end_time', 'ID', 'summary']
        )
        fig.add_vline(x=datetime.now(), line_width=1, line_color="red")  # current time indication

        # Turn the HTML plot into a widget and do not open it within a browser
        self.browser.setHtml(fig.to_html(include_plotlyjs='cdn'))

    def get_agenda_data(self):
        """Return the data and range of the activities in agenda.

        The graph will be slightly different depending on whether the agenda is filled.
        """
        self.agenda.remove_activity_over()
        x_start = self.agenda.now - timedelta(minutes=30)

        # It is important to make the distinction between empty agenda and filled agenda
        if self.agenda.agenda:
            df = self.agenda.agenda_dataframe
            df['ID'] = [str(i) for i in range(0, len(df) + 0)]
            x_start = min(x_start, self.agenda.agenda[0].start_time)
        else:
            data = {
                'activity': ['Nothing is planned'], 'start_time': [x_start], 'end_time': [x_start],
                'ID': [''], 'summary': ['']
            }
            df = pd.DataFrame(data)

        x_range = [x_start,
                   self.agenda.now + timedelta(hours=8)]  # x-axis scaled to (about usually) 8 hours
        return df, x_range

    def add_activity(self, activity):
        """Add the activity to the agenda and refresh the page."""
        self.agenda.add_activity(activity)
        self.start()

    def modify_activity(self, identifier, activity, start_time, end_or_dur, summary):
        """Modify the activity in the agenda and refresh the page."""
        self.agenda.modify_activity(identifier, activity, start_time, end_or_dur, summary)
        self.start()

    def delete_activity(self, identifier):
        """Delete the activity from the agenda and refresh the page."""
        self.agenda.pop_activity(identifier)
        self.start()
