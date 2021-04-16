# Project: Price Scraping

The Target Website used for this script is https://books.toscrape.com/
#### Usage cases

- [x] scrape informations for __ONE BOOK__
- [x] scrape informations for __ONE CATEGORY OF BOOK__
- [x] scrape informations for __ALL CATEGORIES OF BOOKS__
- [x] scrape __BOOK IMAGE OF EACH PRODUCT PAGE VISITED__
  
## Installation

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

## commands 
```
python scrape.py [arg1] [arg2] [arg3] [arg4] [arg5]
```

arg1: choice for the functions:

- __book__: to scrape data from one book
- __category__: to scrape category from one category
- __everything__ : to scrape everything

arg2: depends on the function you have chosen:
- if __book__: type the __url__ of the product page of the book you want to scrape,
- else if __category__: type the __name of the category__ you have chosen. (all characters must be lowercased, no spaces but only dashes),
- else __everything__ : type 'everything' to scrape all the datas .

arg3: destination folder. Type the name one you want for the folder which will store the data you want to scrape

arg4: destination csv file. Type the name you want, without the extension '.csv', for the csv file to be created.

arg5: choice for the image downloading and saving. Images will be saved in the folder you specified in arg3.

- __yes__: to download the images,
- __no__: to not download the images.

### 1. book
#### Usage cases
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

will write a csv file with the name specified in arg4
will store it in a folder with the name specified in arg3
if arg5 == yes: will store the image of the product in the folder named 'cover-images', within the folder specified in arg3.
  
#### commands example

```
python scrape.py book [arg2] [arg3] [arg4] [arg5]
```

```
python scrape.py book https://books.toscrape.com/catalogue/scott-pilgrims-precious-little-life-scott-pilgrim-1_987/index.html dataOneBook dataBook_scott yes
```

### 2. One category of book
#### Usage cases
- [x] scrape informations for one category of book
- [x] scrape book image of each product page visited

will write all the data (the 10 data listed above) of each book for one category, 
will write a csv file with the name specified in arg4 and store it in the folder specified in arg3 
if arg5 == yes: will store the image of the product pages visited in a folder named 'cover-images', within the folder specified in arg3.

#### commands example

```
python scrape.py category [arg2] [arg3] [arg4] [arg5]
```

```
python scrape.py category mystery dataOneCategory dataCat_mystery yes
```

### 3. All categories
#### Usage cases
- [x] scrape informations for all categories of books
- [x] scrape book image of each product page visited

will extract all the informations for each book of each categories.
will store all the files in a folder with the name specified in arg3.
the desination folder will contain one folder for each category, with the name of the category. 
if arg5 = yes:
    the folders for each category will contain 2 fodlers:
    - cover-images
    - csv

__Here arg2 and arg4 need to be dots: '.', check the code below.__

#### commands example

:exclamation: Use this command to scrape all the datas :exclamation:  
you can still change the name of the destination folder 'allData' and change yes to no, to not download the images.

```
python scrape.py all . allData . yes
```

