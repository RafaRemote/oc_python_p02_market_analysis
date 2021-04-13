# all the main functions are grouped in this file

import requests # to make the get request to the url
from bs4 import BeautifulSoup # to parse the html
import csv # to write the csv file
import re # for regex operations
import itertools # for the iteration to infinity
import os.path # to create a directory if no exsiting
import urllib

urlbase = 'https://books.toscrape.com/'
          
# check if a directory exists or not, creating it when needed


def checkOneDir(directory):
    parent_directory = "../"
    path = os.path.join(parent_directory, directory)
    while not os.path.isdir(path):
        try:
            os.mkdir(path)
        except:
            break
            

def checkDir(directory, category):
    parent_directory = "../"
    checkOneDir(directory)
    path = os.path.join(parent_directory, directory, category)
    print("path checked", path)
    while not os.path.isdir(path):
        try:
            os.mkdir(path)
        except:
            break

# function to find the review_rating: will be used by find_datas()
def find_rating(string_to_parse):
    raitings = {'One': 1, 'Two': 2, 'Three': 3, "Four": 4, "Five": 5}
    review_rating = None
    for rating in ['One', 'Two', 'Three', 'Four', 'Five']:
        if string_to_parse.find(rating) != -1:
            review_rating = raitings[rating]
            return review_rating

def find_datas(url_to_parse, a_csv, destination_dir):
    response = requests.get(url_to_parse) # requesting
    if response.ok:
        soup = BeautifulSoup(response.text, 'lxml') # to parse the html
        upc = soup.find('td').text # find universal_ product_code
        title = soup.find('h1').text # find title
        price_including_tax = soup.findAll('td')[3].text[1:] # find price incl tax, with the £ sign
        price_excluding_tax = soup.findAll('td')[2].text[1:] # find price excl tax, with the £ sign
        number_available = str(re.findall('[0-9]+', soup.findAll('td')[5].text))[2:-2] # find the number_available
        product_description = soup.findAll('p')[3].text # find the description
        category = soup.findAll('a')[3].text  # find the category
        review_rating = find_rating(str(soup.find("p", {"class": "star-rating"})))  # find the review_rating using the function defined above 
        image_url = urlbase + soup.find("img")['src'][5:] # find the image_url
        with open("../" + destination_dir + "/" + a_csv, 'a', newline='') as a_csv_csv:
            csv_writer = csv.writer(a_csv_csv)
            csv_writer.writerow([url_to_parse, upc, title, price_including_tax, price_excluding_tax, number_available, product_description, category, review_rating, image_url ])
    else:
        print('not able to get this url')

def find_all_books_per_category(url, destin_dir):

    print('destin_dir', destin_dir)

    urlbase = 'https://books.toscrape.com/catalogue/'

    # name of the category
    category = re.split('_[0-9].+$', url[52:].capitalize())[0]

    # writing data in the destination dir
    out_csv ='../'+ destin_dir + '/' + category + '/dataBooksPerCategory_' + category + '.csv'
    print('out_csv', out_csv)
    checkDir(destin_dir, category)
    with open(out_csv, 'w', newline='') as a_csv_csv:
        csv_writer = csv.writer(a_csv_csv)
        csv_writer.writerow(['product_page_url', 'universal_product_code(upc)', 'title', 'price_including_tax', 'price_excluding_tax', 'number_available', 'product_description', 'category', 'review_rating', 'image_url'])

    # informing the user in the console
    print("creating the csv files containing all the book datas for the category: ", category)
    print("please wait...")

    # creating a list which will be populated with all the url of pages to parse
    url_list = list() 
    url_list.append(url)
    url_cat_page_base = url[:-10] + 'page-'
    for num_page in itertools.count(start=2):
        url_page_to_parse = url_cat_page_base + str(num_page) + ".html"
        if requests.get(url_page_to_parse).ok:
            url_list.append(url_page_to_parse)
        else:
            break

    # creating a list which will be populated with the product urls    
    product_url_list = list() 

    # creating a function: will parse a url, create a list, and write a csv file.
    # each time a product page is visited: saveImagUr() will store the image of the book in the folder scrapedImages
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
                    print('saving image found @: ', product_url)
                    saveImageUrl(product_url, category)
                    a_list.append(product_url)
                    out_csv = category + '/' + 'dataBooksPerCategory_' + category + '.csv'
                    find_datas(product_url, out_csv, destin_dir)
        else:
            print('unable to get the url :', a_url, response)
    
    # calling the function
    for i in url_list:
        print("parsing page: ", i, "please wait...")
        extract_product_url(i, product_url_list)
        print("looking if there is a next page to parse")
        
    # informing the user in the console that the operation ended
    print("No more pages to scrape for this category!")
    print("The csv file with the books for ", category, " is available in the folder 'scraped_datas'")

def saveImageUrl(url, category):
    destination_dir = 'scrapedImages'
    img_name = url.split('/')[-2].split('_')[-2]
    checkDir(destination_dir, category)
    urlbase = 'https://books.toscrape.com'
    response = requests.get(url)
    image_url_list = list()
    if response.ok:
        soup = BeautifulSoup(response.text, 'lxml')
        image_url = urlbase + soup.find('img')['src'][5:]
        response = requests.get(image_url)
        with open('../' + destination_dir + '/' + category + '/Cover of ' + img_name.replace('-', ' ').capitalize() + ".jpg", "wb") as f:
            f.write(response.content)