import sys
from datetime import datetime, timedelta
import pandas as pd
import plotly.express as px
from PyQt5 import QtWidgets, QtWebEngineWidgets, QtCore


# This is added by Nils
# class AgendaWidget(QtWidgets.QGroupBox):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.setTitle("The agenda can be seen below")
#         self.button = QtWidgets.QPushButton('agenda')
#         layout = QtWidgets.QVBoxLayout()
#         layout.addWidget(self.button)
#         self.setLayout(layout)
from PyQt5.QtCore import QTimer, QDateTime
from PyQt5.QtWidgets import QApplication, QListWidget, QLabel, QPushButton, QGridLayout, QWidget, QHBoxLayout


class AgendaWidget(QtWidgets.QGroupBox):
    def __init__(self, agenda, parent=None):
        super().__init__(parent)
        self.agenda = agenda
        self.setTitle("The agenda can be seen below")
        self.update_button = QtWidgets.QPushButton('Show && Update Agenda', self)
        self.stop_button = QtWidgets.QPushButton('Stop Updating Agenda', self)

        self.browser = QtWebEngineWidgets.QWebEngineView(self)

        self.timer = QTimer()
        self.timer.timeout.connect(self.show_graph)

        self.buttonsWidget = QWidget()
        self.buttons_layout = QHBoxLayout(self.buttonsWidget)
        self.buttons_layout.addWidget(self.update_button)
        self.buttons_layout.addWidget(self.stop_button)
        self.buttonsWidget.setFixedHeight(40)

        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.buttonsWidget)
        layout.addWidget(self.browser)

        self.update_button.clicked.connect(self.start)
        self.stop_button.clicked.connect(self.stop)
        self.resize(1000, 800)

    def start(self):
        self.timer.start(60000)
        self.show_graph()
        self.update_button.setEnabled(False)
        self.stop_button.setEnabled(True)

    def stop(self):
        self.timer.stop()
        self.update_button.setEnabled(True)
        self.stop_button.setEnabled(False)

    def show_graph(self):
        activities = self.agenda.agenda
        now = datetime.now()

        # It is important to make the distinction between empty agenda and filled agenda
        if activities:
            # Turn every activity object attributes into a dataframe values for the graph
            data = []
            for identifier, activity in enumerate(activities):
                ac_dic = activity.__dict__
                ac_dic['id'] = str(identifier)
                data.append({key.capitalize().replace('_', ' '): ac_dic[key]
                             for key in ['activity', 'start_time', 'end_time', 'id']})
            x_start = activities[0].start_time
        else:
            x_start = now-timedelta(minutes=30)
            data = {
                'Activity': ['Nothing is planned'],
                'Start time': [x_start],
                'End time': [x_start],
                'Id': ['']
            }
        x_range = [x_start, now + timedelta(days=1)]  # x-axis scaled to (about usually) one day
        df = pd.DataFrame(data)

        # Plot the figure
        fig = px.timeline(
            df, x_start="Start time", x_end="End time", y="Activity", color="Id", range_x=x_range)
        fig.update_yaxes(autorange="reversed")  # otherwise tasks are listed from the bottom up
        fig.add_vline(x=datetime.now(), line_width=1, line_color="red")  # current time indication

        # Turn the HTML plot into a widget and do not open it within a browser
        self.browser.setHtml(fig.to_html(include_plotlyjs='cdn'))
