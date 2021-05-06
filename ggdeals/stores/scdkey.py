from utils import get_digits_only
from urllib.parse import urljoin

merchant_id = 122


def get_price(**kwargs):
   xpath = '//p[@class="special-price"]/span[@class="price"]/text()'
   self = kwargs['self']
   self.url = urljoin(self.url, '?currency=EUR')
   self.init_request()
   price = self.parse_response_xpath(xpath)[0]
   self.price = get_digits_only(price)
   return self

