from utils import init_request, parse_response_xpath, get_digits_only

merchant_id = 81

def get_price(**kwargs):
    url = kwargs['url']
    xpath = '//a[contains(text(),"Add")]/following-sibling::span/text()'
    header = {
        'cookie': '__cfduid=dd06096eb608cb4e05b104d028156d3881619061150; GameBilletCustomer=23e02088-e938-42fc-8061-6ec3c5d4be6a; __utma=198222521.1998871804.1619061155.1619061155.1619061155.1; __utmc=198222521; __utmz=198222521.1619061155.1.1.utmcsr=allkeyshop.com|utmccn=(referral)|utmcmd=referral|utmcct=/; __utmt=1; __utmb=198222521.5.10.1619061155',
        'accept-encoding': 'gzip, deflate, br',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'cache-control': 'max-age=0',
        'referer': 'https://www.allkeyshop.com/',
        'sec-ch-ua': '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'cross-site',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1'
    }
    response = init_request(url,add_header=header)
    print(response)
    print(response.request.headers)
    # price = parse_response_xpath(response, xpath)[0]
    # price = get_digits_only(price)
    # return price

# from utils import ( init_request, parse_response_xpath, 
#                     get_digits_only, randomize_selenium_proxies)
# from my_driver import driver_wait_xpath, run_driver
# import time
# merchant_id = 81



# def get_price(url,headless=False):
#     price = None
#     driver = run_driver(randomize_selenium_proxies)
#     driver.get(url)

#     time.sleep(150)
#     xpath = '//a[contains(text(),"Add")]/following-sibling::span'
#     price = driver_wait_xpath(driver,xpath).text

#     time.sleep(2)
#     driver.close()
#     driver.quit()
#     time.sleep(1)
#     return get_digits_only(price)

