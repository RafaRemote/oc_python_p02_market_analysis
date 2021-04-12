""" Purpose of this script:
---------------------------

- main project: Price Scraping
- target Website: books.toscrape.com
 
this script will extract the product_page_url of each book of a chosen category on the target website, then:
it will associate this data with the ones extracted by scrapeOneBook.py, then:
it will write all the datas in one csv file: 'dataBooksPerCategory_[Category].csv'.

Instructions:
-------------

choose a product category of books on books.toscrape.com, 
copy the url of the index page of the category,
attibute this url to the variable 'url', declared just after the importations on this file

open a terminal
check that you are in the folder 'python-web-scraping'
type: 'python3 scrapeBooksPerOneCategory.py'

dataBooksPerCategory_[Category].csv will appear in the folder 'scraped_datas'.
"""

import scrapeFunctions # the main function of this script is located in scrapeFunctions.py

# declaring the variable that will be the url to parse
url = 'https://books.toscrape.com/catalogue/category/books/sequential-art_5/index.html'

# calling the main function with the arguments needed. Second argument = amount of url to parse.
scrapeFunctions.find_all_books_per_category(url)