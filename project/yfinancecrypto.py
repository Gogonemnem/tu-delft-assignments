import time
from warnings import simplefilter

import numpy as np
import pandas as pd
import pandas_ta as ta
import yfinance as yf

# Remove performance warnings
simplefilter(action="ignore", category=pd.errors.PerformanceWarning)

# Remove restrictions on dataframe columns/rows
# pd.set_option('display.max_columns', None, 'display.max_rows', None)
pd.set_option('display.max_columns', None)


def main():
    # symbols = 'ETH-USD BTC-USD BNB-USD ADA-USD LINK-USD DOT1-USD LTC-USD'
    symbols = 'LINK-USD'

    df = apply_indicators(symbols)
    apply_signals(df, symbols)


class CryptoCurrencies:
    def __init__(self, symbols, intervals, periods):
        self.symbols = symbols
        self.intervals = intervals
        self.periods = periods
        # Use group_by function to be able to add indicators to dataframe with multiple coins
        self.data = yf.download(tickers=self.symbols, group_by='Ticker',
                                period=self.periods, interval=self.intervals)
        # print(self.data)
        self.data.dropna(inplace=True)

    def stochastic_oscillator(self):
        """Calculates stochastic oscillator indicator
        to see if a coin/stock has been oversold/overbought"""
        # Check how many symbols are given
        if len(self.symbols.split(' ')) > 1:
            for symbol in self.symbols.split(' '):
                self.data[[(symbol, '%K'), (symbol, '%D')]] = \
                    ta.stoch(
                        high=self.data[symbol, 'High'], low=self.data[symbol, 'Low'],
                        close=self.data[symbol, 'Close'], k=14, d=3, append=True
                    )
                # sort indicator values by other values from the same symbol
        # only 1 symbol given
        else:
            self.data[['%K', '%D']] = ta.stoch(
                high=self.data['High'], low=self.data['Low'],
                close=self.data['Close'], k=14, d=3, append=True
                )
        return self.data

    def simple_moving_average(self):
        """Calculates moving averages over N candlesticks"""
        # Check how many symbols are given
        if len(self.symbols.split(' ')) > 1:
            for symbol in self.symbols.split(' '):
                # self.ma = ta.hma(close=self.data[(symbol, 'Close')], length=30, append=True)
                self.data[(symbol, 'MA_20')] = ta.sma(
                    close=self.data[(symbol, 'Close')], length=20, append=True)
                self.data[(symbol, 'MA_50')] = ta.sma(
                    close=self.data[(symbol, 'Close')], length=50, append=True)
                self.data[(symbol, 'MA_200')] = ta.sma(
                    close=self.data[(symbol, 'Close')], length=200, append=True)
                # sort indicator values by other values from the same symbol
        # only 1 symbol given
        else:
            self.data['MA_20'] = ta.sma(
                close=self.data['Close'], length=20, append=True)
            self.data['MA_50'] = ta.sma(
                close=self.data['Close'], length=50, append=True)
            self.data['MA_200'] = ta.sma(
                close=self.data['Close'], length=200, append=True)
        # return self.ma
        return self.data

    def bollinger_bands(self):
        """Calculates the bollinger bands indicator
        to check if a coin/stock has been oversold/overbought"""
        # Check how many symbols are given
        if len(self.symbols.split(' ')) > 1:
            for symbol in self.symbols.split(' '):
                self.data[[
                    (symbol, 'BBL'), (symbol, 'BBM'), (symbol, 'BBU'), (symbol, 'BBB'),
                    (symbol, 'BBP')
                    ]] = \
                    ta.bbands(
                        close=self.data[symbol, 'Close'], length=20, StdDev=2, append=True
                        )
                # sort indicator values by other values from the same symbol
        # only 1 symbol given
        else:
            self.data[['BBL', 'BBM', 'BBU', 'BBB', 'BBP']] = ta.bbands(
                close=self.data['Close'], length=20, StdDev=2, append=True)
        return self.data

    def moving_average_convergence_divergence(self):
        """Calculates the MACD to check for momemtum indications"""
        # Check how many symbols are given
        if len(self.symbols.split(' ')) > 1:
            for symbol in self.symbols.split(' '):
                self.data[[(symbol, 'MACD'), (symbol, 'MACDh'), (symbol, 'MACDs')]] = ta.macd(
                    close=self.data[(symbol, 'Close')], append=True)
        # only 1 symbol given
        else:
            self.data[['MACD', 'MACDh', 'MACDs']] = ta.macd(
                close=self.data['Close'], append=True)
        return self.data

    def rsi(self):
        """Calculates the stochastic RSI
        to check if a coin/stock is oversold/overbought ( I THINK )"""
        # Check how many symbols are given
        if len(self.symbols.split(' ')) > 1:
            for symbol in self.symbols.split(' '):
                self.data[(symbol, 'RSI_14')] = ta.rsi(
                    close=self.data[(symbol, 'Close')], length=14, append=True)
        # only 1 symbol given
        else:
            self.data['RSI_14'] = ta.rsi(
                close=self.data['Close'], length=14, append=True)
        return self.data

    def exponential_moving_average(self):
        if len(self.symbols.split(' ')) > 1:
            for symbol in self.symbols.split(' '):
                self.data[(symbol, 'EMA_200')] = ta.ema(
                    close=self.data[(symbol, 'Close')], length=200, append=True)
                self.data[(symbol, 'EMA_100')] = ta.ema(
                    close=self.data[(symbol, 'Close')], length=100, append=True)
                self.data[(symbol, 'EMA_50')] = ta.ema(
                    close=self.data[(symbol, 'Close')], length=50, append=True)
        else:
            self.data['EMA_200'] = ta.ema(
                close=self.data['Close'], length=200, append=True)
            self.data['EMA_100'] = ta.ema(
                close=self.data['Close'], length=100, append=True)
            self.data['EMA_50'] = ta.ema(
                close=self.data['Close'], length=50, append=True)
        return self.data

    def money_flow_index(self):
        if len(self.symbols.split(' ')) > 1:
            for symbol in self.symbols.split(' '):
                self.data[(symbol, 'MFI_14')] = ta.mfi(
                    close=self.data[(symbol, 'Close')], low=self.data[(symbol, 'Low')],
                    high=self.data[(symbol, 'High')], volume=self.data[(symbol, 'Volume')],
                    length=14, append=True
                    )
        else:
            self.data['MFI_14'] = ta.mfi(
                close=self.data['Close'], low=self.data['Low'],
                high=self.data['High'], volume=self.data['Volume'], length=14, append=True)
        return self.data

    def stochastic_rsi(self):
        if len(self.symbols.split(' ')) > 1:
            for symbol in self.symbols.split(' '):
                self.data[[(symbol, 'StochRSI_%K'), (symbol, 'StochRSI_%D')]] = ta.stochrsi(
                    close=self.data[(symbol, 'Close')], length=14, rsi_length=14,
                    k=3, d=3, append=True
                )
        else:
            self.data[['StochRSI_%K', 'StochRSI_%D']] = ta.stochrsi(
                close=self.data['Close'], length=14, rsi_length=14, k=3, d=3, append=True)
        return self.data


