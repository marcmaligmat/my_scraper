import scrapy
from scrapy.selector import Selector
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
import csv,json,requests,time


API_KEY = "<2captcha api>"
data_sitekey = '33f96e6a-38cd-421b-bb68-7806e1764460'
page_url ='https://www.auto-doc.it'



class GgdealsLinks(scrapy.Spider):
    name = 'autodoc'

    def start_requests(self):
        yield SeleniumRequest(
            
            url='https://autocarri.auto-doc.it/',
            wait_time='3',
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36',
            },
            callback=self.bypass_hcaptcha
        )

    def bypass_hcaptcha(self,response):
        driver = response.meta['driver']
        driver.set_window_size(1920, 1080)
        driver.page_source
        
        u1 = f"http://2captcha.com/in.php?key={API_KEY}&method=hcaptcha&sitekey={data_sitekey}&pageurl={page_url}&json=1&invisible=1"
        r1 = requests.get(u1)
        print(r1.json())
        rid = r1.json().get("request")
        u2 = f"https://2captcha.com/res.php?key={API_KEY}&action=get&id={int(rid)}&json=1"
        time.sleep(10)
        while True:
            r2 = requests.get(u2)
            print(r2.json())
            if r2.json().get("status") == 1:
                token = r2.json().get("request")
                break
            time.sleep(5)
        wirte_tokon_js2 = f"document.querySelector('[name=h-captcha-response]').innerText = '{token}';"
        submit_js = "document.querySelector('.challenge-form').submit()"
        time.sleep(3)
        driver.execute_script(wirte_tokon_js2)
        time.sleep(3)
        driver.execute_script(submit_js)
        time.sleep(10)

        print('getting the exact link')
        with open('product.csv', 'r') as read_obj:
            csv_reader = csv.reader(read_obj)
            limit = 100
            n = 1
            for row in csv_reader:
                if n <= limit:
                    product_id = row[0]
                    query_link = f'https://www.auto-doc.it/ajax/search/autocomplete?query={product_id}'
                    driver.get(query_link);
                    self.log(f'Scraping the Product ID:{product_id}')
                    self.log(f'Scraping the link:{query_link}')
                    response = Selector(text=driver.page_source)
                    result = json.loads(response.xpath('//pre/text()').get())
                    final_link = result['data'][0]['values']['url'] 
                    driver.get(final_link)
                    time.sleep(5)
                    driver.find_element_by_name("").send_keys(Keys.PAGE_DOWN)
                    time.sleep(5)
                    try:
                        driver.find_element_by_xpath("(//div[contains(@class,'accordion-button')])[1]").click()
                    except WebDriverException as e:
                        print('oops. click failed')
                        print(e)

                    
                    time.sleep(5)
                    resp = Selector(text=driver.page_source)
                    number = 1
                    accordion_content = resp.xpath("//div[@class='accordion-content']")
                    final_data = [product_id]
                   
                    for content in accordion_content:
                        
                        result_text=''
                        for text in content.xpath(".//ul/li/b/i[@class='icon arrow']/following-sibling::text()").getall():
                            if number <= len(accordion_content):
                                result_text += text+"\n"
                            else:
                                result_text += text
                            
                        final_data.append(result_text)  
                        number =+ 1

                    with open('output.csv','a', newline='',encoding="utf-8") as output_file:
                        writer = csv.writer(output_file)
                        writer.writerow(final_data)

                n += 1

        print('sleeping 15seconds')
        time.sleep(15)
        print('Closing')
        driver.close()