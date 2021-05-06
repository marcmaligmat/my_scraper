import scrapy
from scrapy_selenium import SeleniumRequest


class ExampleSpider(scrapy.Spider):
    name = 'example'

    def start_requests(self):
        yield SeleniumRequest(
            url ='https://duckduckgo.com',
            wait_time=3,
            screenshot=True,
            callback=self.parse
        )

    def parse(self, response):
        # print(response.body)
        # img = response.meta['screenshot']
        # print(img)
        # with open('screenshot.png', 'wb') as f:
        #     f.write(img)
        print(response.meta)
        driver = response.meta['driver']
        search_input = driver.find_element_by_xpath("//input[@id='search_form_input_homepage']")
        search_input.send_keys('Hello World')

        driver.save_screenshot('after_filling_input.png')