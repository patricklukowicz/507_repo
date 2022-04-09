from bs4 import BeautifulSoup
import requests
import time
import json


BASE_URL = 'https://musicbrainz.org'
MC5_PATH = '/artist/08b736bb-1c82-40b4-8b0b-49e2182a067a'
STOOGES_PATH = '/artist/794c6bf2-3241-416f-9b8f-24e2d84a1c4b'
CACHE_FILE_NAME = 'cacheMB_Scrape.json'
CACHE_DICT = {}

headers = {'User-Agent': 'SI507 Final Project - Python Web Scraping','From': 'lukowicz@umich.edu','MusicBrainz-Page': 'https://musicbrainz.org/artist/08b736bb-1c82-40b4-8b0b-49e2182a067a'}

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
        print("Fetching")
        time.sleep(1)
        response = requests.get(url, headers=headers)
        cache[url] = response.text
        save_cache(cache)
        return cache[url]

def pull_artist_urls(soup):
    # Extract sidebar divs where genres are located
    sidebar_tags_parent = soup1.find('div', class_='genre-list')
    tags_a = sidebar_tags_parent.find_all('a')

    # Extract genre urls
    genre_urls = []
    for a in tags_a:
        genre_path = a['href']
        genre_url = BASE_URL + genre_path
        genre_urls.append(genre_url)

    # Extract artist tab urls and pull releases and relationships links
    artist_tabs_parent = soup1.find('div', class_='tabs')
    tabs = artist_tabs_parent.find_all('li')
    artist_info_urls = []
    for tab in tabs:
        artist_info_tag = tab.find('a')
        artist_info_path = artist_info_tag['href']
        artist_info_url = BASE_URL + artist_info_path
        artist_info_urls.append(artist_info_url)

    # These house the releases (label info) and relationships (band member info) for MC5
    artist_releases_url = artist_info_urls[1]
    artist_relationships_url = artist_info_urls[5]

    return genre_urls, artist_releases_url, artist_relationships_url

# Load the cache, save in global variable
CACHE_DICT = load_cache()

# Make the soup for the MC5 Artist Page
MC5_page_url = BASE_URL + MC5_PATH
url_text1 = make_url_request_using_cache(MC5_page_url, CACHE_DICT)
response1 = requests.get(MC5_page_url)
soup1 = BeautifulSoup(response1.text, 'html.parser')
MC5_info = pull_artist_urls(soup1)

# Make the soup for the Stooges Artist page
Stooges_page_url = BASE_URL + STOOGES_PATH
url_text2 = make_url_request_using_cache(Stooges_page_url, CACHE_DICT)
response2 = requests.get(Stooges_page_url)
soup2 = BeautifulSoup(response2.text, 'html.parser')
Stooges_info = pull_artist_urls(soup2)

print(MC5_info)
print(Stooges_info) # This is returning the MC5 urls a second time instead of Stooges; cache issue?

print('-' * 50) # seperator