# Amazon bestsellers scraper for Books

### Objective: 
To scrape details such as book name, price, author, rating, number of reviews and rank. 
<p> This gets the top 100 bestsellers books from the main page and the top 100 from each genre page. </p>

### Method: 
1. Make a request to each URL using selenium webdriver and grab the source code. 
2. Parse the HTML through the LXML parser in BeautifulSoup. 
3. Then identify the data points using CSS selectors and save the data as a dataframe. 

### Dependencies:
* Google Chrome driver - download from the site according to browser settings. [(download here)](https://chromedriver.chromium.org/downloads)

**The python packages:**
- bs4 : BeautifulSoup package for converting HTML code into a soup object to gather data. 
- pandas : To store and manipulate data using dataframes. 
- time : To introduce wait functionality in the code while the page is loading.
- re : python regex package to check for patterns.
- selenium - To use chrome driver to make a request to the URL and capture the HTML source code. 

**Install package requirements via command line:**
`pip install -r requirements.txt`


### Code: 
[**Python web scraper**](https://github.com/evil-in/amz_bestsellers_books/blob/main/amz_books_bestseller_scraper.py)

### Kaggle Dataset:
[Link to dataset published on kaggle](https://www.kaggle.com/datasets/preethievelyn/amazon-top-100-bestsellers-in-books)
[Link to EDA of the dataset published on Kaggle](https://www.kaggle.com/code/preethievelyn/eda-amazon-top-100-bestseller-books)

