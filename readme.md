# Project: Price Scraping

Here are the scripts you asked for.  
The Target Website use for these processes is _books.toscrape.com_
  
Functionalities:
- [x] scrape informations for one book
- [x] scrape informations for one categories
- [x] scrape informations for all categories
- [x] scrape image of each product page visited
  
## Instructions

Clone the repository in the folder of your choice.  
Check the descriptions of the scripts you want to use before using them.  
Open a terminal and check that you are in the folder: 'python-web-scraping'.  
You can use the scripts by typing:  
  
> python3 scrapeOneBook.py  
  
or  
  
> python3 scrapeBooksPerOneCategory.py  
  
or  
  
> python3 scrapeBooksPerAllCategories.py  
  
## Descriptions of scripts

_Note that Each script will create folders to store the extracted informations: csv or images_
### 1. scrapeOneBook.py

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
  
will store the data above in the auto-generated folder: _scrapedOneBook_  
will store the image of the product page visited in the auto-generated folder: _scrapedImages_.  
  
### 2. scrapeBooksPerCategory.py

will extract the product url of each book for one category, then it will concatenate this information with the 10 other ones listed above.  
will write a file: dateBooksPerCategory_[category].csv  
will store this file in the auto-generated folder: _scrapedOneCategory_  
will store the image of the product pages visited in the auto-generated folder: _scrapedImages_.  
  
### 3. scrapeBooksPerAllCategories.py

will extract all the informations for each book of each categories.  
will write one csv file for each category, using the same form defined above: dateBooksPerCategory_[category].csv  
will store all these files in the auto-generated folder: _scrapedAllCategories_ 
will store the image of the product pages visited in the auto-generated folder: _scrapedImages_.  