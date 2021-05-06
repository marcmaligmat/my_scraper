from utils import get_digits_only

merchant_id = 2

def get_price(**kwargs):
   xpath = '//span[@class="product-sheet-price"]/text()'
   self = kwargs['self']
   self.init_request()
   price = self.parse_response_xpath(xpath)[0]
   self.price = get_digits_only(price)
   return self