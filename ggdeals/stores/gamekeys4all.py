from utils import get_digits_only
import json
import re

merchant_id = 31

def get_price(**kwargs):
   xpath = '//span[@id="our_price_display"]/text()'
   self = kwargs['self']
   self.init_request()
   price = self.parse_response_xpath(xpath)[0]
   self.price = get_digits_only(price)
   return self
    
