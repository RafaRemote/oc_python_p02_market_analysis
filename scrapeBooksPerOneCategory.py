# Purpose of this script:
# 
# First: choose a product category of books on books.toscrape.com, then:
# the script scrapeBooksPerOneCategory.py will extract the product_page_url of each books of this category, then:
# it will associate this data with the ones exactracted by scrapeOneBook.py, then:
# it will write all the datas in one csv file: dataBooksPerCategory.csv
# dataBooksPerCategory.csv will appear in the same directory as scrapeBooksPerOneCategory.

import requests # to make the get request to the url
from bs4 import BeautifulSoup # to parse the html
import csv # to write the csv file
import re # for regex operations
from scrapeOneBook import find_datas

# delclaring all the variables needed
url = 'https://books.toscrape.com/catalogue/category/books/sequential-art_5/index.html'
urlbase = 'https://books.toscrape.com/catalogue/' 
url_list = list() # creating a list which will be populated with all the urls to parse
url_list.append(url)
url_cat_page_base = url[:-10] + 'page-'
for num_page in range(2,9):
    url_list.append(url_cat_page_base + str(num_page) + ".html")
product_url_list = list() # creating a list which will be populated with the product urls
# creating the csv that will be populated with datas
with open('dataBooksPerCategory.csv', 'a', newline='') as a_csv_csv:
    csv_writer = csv.writer(a_csv_csv)
    csv_writer.writerow(['product_page_url', 'universal_product_code(upc)', 'title', 'price_including_tax', 'price_excluding_tax', 'number_available', 'product_description', 'category', 'review_rating', 'image_url'])

# creating a function: will parse a url, create a list, and write a csv file.
def extract_product_url(a_url, a_list):
    response = requests.get(a_url)
    if response.ok:
        soup = BeautifulSoup(response.text, 'lxml')
        a_tag = soup.findAll('a') 
        for i in a_tag: 
            a_href = i['href']  
            searchingFor = "^../../../"   
            notsearchingFor = "^../../../../"
            if ((re.match(searchingFor, i['href'])) and not (re.match(notsearchingFor, i['href'])) and not ((urlbase + i['href'][9:]) in a_list)):
                product_url = urlbase + i['href'][9:]
                a_list.append(product_url)
                find_datas(product_url, "dataBooksPerCategory.csv")
    else:
        print('unable to get the url :', a_url, response)

# calling the function
for i in url_list:
    extract_product_url(i, product_url_list)