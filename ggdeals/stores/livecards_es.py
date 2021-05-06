from utils import get_digits_only

merchant_id = 315

def get_price(**kwargs):
   xpath = '(//div[@class="price"]/p[@class="game-price"]/span[@class="the-price"]/text())[2]'
   self = kwargs['self']
   self.init_request()
   price = self.parse_response_xpath(xpath)[0]
   self.price = get_digits_only(price)
   return self
