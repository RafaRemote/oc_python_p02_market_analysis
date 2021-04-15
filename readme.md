# Project: Price Scraping

Here are the scripts you asked for.  
The Target Website use for these processes is https://books.toscrape.com/
  
#### Usage cases

- [x] scrape informations for __ONE BOOK__
- [x] scrape informations for __ONE CATEGORY OF BOOK__
- [x] scrape informations for __ALL CATEGORIES OF BOOKS__
- [x] scrape __BOOK IMAGE OF EACH PRODUCT PAGE VISITED__
  
## Installation

```
git clone https://github.com/RafaRemote/pythonWebScraper.git
```
```
python -v venv env
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

python scrape.py [arg1] [arg2] [arg3] [arg4] [arg5]

arg1: choice for the functions:

book: to scrape data from one book
category: to scrape category from one category
everything : to scrape everything

arg2: depends on the function you have chosen
- book: type the url of the product page of the book you want to scrape
- category: type the name of the category you have chosen. (all characters lowercase, no spaces but only dashes)
- everything : type 'evrything' to scrape all the datas 

arg3: destination folder. If the folder you're asking for is not existing, it will be created

arg4: destination csv file. If the csv does not exist it will be created.

arg5: choice for the image downloading and saving. Images will be saved in the folder you specified in arg3.

- yes to download the images,
- no to not download the images.

### 1. book
```
python scrape.py book [arg2] [arg3] [arg4] [arg5]
```

#### Usage cases
- [x] scrape informations for one book
- [x] scrape book image of each product page visited

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
if arg5 == yes: will store the image of the product in the folder specified in arg3
  
#### commands example

```
python scrape.py book https://books.toscrape.com/catalogue/scott-pilgrims-precious-little-life-scott-pilgrim-1_987/index.html scott dataScott yes
```

### 2. One category of book
#### Usage cases
- [x] scrape informations for one category of book
- [x] scrape book informations for one category

will all the data (the 10 data listed above) of each book for one category, 
will write a csv file with the name specified in arg4 and store it in the folder specified in arg3 
if arg5 == yes: will store the image of the product pages visited in the folder specified in arg3.

### 3. All categories of book scraping
#### Usage cases
- [x] scrape informations for all categories of books
- [x] scrape book image of each product page visited

will extract all the informations for each book of each categories.  
will write one csv file for each category, 
will store all these files in the folder specified in arg3
if arg5 == yes: will store the image of the product pages visited in the folder specified in arg3
