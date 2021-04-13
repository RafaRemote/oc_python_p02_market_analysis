""" Purpose of this script:
---------------------------

- main project: Price Scraping
- target Website: books.toscrape.com

will extract the following 10 informations for a chosen product on the target website:

product_page_url
universal_ product_code (upc)
title
price_including_tax
price_excluding_tax
number_available
product_description
category
review_rating
image_url

will write a csv file (dataOneBook.csv) with all these datas above.
will store the image found in the url visited in the folder: 'scrapedImages'.

Instructions for this script:
----------------------------

choose a product page on books.toscrape.com, then:
replace the url variable defined below by the one of the product page you have chosen
open a terminal
check that you are in the folder 'python-web-scraping'
type: 'python3 scrapeOneBook.py'

dataOneBook_[name of the book].csv will appear in the folder 'scrapedOneBook'.
image_[image name].jpg will appear in the folder 'scrapedImages".

"""

import csv # to write the csv file
import re # for regex operations
import scrapeFunctions 

# the first paramater of the function find_datas()
url = 'https://books.toscrape.com/catalogue/the-lucifer-effect-understanding-how-good-people-turn-evil_758/index.html'
nameOfBook = re.split('_[0-9].+$', url[37:].capitalize())[0]
destination_dir = "scrapedOneBook/" + nameOfBook
scrapeFunctions.checkDir("scrapedOneBook", nameOfBook)
category = nameOfBook
# informing the user in the console
print("Data from the book ", nameOfBook, " is being written in a csv file, please wait...")

# creating the csv file with the name of the columns
with open('../' + destination_dir + '/dataOneBook_' + nameOfBook + '.csv', 'w', newline='') as a_csv_csv:
            csv_writer = csv.writer(a_csv_csv)
            csv_writer.writerow(['product_page_url', 'universal_product_code(upc)', 'title', 'price_including_tax', 'price_excluding_tax', 'number_available', 'product_description', 'category', 'review_rating', 'image_url'])

# calling the function with the two arguments needed
scrapeFunctions.find_datas(url, 'dataOneBook_' + nameOfBook + '.csv', destination_dir)

# informing the user in the console
print("The csv file created is available in the directory: 'scrapedOneBook'")

# script for the image extraction
scrapeFunctions.saveImageUrl(url, category)