class CryptoStrategy(CryptoCurrencies):
    def __init__(self, symbols, intervals, periods, strategy):
        super().__init__(symbols, intervals, periods)
        self.strategy = strategy
        if strategy == 'strategy_1':
            CryptoStrategy.strategy_1(self)

    def strategy_1(self):
        # Only works when multiple coins inserted now
        """Give buy/sell advice when price goes below/above bollinger bands.
        Also the stochastic oscillator needs to be below 20 / above 80"""
        CryptoCurrencies.bollinger_bands(self)
        CryptoCurrencies.stochastic_oscillator(self)
        for symbol in self.symbols.split(' '):
            self.data[(symbol, 'Buy!')] = np.where((self.data[(symbol, '%K')] < 20) & (
                self.data[(symbol, '%D')] < 20) & (self.data[(symbol, 'BBP')] < 0), True, False)
            self.data[(symbol, 'Sell!')] = np.where((self.data[(symbol, '%K')] > 80) & (
                self.data[(symbol, '%D')] > 80) & (self.data[(symbol, 'BBP')] > 1), True, False)
        return self.data


class CalculateSignals:
    def __init__(self, df, symbols):
        self.df = df
        self.dic = {}
        self.symbols = symbols

    def stochastic_signal(self):
        """Stochastic oscillator"""
        if len(self.symbols.split(' ')) > 1:
            for symbol in self.symbols.split(' '):
                k = self.df[(symbol, '%K')].iat[-1].round(3)
                d = self.df[(symbol, '%D')].iat[-1].round(3)
                if k >= 80 and d >= 80:
                    signal = 'Sell'
                elif k <= 20 and d <= 20:
                    signal = 'Buy'
                else:
                    signal = 'Hold'
                self.dic[(symbol, 'Stochastic Oscillator')] = signal, '%K: ' + str(k) + '        ' + ' %D: ' + str(d)
        else:
            k = self.df['%K'].iat[-1].round(3)
            d = self.df['%D'].iat[-1].round(3)
            if k >= 80 and d >= 80:
                signal = 'Sell'
            elif k <= 20 and d <= 20:
                signal = 'Buy'
            else:
                signal = 'Hold'
            self.dic['Stochastic Oscillator'] = signal, '%K: ' + str(k) + '        ' + '%D: ' + str(d)
        return self.dic

    def bollinger_signal(self):
        if len(self.symbols.split(' ')) > 1:
            for symbol in self.symbols.split(' '):
                bbp = self.df[(symbol, 'BBP')].iat[-1].round(3)
                if bbp > 1:
                    signal = 'Sell'
                elif bbp < 0:
                    signal = 'Buy'
                else:
                    signal = 'Hold'
                self.dic[(symbol, 'Bollinger Bands')] = signal, '%BB: ' + str(bbp)
        else:
            bbp = self.df['BBP'].iat[-1].round(3)
            if bbp > 1:
                signal = 'Sell'
            elif bbp < 0:
                signal = 'Buy'
            else:
                signal = 'Hold'
            self.dic['Bollinger Bands'] = signal, '%BB: ' + str(bbp)
        return self.dic

    def mfi_signal(self):
        if len(self.symbols.split(' ')) > 1:
            for symbol in self.symbols.split(' '):
                mfi = self.df[(symbol, 'MFI_14')].iat[-1].round(3)
                if mfi >= 90:
                    signal = 'Sell'
                elif mfi <= 10:
                    signal = 'Buy'
                else:
                    signal = 'Hold'
                self.dic[(symbol, 'Money Flow Index')] = signal, 'MFI-14: ' + str(mfi)
        else:
            mfi = self.df['MFI_14'].iat[-1].round(3)
            if mfi >= 90:
                signal = 'Sell'
            elif mfi <= 10:
                signal = 'Buy'
            else:
                signal = 'Hold'
            self.dic['Money Flow Index'] = signal, 'MFI-14: ' + str(mfi)
        return self.dic

    def macd_signal(self):
        if len(self.symbols.split(' ')) > 1:
            for symbol in self.symbols.split(' '):
                MACD = self.df[(symbol, 'MACD')].iat[-1].round(3)        # black line
                # MACDh = self.df[(symbol, 'MACDh')]      # difference betweeen MACD and MACDs
                MACDs = self.df[(symbol, 'MACDs')].iat[-1].round(3)      # red line
                if MACDs < MACD < 0:
                    signal = 'Buy'
                elif MACDs > MACD > 0:
                    signal = 'Sell'
                else:
                    signal = 'Hold'
                self.dic[(symbol, 'Moving Average Convergence Divergence')] = signal, 'MACD-Line: ' + str(MACD) + \
                    '      ' + 'Slow-Line: ' + str(MACDs)
        else:
            MACD = self.df['MACD'].iat[-1].round(3)   # black line
            # MACDh = self.df[(symbol, 'MACDh')]      # difference betweeen MACD and MACDs
            MACDs = self.df['MACDs'].iat[-1].round(3)   # red line
            if MACDs < MACD < 0:
                signal = 'Buy'
            elif MACDs > MACD > 0:
                signal = 'Sell'
            else:
                signal = 'Hold'
            self.dic['Moving Average Convergence Divergence'] = signal, 'MACD-Line: ' + str(MACD) + '      ' \
                + 'Slow-Line: ' + str(MACDs)
        return self.dic

    def long_term_trend(self):
        if len(self.symbols.split(' ')) > 1:
            for symbol in self.symbols.split(' '):
                ema = self.df[(symbol, 'EMA_200')].iat[-1].round(3)
                close = self.df[(symbol, 'Close')].iat[-1].round(3)
                if ema - close > 0:
                    signal = 'Buy/Bullish'
                else:
                    signal = 'Sell/Bearish'
                self.dic[(symbol, 'Long Term Trend')] = signal, 'EMA: ' + str(ema) + '      ' + \
                    'Close-price: ' + str(close)
        else:
            ema = self.df['EMA_200'].iat[-1].round(3)
            close = self.df['Close'].iat[-1].round(3)
            if ema - close > 0:
                signal = 'Buy/Bullish'
            else:
                signal = 'Sell/Bearish'
            self.dic['Long Term Trend'] = signal, 'EMA-200: ' + str(ema) + '      ' + \
                'Close-price: ' + str(close)
        return self.dic

    def rsi_signal(self):
        if len(self.symbols.split(' ')) > 1:
            for symbol in self.symbols.split(' '):
                rsi = self.df[(symbol, 'RSI_14')].iat[-1].round(3)
                if rsi >= 70:
                    signal = 'Sell'
                elif rsi <= 30:
                    signal = 'Buy'
                else:
                    signal = 'Hold'
                self.dic[(symbol, 'Relative Strength Index')] = signal, 'RSI-14: ' + str(rsi)
        else:
            rsi = self.df['RSI_14'].iat[-1].round(3)
            if rsi >= 70:
                signal = 'Sell'
            elif rsi <= 30:
                signal = 'Buy'
            else:
                signal = 'Hold'
            self.dic['Relative Strength Index'] = signal, 'RSI-14: ' + str(rsi)
        return self.dic


