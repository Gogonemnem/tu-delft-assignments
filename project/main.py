import pandas as pd
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow

from input import Input
from overview import Overview


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        uic.loadUi("../project/MainWindow.ui", self)

        input_tab = Input(self, df)
        Overview(self, input_tab)


if __name__ == "__main__":
    import sys

    column_names = ['Symbol', 'Name', 'Sector']
    assets = [['AAPL', 'Apple Inc.', 'Technology'], ['AMZN', 'Amazon.com, Inc.', 'Consumer Cyclical'], \
            ['TSLA', 'Tesla, Inc.', 'Consumer Cyclical'], ['FB', 'Meta Platforms, Inc.', 'Communication Services'], \
            ['BTC-USD', 'Bitcoin', 'Cryptocurrency'], ['ETH-USD', 'Ethereum', 'Cryptocurrency'], \
            ['BNB-USD', 'Binance Coin', 'Cryptocurrency']]
    df = pd.DataFrame(assets, columns = column_names)

    pd.options.mode.chained_assignment = None  # default='warn'

    app = QApplication(sys.argv)
    ui = MainWindow()
    ui.showMaximized()
    sys.exit(app.exec())
