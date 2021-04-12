# Project: Price Scraping

Here are the 4 scripts you asked for.

Target Website use for these processes: _books.toscrape.com_


## Instructions



## Descriptions of scripts

_Note that each scripts will extract informations that will be stored in the folder: *scraped_datas*._

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

and will write them in a file: dataOneBook_[name of the book].csv

### 2. scrapeBooksPerCategory.py

will extract the product url of each book for one category, then it will concatenate this information with the 10 other ones listed above.

will write a file: dateBooksPerCategory_[category].csv

### 3. scrapeBooksPerAllCategories.py

will extract all the informations for each book of each categories. 

will write one csv file for each category, using the same form defined above: dateBooksPerCategory_[category].csv

### 4. scrapeImagesOfEachProductseen.py

will save the images


