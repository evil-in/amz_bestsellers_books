from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import time
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def parser(url):
    """This function takes the URL sent and makes a request to the website to grab the HTML source code.
    This is done using selenium and chrome driver. It also scrolls through the webiste to load the page.
    It is then parsed to BeautifulSoup and returns a soupp object"""
    options = Options()
    options.headless = False  # hide GUI
    options.add_argument("start-maximized")  # ensure window is full-screen
    driver = webdriver.Chrome(options=options)
    driver.get(url) # makes a request to the URL using chrome driver.
    time.sleep(3) #waits for the page to load
    step = 0.9
    scroll = 8
    screen_size = driver.execute_script("return window.screen.height;")
    while scroll> 0:
        driver.execute_script("window.scrollTo(0,{screen_height}*{i});".format(screen_height = screen_size, i = step))
        step+= 0.9
        time.sleep(3)
        scroll -= 1
    html_text = driver.page_source #grabbing the source code
    driver.close()
    soup = BeautifulSoup(html_text,'lxml') # parsing the HTML code through the LXML parser.
    print(f'Scraping: {soup.title.text}')
    return soup

def features(soup, genre):
    """ This function takes the soup object and extracts out the features.
    It returns a dataframe.  """
    name_list = []
    author_list = []
    link_list = []
    price_list = []
    rating_list = []
    review_list = []
    rank_list = []
    genre_list = []
    # finding the soup elements using CSS elements
    for s in soup.findAll("div", attrs = {'id':'gridItemRoot' , 'class': 'a-column a-span12 a-text-center _p13n-zg-list-grid-desktop_style_grid-column__2hIsc'}):
        name = s.find("div", attrs= {"class":"_p13n-zg-list-grid-desktop_truncationStyles_p13n-sc-css-line-clamp-1__1Fn1y"})
        author = s.find("div", attrs = {"class": "a-row a-size-small"})
        link = s.find("a", attrs= {"class":"a-link-normal", "role": "link", "tabindex":"-1"})
        price = s.find("span", attrs = {"class":"_p13n-zg-list-grid-desktop_price_p13n-sc-price__3mJ9Z"})
        rating = s.find("span", attrs = {"class": "a-icon-alt"})
        review = s.find("span", attrs = {"class":"a-size-small"})
        rank = s.find("span", attrs = {"class": "zg-bdg-text"})

        if name is not None:
            name_list.append(name.get_text())
        else:
            name_list.append("NA")

        if author is not None:
            author_list.append(author.get_text())
        else:
            author_list.append("NA")

        if link is not None:
            link_list.append('https://amazon.in' + link.get('href'))
        else:
            link_list.append("NA")

        if price is not None:
            price_list.append(price.get_text().replace('₹', ''))
        else:
            price_list.append("NA")

        if rating is not None:
            rating_list.append(rating.get_text()[:3])
        else:
            rating_list.append("NA")

        if review is not None:
            x = re.findall("[0-9]", review.get_text()) # using regex to check only for numbers
            if x:
                review_list.append(review.get_text())
            else:
                review_list.append("NA")
        else:
            review_list.append("NA")

        if rank is not None:
            rank_list.append(rank.get_text().replace('#', ''))
        else:
            rank_list.append("NA")


    all_products = {'Ranks': rank_list,
                    'Product': name_list,
                    'Author': author_list,
                    'Links': link_list,
                    'Price': price_list,
                    'Rating': rating_list,
                    'Reviews': review_list,
                   }

    df_products = pd.DataFrame(data = all_products)
    df_products['Genre'] = genre
    return df_products

def genre_features(soup):
    """ This function grabs the Genre name and link from the main bestsellers page.
    It returns a dataframe with the genre and links. """
    genre_list = []
    main_links_list  = []
    # selects the genre and href using CSS elements
    for i in soup.findAll("div", attrs = {"role": "treeitem", "class": "_p13n-zg-nav-tree-all_style_zg-browse-item__1rdKf _p13n-zg-nav-tree-all_style_zg-browse-height-large__1z5B8"}):
        genre = i.find("a")
        main_links = i.find("a")
        if genre is not None:
            genre_list.append(genre.get_text())
        else:
            genre_list.append("NA")

        if main_links is not None:
            main_links_list.append('https://amazon.in' + main_links.get('href'))
        else:
            main_links_list.append("NA")

    all_links = {'Genre': genre_list,
                'Page1': main_links_list}

    df_link = pd.DataFrame(all_links)
    df_links_sub = df_link.iloc[1:]
    df_links = df_links_sub.copy()
    df_links['Page2'] = df_links.Page1.str.replace('_nav_books_1', '_pg_2?ie=UTF8&pg=2') # creating a column with the page 2 links (follows a pattern)

    return df_links

def main():
    """ This function controls the execution of the code. The steps involved are:
    1. Scraping the main bestsellers page of amazon books, using the parser(url) function.
    2. Parsing the HTML code to get the data points, using the features(soup_object, genre) function
    3. Getting the genre and the links of the sub-division of bestseller pages, using the genre_features(soup_object) function
    4. Scraping each link for the data, using parser(url) and features(soup_object, genre) """

    url1 = 'https://www.amazon.in/gp/bestsellers/books/ref=zg_bs_nav_0'
    url2 = 'https://www.amazon.in/gp/bestsellers/books/ref=zg_bs_pg_2?ie=UTF8&pg=2'
    s1 = parser(url1)
    s2 = parser(url2)
    df1 = features(s1, "All")
    df2 = features(s2, "All")
    df_final = df1.append(df2)

    genre_links_df = genre_features(s1)
    links1 = genre_links_df.Page1.tolist()
    links2 = genre_links_df.Page2.tolist()
    genre = genre_links_df.Genre.tolist()

    # looping through the different genres
    for row in range(0, len(genre)):
        s1 = parser(links1[row])
        s2 = parser(links2[row])
        df1 = features(s1, genre[row])
        df_final = df_final.append(df1)
        df2 = features(s2, genre[row])
        df_final = df_final.append(df2)

    df_final = df_final[['Genre','Ranks', 'Product', 'Author', 'Links', 'Price', 'Rating','Reviews']]
    df_final.to_csv('Amazon_Bestseller_books.csv', index = False)

if __name__ == '__main__':
    main()
