import requests
import re
from bs4 import BeautifulSoup
import os.path
import csv
import sys
import itertools

chooser = (sys.argv[1])
funArgChoice = (sys.argv[2])
folderChoice = (sys.argv[3])
csvChoice = (sys.argv[4])
imageChoice = (sys.argv[5])

urlbase = "https://books.toscrape.com/"
urlbasecat = urlbase + "catalogue/category/books/"

category_list = list()
response_homepage = requests.get(urlbase)
if response_homepage.ok:
    soup = BeautifulSoup(response_homepage.text, 'lxml')
    categories = soup.findAll("a")
    for i in categories:
        if (str(i).count("books") > 0):
            category_list.append(str(i).split()[2:-1])
del category_list[0]
categories_list = []
for i in category_list:
    if (len(i) == 1):
        categories_list.append(i[0].lower())
    elif (len(i) == 2):
        categories_list.append((i[0] + '-' + i[1]).lower())
    else:
        categories_list.append((i[0] + '-' + i [1] + '-' + i[2]).lower())
categories_list_full = []
i = 2
for j in categories_list:
    categories_list_full.append(j + '_' + str(i))
    i += 1

categoriesIndex = list()
response = requests.get(urlbase)
if response.ok:
    soup = BeautifulSoup(response.text, 'lxml')
    a_tags = soup.findAll('a')
    for i in a_tags:
        if (re.search('.*books', str(i))):
            element_to_append = (re.split('">.*', str(i))[0])
            element_to_append_clean = (re.split('^<a href="', element_to_append)[1])
            url_to_append = urlbase + element_to_append_clean
            categoriesIndex.append(url_to_append)

def chooser(choice, funArgChoice, folderChoice, csvChoice, imageChoice):
    myCsvWriter(folderChoice, csvChoice)
    argList = list()
    argList.append(choice)
    for i in argList:
        if (i == "book"):
            oneBook(funArgChoice, folderChoice, csvChoice, imageChoice)
        elif (i == "category"):
            oneCategory(funArgChoice, folderChoice, csvChoice, imageChoice)
        elif (i == "everything"):
            allCategories(funArgChoice, folderChoice, csvChoice, imageChoice)
        else:
            print("choices available are: book, category or all")

def myCsvWriter(folderChoice, csvChoice):
    while not os.path.isdir(folderChoice):
                try:
                    os.makedirs(folderChoice)
                except:
                    print("there was a problem with the path ", folderChoice)
                    break
    with open(folderChoice + '/' + csvChoice + '.csv' , 'w', newline='') as pathCsv:
                csv_writer = csv.writer(pathCsv)
                csv_writer.writerow(['product_page_url', 'universal_product_code(upc)', 'title', 'price_including_tax', 'price_excluding_tax', 'number_available', 'product_description', 'category', 'review_rating', 'image_url'])
    

def oneBook(funArgChoice, folderChoice, csvChoice, imageChoice):
    dataListOneBook = list()
    try:
        response_url = requests.get(funArgChoice) 
        if response_url.ok:
            nameOfBook = re.split('_[0-9].+$', funArgChoice[37:].capitalize())[0].replace(' ', '_').replace('-', '_')
            soup = BeautifulSoup(response_url.text, 'lxml')
            upc = soup.find('td').text
            title = soup.find('h1').text.replace(' ','_')
            price_including_tax = soup.findAll('td')[3].text[1:] 
            price_excluding_tax = soup.findAll('td')[2].text[1:] 
            number_available = str(re.findall('[0-9]+', soup.findAll('td')[5].text))[2:-2] 
            product_description = soup.findAll('p')[3].text 
            category = soup.findAll('a')[3].text  
            review_ratings = str(soup.find("p", {"class": "star-rating"}))
            raitings = {'One': 1, 'Two': 2, 'Three': 3, "Four": 4, "Five": 5}
            review_rating = None
            for rating in ['One', 'Two', 'Three', 'Four', 'Five']:
                if review_ratings.find(rating) != -1:
                    review_rating = raitings[rating]
            image_url = "" + soup.find("img")['src'][5:]
            with open(folderChoice + '/' + csvChoice + '.csv' , 'a', newline='') as f:
                csv_writer = csv.writer(f)
                csv_writer.writerow([funArgChoice, upc, title, price_including_tax, price_excluding_tax, number_available, product_description, category, review_rating, image_url ])        
            response_image = requests.get(urlbase + image_url)
            response_image = requests.get(urlbase + image_url)
            if response_image.ok and imageChoice == "yes":
                with open(folderChoice + '/Cover_of_' + title.capitalize() + ".jpg", "wb") as f:
                    f.write(response_image.content)
    except requests.exceptions.MissingSchema:
        print('it is not a valid url')
            
def oneCategory(funArgChoice, folderChoice, csvChoice, imageChoice):
    if funArgChoice not in categories_list:
        print("it is not a listed category. Type the exact name of the category, all characters must be lowercase. Replace spaces by dashes '-' ")
        exit()
    else:
        for i in categories_list_full:
            if i.split('_')[0] == funArgChoice:
                caturl = i
                break
    out_csv = folderChoice + '/' + csvChoice +'.csv'
    while not os.path.isdir(folderChoice):
        try:
            os.makedirs(folderChoice)
        except:
            print("there was a problem with the path ", folderChoice)
            break
    url_list = list() 
    url_list.append(urlbasecat + caturl + '/index.html')
    url_cat_page_base = urlbasecat + caturl + '/page-'
    for num_page in itertools.count(start=2):
        url_page_to_parse = url_cat_page_base + str(num_page) + ".html"
        if requests.get(url_page_to_parse).ok:
            url_list.append(url_page_to_parse)
        else:
            break
    product_url_list = list() 
    for i in url_list:
        response = requests.get(i)
        if response.ok:
            soup = BeautifulSoup(response.text, 'lxml')
            a_tag = soup.findAll('a')
            for i in a_tag: 
                a_href = i['href']
                if (str(i).count('../')== 3):
                    product_url = urlbase+ 'catalogue/' + i['href'][9:]
                    product_url_list.append(product_url)
    currentDone = 0
    for i in product_url_list:
        counterTotal = len(product_url_list)
        oneBook(i, folderChoice, csvChoice, imageChoice)
        currentDone += 1
        print("parsing page ", currentDone, "on ", counterTotal)


def allCategories(funArgChoice, folderChoice, csvChoice, imageChoice):
    counter = len(categories_list)
    print("----there is ", counter ," categories to parse.----")
    for i in categories_list:
        oneCategory(i, folderChoice, csvChoice, imageChoice)
        counter -= 1
        print("----there is ", counter, " categories left to parse !----")

    




if __name__ == '__main__':
    chooser(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])