from utils import get_digits_only

merchant_id = 701

def get_price(**kwargs):
    xpath = '//span[contains(text(),"Availa")]/preceding-sibling::span/span[@class="price_current"]/text()'
    self = kwargs['self']
    self.init_request()
    price = self.parse_response_xpath(xpath)[0]
    self.price = get_digits_only(price)
    self.price *= 1.15
    return self