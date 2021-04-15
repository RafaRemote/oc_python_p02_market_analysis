import requests
import re
from bs4 import BeautifulSoup
import os.path
import csv
import sys
import itertools

# to be able to use variables from the command line
chooser = (sys.argv[1])
funArgChoice = (sys.argv[2])
folderChoice = (sys.argv[3])
csvChoice = (sys.argv[4])
imageChoice = (sys.argv[5])

# will be used to manage the organisation of the folders for the storing of images
skip = ""

# variable for the target website
urlbase = "https://books.toscrape.com/"
urlbasecat = urlbase + "catalogue/category/books/"

# creating the list of categories
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

# to be able to choose the function we want to use within the command line.
def chooser(choice, funArgChoice, folderChoice, csvChoice, imageChoice):
    myCsvWriter(folderChoice, csvChoice)
    argList = list()
    argList.append(choice)
    for i in argList:
        if (i == "book"):
            oneBook(funArgChoice, folderChoice, csvChoice, imageChoice, skip)
        elif (i == "category"):
            oneCategory(funArgChoice, folderChoice, csvChoice, imageChoice)
        elif (i == "everything"):
            allCategories(funArgChoice, folderChoice, csvChoice, imageChoice)
        else:
            print("choices available are: book, category or all")

# is writing a csv file within a folder of our choice, and a csv file of our choice
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
    
# function to scrape the data from one book.
def oneBook(funArgChoice, folderChoice, csvChoice, imageChoice, skip):
    try:
        response_url = requests.get(funArgChoice) 
        if response_url.ok:
            nameOfBook = re.split('_[0-9].+$', funArgChoice[37:].capitalize())[0].replace(' ', '_').replace('-', '_')
            soup = BeautifulSoup(response_url.text, 'lxml')
            upc = soup.find('td').text
            title = soup.find('h1').text.replace(' ','_').replace('/','-')
            price_including_tax = soup.findAll('td')[3].text[1:] 
            price_excluding_tax = soup.findAll('td')[2].text[1:] 
            number_available = str(re.findall('[0-9]+', soup.findAll('td')[5].text))[2:-2] 
            product_description = soup.findAll('p')[3].text.replace('\n','')
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
            imageDict = dict()
            imageRef = urlbase + image_url
            imageDict[title] = imageRef
            if (skip != 'skip'):
                imageSaver(folderChoice, imageDict, 'pass')
    except requests.exceptions.MissingSchema:
        print('it is not a valid url ', funArgChoice, requests.exceptions.MissingSchema)

# to scrape the data from one category
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
    for i in url_list:
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
    imageDict = dict()
    for i in product_url_list:
        name = i.split('/')[-2].split('_')[-2].capitalize()
        response = requests.get(i)
        if response.ok:
            soup = BeautifulSoup(response.text, 'lxml')
            image_url = urlbase + soup.find("img")['src'][5:]
            imageDict[name] = image_url
    imageSaver(funArgChoice, imageDict, funArgChoice)
    currentDone = 0
    for i in product_url_list:
        counterTotal = len(product_url_list)
        oneBook(i, folderChoice, csvChoice, imageChoice, 'skip')
        currentDone += 1
        print("parsing page ", currentDone, "on ", counterTotal)

# to scrape the data from all categories
def allCategories(funArgChoice, folderChoice, csvChoice, imageChoice):
    counter = len(categories_list)
    print("----there is ", counter ," categories to parse.----")
    print("----please wait----")
    for i in categories_list:
        oneCategory(i, folderChoice, csvChoice, imageChoice)
        counter -= 1
        print("----there is ", counter, " categories left to parse !----")

# to save the images
def imageSaver(folder, imageDict, category):
    if(category == 'pass'):
        for i, j in imageDict.items():
            response_image = requests.get(j)
            if response_image.ok and imageChoice == "yes":
                with open(folderChoice + '/Cover_of_' + i + '.jpg', 'wb') as f:
                    f.write(response_image.content)
    else:
        path = os.path.join(folderChoice, folder)
        while not os.path.isdir(path):
                try:
                    os.makedirs(path)
                except:
                    print("there was a problem with the path ", path)
                    break
        for i, j in imageDict.items():
            response_image = requests.get(j)
            if response_image.ok and imageChoice == "yes":
                print('saving image cover of ', i, ' in ', path)
                with open(path + '/Cover_of_' + i + '.jpg', 'wb') as f:
                    f.write(response_image.content)
        
# to be able to use the functions within the command line
if __name__ == '__main__':
    chooser(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])