from utils import ( init_request, parse_response_xpath, 
                    get_digits_only, randomize_selenium_proxies)
from aks_utils import get_edition_name
from my_driver import driver_wait_xpath, run_driver

import time
import re
import requests


merchant_id = 1


def get_price(**kwargs):
    url = kwargs['url']
    edition = kwargs['edition']
    print(edition)
    

    price = None
    driver = run_driver(randomize_selenium_proxies)
    try:
        driver.get(url)
    except:
        print("cannot load url")
        driver.close()
        driver.quit()
    driver.execute_script('videos = document.querySelectorAll("video"); for(video of videos) {video.pause()}')

    xpath = '(//div[@class="game_purchase_price price"])[1]'
    

    try:
        driver_wait_xpath(driver,'//option[@value="1989"]').click()
        driver_wait_xpath(driver,'//span[contains(text(),"View Page")]').click()
    except:
        pass

    
    if edition != '1':
        edition_name = get_edition_name(edition)
        print(edition_name)
        edition_name = re.sub(r"\s.+","",edition_name)
        print(edition_name)
        xpath2 = f'//div[@class="game_area_purchase_platform"]/following-sibling::h1[contains(text(),"{edition_name}")]/following-sibling::div//div[@class="game_purchase_price price"]'

        try:
            price = driver_wait_xpath(driver, xpath2).text
        except:
            price = driver_wait_xpath(driver, '(//div[@class="game_purchase_action"]//div[@class="discount_final_price"])[1]').text
    else:
        price = driver_wait_xpath(driver, xpath).text

    time.sleep(2)
    driver.close()
    driver.quit()
    time.sleep(1)
    return get_digits_only(price)