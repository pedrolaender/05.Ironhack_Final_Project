<p align="center">
  <img src=""/>
</p>

# Final Project

  Project Completed.
## Abstract

  This is the final project of the Ironhack's Data Analytics Bootcamp - Oct/2022. The objective of this project is to compare the stock prices of companies that belong to perennial sector and those that do not in periods of crises, both in Brazil and United States.
## Introduction

  <img width="25%" src="https://github.com/pedrolaender/05.Ironhack_Final_Project/blob/main/Presentation/Barsi%20-%20rev1.png?raw=true">
  
  Luiz Barsi Filho is the biggest single investor in Brazil with a fortune estimated of R$ 4 billions. His strategy is to build a monthly income portfolio and is based in 4 main fundamentals:
  
  **<ins>Perennial Sectors:</ins>** Activity sectors essential for the survival of a country. Sectors in which demand is always growing or at least stable in periods of crisis.
  - Banks
  - Energy
  - Insurance
  - Sanitation
  - Telecommunications
  
  **<ins>Dividends:</ins>** Dividends are the portion of the company's profit that is distributed to shareholders, it is proportional to the number of shares.

  **<ins>Sustainability:</ins>** Companies wich activities are sustainable.

  **<ins>Good Projects:</ins>** Companies that presents good projects for the future.

### Business Question
  
  Knowing that, we wondered two things:
  - Do the stock prices of companies in perennial sectors behave differently from companies in other sectors in periods of crisis?
  - Is taking into account only the fact that they operate in perennial sectors of the economy a good filter for choosing stocks on the stock exchange?


### Technologies 

  - Python
  - MySQL
  - Power BI

### Methods

  - Filtering
  - Grouping
  - Visualization
  - Functional Programming
  - Web Scrapping
  - API

### Libraries

  - Pandas
  - BeautifulSoup
  - Selenium
  - Regex
  - Yfinance
  - Numpy
  - SQLAlchemy
  - Dotenv
  - Glob
  - Time

## Project Description

