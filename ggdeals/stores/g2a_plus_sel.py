from utils import ( init_request, parse_response_xpath, 
                    get_digits_only, randomize_selenium_proxies)
from my_driver import driver_wait_xpath, run_driver
import time
merchant_id = 61616



def get_price(**kwargs):
    url = kwargs['url']
    driver = run_driver(randomize_selenium_proxies, False)
    try:
        driver.get(url)
    except:
        print("cannot load url")
        driver.close()
        driver.quit()
    xpath = '//span[@class="sc-igOljT PuBBG"]'
    
    price = driver_wait_xpath(driver,xpath).text
    

    time.sleep(4)
    driver.close()
    driver.quit()
    time.sleep(1)
    return get_digits_only(price)
