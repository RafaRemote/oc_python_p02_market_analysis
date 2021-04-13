# Project: Price Scraping

Here are the scripts you asked for.  
The Target Website use for these processes is https://books.toscrape.com/
  
#### Usage cases

- [x] scrape informations for __ONE BOOK__
- [x] scrape informations for __ONE CATEGORY OF BOOK__
- [x] scrape informations for __ALL CATEGORIES OF BOOKS__
- [x] scrape __BOOK IMAGE OF EACH PRODUCT PAGE VISITED__
  
## Installation

Clone the repository in the folder of your choice.  
  
### 1. One book scraping

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
  
will store the data above in a csv file in the auto-generated folder: _data per book/[name of the book]_  
will store the image of the product visited in the same folder, besides the csv file.  

#### command

Open a terminal and check that you are in the folder: 'python-web-scraping'.  
You can use the script by typing:  
  
```
python3 scrapeOneBook.py  
```
  
### 2. One category of book
#### Usage cases
- [x] scrape informations for one category of book
- [x] scrape book informations for one category

will extract the product url of each book for one category, with the listed informations above for one book, 
will write a file: 'dataBooksPerCategory_[category].csv'
will store this file in the auto-generated folder: _data per category_  
will store the image of the product pages visited in a folder '[category]'

#### command

Open a terminal and check that you are in the folder: 'python-web-scraping'.  
You can use the script by typing:  
    
```
python3 scrapeBooksPerOneCategory.py  
```
  
### 3. All categories of book scraping
#### Usage cases
- [x] scrape informations for all categories of books
- [x] scrape book image of each product page visited

will extract all the informations for each book of each categories.  
will write one csv file for each category, using the same form defined above: dataBooksPerCategory_[category].csv  
will store all these files in the auto-generated folder: _data for all categories_ 
will be one folder '[category]' per category with one csv files for the data and one folder 'Cover images' for the images.
#### command

Open a terminal and check that you are in the folder: 'python-web-scraping'.  
You can use the script by typing:  
   
```
python3 scrapeBooksPerAllCategories.py  
```
  
### 4. Book image scraping

Each time a product page is visited by a script, the script does store the image of the product, as specified in the detailed description of the scripts.