from bs4 import BeautifulSoup
import requests
import re
import os.path
import csv
import itertools

print("Welcome to your scraping script!")
list_of_options = ['book', 'category', 'all']
question_choice_image = "Do you want to download the images ? ('yes' to download, anything else to not download') "


# variable for the target website
urlbase = "https://books.toscrape.com/"
urlbasecat = urlbase + "catalogue/category/books/"

# creating the list of categories
# category list will be a list with lists inside, example of list inside: ['Short', 'Stories'] 
category_list = list()
response = requests.get(urlbase)
if response.ok:
    soup = BeautifulSoup(response.text, 'lxml')
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


# function to check if a path exist or not
def checkdir(path_to_check):
    while not os.path.isdir(path_to_check):
        try:
            os.makedirs(path_to_check)
        except OSError:
            # print("line 55: there was a problem with the path ", path_to_check)
            break


# function to scrape the data from one book.
def onebook(book_option, chosen_url, image_one_book_option, path_to_one_book_data):
    try:
        response = requests.get(chosen_url)
        if response.ok:
            soup = BeautifulSoup(response.text, 'lxml')
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
            if book_option == "book":
                path_to_one_book_data = path_to_one_book_data + title
                checkdir(path_to_one_book_data + '/csv/')
                path_one_book_csv = path_to_one_book_data + '/csv/' + 'book_title_' + title + '.csv'
                with open(path_one_book_csv, 'a', newline='') as f:
                    csv_writer = csv.writer(f)
                    csv_writer.writerow(
                        ['product_page_url', 'universal_product_code(upc)', 'title', 'price_including_tax',
                         'price_excluding_tax', 'number_available', 'product_description', 'category', 'review_rating',
                         'image_url'])
                    csv_writer.writerow(
                        [chosen_url, upc, title, price_including_tax, price_excluding_tax, number_available,
                         product_description, category, review_rating, urlbase + image_url])
                print('csv: book_title_' + title + '.csv created. Path is ', path_one_book_csv)
            else:
                with open(path_to_one_book_data, 'a', newline='') as f:
                    csv_writer = csv.writer(f)
                    csv_writer.writerow(
                        [chosen_url, upc, title, price_including_tax, price_excluding_tax, number_available,
                         product_description, category, review_rating, urlbase + image_url])
            # creating a dict with the title of the books and their url to send to imageSaver() to save them
            if book_option == 'book' and image_one_book_option == 'yes':
                image_dict = dict()
                image_ref = urlbase + image_url
                image_dict[title] = image_ref
                imagesaver(book_option, path_to_one_book_data, image_dict)
    except requests.exceptions.MissingSchema:
        print('Looks like ', chosen_url, ' is not a valid url.')
        print('try again')
        start()


# to scrape the data from one category
def onecategory(category_option, chosen_category, images_for_category_or_not, path_to_one_category_data):
    caturl = ""
    print('----please wait----')
    path_to_csv = ''
    if category_option == 'category':
        path_to_csv = path_to_one_category_data + chosen_category + '/csv/'
        checkdir(path_to_csv)
    elif category_option == 'all':
        path_to_csv = path + chosen_category + '/csv/' 
        checkdir(path_to_csv)
    with open(path_to_csv + chosen_category + '.csv', 'w', newline='') as pathcsv:
        csv_writer = csv.writer(pathcsv)
        csv_writer.writerow(['product_page_url', 'universal_product_code(upc)', 'title', 'price_including_tax',
                             'price_excluding_tax', 'number_available', 'product_description', 'category',
                             'review_rating', 'image_url'])


# creating the list of page to visit. Requesting pages to check their existence.
    for i in categories_list_full:
        if i.split('_')[0] == chosen_category:
            caturl = i
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
 
    # calling the onebook()
    # creating an information to show to the user in the console
    current_done = 0
    for i in product_url_list:
        counter_total = len(product_url_list)
        path_to_category_csv = path_to_one_category_data + chosen_category + '/csv/' + chosen_category + '.csv'
        onebook(category_option, i, images_for_category_or_not, path_to_category_csv)
        current_done += 1
        print("parsing page ", current_done, "on ", counter_total)

    # creating a dict with name of the book and the url of their image.
    # will be send to function imageSaver(),
    # example of key/value pair inside the dict:
    # {'The-bhagavad-gita': 'https://books.toscrape.com//media/cache/13/27/13270087ac5cba3e999166a64991187a.jpg'}
    if images_for_category_or_not == 'yes':
        image_dict = dict()
        for i in product_url_list:
            name = i.split('/')[-2].split('_')[-2].capitalize()
            response = requests.get(i)
            if response.ok:
                soup = BeautifulSoup(response.text, 'lxml')
                image_url = urlbase + soup.find("img")['src'][5:]
                image_dict[name] = image_url

        # calling imageSaver
        imagesaver(category_option, path + chosen_category, image_dict)


# to scrape the data from all categories: calling onecategory()
def allcategories(all_images_or_not, path_to_all_data):
    counter = len(categories_list)
    print("----there is ", counter, " categories to parse !----")
    for i in categories_list:
        onecategory('all', i, all_images_or_not, path)
        counter -= 1
        print("----there is ", counter, " categories left to parse !----")


# to save the images
def imagesaver(choice, path_image_folder, image_dictionary):
    if choice == 'book':
        path_image_folder = path_image_folder + "/cover_image/"
        checkdir(path_image_folder)
    else:
        path_image_folder = path_image_folder + "/cover_images/"
        checkdir(path_image_folder)
    for i, j in image_dictionary.items():
        response_image = requests.get(j)
        if response_image.ok:
            print('saving image cover of ', i, ' in ', path)
            with open(path_image_folder + '/Cover_of_' + i + '.jpg', 'wb') as f:
                f.write(response_image.content)


# to be able to choose the function we want to use within the command line.
def chooser(option):
    global path
    if option == 'book':
        path = 'data/one_book_data/'
        argument_for_book = input('Please paste the product page url of the book you want to scrape : ')
        if urlbase not in argument_for_book:
            print('it is not a valid url. You need to choose a book product page url from ', urlbase[:-2])
            chooser('book')
        book_image = input(question_choice_image)
        path_book = 'data/one_book_data/'
        checkdir(path_book)
        onebook(option, argument_for_book, book_image, path_book)
    elif option == 'category':
        path = 'data/one_category_data/'
        argument_for_category = input("Which category do you want to scrape ? (use lowercase and dashes) ")
        if argument_for_category not in categories_list:
            print("use only lowercase and dashes.")
            print('Example: for "Christian Fiction", type "christian-fiction"')
            chooser('category')
        else:
            category_images = input(question_choice_image)

            path_category = 'data/one_category_data/'
            checkdir(path_category)
            onecategory(option, argument_for_category, category_images, path_category)
    else:
        path = 'data/all_categories_data/'
        all_image = input(question_choice_image)
        path_all = 'data/all_categories_data/'
        allcategories(all_image, path_all)


def start():
    answer = input('First, type what you want to scrape: "book", "category" or "all" : ')
    if answer not in list_of_options:
        print('answer need to be either: "book" or "category" or "all"')
        start()
    else:
        chooser(answer)


start()
