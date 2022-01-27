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
# new = yf.Ticker('CVX')
# for key in new.info.keys():
#     print(key)

def financial_background(symb):
    df = yf.Ticker(symb).info
    all_comp = {}
    all_comp['PE'] = df['trailingPE']
    all_comp['PEG'] = df['pegRatio']
    all_comp['PTB'] = df['priceToBook']
    all_comp['CR'] = df['currentRatio']
    all_comp['DTE'] = df['debtToEquity']
    if df['dividendRate'] is None:
        DR = 0
    else:
        DR = df['dividendRate']

    all_comp['DPS'] = DR/df['trailingEps']
    # all_comp['EPS'] = df['trailingEps']
    return all_comp


class CryptoCurrencies:
    interval_period = {
        '1m': '5d',
        '5m': '10d',
        '15m': '15d',
        '30m': '30d',
        '1h': '60d',
        '1d': '5y',
        '1wk': '10y',
        '1mo': '10y',
        '3mo': '10y'
    }

    def __init__(self, symbols, intervals, periods=None):
        self.symbols = symbols
        self.intervals = intervals
        if periods:
            self.periods = periods
        elif intervals in CryptoCurrencies.interval_period:
            self.periods = CryptoCurrencies.interval_period[intervals]
        else:
            self.periods = 'max' # default
        # Use group_by function to be able to add indicators to dataframe with multiple coins
        self.data = yf.download(tickers=self.symbols, group_by='Ticker',
                                period=self.periods, interval=self.intervals)

        if len(symbols) == 1:
            self.data.loc[symbols[0], :] = symbols[0]
            self.data = self.data.transpose().set_index(symbols[0], append=True) \
                            .swaplevel().transpose()

        self.data.dropna(inplace=True)

    def stochastic_oscillator(self):
        """Calculates stochastic oscillator indicator
        to see if a coin/stock has been oversold/overbought"""
        for symbol in self.symbols:
            self.data[[(symbol, '%K'), (symbol, '%D')]] = \
                ta.stoch(
                    high=self.data[symbol, 'High'], low=self.data[symbol, 'Low'],
                    close=self.data[symbol, 'Close'], k=14, d=3, append=True
                )
        return self.data

    def simple_moving_average(self):
        """Calculates moving averages over N candlesticks"""
        for symbol in self.symbols:
            if len(self.data) >= 100:
                self.data[(symbol, 'MA_100')] = ta.sma(
                    close=self.data[(symbol, 'Close')], length=100, append=True)
            if len(self.data) >= 50:
                self.data[(symbol, 'MA_50')] = ta.sma(
                    close=self.data[(symbol, 'Close')], length=50, append=True)
            if len(self.data) >= 20:
                self.data[(symbol, 'MA_20')] = ta.sma(
                    close=self.data[(symbol, 'Close')], length=20, append=True)
        return self.data

    def bollinger_bands(self):
        """Calculates the bollinger bands indicator
        to check if a coin/stock has been oversold/overbought"""
        for symbol in self.symbols:
            self.data[[
                (symbol, 'BBL'), (symbol, 'BBM'), (symbol, 'BBU'), (symbol, 'BBB'),
                (symbol, 'BBP')
                ]] = \
                ta.bbands(
                    close=self.data[symbol, 'Close'], length=20, StdDev=2, append=True
                    )
        return self.data

    def moving_average_convergence_divergence(self):
        """Calculates the MACD to check for momemtum indications"""
        for symbol in self.symbols:
            self.data[[(symbol, 'MACD'), (symbol, 'MACDh'), (symbol, 'MACDs')]] = ta.macd(
                close=self.data[(symbol, 'Close')], append=True)
        return self.data

    def rsi(self):
        """Calculates the stochastic RSI
        to check if a coin/stock is oversold/overbought ( I THINK )"""
        for symbol in self.symbols:
            self.data[(symbol, 'RSI_14')] = ta.rsi(
                close=self.data[(symbol, 'Close')], length=14, append=True)
        return self.data

    def exponential_moving_average(self):
        for symbol in self.symbols:
            if len(self.data) >= 100:
                self.data[(symbol, 'EMA_100')] = ta.ema(
                        close=self.data[(symbol, 'Close')], length=100, append=True)
            if len(self.data) >= 50:
                self.data[(symbol, 'EMA_50')] = ta.ema(
                    close=self.data[(symbol, 'Close')], length=50, append=True)
            if len(self.data) >= 20:
                self.data[(symbol, 'EMA_20')] = ta.ema(
                    close=self.data[(symbol, 'Close')], length=20, append=True)
        return self.data

    def money_flow_index(self):
        for symbol in self.symbols:
            self.data[(symbol, 'MFI_14')] = ta.mfi(
                close=self.data[(symbol, 'Close')], low=self.data[(symbol, 'Low')],
                high=self.data[(symbol, 'High')], volume=self.data[(symbol, 'Volume')],
                length=14, append=True
                )
        return self.data

    def stochastic_rsi(self):
        for symbol in self.symbols:
            self.data[[(symbol, 'StochRSI_%K'), (symbol, 'StochRSI_%D')]] = ta.stochrsi(
                    close=self.data[(symbol, 'Close')], length=14, rsi_length=14,
                    k=3, d=3, append=True
                )
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
        for symbol in self.symbols:
            k = self.df[(symbol, '%K')].iat[-1].round(3)
            d = self.df[(symbol, '%D')].iat[-1].round(3)
            if k >= 80 and d >= 80:
                signal = 'Sell'
            elif k <= 20 and d <= 20:
                signal = 'Buy'
            else:
                signal = 'Hold'
            self.dic[(symbol, 'Stochastic Oscillator')] = \
                signal, '%K: ' + str(k) + '        ' + ' %D: ' + str(d)
        return self.dic

    def bollinger_signal(self):
        for symbol in self.symbols:
            bbp = round(self.df[(symbol, 'BBP')].iat[-1], 3)
            if bbp > 1:
                signal = 'Sell'
            elif bbp < 0:
                signal = 'Buy'
            else:
                signal = 'Hold'
            self.dic[(symbol, 'Bollinger Bands')] = signal, '%BB: ' + str(bbp)
        return self.dic

    def mfi_signal(self):
        for symbol in self.symbols:
            mfi = self.df[(symbol, 'MFI_14')].iat[-1].round(3)
            if mfi >= 90:
                signal = 'Sell'
            elif mfi <= 10:
                signal = 'Buy'
            else:
                signal = 'Hold'
            self.dic[(symbol, 'Money Flow Index')] = signal, 'MFI-14: ' + str(mfi)
        return self.dic

    def macd_signal(self):
        for symbol in self.symbols:
            MACD = self.df[(symbol, 'MACD')].iat[-1].round(3)        # black line
            # MACDh = self.df[(symbol, 'MACDh')]      # difference betweeen MACD and MACDs
            MACDs = self.df[(symbol, 'MACDs')].iat[-1].round(3)      # red line
            if MACDs < MACD < 0:
                signal = 'Buy'
            elif MACDs > MACD > 0:
                signal = 'Sell'
            else:
                signal = 'Hold'
            self.dic[(symbol, 'Moving Average CD')] = signal, 'MACD-Line: ' + str(MACD) + \
                '      ' + 'Slow-Line: ' + str(MACDs)
        return self.dic

    def long_term_trend(self):
        for symbol in self.symbols:
            if len(self.df) >= 100:
                ema = self.df[(symbol, 'EMA_100')].iat[-1].round(3)
                close = round(self.df[(symbol, 'Close')].iat[-1], 3)
                if ema - close > 0:
                    signal = 'Buy/Bullish'
                else:
                    signal = 'Sell/Bearish'
                self.dic[(symbol, 'Long Term Trend')] = signal, 'EMA: ' + str(ema) + '      ' + \
                    'Close-price: ' + str(close)
        return self.dic

    def rsi_signal(self):
        for symbol in self.symbols:
            rsi = self.df[(symbol, 'RSI_14')].iat[-1].round(3)
            if rsi >= 70:
                signal = 'Sell'
            elif rsi <= 30:
                signal = 'Buy'
            else:
                signal = 'Hold'
            self.dic[(symbol, 'Relative Strength Index')] = signal, 'RSI-14: ' + str(rsi)
        return self.dic

    def finance_signals(self):
        """""Takes all the financial data and gives an opinion
        on if the company seems financially stable based on this data"""
        for symbol in self.symbols:
            information = yf.Ticker(symbol).info
            # checks if it is not a crypto, because cryptos dont have financials
            if '-USD' in symbol:
                continue

            PE = information['trailingPE']
            PEG = information['pegRatio']
            PTB = information['priceToBook']
            CR = information['currentRatio']
            DTE = information['debtToEquity']

            # PE ratio advice
            signalPE = splitter(PE, [10, 50], ['Undervalued', 'Neutral', 'Overvalued'])
            self.dic[(symbol, 'PE ratio')] = signalPE, 'PE: ' + str(PE)[:5]

            #PEG ratio advice
            signalPEG = splitter(PEG, [0.9, 1.1], ['Undervalued', 'Neutral', 'Overvalued'])
            self.dic[(symbol, 'PEG ratio')] = signalPEG, 'PEG: ' + str(PEG)[:5]

            # Price to book advice
            signalPTB = splitter(PTB, [1, 8], ['Undervalued', 'Neutral', 'Overvalued'])
            self.dic[(symbol, 'Price to book ratio')] = signalPTB, 'PtB: ' + str(PTB)[:5]

            # Current ratio advice
            signalCR = splitter(CR, [1, 3], ['Undervalued', 'Neutral', 'Overvalued'])
            self.dic[(symbol, 'Current ratio')] = signalCR, 'CR: ' + str(CR)[:5]

            # Debt to Equity advice
            signalDTE = splitter(DTE, [0.2, 0.7], ['Undervalued', 'Neutral', 'Overvalued'])
            self.dic[(symbol, 'Debt to Equity')] = signalDTE, 'DtE: ' + str(DTE)[:6]

            # Dividend payout ratio advice
            DR = 0 if information['dividendRate'] is None else information['dividendRate']
            percentage = DR/information['trailingEps']
            signalDPS = splitter(percentage, [0, 0.55], ['Neutral', 'Undervalued', 'Overvalued'])
            self.dic[(symbol, 'Dividend Payout Ratio')] = \
                signalDPS, 'DPR: ' + str(percentage)[:5] + '%'

            return self.dic

