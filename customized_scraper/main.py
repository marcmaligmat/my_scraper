import json
import os
import random
import requests
import time
from my_driver import MyDriver
from stores import *

name = "name"
discord_auth = '<AUTH>'
# discord_bot_team = "https://discord.com/api/v8/channels/<DISCORD ID>/messages"

discord_bot_team = 'https://discord.com/api/v8/channels/<DISCORD ID>/messages'
discord_claveria = 'https://discord.com/api/v8/channels/<DISCORD ID>/messages'

def start_requests(driver):
    driver.get('https://gg.deals')
    time.sleep(6)
    links = driver.find_elements_by_xpath("*//div[@id='Top25']/a")
    parse_links(driver,links)

def parse_links(driver,links):
    top_links = [link.get_attribute("href") for link in links]
    for top_link in top_links:
        print(top_link)
        driver.get(top_link)
        time.sleep(8)
        game_id = driver.find_element_by_xpath(
            '(//div[contains(@class,"metacritic-button")])[1]'
            ).get_attribute('data-product-id')
        website_data = get_website_data(game_id)
        # print(website_data)
        time.sleep(20)
        parse_prices(driver,website_data,top_link)
        

def parse_prices(driver,website_data,top_link):
    for data in website_data:
        website_price = data['price']
        merchant_id = data['merchant']
        store_url = data['buy_url']
        data['website_link'] = top_link

        if merchant_id in skip_stores:
            continue
        
        store_url = clean_url(merchant_id,store_url)
        print(f"Merchant ID: {merchant_id}  Going to {store_url} ")
        if merchant_id not in api_stores:
            driver.get(store_url)
        time.sleep(8)
        store_price = get_store_price(driver,merchant_id,store_url)
        
        data['store_price'] = store_price
        create_discord_message(data)

def create_discord_message(data):
    discord_endpoint = discord_claveria
    main_message = ''
    if data['store_price'] == None:
        main_message =  "**HAVE XPATH BUT WRONG**"
    elif data['store_price'] == 'NoFunction':
        main_message = "**CREATE XPATH FUNCTION**"

    elif float(data['price']) != float(data['store_price']):
        main_message = "**PRICE ERROR**"
        discord_endpoint = discord_bot_team

    main_content = f""">>> {main_message} STORE ID = {data['merchant']}
website LINK = {data['website_link']}
    website PRICE = {data['price']}
STORE LINK = {data['buy_url']}
    STORE PRICE = {data['store_price']}
    """
    print(main_content)
    if main_message:
        send_discord_msg(main_content,discord_auth,discord_endpoint)

def send_discord_msg(content,discord_auth,discord_endpoint):
    payload = {
        "content":content,
    }
    headers = {
        'authorization': discord_auth
    }
    r = requests.post(discord_endpoint, data=payload, headers=headers)
    print(content)

def get_api_data(game_id):
    api=f"https://my.com/marc_api.php?game_id={game_id}&version={time.time()}"
    r = requests.get(api)
    return json.loads(r.text)


def main():
    proxies = [

    '102.165.1.59:5432',
    '102.165.5.104:5432',
    '179.61.138.115:5432'
    ]
    proxy = proxies[random.randrange(0,len(proxies))]
    credentials = "username:password"
    driver = MyDriver.run_driver(proxy,credentials)
    start_requests(driver)


if __name__ == '__main__':
    print(os.path.dirname(os.path.abspath(__file__)))
    print(f"Starting {name} Bot!")
    main()
    print("Bye!")
    