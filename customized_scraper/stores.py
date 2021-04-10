import json
import random
import re
import time

import requests

from lxml import html
from proxies import proxies
from urllib.parse import urljoin, urlparse

### ADD BCDKEY need to go a certain link
#using requests, add merchant id to stop the crawler to go its link
api_stores = ['61616','61','218','2180','158']
stores_dont_clean_url = ['270','47','228']

# skip gamivo smart, not shown in page
skip_stores = ['2180']
proxies = {
    'http': proxies[random.randrange(0,len(proxies))]
}
def parse_headers(add_header=''):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36',
    }
    if add_header:
        for key,value in add_header.items():
            headers[key]=value
    return headers

def init_request(url,add_header=''):
    response = requests.get(
        url,
        headers=parse_headers(add_header),
        proxies=proxies,
        allow_redirects=True
    )
    time.sleep(8)
    return response

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

def get_store_price(driver,merchant_id,store_url):
    
    # gamivo we use api and request
    if merchant_id == '218':
        url = re.findall(r'[^\/]+$',store_url)[0]
        url = f"https://www.gamivo.com/api/product/product-by-slug/{url}"
        
        print(url)
        response = init_request(url)
        data = json.loads(response.text)['offers'][0]
        price = data['0']['price']
        return price
    
    # gamivo we use api and request
    if merchant_id == '2180':
        url = re.findall(r'[^\/]+$',store_url)[0]
        url = f"https://www.gamivo.com/api/product/product-by-slug/{url}"
        print(url)
        response = init_request(url)
        data = json.loads(response.text)['offers'][0]
        price = data['0']['price_with_smart_coupon']
        return price

    # void we use request, change currency first
    if merchant_id == '222':
        url = re.findall(r'[^\/]+$',store_url)[0]
        url = f"https://www.voidu.com/Common/SetLanguageAndCurrency?customerCurrency=6&langid=1&returnUrl=/{url}"
        print(url)
        response = init_request(url)
        price = tree.xpath('//div[@class="product-price"]/span/text()')
        return get_digits_only(price[0])

    # g2a we use request
    # + header 'accept-language': 'en-US,en;q=0.9'
    if merchant_id == '61':
        add_header = {'accept-language': 'en-US,en;q=0.9'}
        response = init_request(store_url,add_header)
        tree = html.fromstring(html=response.text)
        return tree.xpath('//span[@class="sc-igOljT eZYAZY"]/text()')[0]

    if merchant_id == '61616':
        add_header = {'accept-language': 'en-US,en;q=0.9'}
        response = init_request(store_url,add_header)
        tree = html.fromstring(html=response.text)
        return tree.xpath('//span[@class="sc-igOljT PuBBG"]/text()')[0]

    # electronic first
    if merchant_id == '158':
        response = init_request(store_url,add_header)
        tree = html.fromstring(html=response.text)
        return tree.xpath('//div[@class="efproductprice"]/text()')[0]



    func = {}
    func['94'] = {
            'xpath': '//div[@class="price_list"]/div[@class="price"]',
            'data_location': 'attribute',
            'attribute_name':'content'
    }
    func['9'] = {
        'xpath': '(//div[@class="product-info-price"])[1]',
        'data_location': 'text',
    }
    func['47'] = {
        'xpath': '(//span[@itemprop="price"])[1]',
        'data_location': 'text',
    }
    func['272'] = {
        'xpath1': '(//span[@class="_1fTsyE"]/span[@class="_3RZkEb"])[2]',
        'xpath2': '(//span[@class="_1fTsyE"]/span[@class="_3RZkEb"])[1]',
        'data_location': 'custom_text',
    }
    func['224'] = {
        'xpath': '//meta[@itemprop="price"]',
        'data_location': 'attribute',
        'attribute_name':'content'
    }

    func['13'] = {
        'xpath': '//div[@class="price"]',
        'data_location': 'text',
    }
    func['77'] = {
        'xpath': '//div[@class="product__info__prices__wrapper"]//h2',
        'data_location': 'text',
    }
    func['73'] = {
        'xpath': '//div[@class="price"]',
        'data_location': 'custom_second_instance_text',
    }

    func['67'] = {
        'xpath': '//em[@class="ProductPrice VariationProductPrice"]',
        'data_location': 'custom_second_instance_text',
    }

    func['315'] = {
        'xpath': '(//div[@class="price"]/p[@class="game-price"])[2]',
        'data_location': 'text',
    }

    func['318'] = {
        'xpath': '(//div[@class="price"]/p[@class="game-price"])[2]',
        'data_location': 'text',
    }

    func['40'] = {
        'xpath': '//div[@class="proMoney"]/p',
        'data_location': 'text',
    }

    func['307'] = {
        'xpath': '//div[contains(@class,"field-item ")]',
        'data_location': 'text',
    }

    func['49'] = {
        'xpath': '//span[@class="price_val"]',
        'data_location': 'text',
    }

    func['122'] = {
        'xpath': '//p[@class="special-price"]/span[@class="price"]',
        'data_location': 'text',
    }

    func['63'] = {
        'xpath': '(//div[@class="prices-details"])[2]',
        'data_location': 'text',
    }

    func['228'] = {
        'xpath': '//div[@class="price"]/b/span',
        'data_location': 'text',
    }

    func['126'] = {
        'xpath': '//span[@class="current-price"]',
        'data_location': 'text',
    }

    func['157'] = {
        'xpath': '//span[@data-component="Price"]',
        'data_location': 'text',
    }

    func['61616'] = {
        'xpath': '//span[@class="sc-igOljT PuBBG"]',
        'data_location': 'text',
    }



    try:
        store = func[merchant_id]
    except:
        return 'NoFunction'

    if store['data_location'] == 'text':
        try:
            result = driver.find_element_by_xpath(store['xpath']).text
            return get_digits_only(result)
        except:
            return None

    if store['data_location'] == 'attribute':
        try:
            result = driver.find_element_by_xpath(store['xpath']).get_attribute(store['attribute_name'])
            return get_digits_only(result)
        except:
            return None

    if store['data_location'] == 'custom_text':
        try:
            result = driver.find_element_by_xpath(store['xpath1']).text
            result2 = driver.find_element_by_xpath(store['xpath2']).text
            try:
                if result < result2:
                    return get_digits_only(result)
                else:
                    return get_digits_only(result2)
            except:
                pass

            if result:
                return get_digits_only(result)
            if result2:
                return get_digits_only(result2)
        except:
            return None

    if store['data_location'] == 'custom_second_instance_text':
        result = driver.find_element_by_xpath(store['xpath']).text
        return get_digits_only(result,1)

    

def get_digits_only(result,instance = 0):
    try:
        price = re.findall("\d+\D\d+", result)[instance]
    except:
        price = re.findall("\d+\D\d+", result)[0]
    return price.replace(",",".")
