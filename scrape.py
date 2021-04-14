import requests
import re
from bs4 import BeautifulSoup
import os.path
import csv
import sys
import itertools

destin_dir_book = "oneBook"
destin_dir_category = "oneCategory"
destin_dir_all_categories = "allCategories"

urlbase = "https://books.toscrape.com/"
urlbasecat = urlbase + "catalogue/category/books/"


url = (sys.argv[1])
cat = (sys.argv[2])
# every = (sys.argv[3])

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

def oneBook(url):
    if (url == 'pass'):
        return
    else:
        response_url = requests.get(url) 
        if response_url.ok:
            nameOfBook = re.split('_[0-9].+$', url[37:].capitalize())[0].replace(' ', '_').replace('-', '_')
            destin_dir = destin_dir_book + '/' + nameOfBook
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
            while not os.path.isdir(destin_dir):
                try:
                    os.makedirs(destin_dir)
                except:
                    print("there was a problem with the path ", path)
                    break
            with open(destin_dir + '/data_' + title + '.csv' , 'a', newline='') as f:
                csv_writer = csv.writer(f)
                csv_writer.writerow(['product_page_url', 'universal_product_code(upc)', 'title', 'price_including_tax', 'price_excluding_tax', 'number_available', 'product_description', 'category', 'review_rating', 'image_url'])
                csv_writer.writerow([url, upc, title, price_including_tax, price_excluding_tax, number_available, product_description, category, review_rating, image_url ])        
            response_image = requests.get(urlbase + image_url)
            if response_image.ok:
                with open(destin_dir + '/Cover_of_' + title.capitalize() + ".jpg", "wb") as f:
                    f.write(response_image.content)
            else:
                print('you need to provide a product url from books.toscrape.com')

def oneCategory(cat):
    for i in categories_list:
        print(i)
    if cat not in categories_list:
         print("it is not a listed category. Type the exact name of the category, all characters must be lowercase. Replace spaces by dashes '-' ")
         exit()
    else:
        for i in categories_list_full:
            if i.split('_')[0] == cat:
                caturl = i
                break
    out_csv = destin_dir_category + '/dataCategory_' + cat + '.csv'
    while not os.path.isdir(destin_dir_category):
        try:
            os.makedirs(destin_dir_category)
        except:
            print("there was a problem with the path ", path)
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

    # product_url_list = list() 

    # def extract_product_url(a_url, a_list):
    #     response = requests.get(a_url)
    #     if response.ok:
    #         soup = BeautifulSoup(response.text, 'lxml')
    #         a_tag = soup.findAll('a') 
    #         for i in a_tag: 
    #             a_href = i['href']
    #             if (i.count('../')== 3):
    #                 product_url = urlbase + i['href'][9:]
    #                 print('saving image found @: ', product_url)
    #                 saveImageUrl(product_url, destin_dir + '/' + category + '/' + 'Cover Images')
    #                 a_list.append(product_url)
    #                 out_csv = category + '/' + 'dataBooksPerCategory_' + category + '.csv'
    #                 find_datas(product_url, out_csv, destin_dir)
    #     else:
    #         print('unable to get the url :', a_url, response)

    # for i in url_list:
    #     print("parsing page: ", i, "please wait...")
    #     extract_product_url(i, product_url_list)
    #     print("looking if there is a next page to parse")
        






# def allCategories(every):
#     print(every)




if __name__ == '__main__':
    oneBook(sys.argv[1])
    oneCategory(sys.argv[2])
    # allCategories(sys.argv[3])