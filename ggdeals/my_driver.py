import os
import random
import re
import time
import zipfile
import config

import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from utils import generate_extension, randomize_selenium_proxies


def run_driver(proxy,headless = False):

    # path_to_chromedriver_binary = 'driver/chromedriver' 
    options = Options()

    #removing images
    chrome_prefs = {}
    options.experimental_options["prefs"] = chrome_prefs
    chrome_prefs["profile.default_content_settings"] = {"images": 2}
    chrome_prefs["profile.managed_default_content_settings"] = {"images": 2}
    
    

    options.binary_location = config.path_to_chrome_binary
    options.headless = headless
    options.add_argument("--proxy-server=%s" % randomize_selenium_proxies())
    options.add_argument("--log-level=3")
    
    options.add_argument("--enable-popup-blocking")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36")

    #optional
    options.add_argument("disable-infobars")
    options.add_argument("window-size=1400,600")
    options.add_argument("no-sandbox")
    options.add_argument("disable-dev-shm-usage")
    options.add_argument("disable-gpu")

    driver = webdriver.Chrome(
        executable_path = config.path_to_chromedriver_binary,
        options=options,
    )
    driver.implicitly_wait(30)
    driver.set_page_load_timeout(60)
    
    # driver.maximize_window()
    return driver


def driver_wait_xpath(driver,xpath,time=1):
    try:
        driver.find_element_by_xpath(xpath)
    except:
        print('Cannot Find price')
        driver.close()
        driver.quit()

    return driver
    # wait =  WebDriverWait(driver,time)
    # return wait.until(lambda driver: driver.find_element_by_xpath(xpath))
    
# class MyDriverWithCredentials(object):
#     def run_driver(proxy,credentials):
#         path_to_chrome_binary = 'C:/Program Files/Google/Chrome/Application/chrome.exe' 
#         path_to_chromedriver_binary = 'driver/chromedriver' 
#         extension_name = generate_extension(proxy, credentials)
#         options = Options()

#         #removing images
#         chrome_prefs = {}
#         options.experimental_options["prefs"] = chrome_prefs
#         chrome_prefs["profile.default_content_settings"] = {"images": 2}
#         chrome_prefs["profile.managed_default_content_settings"] = {"images": 2}

#         options.binary_location = path_to_chrome_binary
        
#         ###uncomment if need proxy
#         options.add_extension(extension_name)
        
#         options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36")
#         driver = webdriver.Chrome(
#         executable_path = path_to_chromedriver_binary,
#         options=options,
#         )
#         return driver



        

    


  