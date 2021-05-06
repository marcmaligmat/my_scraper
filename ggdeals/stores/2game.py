from utils import get_digits_only

merchant_id = 12

def get_price(**kwargs):
    self = kwargs['self']
    xpath = '(//div[@class="details-info-left"]//span[@class="price"]/text())[1]'
    xpath2 = '(//div[@class="details-info-left"]//span[@class="price"]/text())[2]'
    self.init_request()


    try:
        price = self.parse_response_xpath(xpath2)[0]
        self.message += "\n Have Second price"
    except:
        price = self.parse_response_xpath(xpath)[0]

    self.price = get_digits_only(price)
    return self
