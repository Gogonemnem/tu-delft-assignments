# Project Report

## Development plan
Objectives:

- Give advice whether to buy or sell or hold different stocks/crypto based on indicators.
- It doesn’t make trades for the user. The software does not guarantee profit.
    
Requirements:

### Must Haves:
- Retrieve historical (including current/live) prices (from web)a
- Give advice on single indicators based on historical prices whether to buy or sell certain stocks/crypto. E.g., moving averages, oscillators & momentum. Compare these results to (a) value(s). 
- Give overview of all user selected stocks/crypto
    
### Should Haves:
- Add financial data advice on indicators
- Retrieve & show analysts’ consensus (buy/sell)
- Combine advice of indicators into a single advice
- Give advice for different intervals of the data (1 minute/ day/ week/ month)
    
### Could Haves:
- Show the recent news (url) for the stock/crypto
- Ability to sort the stocks/crypto on a certain value
- Compare indicators with some market index (for stocks) or Bitcoin (or similar market index for crypto if it exists)
- Filter overview by market (/industry/sector)
- Select two stocks or two crypto to compare
    
### Won’t Haves:
- Make trades for the user
- Do ‘advanced’ data analysis (regression, machine learning)
    
### Constraints:
- Completely dependent on yahoo finance working
- Market needs to be open
- Dependent on scraper library working
- Computer needs internet to scrape
- Our capabilities
    
### Expected results:
- Must haves are expected to be completed
- Won’t haves are not expected to be completed, but may be started if time permits
- Indicators are expected to be correctly computed resulting correct advices on average
- The application is expected to have a user-friendly GUI


## Design plan, design document set, design validation document
Our program starts at the so-called Input tab. In this tab, the user is able to input the ticker of a stock / cryptocurrency of interest
into a search box, where the ticker gets added to a table with its corresponding name. When the ticker can't be found by yfinance, 
a pop-up message will appear with the message to input a valid ticker. When the user saves the list with selected 
stocks / cryptocurrencies by clicking on a save-button, the list will be written to a csv-file. 
To import this list in the future, the user can click on an import-button and the list of tickers will be added back 
to the table. When the user clicks on the delete-button, the selected tickers get deleted from the table and when 
no tickers were selected, a pop-up message will appear to make clear that no tickers were selected. 

To get an overview of the selected tickers in the list, the user gets redirected to the Overview tab, after having 
clicked on the 'Get overview' button in the Input tab. The Overview tab contains a table which consists of the tickers
and their names, price, sector and advice. In both tables, the user is able to see the tickers with their
name, price and the calculated advice to either hold, sell or buy this stock / cryptocurrency. Besides that, there is a
dropdown menu in which different time-intervals can be chosen. With the calculation methods written in the yfinancecrypto.py file, 
an advice will be produced based on the selected interval.
When the user wants to acquire more information about a certain stock / cryptocurrency, it is possible to indicate this 
in the same tab. By clicking on the "Get results" button after having set the stock / cryptocurrency of interest and the 
'Single' option, one will be redirected to the Individual tab. When one wants to compare two stocks or two cryptocurrencies 
with each other, the user will be redirected to the Comparison tab by clicking on the "Get results" button 
after having set the stocks / cryptocurrencies and clicked on the 'Comparison' button. 

The Individual tab contains the following: a table with the highest and lowest prices at certain dates and times of the ticker, 
a table with the indicators (historical and financial) with the advice and value of the indicator,
a table with advices from analysts, news articles related to the ticker, a graph of the price over a certain 
amount of time, a volume chart and a table which contains a fear indicator and an indicator containing the final advice. 

The comparison tab contains the sane features as the individual tab, but for two different tickers instead of just for one. 


## Implementation plan, version management plan

We divided the project into four main parts; input, overview, individual and comparison. By prioritizing each feature, 
we were able to make clear each week which features had to be done and by whom. 

For version management, we created branches in Gitlab. For each issue that had to be done, we created a subbranch
from the master branch. When issues were done, we merged the branches of these issues with the master branch.
This way everyone was able to work on their assigned issue, while maintaining a main branch with the latest working 
version. 