### Select the Companies

  The first thing to start building the dataset was to choose wich companies would be part of it. For Brazil we selected all companies listed on IBrA (Índice Brasil Amplo) and Ibovespa totalizing 201 companies. For USA we selected all companies in S&P500 (Standard & Poor's 500), Nasdaq 100 and Dow Jone Industrial Average totalizing 525 companies.

  The list of companies belonging to this indexes were gathered by Web Scrapping on B3 website, for brazilian index, and Wikipedia for americans.

  Having selected the companies that would be part of the analysis, the need for two different datasets was identified, one containing the characteristics of the companies and the other the historical series of stock prices

### Companies Characteristics Dataset

  Once the analysis proposed in this project rely on the company's activity sector, it is the most important characteristic to be gathered. To standardize the sectors, we got it from Yahoo Finance website by webscrapping, both for brazilian and american companies. By doing this we got the dataset as shown below.

<p align="center" width="100%">
<img width="100%" src="https://github.com/pedrolaender/05.Ironhack_Final_Project/blob/main/Presentation/01.%20features%20before.png?raw=true">
</p>

  Besides the sector, we found important to add some other features, so after checking the integrity of the already gathered data we add some other informations about the companies as if it is Perennial (yes/no), the Country, Type (company/index) and group the sectors to fit in the perennial sectors describe above, because it was to specific. After this cleaning and transforming we got a dataset as shown below.

<p align="center" width="100%">
<img  width="100%" src="https://github.com/pedrolaender/05.Ironhack_Final_Project/blob/main/Presentation/02.%20features%20after.png?raw=true">
</p>

### Company's Stock Price Historical Series Dataset

  The company's historical series were also gathered from Yahoo Finance, but through the API this time, once this ways makes getting the information easyer and saves a lot o processing time. The raw dataset after getting the data had some nulls and outlier as seen in the image below.

<p align="center" width="100%">
<img width="100%" src="https://github.com/pedrolaender/05.Ironhack_Final_Project/blob/main/Presentation/03%20historical%20before.png?raw=tru">
</p>

  After cleaning we ended with a dataset as shown below. It contains near to 5 millions entries.

<p align="center" width="100%">
<img width="75%" src="https://github.com/pedrolaender/05.Ironhack_Final_Project/blob/main/Presentation/04.%20historiacal%20after.png?raw=true">
</p>

### Uploading to SQL

  Having both datasets ready to work we uploaded it to SQL.

  <p align="center" width="100%">
 <img width="50%" src="https://github.com/pedrolaender/05.Ironhack_Final_Project/blob/main/Presentation/05.%20sql%20tables%20.PNG?raw=true">
  </p>

  <p align="center" width="100%">
 <img width="85%" src="https://github.com/pedrolaender/05.Ironhack_Final_Project/blob/main/Presentation/06.%20sql%20historical.PNG?raw=true">
  </p>

  <p align="center" width="100%">
 <img width="100%" src="https://github.com/pedrolaender/05.Ironhack_Final_Project/blob/main/Presentation/07.%20sql%20companies.PNG?raw=true">
  </p>
  
### Automating Historical Dataset Update

  Now that we have the main dataset, we have to make a way to uptade it automatically. For that we separeted the data gathering, cleaning, tranforming and appending steps in functions to be run automatically every day. The sequence of the process is decribed below:
  
<img align="right" width="55%" src="https://github.com/pedrolaender/05.Ironhack_Final_Project/blob/main/Presentation/08.%20functions.png?raw=true">

  - Link to database (SQL)
  - Search last update date
  - Search list of companies
  - Search for stock quotes on Yfinance
  - Process the data
  - Add to main database


## Visualization and Analysis

  In order to make the analysis we elaborate a Power BI Dashboard.

  The first page presents an exploratory analysis of the data in wich we can see that it is unbalanced with regard to the number of companies that belong to perennial sectors and thoose that do not. I was already as expected once we have only 5 sector considered perennial. Another thing importante to be considered is that the number of companies grow through the years.

<p align="center" width="100%">
<img width="100%" src="https://github.com/pedrolaender/05.Ironhack_Final_Project/blob/main/Presentation/09.%20exploratory%20analysis.PNG?raw=true">
</p>

  The next pages show a line graphic that contains a reference index and the behavior of the mean price of stocks of two sectors considered perennial and two that are not, both for Brazil and USA. The analysis were made considering two periods of time 2019-2022 and 2012-2022 as shown below.
  
  **Brazil 2019-2022**
<p align="center" width="100%">
<img width="100%" src="https://github.com/pedrolaender/05.Ironhack_Final_Project/blob/main/Presentation/10.%20brasil%202019.PNG?raw=true">
</p>

**Brazil 2012-2022**
<p align="center" width="100%">
<img width="100%" src="https://github.com/pedrolaender/05.Ironhack_Final_Project/blob/main/Presentation/11.%20brasil%202012.PNG?raw=true">
</p>

**USA 2019-2022**
<p align="center" width="100%">
<img width="100%" src="https://github.com/pedrolaender/05.Ironhack_Final_Project/blob/main/Presentation/12.%20eua%202019.PNG?raw=true">
</p>

**USA 2012-2022**
<p align="center" width="100%">
<img width="100%" src="https://github.com/pedrolaender/05.Ironhack_Final_Project/blob/main/Presentation/13.%20eua%202012.PNG?raw=true">
</p>

## Conclusion

  Analyzing the dashboard, we were able to begin to answer the questions that guided this project:

  ***Do the stock prices of companies in perennial sectors behave differently from companies in other sectors in periods of crisis?***

  **Answer:** No, the main hypoteses that perennial sector company's stock price behave diferently than non-perennial in period of crisis is discarded. Regarding to the price, all sectors analysed follow the same pattern, they acompany the main indexes of the country. The difference we could observe is the scale in wich this variations happens. The non-perennial sectors have a bigger variation.

  ***Is taking into account only the fact that they operate in perennial sectors of the economy a good filter for choosing stocks on the stock exchange?***

  **Answer:** It is a good start once the volatility of perennial sectors is lower than other sectors, but can't be the only thing taken into account, once "Bad Companies" compensate the growing price of "Good Companies". So analysing the image below we can see that a portifolio following Barsi's ideal (*light blue with Barsi label*) is the one having the best growing in the long term. 

  <p align="center" width="100%">
<img width="100%" src="https://github.com/pedrolaender/05.Ironhack_Final_Project/blob/main/Presentation/11.%20brasil%202012.PNG?raw=true">
</p>

  
## Contact

  Pedro Laender
  
  Github - (https://github.com/pedrolaender)