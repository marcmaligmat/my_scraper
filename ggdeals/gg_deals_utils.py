import json
import random
import re
import time

import requests

from lxml import html
from proxies import proxies

from selenium.webdriver.support.ui import WebDriverWait

from urllib.parse import urljoin, urlparse
import config


### Gamesplanet uk need conversion from google first
### ADD BCDKEY need to go a certain link
### instantgaming
#using requests, add merchant id to stop the crawler to go its link
api_stores = ['218','2180','158']
stores_dont_clean_url = ['270','47','228','63','310']
stores_needs_head = ['61','61616']
stores_uses_sku = ['67']
# skip gamivo smart, not shown in page
# skip humblebunde, GBP price,
#MEDION not shown in page
#g2a plus
#gamebillet challenge
skip_stores = ['2180','126','286','61616','409','81','176']
proxies = {
    'http': proxies[random.randrange(0,len(proxies))]
}

selenium_stores = ['68','69','175','157','228','61','63','47','49','1','224']

def get_aks_data(game_id):
        api = f"https://www.gg.deals/admin/bot_de_v2/marc_api.php?game_id={game_id}&version={time.time()}"
        r = requests.get(api, auth=(config.user, config.password))
        return json.loads(r.text)


def driver_wait_xpath(driver,xpath,time=1):
    wait =  WebDriverWait(driver,time)
    return wait.until(lambda driver: driver.find_element_by_xpath(xpath))

def driver_wait_xpath_lists(driver,xpath,time=1):
    wait =  WebDriverWait(driver,time)
    return wait.until(lambda driver: driver.find_elements_by_xpath(xpath))
 

def get_edition_name(edition_id):
    api = f"https://www.gg.deals/admin/bot_de_v2/marc_api.php?edition_name={edition_id}"
    r = requests.get(api, auth=(config.user, config.password))
    return r.text

def parse_headers(add_header=''):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9'
    }
    if add_header:
        for key,value in add_header.items():
            headers[key]=value
    return headers




def clean_url(merchant_id,url):
    if merchant_id == '122':
        return f"{remove_query_params(url)}?currency=EUR"

    # electronic first
    if merchant_id == '158':
        return f"{remove_query_params(url)}?c=EUR"

    if merchant_id not in stores_dont_clean_url:
        return remove_query_params(url)


    return url

def remove_query_params(url):
    return urljoin(url, urlparse(url).path)


