# Purpose of this script:
#
# - main project: Price Scraping
# - target Website: books.toscrape.com
#  
# this script will extract the product_page_url of each book of a chosen category on the target website, then:
# it will associate this data with the ones extracted by scrapeOneBook.py, then:
# it will write all the datas in one csv file: 'dataBooksPerCategory.csv'.
#
# Instructions for this script
#
# choose a product category of books on books.toscrape.com, 
# copy the url of the index page of the category,
# attibute this url to the variable 'url', declared just after the importations on this file
# 
# open a terminal
# check that you are in the folder 'python-web-scraping'
# type: 'python3 scrapeBooksPerOneCategory.py'
#
# dataBooksPerCategory.csv will appear in the folder 'scraped_datas'.

import requests # to make the get request to the url
from bs4 import BeautifulSoup # to parse the html
import csv # to write the csv file
import re # for regex operations
import itertools # for the iteration to infinity
from scrapeFunctions import find_datas # the main function of this script is located in scrapeFunctions.py

# declaring all the variables needed
url = 'https://books.toscrape.com/catalogue/category/books/sequential-art_5/index.html'

# calling the main function
scrapeFunctions.find_all_books_per_category(url)

