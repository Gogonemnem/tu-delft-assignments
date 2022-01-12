import pandas as pd
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow

from input import Input
from overview import Overview


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        #loading ui is temporary as layout changes every time
        uic.loadUi("./MainWindow.ui", self)

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
