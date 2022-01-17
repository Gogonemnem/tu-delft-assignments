import pandas as pd
import yfinance as yf
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWidgets import QHeaderView, QLabel, QMainWindow, QTableView

from dataframe_model import DataFrameModel
from graphdesigner import GraphDesigner


class Individual:
    def __init__(self, main_window: QMainWindow, dataframe: pd.DataFrame,
                 advice: pd.DataFrame, symbol, interval, overall_advice):

        self.main_window = main_window
        dataframe = dataframe.droplevel(0, axis=1)
        self.dataframe = dataframe
        self.advice = advice
        self.price_df = dataframe[['High', 'Low', 'Close', 'Volume']].round(3)
        self.ticker = yf.Ticker(symbol)
        self.news_frame = pd.DataFrame(self.ticker.news)
        self.news_frame = self.news_frame.drop(['uuid', 'providerPublishTime', 'type'], 1)
        self.interval = interval
        self.symbol = symbol
        self.overall_advice = overall_advice

        if self.ticker.info['toCurrency'] is None:
            self.recommendationsframe = pd.DataFrame(self.ticker.recommendations.tail())
            self.recommendationsframe = self.recommendationsframe.drop(['From Grade', 'Action'], 1)
        else:
            self.recommendationsframe = pd.DataFrame({'': f'No available for the selected currency: {symbol}'}, index=[0])

        self.set_recommendations()
        self.set_news()
        self.set_prices()
        self.set_advice()
        self.set_labels()
        self.draw_graphs()

    def set_recommendations(self):
        recommendations_model = DataFrameModel(self.recommendationsframe)
        recommendationsview: QTableView = self.main_window.findChild(QTableView, 'tableView_3')
        recommendationsview.setModel(recommendations_model)
        recommendationsview.resizeRowsToContents()
        header = recommendationsview.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        vertheader = recommendationsview.verticalHeader()
        vertheader.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

    def set_news(self):
        news_model = DataFrameModel(self.news_frame)
        newsview: QTableView = self.main_window.findChild(QTableView, 'tableView_4')
        newsview.setModel(news_model)
        header = newsview.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

    def set_prices(self):
        model = DataFrameModel(self.price_df)
        view: QTableView = self.main_window.findChild(QTableView, 'price_table')
        view.setModel(model)
        view.resizeRowsToContents()
        header = view.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

    def set_advice(self):
        model2 = DataFrameModel(self.advice)
        advice_view: QTableView = self.main_window.findChild(QTableView, 'tableView_2')
        advice_view.setModel(model2)
        advice_view.resizeRowsToContents()
        horizontal_header = advice_view.horizontalHeader()
        vertical_header = advice_view.verticalHeader()
        horizontal_header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        vertical_header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

    def set_labels(self):
        symbol_label = self.main_window.findChild(QLabel, "symbol_label")
        symbol_label.setText(self.symbol)
        full_ticker_label = self.main_window.findChild(QLabel, "label")
        full_ticker_label.setText(self.ticker.info['shortName'])

        interval_label = self.main_window.findChild(QLabel, "interval_label")
        interval_label.setText('Interval: ' + self.interval)

        advice_label = self.main_window.findChild(QLabel, 'label_3')
        advice_label.setText('Advice: ' + self.overall_advice[self.symbol])

    def draw_graphs(self):
        price_change = self.main_window.findChild(QWebEngineView, 'price_change')
        price_graph = self.main_window.findChild(QWebEngineView, 'price_graph')
        indicator_chart = self.main_window.findChild(QWebEngineView, 'indicator_chart')

        price_change.setHtml(GraphDesigner.show_price(
            self.price_df).to_html(include_plotlyjs='cdn'))

        price_graph.setHtml(GraphDesigner.draw_prices(
                    self.dataframe, self.symbol).to_html(include_plotlyjs='cdn'))

        indicator_chart.setHtml(
            GraphDesigner.indicator_chart(self.interval, self.symbol).to_html(include_plotlyjs='cdn'))

if __name__ == "__main__":
    raise Exception("De executie is verplaatst naar main.py")
