from utils import get_digits_only

merchant_id = 272


def get_price(**kwargs):
    self = kwargs['self']
    # xpath = '(//span[@class="_1fTsyE"]/span[@class="_3RZkEb"]/text())[1]'
    # xpath2 = '(//span[@class="_1fTsyE"]/span[@class="_3RZkEb"]/text())[2]'
    xpath = '(//meta[@itemprop="price"]/@content)[1]'
    xpath2 = '(//meta[@itemprop="price"]/@content)[2]'
    response = self.init_request()

    price = self.parse_response_xpath(xpath)[0]

    try:
        price2 = self.parse_response_xpath(xpath2)[0]

        if price2 and get_digits_only(price2) < get_digits_only(price):
            price = price2
            
        self.message += "\n Have Second price"
    except:
        self.message += "\n No Second price"

    self.price = get_digits_only(price)
    return self
