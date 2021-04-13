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

will create a folder: [name of the book]
    inside this folder will write:
        a csv file 'Data of [name of the book].csv' with all these datas above.
        the image file 'Cover of [name of the book[.jpg' of the book 

Instructions for this script:
----------------------------

choose a product page on books.toscrape.com, then:
replace the url variable defined below by the one of the product page you have chosen
open a terminal
check that you are in the folder 'python-web-scraping'
type: 'python3 scrapeOneBook.py'

'Data of [name of the book].csv' will appear in the folder [name of the book]
'Cover of [name of the book[.jpg' will appear in the folder [name of the book]

"""

import csv # to write the csv file
import re # for regex operations
import scrapeFunctions 

url = 'https://books.toscrape.com/catalogue/lab-girl_595/index.html'
nameOfBook = re.split('_[0-9].+$', url[37:].capitalize())[0]
destination_dir = "data per book/" + nameOfBook
scrapeFunctions.checkDir("data per book", nameOfBook) # checking if directory is existing, if not, does create it

# informing the user in the console
print("Data from the book ", nameOfBook, " is being written in a csv file, please wait...")

# creating the csv file with the name of the columns
with open('../' + destination_dir + '/Data of ' + nameOfBook + '.csv', 'w', newline='') as a_csv_csv:
            csv_writer = csv.writer(a_csv_csv)
            csv_writer.writerow(['product_page_url', 'universal_product_code(upc)', 'title', 'price_including_tax', 'price_excluding_tax', 'number_available', 'product_description', 'category', 'review_rating', 'image_url'])

# calling the function with the three arguments needed
scrapeFunctions.find_datas(url, 'Data of ' + nameOfBook + '.csv', destination_dir)

# informing the user in the console
print("The csv file created is available in the directory: 'scrapedOneBook'")

# calling script for the image extraction
scrapeFunctions.saveImageUrl(url, destination_dir)