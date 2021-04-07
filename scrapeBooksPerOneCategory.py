import requests
from bs4 import BeautifulSoup
import csv
import re


url = 'https://books.toscrape.com/catalogue/category/books/sequential-art_5/index.html'
urlbase = 'https://books.toscrape.com/catalogue/'
url_list = list()
response = requests.get(url)

print(response)

if response.ok:
    soup        = BeautifulSoup(response.text, 'lxml')
    a_tag       = soup.findAll('a')
    for i in a_tag:
        a_href      = i['href']
        searchingFor = "^../../../"
        notsearchingFor = "^../../../../"
        if (re.findall(searchingFor, i['href'])):
            if not (re.findall(notsearchingFor, i['href'])):
                if not (i['href'] in url_list):
                    url_list.append(urlbase + i['href'][9:])
                print(url_list,len(url_list))

    

    for j in range(2,9):
        url = "https://books.toscrape.com/catalogue/category/books/sequential-art_5/page-" + str(j) + ".html"
        if response.ok:
            soup        = BeautifulSoup(response.text, 'lxml')
            a_tag       = soup.findAll('a')
            for i in a_tag:
                a_href      = i['href']
                searchingFor = "^../../../"
                notsearchingFor = "^../../../../"
                if (re.findall(searchingFor, i['href'])):
                    if not (re.findall(notsearchingFor, i['href'])):
                        if not (i['href'] in url_list):
                            url_list.append(i['href'][9:])

        




else:
    print('not able to get this url')