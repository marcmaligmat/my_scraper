import csv
import json
import math
import re
from time import sleep
from urllib.parse import urljoin

import urllib3
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import config
from driver.driver import build_driver
from steps.login import login
from utils import get_job_links
import os


# sleep(2000)
job_post_file = './output/job_post_links.csv'
if os.path.exists(job_post_file):
    os.remove(job_post_file)

output_file = './output/output.csv'
if os.path.exists(output_file):
    os.remove(output_file)

def append_jobs_list(job_lists):
    
    with open(job_post_file,'a+', newline='',encoding="utf-8") as output_file:
        print(f"Found {len(job_lists)} Jobs")

        writer = csv.writer(output_file)
        for _job_list in job_lists:
            _link = _job_list.get_attribute('href')
            cleaned_job_links = re.sub("\?.+$","",_link)
            writer.writerow([cleaned_job_links])


def run():
    driver = build_driver('./driver/chromedriver')

    driver = login(driver,config.li_username,config.li_password)
    driver.add_cookie({
                'name': 'li_at',
                'value': config.li_value,
                'domain': '.www.linkedin.com'
            })
    driver.maximize_window()
    sleep(2)
    # sitekey =3117BF26-4762-4F5A-8ED9-A85E69209A46
    
    driver.get(config.starting_url)
    sleep(2)


    append_jobs_list(get_job_links(driver))


    sleep(2)

    

    buttons = driver.find_elements_by_xpath('//ul[@class="artdeco-pagination__pages artdeco-pagination__pages--number"]//button')
    num_buttons = int(len(buttons))
    # print(len(buttons))
    
    start = 0
    i = 1
    while i in range(0,num_buttons):
        i += 1
        print(f"pagination for {i}")
        start += 25
        driver.get(f"{config.starting_url}&start={start}")
        sleep(3)
        append_jobs_list(get_job_links(driver))
        sleep(3)
 
    
    

    sleep(2)

    # driver = login(driver,config.li_username,config.li_password)
    with open('./output/job_post_links.csv', 'r') as read_obj:
        csv_reader = list(csv.reader(read_obj))
        for row in csv_reader:
            job_post_link = row[0]
            driver.get(job_post_link)
            print(f"scraping Job Post Link: {job_post_link}")
            sleep(3)
            driver.find_element_by_xpath('//div[@class="p5"]/a').click()  
            
            # Wait for initialize, in seconds
            wait = WebDriverWait(driver, 10)
            about_accordion = wait.until(EC.visibility_of_element_located((By.XPATH, '//ul[@class="org-page-navigation__items "]/li[2]')))
            about_accordion.click()


            # driver.find_element_by_xpath('//ul[@class="org-page-navigation__items "]/li[2]').click()
            sleep(2)
       
            try:
                website = driver.find_element_by_xpath('//dt[text() = "Website"]/following-sibling::dd/a').get_attribute('href')
            except:
                website = 'N/A'
                

            try:
                phone = driver.find_element_by_xpath('//dt[text() = "Phone"]/following-sibling::dd/a/span[1]').text
            except:
                phone = 'N/A'
                
            

            try:
                employees_num = driver.find_element_by_xpath('//dt[text() = "Company size"]/following-sibling::dd[1]').text
            except:
                employees_num = 'N/A'
                

            try:
                emp_in_linkedin = driver.find_element_by_xpath('//dt[text() = "Company size"]/following-sibling::dd[2]').text
                emp_in_linkedin = re.search('\d.*\D?\d+\s+on\s+LinkedIn', emp_in_linkedin, flags=re.IGNORECASE).group(0)
            except:
                emp_in_linkedin = 'N/A'
                print('No employees found in LinkedIN')

            
            #go to the list of employees page
            sleep(2)

            try:
                driver.find_element_by_xpath('//div[contains(@class,"org-top-card__primary-content")]/following-sibling::div//a').click()
            except:
                try:
                    driver.find_element_by_xpath('//div[contains(@class,"org-top-card-listing__summary")]//a').click()
                except:
                    print("Bad data, skip this")
                    employees_list = 'Bad Data'
                    final_data = []
                    final_data.append(job_post_link)
                    final_data.append(website)
                    final_data.append(phone)
                    final_data.append(employees_num)
                    final_data.append(emp_in_linkedin)
                    final_data.append(employees_list)
                    with open('./output/output.csv','a+', newline='',encoding="utf-8") as output_file:
                        writer = csv.writer(output_file)
                        writer.writerow(final_data)
                    continue
                

                

            print(f"scraping Company Page: {driver.current_url}")
            sleep(2)
            employees = driver.find_elements_by_xpath('//a[@class="app-aware-link"]/span/span[1]')
            employees_list = [obj.text for obj in employees]
            sleep(2)

            final_data = []
            final_data.append(job_post_link)
            final_data.append(website)
            final_data.append(phone)
            final_data.append(employees_num)
            final_data.append(emp_in_linkedin)
            final_data.append(employees_list)
            with open('./output/output.csv','a+', newline='',encoding="utf-8") as output_file:
                writer = csv.writer(output_file)
                writer.writerow(final_data)




            sleep(5)

if __name__ == '__main__':
    run()
    # try:
    #     run()
    # except Exception as e:
        
    #     print('There was a problem')
    #     print(e)
        