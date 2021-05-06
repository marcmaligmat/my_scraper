import re

from utils import get_digits_only

merchant_id = 67

def get_price(**kwargs):
    self = kwargs['self']
    self.url = f"{self.url}?setCurrencyId=3"
    response = self.init_request()
    results = re.findall(r"price:\s\'\D(\d+\D\d+)\'\,\s+sku\:\s+\'([^\,]*)\'", response.text)
    if len(results) > 0:
        if len(results) > 1:
            for res in results:
                res = list(res)
                if self.buy_url_tier == res[1]:
                    self.price = res[0]
                    break
        else:
            price = list(results[0])[0]
            self.price = float(price)
            
    else:
        xpath = '//em[@class="ProductPrice VariationProductPrice"]/text()'
        try:
            result = self.parse_response_xpath(xpath)
            self.price = get_digits_only(result[1])
        except:
            self.price = get_digits_only(result[0])
            
    return self



    