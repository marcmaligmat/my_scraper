from utils import ( init_request, parse_response_xpath, 
                    get_digits_only, randomize_selenium_proxies)
from my_driver import driver_wait_xpath, run_driver
import time
merchant_id = 157



def get_price(**kwargs):
    url = kwargs['url']
    price = None
    driver = run_driver(randomize_selenium_proxies)
    try:
        driver.get(url)
    except:
        print("cannot load url")
        driver.close()
        driver.quit()
    
    time.sleep(2)
    xpath = '//span[@data-component="Price"]'
    price = driver_wait_xpath(driver,xpath).text

    time.sleep(2)
    driver.close()
    driver.quit()
    time.sleep(1)
    return get_digits_only(price)

    