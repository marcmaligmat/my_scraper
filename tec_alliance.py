import scrapy
import csv,json,time

from scrapy.exceptions import CloseSpider
from scrapy.selector import Selector
from scrapy_selenium import SeleniumRequest
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException

#login
#loop via links.csv and getting the index in outputcsv
#gotolink
    #click vehicle linkages
    #get data in pop up


API_KEY = "<API>"
LINK_FILE_NAME = 'tec_alliance_links_test.csv'
INPUT_CSV = 'tec_alliance_rescrape_links.csv'
OUTPUT_CSV = 'tec_alliance_rescrape_output.csv'

class TecAlliance(scrapy.Spider):
    name = 'tec_alliance'
    start_try = 1
    try_limit = 3
    rcount = ''
    target_link = ''

    def start_requests(self):
        yield SeleniumRequest(
            url='https://web.tecalliance.net/',
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36', 
            },
            callback=self.parse
        )

    def parse(self,response):
        self.driver = response.meta['driver']
        self.login()

    def login(self):
        self.myprint('LOGGING IN')
        self.driver.get('https://web.tecalliance.net/abakusautolamp/en/login')
        self.driver.set_window_size(1920, 1300)
        self.wait(10)
        try:
            self.driver.find_element_by_xpath("//button[@id='ppms_cm_reject-all']").click()
        except WebDriverException as e:
            self.myprint('Just Continue')
            
        self.wait(2)
        self.driver.find_element_by_xpath("//input[@id='userName']").send_keys('user')
        self.wait(2)
        self.driver.find_element_by_xpath("//input[@id='password']").send_keys('password')
        self.wait(2)
        self.driver.find_element_by_xpath("//button[contains(@class,'btn-sm')]").click()
        self.wait(5)
        self.process_links()

    def process_links(self):
        #check existing links
        with open(OUTPUT_CSV) as f:
            row_count = sum(1 for line in f)
            self.rcount = row_count + 1
        with open(INPUT_CSV, 'r') as read_obj:
            csv_reader = list(csv.reader(read_obj))
            self.stop_if_not_in_sync(row_count)
                
            for row in csv_reader[row_count:]:
                print('----------------------STARTING OF A LOOP------------------------------------------------------------------')
                self.product_id = row[0]
                self.target_link = row[1]

                self.myprint(f'GETTING LINK:{self.target_link}')
                self.driver.get(self.target_link)
                self.wait(3)
                #check if still logged in
                try:
                    if self.driver.find_element_by_xpath("//h3[@class='text-left text-secondary']"):
                        self.myprint('RESTARTING REQUEST')
                        return self.login()

                except WebDriverException as e:
                    self.myprint('Still Logged In')
                    self.get_final_data()
                    print(e)
                    
        
    
    def get_final_data(self):
        try:
            clickables = self.driver.find_elements_by_xpath("//i[@class='ta-icon icon-favorite ta-icon-open-window link pr-2']")
            self.final_data = [self.product_id]
            self.listToString = 'no_data_available'
            if clickables:
                tecdoc_num = []
                for clickable in clickables:
                    clickable.click()
                    self.myprint(f'CLICKABLE FOUND')
                    self.wait(1)
                    #get text here
                    resp = Selector(text=self.driver.page_source)
                    number_list = resp.xpath("//tr[@class='ng-star-inserted']/th[4]/text()").getall()
                    for number_data in number_list:
                        tecdoc_num.append(number_data)
                    self.wait(1)
                    webdriver.ActionChains(self.driver).send_keys(Keys.ESCAPE).perform()
                    self.wait(1)
                    self.listToString = '|'.join([str(elem) for elem in tecdoc_num])

                self.write_row()
                    
                    
            else:
                if self.start_try < self.try_limit:
                    self.myprint(f'NO CLICKABLE TRYING TO RESTART, TRIES: {self.start_try}')
                    self.wait(2)
                    self.start_try += 1
                    self.get_final_data()
                else:
                    self.myprint(f'NO AVAILABLE DATA AFTER {self.start_try} TRIES!')
                    self.start_try = 1
                    self.write_row()

        except WebDriverException as e:
            self.myprint('RESTARTING REQUEST')
            return self.login()
            print(e)

        
    def stop_if_not_in_sync(self,row_count):
        with open(OUTPUT_CSV, 'r') as read_obj:
            csv_reader= list(csv.reader(read_obj))
            if len(csv_reader) == 0:
                return
            last_row_output = csv_reader[row_count-1]

        with open(INPUT_CSV, 'r') as read_obj:
            csv_reader= list(csv.reader(read_obj))
            last_row_input = csv_reader[row_count-1]

        if last_row_output[0] != last_row_input[0]:
            raise CloseSpider('CSV OUTPUT AND INPUT IS NOT IN SYNC')

        
            
    def write_row(self):

        self.final_data.append(self.listToString)
        self.final_data.append(self.target_link)
        with open(OUTPUT_CSV,'a', newline='',encoding="utf-8") as output_file:
            writer = csv.writer(output_file)
            if (writer.writerow(self.final_data)):
                self.myprint(f'ADDED ROW IN CSV OUTPUT {self.final_data}')
                self.rcount += 1

        
    def wait(self,mytime):
        print( '_____________________________________________________________________________________________')
        print(f'|||||| SLEEPING {mytime} SECONDS ROW#: {str(self.rcount)} LINK: {self.target_link}')
        time.sleep(int(mytime))

    def myprint(self,message):
        print( '_____________________________________________________________________________________________')
        print(f'|||||| {message}')

    
        