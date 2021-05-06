from utils import get_digits_only

merchant_id = 62

def get_price(**kwargs):
   xpath = '//div[@class="ust"]/h3/text()'
   self = kwargs['self']
   self.init_request()
   price = self.parse_response_xpath(xpath)[0]
   self.price = get_digits_only(price)
   return self
    