from utils import get_digits_only
# from ..allkeyshop import AllkeyShop 
merchant_id = 13


def get_price(**kwargs):
   xpath = '//div[@class="price"]/text()'
   self = kwargs['self']
   self.init_request()
   price = self.parse_response_xpath(xpath)[0]
   self.price = get_digits_only(price)
   return self

