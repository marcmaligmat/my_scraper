import csv
import random
from lxml import html
import requests

import scraper.config as config
from scraper.proxies import proxies
import re
from user_agent import generate_user_agent
from decimal import Decimal


def parse_headers(add_header=''):
    headers = {
        'authority': 'www.amazon.com',
        'pragma': 'no-cache',
        'cache-control': 'no-cache',
        'dnt': '1',
        'upgrade-insecure-requests': '1',
        'user-agent': generate_user_agent(),
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'none',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-dest': 'document',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    }
    if add_header:
        for key, value in add_header.items():
            headers[key] = value
    return headers


def randomize_request_proxies(renewed_proxy=''):
    """
    Set a random number to choose a proxy.
    If there is renewed proxy (because of blocked IP), there would be need to
    create new random number.
    """
    if renewed_proxy:
        random_number = renewed_proxy
    else:
        first_random_number = random.randrange(0, len(proxies))
        random_number = first_random_number

    print(random_number)
    proxy = proxies[random_number]

    return {'http': f'http://{config.PROXY_USERNAME}:{config.PROXY_PASS}@{proxy}',
            'https': f'http://{config.PROXY_USERNAME}:{config.PROXY_PASS}@{proxy}'}


def scrape(**kwargs):
    url = kwargs['url']
    print(f"scraping {url}")
    response = requests.get(
        url=url,
        headers=parse_headers(),
        # proxies=randomize_request_proxies(),
        allow_redirects=True,
        timeout=60
    )

    print(response)
    with open("file.html", "w") as file:
        file.write(response.text)

    tree = html.fromstring(html=response.text)
    title = tree.xpath(
        'normalize-space(//span[@id="productTitle"]/text())')

    blocked_but_200status = re.findall(
        r"To discuss automated access to Amazon data please contact api-services\-support\@amazon.com", response.text)

    blocked_but_200status2 = re.findall(
        r"Sorry\! Something went wrong\!", response.text)

    if blocked_but_200status:
        title = "blocked but 200 status"

    if blocked_but_200status2:
        title = "blocked but 200 status2"

    descriptions = tree.xpath(
        '//div[@id="feature-bullets"]//span[@class="a-list-item"]/text()')

    availability = tree.xpath(
        'normalize-space(//div[@id="availability"]/span/text())')

    print(availability)
    price = 0
    if re.findall(r'(\d+ left in stock|In Stock\.)', availability):
        availability = 1
    else:
        availability = 0

    try:
        price = tree.xpath(
            '//span[@id="priceblock_saleprice" or @id="priceblock_ourprice"]/text()')[0]
    except Exception as e:
        print("Price 1 not available trying next")
        print(e)

    try:
        price = tree.xpath(
            '//span[@id="price" or @id="price_inside_buybox"]/text()')[0]
    except Exception as e:
        print("Price 2 not available trying next ")
        print(e)

    try:
        price = tree.xpath(
            # '//span[contains(@id,"color_name") and contains(@class,"a-color-price")]/span/br/following-sibling::text()')
            '//span[contains(@id,"color_name")]/span/br/following-sibling::text()')[0]
    except Exception as e:
        print("Price 3 no more ")
        print(e)

    if price is None:
        availability = 0

    image_links = re.findall(
        r"large\"\:\"(https\:\/\/images\-na\.ssl\-images\-amazon.com.*?\.jpg)", response.text)

    # Title, Description, Current Price, All Image Links, and Stock (Boolean if item is available or not).

    # new_description = '|'.join([str(elem.replace("\n", ""))
    #                             for elem in description])

    # new_images_link = '|'.join([str(elem.replace("\n", ""))
    #                             for elem in images_link])

    description_list = []
    for description in descriptions:
        desc = description.replace("\n", "")
        if desc == "":
            continue
        else:
            description_list.append(desc.replace("\"", ""))

    images_list = []
    for image_link in image_links:
        images_list.append(image_link)

    row = []
    price = get_digits_only(price)
    row.append(str(title))
    row.append(price)
    row.append(availability)
    row.append(kwargs['url'])
    # row.append(str(new_description))

    # row.append(new_images_link)

    print(len(row))
    print(f"Price is {price}")
    print(type(description))
    return {
        'price': price,
        'availablity':  availability,
        'url': url,
        'description_list': description_list,
        'images_list': images_list
    }


def get_digits_only(price):
    '''
    Cleans string type variables. If it is a list, transform it to a string by
    calling its index.
    '''
    try:
        price = re.findall("\d.*\,?\d+\D\d+", price)[0]

    except:
        price = None
    price = Decimal(price.replace(",", ""))
    return price
