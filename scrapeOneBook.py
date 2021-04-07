import requests
from bs4 import BeautifulSoup
import csv
import re

url = 'https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html'
urlbase = 'https://books.toscrape.com/'

response = requests.get(url)

print(response)

if response.ok:

    soup    = BeautifulSoup(response.text, 'lxml')
    upc     = soup.find('td').text
    title   = soup.find('h1').text
    price_including_tax = soup.findAll('td')[3].text[1:]
    price_excluding_tax = soup.findAll('td')[2].text[1:]
    number_available_string = soup.findAll('td')[5].text
    number_available = str(re.findall('[0-9]+', number_available_string))[2:4]
    product_description = soup.findAll('p')[3].text
    category = soup.findAll('a')[3].text
    review_ratings = soup.findAll('p')
    searchingfor = 'rating'
    for i in review_ratings:
        if(re.search(searchingfor, str(i))): 
            if ("star-rating One" in str(i)):
                review_rating = 1
            elif ("star-rating Two" in str(i)):
                review_rating = 2
            elif ("star-rating Three" in str(i)):
                review_rating = 3
            elif ("star-rating Four" in str(i)):
                review_rating = 4
            else:
                review_rating = 5
    image = soup.find("img")
    source = image['src']
    image_url = (urlbase + source[5:])
   
    with open('dataOneBook.csv', 'w', newline='') as dataOneBook_csv:
        csv_writer = csv.writer(dataOneBook_csv)
        csv_writer.writerow(['product_page_url', 'universal_product_code(upc)', 'title', 'price_including_tax', 'price_excluding_tax', 'number_available', 'product_description', 'category', 'review_rating', 'image_url'])
        csv_writer.writerow([url, upc, title, price_including_tax, price_excluding_tax, number_available, product_description, category, review_rating, image_url ])


else:
    print('not able to get this url')