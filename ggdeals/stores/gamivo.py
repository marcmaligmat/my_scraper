from utils import get_digits_only
import json
import re

merchant_id = 218


def get_price(**kwargs):
    self = kwargs['self']
    original_url = self.url
    url = re.findall(r'[^\/]+$',self.url)[0]
    url = f"https://www.gamivo.com/api/product/product-by-slug/{url}"

    self.url = url
    response = self.init_request()
    data = json.loads(response.text)['offers'][0]
    self.price = data['0']['price']
    try:
        data2 = json.loads(response.text)['offers'][1]
        price2 = data2['0']['price']
        if price2 is not None:
            if float(self.price) > float(price2):
                self.price = price2
    except:
        self.message += '\nNo Second Price'
    self.url = original_url
    return self

