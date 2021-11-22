# Project
## Objectives
-   Give advice whether to buy or sell or hold different stocks/crypto based on indicators.
-   It doesn’t make trades for the user. The software does not guarantee profit.
## Requirements
### Must Haves
-   Retrieve historical (including current/live) prices (from web)
-   Give advice on (5) single indicators based on historical prices whether to buy or sell certain stocks/crypto. E.g., moving averages, oscillators & momentum. Compare these results to (a) value(s). 
-   Give advice for different intervals of the data (1 minute/ day/ week/ month)
-   Combine advice of indicators into a single advice
    ___
-   Retrieve financial data
-   Give advice on (5) single indicators based on financial data (/company info) whether to buy or sell certain stocks. E.g., earnings-per-share, debt-to-equity, price-to-earnings. Compare these results to (a) value(s).
-   Combine advice of indicators into a single advice
    ___
-   Give overview of all user selected stocks/crypto
### Should Haves
-   Retrieve & show analysts’ consensus (buy/sell)
    ___
-   Aggregate advices of all sections into a single advice
-   Add (5 for hist. price & 5 for financial data) indicators
-   Compare indicators with some market index (for stocks) or Bitcoin (or similar market index for crypto if it exists)
    ___
-   Ability to sort the stocks/crypto on a certain value
### Could Haves
-   Show the recent news (url) for the stock/crypto
    ___
-   Give advice by comparing financial data indicators (mentioned in MH) with other companies in a similar market (/industry/sector) in some market index
-   Find best performer in market and give advice
    ___
-   Select two stocks or two crypto to compare
### Won’t Haves
-   Make trades for the user
-   Do ‘advanced’ data analysis (regression, machine learning)
## Constraints
-   Completely dependent on yahoo finance working
-   Market needs to be open
-   Dependent on scraper library working
-   Computer needs internet to scrape
-   Our capabilities
## Expected Results
-   Must haves are expected to be completed
-   Won’t haves are not expected to be completed, but may be started if time permits
-   Indicators are expected to be correctly computed resulting correct advices on average
-   The application is expected to have a user-friendly GUI
# Design
## Front-end (GUI)
### Input
-   Input box
	-   text input
	-   add button
	-   delete button
-   Current stocks/crypto as a table
	-   delete buttons (if possible)
-   Choose indicators
-   Calculate button
### Overview
-   Interval choice (of historical prices)
-   Dropdown menu for choosing sorting method
-   Left-Right panes: Stock-Crypto
-   Overview: Symbol/Ticker; Name; Price; Advice
-   Mode menu: Individual stock, Comparison of 2, Market best
-   Calculate button
### Individual stock/crypto
-   Indicators
-   Key financial data
-   News
-   Analysts’ recommendation
### Comparison
-   Left-Right: Individual stock/crypto Indicators
-   Mark the better one for each indicator
### Market/Industry best
- Overview for market
## Back-end (Functionality)
### Input
-   csv file with tickers/abbreviation
-   read file
-   write file
-   add stock/crypto with ticker
-   remove stock/crypto
-   pass through indicator choices (multichoice)
### Overview
-   Get all advices
-   Sort
-   Compare
-   Market overview
### Individual stock/crypto
-   Get indicator scores/advices
-   Get key financial data
-   Get news
-   Get analysts’ recommendation
### Indicator (abstract/super class)
-   Calculate score (numerical value)
-   Get advice (category, (strong) buy/sell/neutral
-   Subclasses:
	-   Moving averages
	-   Stochastic
	-   Bollinger bands
### Comparison
-   _Individual stock/crypto_ \[x2\] (superclass)
-   Compare indicators
### Market/Industry best
-   _Overview_ (superclass)
-   Get all stocks (in market index if provided) provided by user
-   Filter market/industry firms
# Planning
-   We will use scrum/sprints to get things done every week
-   Preferences of:
	-   Jelle: Historical price Indicators
	-   Fabian: GUI
	-   Betsie: Indicators
# Testing
-   GUI testing will be done manually, automated if time permits
-   Functionality (back-end) will be tested automatically (>80%)
-   Mocking will be implemented to decrease test dependency on 3rd party library (except pandas
-   Most tests are written before merging