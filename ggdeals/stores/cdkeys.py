from utils import get_digits_only

merchant_id = 9

def get_price(**kwargs):
   xpath = '//div[@class="product-info-price"]//span[contains(@id,"product-price")]/@data-price-amount'
   self = kwargs['self']
   self.init_request()
   price = self.parse_response_xpath(xpath)[0]
   self.price = get_digits_only(price)
   return self

