from utils import get_digits_only

merchant_id = 310

def get_price(**kwargs):
   print("from gamesload")
   self = kwargs['self']
   self.response = self.init_request()
   self.url = self.parse_response_xpath('//a/@href')
   self.url = f"https://www.gamesload.com{self.url[0]}"
   self.url = f"{self.url}?currency=EUR"
   print(self.url)
   xpath = '(//div[@class="buy-block"]//p[@class="price-current"]/text())[1]'
   
   
   self.init_request()
   price = self.parse_response_xpath(xpath)[0]
   self.price = get_digits_only(price)
   return self