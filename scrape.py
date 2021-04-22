from bs4 import BeautifulSoup
import requests
import re
import os.path
import csv
import itertools

print("Welcome to your scraping script!")

# variable for the target website
URLBASE = "https://books.toscrape.com/"
URLBASECAT = URLBASE + "catalogue/category/books/"


# function to check if a path exist or not
def checkdir(path_to_check):
    while not os.path.isdir(path_to_check):
        try:
            os.makedirs(path_to_check)
        except OSError:
            # print("line 55: there was a problem with the path ", path_to_check)
            break


# creating the list of categories
def get_categories():   
    # category list will be a list with lists inside, example of list inside: ['Short', 'Stories'] 
    category_list = list()
    response = requests.get(URLBASE)
    if response.ok:
        soup = BeautifulSoup(response.text, 'lxml')
        categories = soup.findAll("a")
        for i in categories:
            if str(i).count("books") > 0:
                category_list.append(str(i).split()[2:-1])
    del category_list[0]
    # example of one category in the list after this below code: 'short-stories' instead of  ['Short', 'Stories'] previously
    categories_list = list()
    for i in category_list:
        if len(i) == 1:
            categories_list.append(i[0].lower())
        elif len(i) == 2:
            categories_list.append((i[0] + '-' + i[1]).lower())
        else:
            categories_list.append((i[0] + '-' + i[1] + '-' + i[2]).lower())
    return categories_list


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
                         product_description, category, review_rating, URLBASE + image_url])
                print('csv: book_title_' + title + '.csv created. Path is ', path_one_book_csv)
            else:
                with open(path_to_one_book_data, 'a', newline='') as f:
                    csv_writer = csv.writer(f)
                    csv_writer.writerow(
                        [chosen_url, upc, title, price_including_tax, price_excluding_tax, number_available,
                         product_description, category, review_rating, URLBASE + image_url])
            # creating a dict with the title of the books and their url to send to imageSaver() to save them
            if book_option == 'book' and image_one_book_option == 'yes':
                image_dict = dict()
                image_ref = URLBASE + image_url
                image_dict[title] = image_ref
                imagesaver(book_option, path_to_one_book_data, image_dict)
    except requests.exceptions.MissingSchema:
        print('Looks like ', chosen_url, ' is not a valid url.')
        print('try again')


# to scrape the data from one category
def onecategory(category_option, chosen_category, images_for_category_or_not, path_to_one_category_data, cat_list):
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
        # modifying the elements of the list of categories to get the correct syntax and to recreate the correct urls,
        # example of one category: short-stories_45
        categories_list_full = list()
        i = 2
        for j in cat_list:
            categories_list_full.append(j + '_' + str(i))
            i += 1

    # creating the list of page to visit. Requesting pages to check their existence.
    for i in categories_list_full:
        if i.split('_')[0] == chosen_category:
            caturl = i
            break
    url_list = list()
    url_list.append(URLBASECAT + caturl + '/index.html')
    url_cat_page_base = URLBASECAT + caturl + '/page-'
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
                    product_url = URLBASE + 'catalogue/' + j['href'][9:]
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
                image_url = URLBASE + soup.find("img")['src'][5:]
                image_dict[name] = image_url

        # calling imageSaver
        imagesaver(category_option, path + chosen_category, image_dict)


# to scrape the data from all categories: calling onecategory()
def allcategories(all_images_or_not, path_to_all_data):
    list_of_categories = get_categories()
    counter = len(list_of_categories)
    print("----there is ", counter, " categories to parse !----")
    for i in list_of_categories:
        onecategory('all', i, all_images_or_not, path, list_of_categories)
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
            print('saving image cover of ', i, ' in ', path_image_folder)
            with open(path_image_folder + '/Cover_of_' + i + '.jpg', 'wb') as f:
                f.write(response_image.content)


# to be able to choose the function we want to use within the command line.
def chooser():
    global PATH
    list_of_options = ['book', 'category', 'all']
    answer = input('First, type what you want to scrape: "book", "category" or "all" : ')
    if answer not in list_of_options:
        print('answer need to be either: "book" or "category" or "all"')
        chooser()
    else:
        question_choice_image = "Do you want to download the images ? ('yes' to download, anything else to not download') "
        if answer == 'book':
            path = 'data/one_book_data/'
            argument_for_book = input('Please paste the product page url of the book you want to scrape : ')
            if URLBASE not in argument_for_book:
                print('it is not a valid url. You need to choose a book product page url from ', URLBASE[:-2])
                chooser('book')
            book_image = input(question_choice_image)
            path_book = 'data/one_book_data/'
            checkdir(path_book)
            onebook(answer, argument_for_book, book_image, path_book)
        elif answer == 'category':
            path = 'data/one_category_data/'
            argument_for_category = input("Which category do you want to scrape ? (use lowercase and dashes) ")
            categories_list = get_categories()
            if argument_for_category not in categories_list:
                print("use only lowercase and dashes.")
                print('Example: for "Christian Fiction", type "christian-fiction"')
                chooser()
            else:
                category_images = input(question_choice_image)
                path_category = 'data/one_category_data/'
                checkdir(path_category)
                onecategory(answer, argument_for_category, category_images, path_category, categories_list)
        else:
            path = 'data/all_categories_data/'
            all_image = input(question_choice_image)
            path_all = 'data/all_categories_data/'
            allcategories(all_image, path_all)

chooser()
