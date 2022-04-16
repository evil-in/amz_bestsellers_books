# Amazon bestsellers scraper for Books

### Objective: 
To scrape details such as book name, price, author, rating, number of reviews and rank. 
<p> This gets the top 100 bestsellers books from the main page and the top 100 from each genre page. </p>

### Method: 
* Make a request to each URL using selenium. 
* Scroll through the page - this needs to be done to get past the AJAX. 
* Once the entire page has loaded then grab the source code. 
* Parse the HTML through the LXML parser in BeautifulSoup. 
* Then identify the data points using CSS selectors and create a dataframe. 

### Dependencies:
* Google Chrome driver - download from the site according to browser settings. [(download here)](https://chromedriver.chromium.org/downloads)

**The python packages:**
- bs4 : BeautifulSoup package for converting HTML code into a soup object to gather data. 
- pandas : To store and manipulate data using dataframes. 
- time : To introduce wait functionality in the code while the page is loading.
- re : python regex package to check for patterns.
- selenium - To use chrome driver to make a request to the URL and capture the HTML source code. 

**Install package requirements via command line:**
> `pip install -r requirements.txt`


### Code: 
[**Python web scraper**](https://github.com/evil-in/amz_bestsellers_books/blob/main/amz_books_bestseller_scraper.py)

