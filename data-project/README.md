# 'Project Title'
'Project Title' is a stock/cryptocurrency screener that allow investors to quickly sort through the myriad of available stocks, increasing exchange-traded funds and rising cryptocurrencies according to technical analysis. They will also be able to find extra information, such as, historical price, indicators based on financial quantitative analysis and recommendations from established analysts.'Project Title' allows investors to employ their own methodology about what makes a stock or ETF valuable (longer-term traders) or spot a potential trading opportunity (shorter-term traders). 

## How to run the application
- Download the repository
- Install Python 3
- Install the dependencies by running `pip install -r requirements.txt` in the terminal
- Locate the `main.py` file in the `project` directory, and run the file
- If the UI file cannot be found try locations: `../project/MainWindow.ui` or `./project/MainWindow.ui`

## How to get advice
1. Add the tickers of one's interest
2. Press `Get Overview` for an overview of added tickers
3. For an extensive overview, select the ticker in the left box and press `Check Ticker(s)`
4. For a side-by-side view of two tickers, select `Compare Tickers`, select the two tickers in the boxes and press `Check Ticker(s)`

## User Stories
### Short-term trader
As a short-term trader, you want to enter the market low and exit high within a short time range typically around a few minutes to a few days. In order to obtain these profits as often as possible, you want to spot (un)fortunate trends and keep track of current news/events. All displayed in a simple but informative overview of tickers of interest.

### Long-term investor
As a long-term investor, you enter the market with a capital that is enough to accept losses over a short amount of time,
with the idea that the profit will come over a longer amount of time. To get an idea of a good long-term investing plan, 
you are able to get an overview of financial data of stocks and cryptocurrencies. 

## Features
- Adding tickers of one's interest
- Saving and loading tickers from sessions
- Overview of advices for tickers
- Row sorting of overview on all columns
- Filter overview on market sector
- Extensive overview of single ticker
- Extensive side-by-side overview of two tickers


## Future Features
- Overview based on strategy/methodology of the investor's interest
- Extensive overview GUI improvements
- A single advice when comparing two tickers

## Dependencies
- Pandas
- Pandas_ta
- PyQt6
- PyQt6-WebEngine
- Yfinance
- Plotly
- Fear_and_greed

## Developer Team
- Betsie Hartsink 
- Fabian Gebben
- Gonem Lau
- Jelle van Straeten
- Lucas Kruithof