import zipfile
import time
import requests
import random
import re


from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utils import generate_extension

class MyDriver(object):
    def run_driver(proxy,credentials):
        path_to_chrome_binary = 'C:/Program Files/Google/Chrome/Application/chrome.exe' 
        path_to_chromedriver_binary = 'driver/chromedriver' 
        extension_name = generate_extension(proxy, credentials)
        options = Options()

        #removing images
        chrome_prefs = {}
        options.experimental_options["prefs"] = chrome_prefs
        chrome_prefs["profile.default_content_settings"] = {"images": 2}
        chrome_prefs["profile.managed_default_content_settings"] = {"images": 2}

        options.binary_location = path_to_chrome_binary
        options.add_extension(extension_name)
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36")
        driver = webdriver.Chrome(
        executable_path = path_to_chromedriver_binary,
        options=options,
        )
        return driver

    

        

    


  