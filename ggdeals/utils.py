import hashlib
import zipfile
import re
import glob, os
from lxml import html
import time
import random
import requests
from proxies import proxies
import config






# def randomize_request_proxies(renewed_proxy=''):
#     """
#     Set a random number to choose a proxy.
#     If there is renewed proxy (because of blocked IP), there would be need to
#     create new random number.
#     """
#     if renewed_proxy:
#         random_number = renewed_proxy
#     else:
#         first_random_number = get_random_number()
#         random_number = first_random_number
    
#     proxy = proxies[random_number]

#     request_proxy = {'http':f'http://{config.PROXY_USERNAME}:{config.PROXY_PASS}@{proxy}',
#                     'https':f'http://{config.PROXY_USERNAME}:{config.PROXY_PASS}@{proxy}'}
#     return {
#         'request_proxy':request_proxy,
#         'message': f"PROXY NUMBER {random_number}"
#     }




    
def randomize_selenium_proxies():
    random_number = get_random_number()
    print(f"PROXY NUMBER {random_number}")
    return proxies[random_number]

def get_random_number():
    """
    Creates a first random number that will be set as a Global Variable
    To be used on different functions as reference
    """
    global first_random_number
    first_random_number = random.randrange(0,len(proxies))
    ###add static random number for testing purposes of proxies
    # first_random_number = 5
    first_random_number = 0
    return first_random_number

def compile_message(response,xpath,message):
    message += "\n"
    message += str(response.status_code)
    parse_response_xpath(response,xpath,new_ip,message)




def get_store_function(modules_location,merchant_id):

    if 'stores' not in os.getcwd():
        os.chdir("./stores")
    for file in glob.glob("*.py"):
        lines = open(file, 'r').readlines()
        for line in lines:
            if 'merchant_id' in line:
                file_id = re.search("\d+", line)

                if int(merchant_id) ==  int(file_id[0]):
                    module = f"{modules_location}.{(file.replace('.py',''))}"
                    return module
                break


def parse_headers(add_header=''):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36',
        
        'Accept-Language': 'en-US,en;q=0.9',

        # 'Accept-Encoding': 'gzip, deflate, br'
        # 'Upgrade-Insecure-Requests': '1',
        # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        # 'Cache-Control': 'max-age=0',
        # 'Connection': 'keep-alive',
    }
    if add_header:
        for key,value in add_header.items():
            headers[key]=value
    return headers


def get_digits_only(price):
    '''
    Cleans string type variables. If it is a list, transform it to a string by
    calling its index.
    '''
    try:
        price = re.findall("\d+\D\d+", price)[0]
        price = float(price.replace(",","."))
    except:
        price = None

    return price
























def generate_extension(proxy, credentials):
    ip, port = proxy.split(':')
    login, password = credentials.split(':')
    manifest_json = """
    {
        "version": "1.0.0",
        "manifest_version": 2,
        "name": "Chrome Proxy",
        "permissions": [
            "proxy",
            "tabs",
            "unlimitedStorage",
            "storage",
            "",
            "webRequest",
            "webRequestBlocking"
        ],
        "background": {
            "scripts": ["background.js"]
        },
        "minimum_chrome_version":"22.0.0"
    }
    """

    background_js = """
    var config = {
            mode: "fixed_servers",
            rules: {
            singleProxy: {
                scheme: "http",
                host: "%s",
                port: parseInt(%s)
            },
            bypassList: ["localhost"]
            }
        };

    chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

    function callbackFn(details) {
        return {
            authCredentials: {
                username: "%s",
                password: "%s"
            }
        };
    }

    chrome.webRequest.onAuthRequired.addListener(
                callbackFn,
                {urls: [""]},
                ['blocking']
    );
    """ % (ip, port, login, password)

    sha1 = hashlib.sha1()
    sha1.update(("%s:%s" % (proxy, credentials)).encode('utf-8'))
    filename = sha1.hexdigest() + ".zip"

    with zipfile.ZipFile(filename, 'w') as zp:
        zp.writestr("manifest.json", manifest_json)
        zp.writestr("background.js", background_js)

    return filename