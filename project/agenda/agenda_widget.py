from datetime import datetime, timedelta

import pandas as pd
import plotly.express as px
from PyQt5 import QtWidgets, QtWebEngineWidgets, QtCore


# This is added by Nils
class AgendaWidget(QtWidgets.QGroupBox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setTitle("The agenda can be seen below")
        self.button = QtWidgets.QPushButton('agenda')
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.button)
        self.setLayout(layout)


# Added by Gonem, needs to be rewritten to be included in to the main window!
class Widget(QtWidgets.QWidget):
    def __init__(self, agenda, parent=None):
        super().__init__(parent)
        self.button = QtWidgets.QPushButton('Show Agenda', self)
        self.browser = QtWebEngineWidgets.QWebEngineView(self)

        vlayout = QtWidgets.QVBoxLayout(self)
        vlayout.addWidget(self.button, alignment=QtCore.Qt.AlignHCenter)
        vlayout.addWidget(self.browser)

        # HOW DO WE PASS THE AGENDA OBJECT TO THE BUTTON?
        # GLOBAL VARIABLE?
        self.button.clicked.connect(lambda: self.show_graph(agenda))
        self.resize(1000, 800)

    def show_graph(self, agenda):
        dics = []
        activities = agenda.agenda
        for id, activity in enumerate(activities):
            # Turn every activity object attributes into a dictionary
            # and add it to a list and turn it into a dataframe
            ac_dic = activity.__dict__
            ac_dic['id'] = str(id)
            dics.append({key: ac_dic[key] for key in ['activity', 'start_time', 'end_time', 'id']})
        df = pd.DataFrame(dics)

        # Determine range of the x-axis
        if activities:
            x_start = activities[0].start_time
            x_range = [x_start, x_start+timedelta(days=1)]
        else:
            x_range = None

        # Plot the figure
        fig = px.timeline(
            df, x_start="start_time", x_end="end_time", y="activity", color="id", range_x=x_range)
        fig.update_yaxes(autorange="reversed")  # otherwise tasks are listed from the bottom up
        fig.add_vline(x=datetime.now(), line_width=1, line_color="red")  # current time indication

        # Turn the HTML plot into a widget and do not open it within a browser
        self.browser.setHtml(fig.to_html(include_plotlyjs='cdn'))
