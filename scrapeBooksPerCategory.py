import requests
from bs4 import BeautifulSoup
import csv
import re

urlbase = 'https://books.toscrape.com/'

response = requests.get(urlbase)

print(response)

if response.ok:
    categories = []
    soup        = BeautifulSoup(response.text, 'lxml')
    listOfCat   = soup.findAll('a')
    searchingforCategory = 'category'
    searchingForWordBooks = 'books'

    for i in listOfCat:
        if (re.search(searchingforCategory, str(i))) and (re.search(searchingForWordBooks, str(i))):
            categories.append(i.text.strip())
            print(i.text.strip())
            print(categories)
else:
    print('not able to get this url')