def apply_indicators(symbols):
    """Call all indcator functions"""
    btc_1 = CryptoCurrencies(symbols=symbols, periods='1000d', intervals='1d')
    btc_1.stochastic_oscillator()
    btc_1.simple_moving_average()
    btc_1.bollinger_bands()
    btc_1.moving_average_convergence_divergence()
    btc_1.rsi()
    btc_1.exponential_moving_average()
    btc_1.money_flow_index()
    btc_1.stochastic_rsi()
    btc_1.data = btc_1.data.sort_index(level=0, axis=1)
    return btc_1.data


def apply_signals(df, symbols):
    signal = CalculateSignals(df, symbols)
    signal.stochastic_signal()
    signal.bollinger_signal()
    signal.mfi_signal()
    signal.macd_signal()
    signal.long_term_trend()
    signal.rsi_signal()
    signal_df = pd.DataFrame(signal.dic)
    signal_transposed = signal_df.T
    signal_transposed.columns = ['Advice', 'Values']
    signal_transposed = signal_transposed.rename_axis('Indicator', axis=1)
    return signal_transposed


if __name__ == "__main__":
    start_time = time.time()
    main()
    print(f'Runtime= {time.time() - start_time}')


# Different kind of indicators:
# Trend: PSAR, MA_200, MA_20, EMA, MACD
# Volatility: BOLLINGER BANDS, ATR, ADX
# Momentum: MACD, STOCHASTIC, RSI, On Balance Volume, ROC
# Volume: Money Flow Index, On Balance Volume
# Fibonacci retracements


