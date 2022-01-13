import pandas as pd
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow

from input import Input
from overview import Overview


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        #loading ui is temporary as layout changes every time
        uic.loadUi("../project/MainWindow.ui", self)

        # at end of project, remove df as we now use it only for debugging
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
    ui.show()
    sys.exit(app.exec())