## Testing and validation plan
Our testing plan consisted of mainly manual testing, since most of the code was GUI based we made sure to manual test.
For most of our classes we made sure to check every option and track were the code moves.
Making sure it follows our initial plan for the most part and works as intended. For our calculation methods we made some unittests where it is possible.
Some methods and classes require active data to test so this will need to be manually tested as well.
## Test results, validation reports
As of the unittests we tested the CryptoCurrencies class to make sure the correct columns are being created, because this is the backbone of our calculations.
Signals could not be tested in the yfinancecrypto.py because these are based of active data and so the testing could not be predicted, without it being trivial.
By means of manual testing this could still be checked and worked out if working correctly.

As for the manual testing all different tabs were checked if all features worked as intended.
In the input tab the ticker box was tested if correct and wrong inputs were dealt with and if it would not crash if code were to be inserted.
All buttons in all tabs were tested for multi press inputs for overflows and crashes. The correct calculations and visualization for all parts were also looked at.

## Evaluation document
### Requirements
As to our requirements, we have met all of the features that we categorized as 'must have' in time. Because of this,
we were able to also implement most of the 'should have' features, such as the financial indicators, giving advice
for different intervals of the data and showing the consensus of analysts. We were even able to add a 'could have' 
feature, namely the ability to compare two stocks or two crypto currencies with each other. This way, our end product
contains about 70% of all the requirements that we set in the development plan. 

If the future permits it, we certainly would add some more features. For example, a feature where it is possible to see
the recent news concerning the stock or cryptocurrency. Besides that, we would also add a feature that makes it possible
to compare indicators with a certain market index for stocks, and, if it exists, something similar for cryptocurrencies. 

### Problems & Solutions
Like with all team projects, there were some small roadbumps that needed to be solved. There were already some creative differences at the very first meeting. As a group, we unanimously decided to delve deeper into the financial market. However, we needed some extra time to decide whether to focus on the slow-moving traditional market or on the volatile cryptocurrency market. Luckily, there was no need for compromises as Yahoo Finance is able to provide data for both of these markets.

The next problem occurred while envisioning the application. The goal is to provide a simple but relevant overview of the market of interest to the user, with the ability to find more extensive data on a particular ticker. Therefore, a simple console application would not completely suffice for the _complex structure_. PyQt6 was chosen to display the relevant information in a GUI. This module was new to most of the members, causing someone of the group having to initialize the module to be easy to use for the rest of the team. However, designing the layout for the application went well afterwards, although some of the PyQt6 documentation is hard to follow when to make complex custom designs.

Following the design plan, implementing all (/most of) the requirements went relatively straightforward. Due to the semiweekly meetings, where we also assigned tasks each time. Therefore, everyone was able to report their progress often, making it easy to spot when a problem popped up. These problems were then discussed during these meetings, and some were assigned to help the teammember. Due to the frequent meetings, everyone knew who was doing what, making it easy to approach a member outside meetings to ask for help. 

Lastly, the testing and bugfixing went completely as planned: there were some bugs that needed to be fixed. Some were more difficult than others, that mostly depended harmonizing the different modules with each other. Other bugs were more minor and were either solved relatively quickly, while others were bugs carried over from the modules.

### Teamwork
The overall teamwork went well, as already became a clear from the previous section. We assigned teammembers 
in such a way to tasks that people were getting the tasks done that had their preference. Since we had weekly meetings 
where we evaluated the progress, it was easy to address problems about the implementation if there were any. 
There was always a fellow teammember who wanted to help. 

As with every project, there are some things that we could have done better concerning the teamwork and which we
can learn from. For example, since we were quite quickly done with our must have requirements and had not decided yet 
how we wanted to implement the rest of the features, we did not use some of the time we had to start implementing
new features just before the mid-term presentation. That being said, this gave us enough time to wrap up what
we had until then and prepare for the presentation. 

### Guidance
During the course, we had ample opportunities to ask questions to our assigned TA during the meeting but also the other TAs present in the room. All our questions were answered within the same day. Furthermore, we are very thankful that our TA was frequently available on mattermost to answer our questions outside the allotted times. Lastly, the TA often provided us with useful constructive feedback on our project, including but not limited to improving user experience.
