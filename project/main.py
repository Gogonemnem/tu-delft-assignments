import pandas as pd
from PyQt6 import QtWidgets, uic
from project.input import Input
from project.overview import Overview


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        uic.loadUi("./MainWindow.ui", self)

        # at end of project, remove df as we now use it only for debugging
        input_tab = Input(self, df)
        Overview(self, input_tab)


if __name__ == "__main__":
    import sys

    column_names = ['Symbol', 'Name']
    assets = [['AAPL', 'Apple Inc.'], ['AMZN', 'Amazon.com, Inc.'], \
            ['TSLA', 'Tesla, Inc.'], ['FB', 'Meta Platforms, Inc.'], \
            ['Test', 'TEST'], ['LALA', 'LA'], ['CH', 'CHECK']]
    df = pd.DataFrame(assets, columns = column_names)

    app = QtWidgets.QApplication(sys.argv)
    ui = MainWindow()
    ui.show()
    sys.exit(app.exec())
