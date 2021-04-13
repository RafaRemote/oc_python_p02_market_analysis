""" Purpose of this script:
---------------------------

- main project: Price Scraping
- target Website: books.toscrape.com
 
will extract the product_page_url of each book of a chosen category on the target website, then:
will associate this data with the ones extracted by scrapeOneBook.py, then:
will write all the datas in one csv file: 'dataBooksPerCategory_[Category].csv',
will store the folder: 'data per category/[category]',
will store the image found in the urls visited in the folder: 'data per category/[category]/Cover Images'.

Instructions:
-------------

choose a product category of books on books.toscrape.com, 
copy the url of the index page of the category,
attibute this url to the variable 'url', declared just after the importations on this file

open a terminal
check that you are in the folder 'python-web-scraping'
type: 'python3 scrapeBooksPerOneCategory.py'

dataBooksPerCategory_[Category].csv will appear in the folder 'data per category'.
'Cover of [name of the book].jpg' will appear in the folder 'data per category/[category]/Cover Images' .

"""

import scrapeFunctions # the main function of this script is located in scrapeFunctions.py
import re

# declaring the variable that will be the url to parse
url = 'https://books.toscrape.com/catalogue/category/books/travel_2/index.html'

category = re.split('_[0-9].+$', url[52:].capitalize())[0]
destination_dir = 'data per category'
scrapeFunctions.checkDir(destination_dir, category)

# calling the main function with the arguments needed. Second argument = amount of url to parse.
scrapeFunctions.find_all_books_per_category(url, destination_dir)