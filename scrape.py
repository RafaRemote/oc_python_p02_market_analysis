from bs4 import BeautifulSoup
import requests
import re
import os.path
import csv
import sys
import itertools

# to be able to use variables from the command line
choice = (sys.argv[1])
fun_arg_choice = (sys.argv[2])
folder_choice = (sys.argv[3])
csv_choice = (sys.argv[4])
image_choice = (sys.argv[5])

# will be used to manage the organisation of the folders for the storing of images
path = ""

# variable for the target website
urlbase = "https://books.toscrape.com/"
urlbasecat = urlbase + "catalogue/category/books/"

# creating the list of categories
# category list will be a list with lists inside, example of list inside: ['Short', 'Stories'] 
category_list = list()
response_homepage = requests.get(urlbase)
if response_homepage.ok:
    soup = BeautifulSoup(response_homepage.text, 'lxml')
    categories = soup.findAll("a")
    for i in categories:
        if str(i).count("books") > 0:
            category_list.append(str(i).split()[2:-1])
del category_list[0]
# creating a list of all the name of the categories
# example of one category in the list after this below code: 'short-stories' instead of  ['Short', 'Stories'] previously
categories_list = list()
for i in category_list:
    if len(i) == 1:
        categories_list.append(i[0].lower())
    elif len(i) == 2:
        categories_list.append((i[0] + '-' + i[1]).lower())
    else:
        categories_list.append((i[0] + '-' + i[1] + '-' + i[2]).lower())
# modifying the elements of the list to get the correct syntax and to recreate the correct urls,
# example of one category: short-stories_45
categories_list_full = list()
i = 2
for j in categories_list:
    categories_list_full.append(j + '_' + str(i))
    i += 1


# to be able to choose the function we want to use within the command line.
def chooser(choice, fun_arg_choice, folder_choice, csv_choice, image_choice):
    arg_list = list()
    arg_list.append(choice)
    for i in arg_list:
        if i == "book":
            onebook(choice, fun_arg_choice, folder_choice, csv_choice, image_choice, path)
        elif i == "category":
            onecategory(fun_arg_choice, folder_choice, csv_choice, image_choice)
        elif i == "all":
            allcategories(folder_choice, image_choice)
        else:
            print("choices available are: book, category or all")


# function to scrape the data from one book.
def onebook(chooser, fun_arg_choice, folder_choice, csv_choice, image_choice, path):
    while not os.path.isdir(folder_choice):
        try:
            os.makedirs(folder_choice)
        except OSError:
            print("there was a problem with the path ", folder_choice)
            break
    try:
        response_url = requests.get(fun_arg_choice)
        if response_url.ok:
            soup = BeautifulSoup(response_url.text, 'lxml')
            upc = soup.find('td').text
            title = soup.find('h1').text.replace(' ', '_').replace('/', '-')
            price_including_tax = soup.findAll('td')[3].text[1:]
            price_excluding_tax = soup.findAll('td')[2].text[1:]
            number_available = str(re.findall('[0-9]+', soup.findAll('td')[5].text))[2:-2]
            product_description = soup.findAll('p')[3].text.replace('\n', '')
            category = soup.findAll('a')[3].text
            review_ratings = str(soup.find("p", {"class": "star-rating"}))
            raitings = {'One': 1, 'Two': 2, 'Three': 3, "Four": 4, "Five": 5}
            review_rating = None
            for rating in ['One', 'Two', 'Three', 'Four', 'Five']:
                if review_ratings.find(rating) != -1:
                    review_rating = raitings[rating]
            image_url = "" + soup.find("img")['src'][5:]
            if choice == "book":
                while not os.path.isdir(folder_choice + '/csv/'):
                    try:
                        os.makedirs(folder_choice + '/csv/')
                    except OSError:
                        print("there was a problem with the path ", folder_choice + '/csv')
                    break
                path = folder_choice + '/csv/' + csv_choice + '.csv'
                with open(path, 'a', newline='') as f:
                    csv_writer = csv.writer(f)
                    csv_writer.writerow(
                        ['product_page_url', 'universal_product_code(upc)', 'title', 'price_including_tax',
                         'price_excluding_tax', 'number_available', 'product_description', 'category', 'review_rating',
                         'image_url'])
                    csv_writer.writerow(
                        [fun_arg_choice, upc, title, price_including_tax, price_excluding_tax, number_available,
                         product_description, category, review_rating, urlbase + image_url])
            else:
                with open(path, 'a', newline='') as f:
                    csv_writer = csv.writer(f)
                    csv_writer.writerow(
                        [fun_arg_choice, upc, title, price_including_tax, price_excluding_tax, number_available,
                         product_description, category, review_rating, urlbase + image_url])
                    # creating a dict with the title of the books and their url to send to imageSaver() to save them
            if chooser == 'book' and image_choice == 'yes':
                image_dict = dict()
                image_ref = urlbase + image_url
                image_dict[title] = image_ref
                imagesaver(folder_choice, image_dict)
    except requests.exceptions.MissingSchema:
        print('it is not a valid url ', fun_arg_choice)


