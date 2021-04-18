# Project: Price Scraping

Menu

1. Usage cases
2. Installation
3. One book scraping
4. One category scraping
5. All categories scraping


The Target Website used for this script is https://books.toscrape.com/
## 1 - Usage cases

- [x] scrape informations for __ONE BOOK__
- [x] scrape informations for __ONE CATEGORY OF BOOK__
- [x] scrape informations for __ALL CATEGORIES OF BOOKS__
- [x] scrape __BOOK IMAGE OF EACH PRODUCT PAGE VISITED__
  
## 2 - Installation

You need to have Python installed on your machine.
This script has been developed using python 3.9.2.
Check your version of Python, if needed, upgrade your version. 

Open a terminal in the folder of your choice, then type:

```
git clone https://github.com/RafaRemote/pythonWebScraper.git
```
```
python -m venv env
```
```
source env/bin/activate
```
```
pip install --upgrade pip
```
```
pip install -r requirements.txt
```

Now you can use the commands below in the terminal

### commands 
```
python scrape.py arg1 arg2 arg3
```

arg1: choice for the functions:

- __book__: to scrape data from one book
- __category__: to scrape category from one category
- __all__ : to scrape everything

arg2: depends on the function you have chosen:
- if __book__: type the __url__ of the product page of the book you want to scrape,
- else if __category__: type the __name of the category__ you have chosen. (all characters must be lowercased, no spaces but only dashes),
- else __all__ : type '.' 


arg3: choice for the image downloading and saving.

- __yes__: to download the images,
- __no__: to not download the images.

## 3. One book scraping
### Usage cases
- [x] scrape informations for one book,
- [x] scrape book image of each product page visited.

will extract the following datas:

* product_page_url
* universal_ product_code (upc)
* title
* price_including_tax
* price_excluding_tax
* number_available
* product_description
* category
* review_rating
* image_url



if arg3 == yes: will store the image of the product in the folder named 'cover-images'.
  
### command example

```
python scrape.py book arg2 arg3
```

```
python scrape.py book https://books.toscrape.com/catalogue/scott-pilgrims-precious-little-life-scott-pilgrim-1_987/index.html yes
```

## 4. One category scraping
### Usage cases
- [x] scrape informations for one category of book
- [x] scrape book image of each product page visited

will write all the data (the 10 data listed above) of each book for one category, 

if arg3 == yes: will store the image of the product pages visited in a folder named 'cover-images'.

### command example

```
python scrape.py category arg2 arg3
```

```
python scrape.py category religion yes
```

## 5. All categories
### Usage cases
- [x] scrape informations for all categories of books
- [x] scrape book image of each product page visited

will extract all the informations for each book of each categories.
if arg3 = yes:
    the folders for each category will contain 2 fodlers:
    - cover-images
    - csv

__Here arg2 need to be a dot: '.', check the code below.__

### command example

```
python scrape.py category [arg2] [arg3]
```

:exclamation: Use this command to scrape all the datas :exclamation:  
you can still change 'yes' to 'no', to not download the images.

```
python scrape.py all . allData yes
```