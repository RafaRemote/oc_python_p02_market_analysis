""" Purpose of this script

- main project: Price Scraping
- target Website: books.toscrape.com

"""

import scrapeFunctions

destination_dir = 'scrapedImages'
scrapeFunctions.checkDir(destination_dir)

url = 'https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html'

scrapeFunctions.saveImageUrl(url, destination_dir)