from time import sleep

def html_screenshot(driver):
    with open("file.html", "w+") as file:
        file.write(driver.page_source)

def slow_scroll(driver):
    scr1 = driver.find_element_by_xpath('/html/body/div[6]/div[3]/div[3]/div/div/section[1]/div/div')
    speed = 1
    current_scroll_position, new_height= 0, 1
    while current_scroll_position <= new_height:
        current_scroll_position += speed
        driver.execute_script(f"arguments[0].scrollBy(0,{current_scroll_position})", scr1)
        new_height = driver.execute_script("return document.body.scrollHeight")
    sleep(1)

    return driver

def get_job_links(driver):
    driver = slow_scroll(driver)
    sleep(2)
    return driver.find_elements_by_xpath('//ul[@class="jobs-search-results__list list-style-none"]//div[contains(@class, "artdeco-entity-lockup__title")]/a')

def scroll_to_bottom(driver):
    SCROLL_PAUSE_TIME = 2

    results_tab = driver.find_element_by_xpath('//div[@class="jobs-search-results display-flex flex-column"]')

    driver.execute_script("arguments[0].scrollIntoView();", results_tab )

    # # Get scroll height
    # last_height = driver.execute_script("return document.body.scrollHeight")

    # while True:
    #     # Scroll down to bottom
    #     driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    #     # Wait to load page
    #     sleep(SCROLL_PAUSE_TIME)

    #     # Calculate new scroll height and compare with last scroll height
    #     new_height = driver.execute_script("return document.body.scrollHeight")
    #     if new_height == last_height:
    #         break
    #     last_height = new_height

    return driver