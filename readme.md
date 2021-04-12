# Project: Price Scraping

Here are the 4 scripts you asked for.
Target Website use for these processes: _books.toscrape.com_
## Instructions

Clone the repository in the folder of your choice.
Check the descriptions of the scripts you want to use before using them.
Open a terminal and check that you are in the folder: 'python-web-scraping', then:
you can use the scripts by typing:

'python3 scrapeOneBook.py'

or

'python3 scrapeBooksPerOneCategory.py'

or

'python3 scrapeBooksPerAllCategories.py'

or

'python3 scrapeImageOfEachProductSeen.py'

## Descriptions of scripts

_Note that Each script will create its own folder to store the extracted informations: csv or images_

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

### 2. scrapeBooksPerCategory.py

will extract the product url of each book for one category, then it will concatenate this information with the 10 other ones listed above.

will write a file: dateBooksPerCategory_[category].csv

will store this file in the auto-generated folder: _scrapedOneCategory_

### 3. scrapeBooksPerAllCategories.py

will extract all the informations for each book of each categories. 

will write one csv file for each category, using the same form defined above: dateBooksPerCategory_[category].csv

will store all these files in the auto-generated folder: _scrapedAllCategories_

### 4. scrapeImageOfEachProductSeen.py

will save the images of the products that you have visited in the folder *scrapedImages*.

will store these images in the auto-generated folder: _scrapeImages_