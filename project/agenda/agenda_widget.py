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


class AgendaWidget(QtWidgets.QGroupBox):
    def __init__(self, agenda, parent=None):
        super().__init__(parent)
        self.setTitle("The agenda can be seen below")
        self.button = QtWidgets.QPushButton('Show/Update Agenda', self)
        self.browser = QtWebEngineWidgets.QWebEngineView(self)

        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.button, alignment=QtCore.Qt.AlignHCenter)
        layout.addWidget(self.browser)

        self.button.clicked.connect(lambda: self.show_graph(agenda))
        # self.resize(1000, 800)

    def show_graph(self, agenda):
        activities = agenda.agenda
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
