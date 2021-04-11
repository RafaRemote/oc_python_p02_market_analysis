# Purpose of this script:
# 
# First: choose a product page on books.toscrape.com, then:
# 
# replace the url variable defined below by the one of the product page you have chosen
# 
# launch the script: python3 scrapeOneBook.py
# 
# the script will extract the following 10 informations:
# 
# product_page_url
# universal_ product_code (upc)
# title
# price_including_tax
# price_excluding_tax
# number_available
# product_description
# category
# review_rating
# image_url
# 
# Then:
# the script will write a csv file (dataOneBook.csv) with all these datas above.
# dataOneBook_[name of the book].csv will appear in the folder 'scraped_datas'.

import csv # to write the csv file
import re # for regex operations
from scrapeFunctions import find_datas

# declaration of variables: url is the url that will be parsed
url = 'https://books.toscrape.com/catalogue/twenty-yawns_773/index.html'
nameOfBook = re.split('_[0-9].+$', url[37:].capitalize())[0]

#informing the user in the console
print("Data from the book ", nameOfBook, " is being written in a csv file, please wait...")

# creating the csv file with the name of the columns
with open('../scraped_datas/dataOneBook_' + nameOfBook + '.csv', 'w', newline='') as a_csv_csv:
            csv_writer = csv.writer(a_csv_csv)
            csv_writer.writerow(['product_page_url', 'universal_product_code(upc)', 'title', 'price_including_tax', 'price_excluding_tax', 'number_available', 'product_description', 'category', 'review_rating', 'image_url'])

# calling the function, informing the user in the console
find_datas(url, 'dataOneBook_' + nameOfBook + '.csv')
print("The csv file created is available in the directory: 'scraped_datas'")