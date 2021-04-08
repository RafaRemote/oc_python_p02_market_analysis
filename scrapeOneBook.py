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
# dataOneBook.csv will appear in th same folder as scrapeOneBook.py is.


import requests # to make the get request to the url
from bs4 import BeautifulSoup # to parse the html
import csv # to write the csv file
import re # for regex operations

# declaration of variables: url is the url that will be parsed
url         = 'https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html'
urlbase     = 'https://books.toscrape.com/'

# function to find the review_rating
def find_rating(string_to_parse):
    raitings = {'One': 1, 'Two': 2, 'Three': 3, "Four": 4, "Five": 5}
    review_rating = None
    for rating in ['One', 'Two', 'Three', 'Four', 'Five']:
        if string_to_parse.find(rating) != -1:
            review_rating = rating
            return review_rating

# requesting
response = requests.get(url)
print(response)

if response.ok:
    # to parse the html
    soup    = BeautifulSoup(response.text, 'lxml')
    # find universal_ product_code
    upc     = soup.find('td').text
    # find title
    title   = soup.find('h1').text
    # find price incl tax, with the £ sign
    price_including_tax = soup.findAll('td')[3].text[1:]
    # find price excl tax, with the £ sign
    price_excluding_tax = soup.findAll('td')[2].text[1:]
    # find the number_available
    number_available_string = soup.findAll('td')[5].text
    number_available = str(re.findall('[0-9]+', number_available_string))[2:4]
    # find the description
    product_description = soup.findAll('p')[3].text
    # find the category
    category = soup.findAll('a')[3].text  
    # find the review_rating using the function defined above 
    rating_to_find = str(soup.find("p", {"class": "star-rating"}))
    review_rating = find_rating(rating_to_find)
    # find the image_url
    image = soup.find("img")
    source = image['src']
    image_url = (urlbase + source[5:])
   
   # write the csv file dataOneBook.csv
    with open('dataOneBook.csv', 'w', newline='') as dataOneBook_csv:
        csv_writer = csv.writer(dataOneBook_csv)
        csv_writer.writerow(['product_page_url', 'universal_product_code(upc)', 'title', 'price_including_tax', 'price_excluding_tax', 'number_available', 'product_description', 'category', 'review_rating', 'image_url'])
        csv_writer.writerow([url, upc, title, price_including_tax, price_excluding_tax, number_available, product_description, category, review_rating, image_url ])

else:
    print('not able to get this url')