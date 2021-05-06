import re
import time

from my_driver import driver_wait_xpath, run_driver
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from utils import (get_digits_only, init_request, parse_response_xpath,
                   randomize_selenium_proxies)

merchant_id = 61


def get_price(**kwargs):
    url = kwargs['url']
    driver = run_driver(randomize_selenium_proxies, False)


    base_url = 'https://www.g2a.com/en/'
    splitted_url = str.split(url,'/')
    url = f"{base_url}{splitted_url[-1]}"
    # url = re.sub(r"g2a.com\/[^\/]+",'g2a.com/en',url)
    print(url)

    try:
        driver.get(url)
    except:
        print("cannot load url")
        driver.close()
        driver.quit()

    driver.execute_script("document.body.style.zoom='50%'")
    time.sleep(2)
    webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
    time.sleep(2)
    
    
    xpath = '//span[@class="sc-igOljT eZYAZY"]'
    xpath2 = '(//span[@class="sc-hmbsMR frTSYm"])[1]'

    price = driver_wait_xpath(driver,xpath).text
    try:
        price2 = driver.find_element_by_xpath(xpath2).text
        if price2 and float(price2) < float(price):
            price = price2
    except:
        print("cannot see second price")

    

    time.sleep(4)
    driver.close()
    driver.quit()
    time.sleep(1)
    return get_digits_only(price)

# from utils import init_request, parse_response_xpath, get_digits_only

# merchant_id = 61


# def get_price(**kwargs):
#     url = kwargs['url']
#     xpath = '(//span[@class="_1fTsyE"]/span[@class="_3RZkEb"]/text())[1]'
#     xpath2 = '(//span[@class="_1fTsyE"]/span[@class="_3RZkEb"]/text())[2]'
#     base_url = 'https://www.g2a.com/en/'
#     splitted_url = str.split(url,'/')
#     url = f"{base_url}{splitted_url[-1]}"

#     print(url)
#     response = init_request(url)
#     print(response)
#     price = get_digits_only(parse_response_xpath(response, xpath)[0])
#     try:
#         price2 = get_digits_only(parse_response_xpath(response, xpath2)[0])
#         if price2:
#             if price2 < price:
#                 price = price2
#     except:
#         pass

    
        
#     return price
