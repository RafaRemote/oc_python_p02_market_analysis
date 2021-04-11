# Purpose of this script:
# 
# First: choose a product category of books on books.toscrape.com, then:
# the script scrapeBooksPerOneCategory.py will extract the product_page_url of each books of this category, then:
# it will associate this data with the ones exactracted by scrapeOneBook.py, then:
# it will write all the datas in one csv file: dataBooksPerCategory.csv
# dataBooksPerCategory.csv will appear in the folder 'scraped_datas'.

import requests # to make the get request to the url
from bs4 import BeautifulSoup # to parse the html
import csv # to write the csv file
import re # for regex operations
import itertools # for the iteration to infinity
from scrapeFunctions import find_datas

# declaring all the variables needed
url = 'https://books.toscrape.com/catalogue/category/books/sequential-art_5/index.html'

