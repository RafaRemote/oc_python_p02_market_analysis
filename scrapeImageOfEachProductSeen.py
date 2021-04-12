""" Purpose of this script

- main project: Price Scraping
- target Website: books.toscrape.com

"""

import scrapeFunctions

checkDir('scraped_datas')

url = 'https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html'

saveImageUrl(url)