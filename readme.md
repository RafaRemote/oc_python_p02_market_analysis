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

- __'book'__: to scrape data from one book
- __'category'__: to scrape category from one category
- __'all'__ : to scrape everything

arg2: depends on the function you have chosen:
- if __arg1 == 'book'__: type the __url__ of the product page of the book you want to scrape,
- else if __arg1 == 'category'__: type the __name of the category__ you have chosen. (all characters must be lowercased, no spaces but only dashes),
- else if  __arg1 == 'all'__ : type '.' (one dot) 


arg3: choice for the image downloading and saving.

- __'yes'__: to download the images,
- __'no'__: to not download the images.

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


if __arg3 == 'yes'__: will store the image of the visited pages.
  
### command example

```
python scrape.py book arg2 arg3
```

```
python scrape.py book https://books.toscrape.com/catalogue/scott-pilgrims-precious-little-life-scott-pilgrim-1_987/index.html yes
```

### struture of the data downloaded

⬇️ data  
  
&nbsp;&nbsp;&nbsp;&nbsp;⬇️ one_book_data  
  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;⬇️ [name of the book chosen]  
  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-> csv  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-> cover_image  


## 4. One category scraping
### Usage cases
- [x] scrape informations for one category of book
- [x] scrape book image of each product page visited

will write all the data (the 10 data listed above) of each book for one category, 

if __arg3 == 'yes'__: will store the image of the product pages visited.

### command example

```
python scrape.py category arg2 arg3
```

```
python scrape.py category religion yes
```

### structure of the data downloaded

⬇️  data  
  
&nbsp;&nbsp;&nbsp;&nbsp;⬇️  one_category_data  
  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;⬇️  [name of the chosen category]  
  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;->  cover_images  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;->  csv  


## 5. All categories
### Usage cases
- [x] scrape informations for all categories of books
- [x] scrape book image of each product page visited

will extract all the informations for each book of each categories.

if __arg3 == 'yes'__: will store the image of the product pages visited.


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
### structure of the data downloaded 

⬇️ data  
  
&nbsp;&nbsp;&nbsp;&nbsp;⬇️ all_categories_data  
  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;⬇️  [name of the category]  
  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-> cover_images  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-> csv  
  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;⬇️  [name of the category]  
  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-> cover_images  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-> csv  
  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;⬇️  [name of the category]  
  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-> cover_images  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-> csv  
  
(...etc, up to the 50 categories)  

