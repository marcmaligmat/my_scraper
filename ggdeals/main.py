
import importlib
import json
import os
import random
import sys
import time
from concurrent.futures import Future, ProcessPoolExecutor, ThreadPoolExecutor
from lxml import html
import requests

import config
from aks_utils import (clean_url, selenium_stores, skip_stores,
                       stores_dont_clean_url,get_aks_data, parse_headers)
from proxies import proxies
from utils import get_random_number, get_store_function

CONCURRENT_REQUEST = 4
toplinks_start_point = 0
prod_links_start_point = 0

modules_location = "stores"
starting_url = 'https://www.gg.deals/blog/'

target_link = ''
# target_link ='https://www.gamivo.com/product/cyberpunk-2077'
target_link = 'https://www.eneba.com/xbox-sea-of-thieves-anniversary-edition-pc-xbox-one-xbox-key-global?'
#15512
class Ggdeal():
    
    message = "\n------------------------------------------------------------------------------------------"
    def __init__(self, starting_url):
        
        self.top_link_counter = 0
        if target_link:
            self.merchant_id = '272'
            self.buy_url_tier = 'Resident_Evil_Village_Deluxe_Edition_STEAM'
            self.edition = 3
            self.top_link = 'https://www.gg.deals/blog/buy-sea-of-thieves-cd-key-compare-prices/'
            
            if self.merchant_id in stores_dont_clean_url:
                self.url = target_link
            else:
                self.url = clean_url(self.merchant_id, target_link)

            self.aks_price = 0
            self.counter = 0
            self.sent_message_already = False
            self.parse_price()
        else:
            self.url = starting_url
            
            self.start_requests()
        

    def start_requests(self):
        print(f"Getting TOP LINKS of {self.url}")
        links_xpath = '*//div[@id="Top25"]/a/@href'
        self.init_request()
        self.top_links = self.parse_response_xpath(links_xpath)
        self.get_game_data()

    def init_request(self,new_ip=''):
        """
        Receives an Xpath Expression 
        """
        retries = 0
        while retries < 6:
            retries += 1
            time.sleep(1)
            try:
                self.response = requests.get(
                    url = self.url,
                    headers=parse_headers(),
                    proxies=self.randomize_request_proxies(new_ip),
                    allow_redirects=True,
                    timeout = 10
                )
                time.sleep(8)
                return self.response
                
            except requests.ConnectionError as e:
                self.message += "\nOOPS!! Connection Error. Make sure you are connected to Internet. Technical Details given below.\n"
                self.message += f"\n{str(e)}"           
                continue
            except requests.Timeout as e:
                self.message += "\nOOPS!! Timeout Error"
                continue
            except requests.RequestException as e:
                self.message += "\nOOPS!! General Error"
                self.message += f"\n{str(e)}"
                continue
            except KeyboardInterrupt:
                print("Someone closed the program")

    def parse_response_xpath(self,xpath):
        new_ip = self.random_number
        self.message += f" P{new_ip}"
        self.message += f" S{self.response.status_code}"
        while self.response.status_code >= 400:
            self.message += f"\nIP {new_ip} is Blocked, retry request in another IP"
            if int(new_ip) == int(len(proxies) - 1):
                new_ip = 0
            else:
                new_ip += 1
            
            if new_ip == self.first_random_number:
                self.message += "\nALL PROXIES BLOCKED"
                break

            
            self.message += f"\nPROXY NUMBER {new_ip}"
            self.url = self.response.url
            self.response = self.init_request(new_ip)

        tree = html.fromstring(html=self.response.text)
        return tree.xpath(xpath)


    def get_game_data(self):
        for top_link in self.top_links[toplinks_start_point:]:
            self.url = top_link
            self.top_link = top_link
            print(f'Getting ID of {self.url}')
            self.top_link_counter += toplinks_start_point
            game_id_xpath = '//div[contains(@class,"metacritic-button")]/@data-product-id'
            self.init_request()
            self.game_id = self.parse_response_xpath(game_id_xpath)[0]
            self.parse_data(get_aks_data(self.game_id))
            self.top_link_counter += 1

    
    def parse_data(self, data):
        with ProcessPoolExecutor(max_workers=CONCURRENT_REQUEST) as executor:
            for counter, data in enumerate(data[prod_links_start_point:]):
                executor.submit(self.create_async_request,counter,data)
                self.message = "\n------------------------------------------------------------------------------------------"


    def create_async_request(self,counter,data):
        self.merchant_id = data['merchant']
        self.buy_url_tier = data['buy_url_tier']
        self.edition = data['edition']
        self.url = clean_url(self.merchant_id, data['buy_url'])
        self.aks_price = float(data['price'])
        
        self.counter = counter
        self.sent_message_already = False
        self.counter += prod_links_start_point
        

        if self.merchant_id in skip_stores:
            print(f'Skipping this store {self.merchant_id}')
            return

        if self.merchant_id in selenium_stores:
            print(f'Skipping this store needs Selenium {self.merchant_id}')
            return
        
        # if self.merchant_id != '13':
        #     return

        
        self.parse_price()

    def parse_price(self):
        """Actual price parsing on a product url"""
        # print(f"Scraping product link: {self.url} . . . ")
        self.general_message = ''
        price = None
        store_function = get_store_function(modules_location, self.merchant_id)

        
        try:
            module = importlib.import_module(store_function)
        except:
            self.content = "NO FUNCTION YET"
            self.content += f"{self.top_link_counter}-{self.counter} Merchant: {self.merchant_id} {self.message}"
            self.content += f"\n{self.top_link}"
            self.content += f"\n\t{self.aks_price}"
            self.content += f"\n{self.url}"
            self.send_discord_msg(
                self.content, config.discord_lacking_function)

        # self = module.get_price(self=self)
        try:
            self = module.get_price(self=self)

        except:
            self.message += '\nCannot Find Price'
            self.price = None
            self.send_discord_msg(self.message,config.discord_bot_problem)
            
        
        self.create_terminal_message()

        return self.price



    def create_terminal_message(self):
        discord_endpoint = config.discord_bot_problem
        if self.price is not None:
            difference = float(self.aks_price) - float(self.price)
            if difference != 0:
                if abs(difference) > .1:
                    self.general_message = "**PRICE ERROR**"
                    discord_endpoint = config.discord_price_problem
                else:
                    self.general_message = "**SMALL DIFFERENCE**"
                    discord_endpoint = config.discord_bot_small_difference

            else:
                 self.general_message = "Price OK"

        
        self.message += f"\n{self.top_link_counter} - {self.counter} {self.general_message} merchant id:{self.merchant_id}"
        self.message += f"\n{self.top_link}"
        self.message += f"\n\t{self.aks_price}"
        self.message += f"\n{self.url}"
        self.message += f"\n\t{self.price}"
        print(self.message)
        if  self.general_message != 'Price OK':
            self.send_discord_msg(self.message, discord_endpoint)

    def create_discord_message(message=''):
        pass

    def send_discord_msg(self, content, discord_endpoint):
        if self.sent_message_already == False:
            payload = {"content": content, }
            headers = {'authorization': config.DISCORD_AUTH}
            r = requests.post(discord_endpoint, data=payload, headers=headers)
            if r:
                self.sent_message_already = True

        

    

    # def randomize_selenium_proxies():
    #     random_number = get_random_number()
    #     print(f"PROXY NUMBER {random_number}")
    #     return proxies[random_number]

    def randomize_request_proxies(self,renewed_proxy=''):
        """
        Set a random number to choose a proxy.
        If there is renewed proxy (because of blocked IP), there would be need to
        create new random number.
        """
        if renewed_proxy:
            self.random_number = renewed_proxy
        else:
            self.first_random_number = random.randrange(0,len(proxies))
            self.random_number = self.first_random_number

        proxy = proxies[self.random_number]

        return {'http':f'http://{config.PROXY_USERNAME}:{config.PROXY_PASS}@{proxy}',
        'https':f'http://{config.PROXY_USERNAME}:{config.PROXY_PASS}@{proxy}'}
        
        


if __name__ == '__main__':
    aks = AllkeyShop(starting_url)