# Script below to update dataframe every minute

# while True:
#     if datetime.now().second % 60 == 0:
#         btc = DataFrame(symbols='ETH-USD BTC-USD ADA-USD LTC-USD BNB-USD',
#             periods='1d', intervals='1m')
#         # print(btc.stochastic_indicator())
#         print(btc.moving_average())
#         time.sleep(1)


# Difference MA and EMA: by the EMA the last values are more important than the old values
# PSAR: when dots are under the price ->
# bullish trend, when dots are above the price ->
# bearish trend> ! Graph needs to be trending !
#         need to add EMA to check long term trend.
# Try add candle patterns, for example the hammer to show for bullish trend.


# Not working PSAR functions

# DOESN'T work correctly, idk why :(. Gives wrong values.
# Think this function is broken since it also doesn't work on an easy example
# def parabolic_stop_and_reverse(self):
#     """Check if the trend is going up or down, gives indication whether to buy or sell"""
#     # Check how many symbols are given
#     # Don't drop NaN values because 1 column will always contain NaN values
#     if len(self.symbols.split(' ')) > 1:
#         for symbol in self.symbols.split(' '):
#             self.data[[(symbol, 'PSAR-L'), (symbol, 'PSAR-U'), (symbol, 'PSAR-af'),
#               (symbol, 'PSAR-rev')]] = ta.psar(
#               high=self.data[(symbol, 'High')], low=self.data[(symbol, 'Low')],
#               close=self.data[(symbol, 'Close')],
#               af0=0.02, af=0.02, max_af=0.2
#             )
#             self.data = self.data.sort_index(level=0, axis=1)
#     else:
#         self.data[['PSAR-L', 'PSAR-U', 'PSAR-af', 'PSAR-rev']] = ta.psar(high=self.data['High'],
#                     low=self.data['Low'], close=self.data['Close'], max_af=0.2)
#     return self.data

# def strategy_2(self):
#     """NOT working, something wrong with PSAR function. Probably have to delete this -->
#     Need a LOT of data to work properly, 10+years if using day interval.
#     Might still not work correctly"""
#     # Only works when multiple coins inserted now
#     CryptoCurrencies.moving_average(self)
#     CryptoCurrencies.parabolic_stop_and_reverse(self)
    # for symbol in self.symbols.split(' '):
    #     self.data[(symbol, 'Buy!')] = np.where((self.data[(symbol, 'PSAR-rev')] == 1) &
    #     (pd.isna(self.data[(symbol, 'PSAR-U')])) &
    #     ((self.data[(symbol, 'MA_200')]) < (self.data[(symbol, 'Low')])), True, False
    #     )

    #     self.data[(symbol, 'Sell!')] = np.where((self.data[(symbol, 'PSAR-rev')] == 1) &
    #     (pd.isna(self.data[(symbol, 'PSAR-L')])) &
    #     ((self.data[(symbol, 'MA_200')]) < (self.data[(symbol, 'Low')])), True, False
    #     )

    #     self.data[(symbol, 'Go short!')] = np.where((self.data[(symbol, 'PSAR-rev')] == 1) &
    #     (pd.isna(self.data[(symbol, 'PSAR-L')])) &
    #     ((self.data[(symbol, 'MA_200')]) > (self.data[(symbol, 'Low')])), True, False
    #     )
    # return self.data
