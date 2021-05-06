from utils import get_digits_only

merchant_id = 77

def get_price(**kwargs):
   xpath = '//div[@class="product__info__prices__wrapper"]//h2/text()'
   self = kwargs['self']
   self.init_request()
   price = self.parse_response_xpath(xpath)[0]
   self.price = get_digits_only(price)
   return self
    