""" Purpose of this script

- main project: Price Scraping
- target Website: books.toscrape.com

"""

import scrapeFunctions

scrapeFunctions.checkDir('scrapedImages')

url = 'https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html'

scrapeFunctions.saveImageUrl(url)