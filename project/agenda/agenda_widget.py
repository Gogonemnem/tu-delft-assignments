from datetime import datetime, timedelta
import pandas as pd
import plotly.express as px
from PyQt5 import QtWidgets, QtWebEngineWidgets
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QWidget, QHBoxLayout


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

        self.buttons_widget = QWidget()
        self.buttons_layout = QHBoxLayout(self.buttons_widget)
        self.buttons_layout.addWidget(self.update_button)
        self.buttons_layout.addWidget(self.stop_button)
        self.buttons_widget.setFixedHeight(40)

        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.buttons_widget)
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
        self.agenda.remove_activity_over()
        activities = self.agenda.agenda
        now = self.agenda.now

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
