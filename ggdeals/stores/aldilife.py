from utils import get_digits_only

merchant_id = 305

def get_price(**kwargs):
   self = kwargs['self']
   xpath2 = '(//div[@class="product-details__price-subline"]/preceding-sibling::div[1]/text())[2]'
   xpath = '(//div[@class="product-details__price-subline"]/preceding-sibling::div[1]/text())[1]'
   response = self.init_request()

   try:
      price = self.parse_response_xpath(xpath2)[0]
      self.message += "\n Have Second price"
   except:
      price = self.parse_response_xpath(xpath)[0]

   self.price = get_digits_only(price)
   return self