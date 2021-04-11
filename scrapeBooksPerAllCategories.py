# Purpose of this script:
# 
# Scrape all the categories on books.toscrape.com
# write a csv file with the datas of each book of each category. One file per category.
# datasAllCategory with all the csv files will appear in the folder 'scraped_datas'.

import requests # to make the get request to the url
from bs4 import BeautifulSoup # to parse the html
import re # for regex operations
import csv # to create the csv files
import scrapeFunctions

# declaring all the variables needed
url = 'https://books.toscrape.com/'

# list with the name of the categories
categories_list = list()

# creating the list with all the different categories
response = requests.get(url)
soup = BeautifulSoup(response.text, 'lxml')
a_tags = soup.findAll('a')
for i in a_tags:
    if (re.search('.*books', str(i))):
        element_to_append = (re.split('">.*', str(i))[0])
        element_to_append_clean = (re.split('^<a href="', element_to_append)[1])
        url_to_append = url + element_to_append_clean
        categories_list.append(url_to_append)

print("----------There is a total of: ", len(categories_list)-1, " categories to parse.----------")
length_left = len(categories_list)-1
for i in range(1, len(categories_list), 1):
    scrapeFunctions.find_all_books_per_category(categories_list[i], len(categories_list)-1)
    length_left -= 1
    print("----------there is: ", length_left, " categories left to parse.----------")






      



        


