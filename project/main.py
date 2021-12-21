import pandas as pd
from PyQt6 import uic
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWidgets import QApplication, QFrame, QMainWindow

from input import Input
from overview import Overview


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        #loading ui is temporary as layout changes every time
        uic.loadUi("./MainWindow.ui", self)

        # additional loading
        # individual tab
        price_change_frame = self.findChild(QFrame, 'price_frame')
        price_change = QWebEngineView(price_change_frame)
        price_change.setObjectName('price_change')
        price_change_frame.layout().addWidget(price_change)

        price_graph_frame = self.findChild(QFrame, 'price_graph_frame')
        price_graph = QWebEngineView(price_graph_frame)
        price_graph.setObjectName('price_graph')
        price_graph_frame.layout().addWidget(price_graph)

        indicator_chart_view = self.findChild(QFrame, 'indicator_frame')
        indicator_chart = QWebEngineView(indicator_chart_view)
        indicator_chart.setObjectName('indicator_chart')
        indicator_chart_view.layout().addWidget(indicator_chart)

        # comparison tab
        frame_graph = self.findChild(QFrame, 'frame_graph_comparison')
        graph_comparison = QWebEngineView(frame_graph)
        graph_comparison.setObjectName('graph_comparison')
        frame_graph.layout().addWidget(graph_comparison)

        frame_graph = self.findChild(QFrame, 'frame_9')
        indicator_comparison = QWebEngineView(frame_graph)
        indicator_comparison.setObjectName('indicator_comparison')
        frame_graph.layout().addWidget(indicator_comparison)

        price_frame_left = self.findChild(QFrame, 'price_frame_left')
        price_left = QWebEngineView(price_frame_left)
        price_left.setObjectName('price_left')
        price_frame_left.layout().addWidget(price_left)

        price_frame_right = self.findChild(QFrame, 'price_frame_right')
        price_right = QWebEngineView(price_frame_right)
        price_right.setObjectName('price_right')
        price_frame_right.layout().addWidget(price_right)

        # at end of project, remove df as we now use it only for debugging
        input_tab = Input(self, df)
        Overview(self, input_tab)


if __name__ == "__main__":
    import sys

    column_names = ['Symbol', 'Name']
    assets = [['AAPL', 'Apple Inc.'], ['AMZN', 'Amazon.com, Inc.'], \
            ['TSLA', 'Tesla, Inc.'], ['FB', 'Meta Platforms, Inc.'], \
            ['BTC-USD', 'Bitcoin'], ['ETH-USD', 'Ethereum'], \
            ['BNB-USD', 'Binance Coin']]
    df = pd.DataFrame(assets, columns = column_names)

    # symbol = 'BTC-USD'
    # interval = '1d'

    pd.options.mode.chained_assignment = None  # default='warn'

    # ADVICES:
    # df1 = apply_indicators(symbol)
    # advice = apply_signals(df, symbol)

    # app = QtWidgets.QApplication(sys.argv)
    # window = Individual(df, advice, symbol, interval)
    # window.showMaximized()
    # app.exec()

    app = QApplication(sys.argv)
    ui = MainWindow()
    ui.showMaximized()
    sys.exit(app.exec())
