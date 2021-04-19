# Project: Price Scraping

Menu

1. Usage cases
2. Installation
3. Commands
4. One book scraping
5. One category scraping
6. All categories scraping


The Target Website used for this script is https://books.toscrape.com/
## 1 - Usage cases

- [x] scrape information for __ONE BOOK__
- [x] scrape information for __ONE CATEGORY OF BOOK__
- [x] scrape information for __ALL CATEGORIES OF BOOKS__
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

## 3 - Commands

In the terminal, check that you are in the folder 'pythonWebScraper', and enter:

```
python scrape.py
```

Then simply answer the questions as specified.

## 4 - One book scraping
### Usage cases
- [x] scrape information for one book,
- [x] scrape book image of each product page visited.

will extract the following data:

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

### structure of the data downloaded

⬇️ data  
  
&nbsp;&nbsp;&nbsp;&nbsp;⬇️ one_book_data  
  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;⬇️ [name of the book chosen]  
  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-> csv  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-> cover_image  


## 5 - One category scraping
### Usage cases
- [x] scrape information for one category of book
- [x] scrape book image of each product page visited

will write all the data (the 10 data listed above) of each book for one category, 

### structure of the data downloaded

⬇️  data  
  
&nbsp;&nbsp;&nbsp;&nbsp;⬇️  one_category_data  
  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;⬇️  [name of the chosen category]  
  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;->  cover_images  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;->  csv  


## 6 - All categories
### Usage cases
- [x] scrape information for all categories of books
- [x] scrape book image of each product page visited

will extract all the information for each book of each category.

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