# to scrape the data from one category
def onecategory(fun_arg_choice, folder_choice, csv_choice, image_choice):
    caturl = ""
    print('----please wait----')
    if fun_arg_choice not in categories_list:
        print(
            "it is not a listed category. "
            "Type the exact name of the category, all characters must be lowercase. "
            "Replace spaces by dashes '-' ")
        exit()
    else:
        while not os.path.isdir(folder_choice + '/' + fun_arg_choice + '/csv/'):
            try:
                os.makedirs(folder_choice + '/' + fun_arg_choice + '/csv/')
            except OSError:
                print("there was a problem with the path ", folder_choice)
                break
        with open(folder_choice + '/' + fun_arg_choice + '/csv/' + csv_choice + '.csv', 'w', newline='') as pathCsv:
            csv_writer = csv.writer(pathCsv)
            csv_writer.writerow(['product_page_url', 'universal_product_code(upc)', 'title', 'price_including_tax',
                                 'price_excluding_tax', 'number_available', 'product_description', 'category',
                                 'review_rating', 'image_url'])
        for i in categories_list_full:
            if i.split('_')[0] == fun_arg_choice:
                caturl = i
                break

    # creating the list of page to visit. Requesting pages to check their existence.
    url_list = list()
    url_list.append(urlbasecat + caturl + '/index.html')
    url_cat_page_base = urlbasecat + caturl + '/page-'
    for num_page in itertools.count(start=2):
        url_page_to_parse = url_cat_page_base + str(num_page) + ".html"
        if requests.get(url_page_to_parse).ok:
            url_list.append(url_page_to_parse)
        else:
            break

    # creating the whole list or product urls :
    # example of url: https://books.toscrape.com/catalogue/the-bhagavad-gita_60/index.html
    product_url_list = list()
    for i in url_list:
        response = requests.get(i)
        if response.ok:
            soup = BeautifulSoup(response.text, 'lxml')
            a_tag = soup.findAll('a')
            for j in a_tag:
                if str(j).count('../') == 3:
                    product_url = urlbase + 'catalogue/' + j['href'][9:]
                    product_url_list.append(product_url)

    # creating an information to show to the user in the console
    current_done = 0
    for i in product_url_list:
        counter_total = len(product_url_list)
        path = folder_choice + '/' + fun_arg_choice + '/csv/' + csv_choice + '.csv'
        onebook('category', i, folder_choice, fun_arg_choice + '/csv/' + csv_choice, image_choice, path)
        current_done += 1
        print("parsing page ", current_done, "on ", counter_total)
    # creating a dict with name of the book and the url of their image.
    # will be send to function imageSaver(),
    # example of key/value pair inside the dict:
    # {'The-bhagavad-gita': 'https://books.toscrape.com//media/cache/13/27/13270087ac5cba3e999166a64991187a.jpg'}
    if image_choice == 'yes':
        image_dict = dict()
        for i in product_url_list:
            name = i.split('/')[-2].split('_')[-2].capitalize()
            response = requests.get(i)
            if response.ok:
                soup = BeautifulSoup(response.text, 'lxml')
                image_url = urlbase + soup.find("img")['src'][5:]
                image_dict[name] = image_url
        # calling imageSaver
        imagesaver(folder_choice + '/' + fun_arg_choice, image_dict)


# to scrape the data from all categories
def allcategories(folder_choice, image_choice):
    counter = len(categories_list)
    print("----there is ", counter, " categories to parse !----")
    for i in categories_list:
        onecategory(i, folder_choice, i, image_choice)
        counter -= 1
        print("----there is ", counter, " categories left to parse !----")


# to save the images
def imagesaver(path_image_folder, image_dict):
    print('----retrieving images, please wait----')
    while not os.path.isdir(path_image_folder + "/cover-images"):
        try:
            os.makedirs(path_image_folder + "/cover-images")
        except OSError:
            print("there was a problem with the path ", path_image_folder + "/cover-image")
            break
    for i, j in image_dict.items():
        response_image = requests.get(j)
        if response_image.ok and image_choice == "yes":
            print('saving image cover of ', i, ' in ', path_image_folder)
            with open(path_image_folder + '/cover-images' + '/Cover_of_' + i + '.jpg', 'wb') as f:
                f.write(response_image.content)


# to be able to use the functions within the command line
if __name__ == '__main__':
    chooser(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
