from utils import get_digits_only

merchant_id = 174

def get_price(**kwargs):
   xpath = '//div[@class="price"]/text()'
   self = kwargs['self']
   self.url = f"{self.url}?currency=EUR"
   self.init_request()
   price = self.parse_response_xpath(xpath)[0]
   self.price = get_digits_only(price)
   return self