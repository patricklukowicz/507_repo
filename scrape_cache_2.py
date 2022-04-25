#########################################
##### Name: Patrick Lukowicz        #####
##### Uniqname: lukowicz            #####
#########################################

from bs4 import BeautifulSoup
import requests
import time
import json

BASE_URL = 'http://musicwikidetroit.org/index.php'
BANDS_PATH = '/Category:Bands'
CACHE_FILE_NAME = 'cachedDetroitWiki_Scrape.json'
CACHE_DICT = {}

headers = {'User-Agent': 'SI507 Final Project - Python Web Scraping','From': 'lukowicz@umich.edu','MusicWiki-Detroit-Page': 'http://musicwikidetroit.org/index.php/Category:Bands'}

def load_cache():
    try:
        cache_file = open(CACHE_FILE_NAME, 'r')
        cache_file_contents = cache_file.read()
        cache = json.loads(cache_file_contents)
        cache_file.close()
    except:
        cache = {}
    return cache


def save_cache(cache):
    cache_file = open(CACHE_FILE_NAME, 'w')
    contents_to_write = json.dumps(cache)
    cache_file.write(contents_to_write)
    cache_file.close()


def make_url_request_using_cache(url, cache):
    if (url in cache.keys()): # the url is our unique key
        print("Using cache")
        return cache[url]
    else:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        # Find the div that houses all the sidebar table data
        sidebar_table_parent = soup.find('div', id='mw-content-text')
        return sidebar_table_parent
        # Find all tags labeled as table rows
        # sidebar_table = sidebar_table_parent.find_all('tr', recursive=False)
        # # For each table row in the sidebar table:
        # for table_row in sidebar_table:
        #     # Extract band name
        #     band_name = table_row.find('th')
        #     # Extract all sidebar data with p tag
        #     # band_details = table_row.find_all('p')
        #     return band_name.text.strip()

# Make the soup for Bands page
Bands_page_url = BASE_URL + BANDS_PATH
# url_text = make_url_request_using_cache(Bands_page_url, CACHE_DICT)
response = requests.get(Bands_page_url)
soup = BeautifulSoup(response.text, 'html.parser')

# For each band on the Bands page, find their div
band_listing_parent = soup.find('div', class_='mw-content-ltr')
band_listing_divs = band_listing_parent.find_all('div', recursive=False)
band_urls = []
for band_listing_div in band_listing_divs:
    # Extract the band page URL from the band div
    bands = band_listing_div.find_all('li')
    try:
        for b in bands:
            band_link_tag = b.find('a')
            band_details_path = band_link_tag['href']
            # Create soup for each band page, crawl through them and extract band details from sidebar table
            band_details_url = BASE_URL + band_details_path
            band_urls.append(band_details_url)
    except TypeError:
        continue

print('-' * 50)

# Load the cache, save in global variable
CACHE_DICT = load_cache()

# For each band url in the greater list:
for band_url in band_urls:
    # Make the soup for each band page
    response2 = make_url_request_using_cache(band_url, CACHE_DICT)
    print(response2)

print('-' * 50)

time.sleep(1)