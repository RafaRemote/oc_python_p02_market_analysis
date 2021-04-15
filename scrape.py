import requests
import re
from bs4 import BeautifulSoup
import os.path
import csv
import sys
import itertools

chooser = (sys.argv[1])
funChoice = (sys.argv[2])
folderChoice = (sys.argv[3])
csvChoice = (sys.argv[4])

urlbase = "https://books.toscrape.com/"
urlbasecat = urlbase + "catalogue/category/books/"

category_list = []
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

def chooser(choice, funChoice, folderChoice, csvChoice):
    argList = list()
    argList.append(choice)
    for i in argList:
        if (i == "book"):
            oneBook(funChoice, folderChoice, csvChoice)
        elif (i == "category"):
            oneCategory(funChoice, folderChoice, csvChoice)
        elif (i == "all"):
            allCategories(funChoice, folderChoice, csvChoice)
        else:
            print("choices available are: book, category or all")

def oneBook(url, destin_dir_book, destin_csv_book):
    try:
        response_url = requests.get(url) 
        if response_url.ok:
            nameOfBook = re.split('_[0-9].+$', url[37:].capitalize())[0].replace(' ', '_').replace('-', '_')
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
            while not os.path.isdir(destin_dir_book):
                try:
                    os.makedirs(destin_dir_book)
                except:
                    print("there was a problem with the path ", destin_dir_book)
                    break
            with open(destin_dir_book + '/' + destin_csv_book + '.csv' , 'a', newline='') as f:
                csv_writer = csv.writer(f)
                csv_writer.writerow(['product_page_url', 'universal_product_code(upc)', 'title', 'price_including_tax', 'price_excluding_tax', 'number_available', 'product_description', 'category', 'review_rating', 'image_url'])
                csv_writer.writerow([url, upc, title, price_including_tax, price_excluding_tax, number_available, product_description, category, review_rating, image_url ])        
            response_image = requests.get(urlbase + image_url)
            if response_image.ok:
                with open(destin_dir_book + '/Cover_of_' + title.capitalize() + ".jpg", "wb") as f:
                    f.write(response_image.content)
    except requests.exceptions.MissingSchema:
        print('it is not a valid url')
            
def oneCategory(cat, destin_dir_category, destin_csv_category):
    if cat not in categories_list:
        print("it is not a listed category. Type the exact name of the category, all characters must be lowercase. Replace spaces by dashes '-' ")
        exit()
    else:
        for i in categories_list_full:
            if i.split('_')[0] == cat:
                caturl = i
                break
    out_csv = destin_dir_category + '/' + destin_csv_category +'.csv'
    while not os.path.isdir(destin_dir_category):
        try:
            os.makedirs(destin_dir_category)
        except:
            print("there was a problem with the path ", destin_dir_category)
            break
    with open(out_csv, 'w', newline='') as ccsv:
        csv_writer = csv.writer(ccsv)
        csv_writer.writerow(['product_page_url', 'universal_product_code(upc)', 'title', 'price_including_tax', 'price_excluding_tax', 'number_available', 'product_description', 'category', 'review_rating', 'image_url'])

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
    for i in product_url_list:
        print(i)


        #             print(product_url)
        #             print('saving image found @: ', product_url)
        #             saveImageUrl(product_url, destin_dir + '/' + category + '/' + 'Cover Images')
        #             a_list.append(product_url)
        #             out_csv = category + '/' + 'dataBooksPerCategory_' + category + '.csv'
        #             find_datas(product_url, out_csv, destin_dir)
        # else:
        #     print('unable to get the url :', a_url, response)

        






# def allCategories(every):
#     print(every)




if __name__ == '__main__':
    chooser(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])