def splitter(case, boundaries, values):
    if len(boundaries) != len(values)-1:
        return None

    for boundary, value in zip(boundaries, values):
        if case <= boundary:
            return value

    return values[-1]

def apply_indicators(symbols, intervals, periods=None):
    """Call all indcator functions"""
    if len(symbols) == 0:
        return None

    btc_1 = CryptoCurrencies(symbols, intervals, periods)
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


def apply_signals(df, symbols): #this is important func!
    if len(symbols) == 0:
        return None

    signal = CalculateSignals(df, symbols)
    signal.stochastic_signal()
    signal.bollinger_signal()
    signal.mfi_signal()
    signal.macd_signal()
    signal.long_term_trend()
    signal.rsi_signal()
    signal.finance_signals()
    signal_df = pd.DataFrame(signal.dic)
    signal_transposed = signal_df.T
    signal_transposed.columns = ['Advice', 'Values']
    signal_transposed = signal_transposed.rename_axis('Indicator', axis=1)
    return signal_transposed



def advice(signals, symbols):
    overall_advice_dic = {}
    for symbol in symbols:
        tot = 0
        for i in signals.itertuples():
            if i[0][0] == symbol:
                if 'Buy' in i[1]:
                    tot += 1
                if 'Sell' in i[1]:
                    tot -= 1
        if tot == -6:
            overall_advice_dic[symbol] = 'Very strong sell'
        elif -6 < tot <= -4:
            overall_advice_dic[symbol] = 'Strong sell'
        elif -4 < tot <= -2:
            overall_advice_dic[symbol] = 'Sell'
        elif -2 < tot < 2:
            overall_advice_dic[symbol] = 'Hold'
        elif 2 <= tot < 4:
            overall_advice_dic[symbol] = 'Buy'
        elif 4 <= tot < 6:
            overall_advice_dic[symbol] = 'Strong buy'
        elif tot == 6:
            overall_advice_dic[symbol] = 'Very strong buy'
    return overall_advice_dic


def main(symbols):
    # symbols = 'ETH-USD BTC-USD BNB-USD ADA-USD LINK-USD DOT1-USD LTC-USD'.split(' ')
    # symbols = ['LINK-USD']

    df = apply_indicators(symbols, intervals='1m')
    signals = apply_signals(df, symbols)
    overall_advice = advice(signals, symbols)
    return df, signals, overall_advice


if __name__ == "__main__":
    start_time = time.time()
    dataframe, signal_frame, advice = main(['BTC-USD'])
    # print(f'Runtime= {time.time() - start_time}')


# Different kind of indicators
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
