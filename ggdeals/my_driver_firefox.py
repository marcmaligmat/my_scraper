import os
from seleniumwire import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utils import randomize_selenium_proxies
from fake_useragent import UserAgent
import config
import time



def run_driver(proxy,headless = False):
    path_to_firefox_binary = config.FIREFOX_BINARY # !!! set this variable !!!
    path_to_geckodriver_binary = r'driver\geckodriver' # !!! set this variable !!!

    useragent = UserAgent()
    profile = webdriver.FirefoxProfile()
    profile.set_preference("general.useragent.override", useragent.random)
    profile.set_preference('permissions.default.image', 2)
    profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')
    wire_options = {
        'proxy': {
            'http': f'http://{config.PROXY_USERNAME}:{config.PROXY_PASS}@{proxy}',
            'https': f'http://{config.PROXY_USERNAME}:{config.PROXY_PASS}@{proxy}',
            'no_proxy': 'localhost,127.0.0.1'
   
        }
    }
    binary = FirefoxBinary(path_to_firefox_binary)

    options = Options()
    options.headless = False
    
    driver = webdriver.Firefox(
        firefox_profile=profile,
        options=options,
        firefox_binary=binary,
        executable_path=path_to_geckodriver_binary,
        seleniumwire_options=wire_options
    )

    driver.implicitly_wait(25)
    driver.set_page_load_timeout(25)
    return driver
    


def driver_wait_xpath(driver,xpath,time=1):
    # wait =  WebDriverWait(driver,time)
    # return wait.until(lambda driver: driver.find_element_by_xpath(xpath))
    return driver.find_element_by_xpath(xpath)


        

    


  