#### ###############
## TESTING STORES
####################
import importlib
# from utils import get_store_function
# need to add cdkeysales 176
# store_url = 'https://whatismyipaddress.com/'
headless = True
store_url = 'https://www.eneba.com/steam-resident-evil-village-resident-evil-8-steam-key-europe'
merchant_id = 272
modules_location = 'stores'
def parse_price():
    price = None
    store_function = get_store_function(modules_location, merchant_id)
    module = importlib.import_module(store_function)
    result = module.get_price(url = store_url,edition='champion')
    # try:
    #     price = module.get_price(url = store_url,edition='champion')
    # except:
    #     message = 'Cannot Find Price'


    
    print(result["message"])
    print(result["price"])
parse_price()



###################
### Testing firefox
##################
# from selenium import webdriver
# from selenium.webdriver.firefox.options import Options
# options = Options()
# options.binary_location = r'C:\Program Files\Mozilla Firefox\firefox.exe'
# driver = webdriver.Firefox(executable_path=r'geckodriver.exe', firefox_options=options)
# driver.get('http://google.com/')


###################
### Testing re
##################
# import re

# string =" VariationList[4702] = { combination: '648',  saveAmount: '',  price: '£21.40',  sku: 'Minecraft_Windows_10_Edition_retail_key',  weight: '0.00 LBS',  thumb: '',  image: '',  instock: true};"
# string += "VariationList[4703] = { combination: '649',  saveAmount: '£11.43',  price: '£7.56',  sku: 'Minecraft_Windows_10_Edition_VPN_argentina_key',  weight: '0.00 LBS',  thumb: '',  image: '',"

# results = re.findall(r"price:\s\'\D(\d+\D\d+)\'\,\s+sku\:\s+\'([^\,]*)\'", string)
# url_tier = 'Minecraft_Windows_10_Edition_retail_key'
# print(list(results[0])[0])
# if len(results) > 1:
#     for res in results:
#         res = list(res)
#         if url_tier == res[1]:
#             print(res[0])
#             break
# else:
#     list(results[0])[0]
# 
# print(list(m[1]))
# print(len(m))

###################
### Testing if statement
##################
# difference = float(10.01) - float(10.00)
# if difference != 0:
#     print(difference)

###################
### Testing request with user pass
##################
# import requests
# import json
# api = f"https://www.gg.deals/admin/bot_de_v2/marc_api.php?game_id=281"
# r = requests.get(api,auth=(USER,PASS))
# print(json.loads(r.text))

###################
### Testing if Print
##################

# message = "32-4\nwww.google.com\n\tprice 44\nwww.yahoo.com\n\tprice 43"
           

# print(message)

# from time import sleep

# def progress(percent=0, width=30):
#     left = width * percent // 100
#     right = width - left
#     print('\r[', '#' * left, ' ' * right, ']',
#           f' {percent:.0f}%',
#           sep='', end='', flush=True)

# for i in range(101):
#     progress(i)
#     sleep(0.2)

# print('\r[', '#' * 3, ' ' * 5, ']',
#           f' {0:.0f}%',
#           sep='', end='', flush=True)