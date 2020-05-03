import time

from selenium import webdriver


def find_apartment_urls():
    driver = webdriver.Chrome('/Users/mac/projects/ChromeWebDriver/chromedriver')
    driver.get('https://www.dabangapp.com/search#/map')

    driver.find_element_by_name('keyword').send_keys('성수동1가')
    time.sleep(2)

    button = driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div/div[1]/ul/li[1]/ul/li[1]')
    driver.execute_script("arguments[0].click();", button)
    time.sleep(2)

    button = driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div/div[2]/div[1]/div')
    driver.execute_script("arguments[0].click();", button)
    time.sleep(2)

    button = driver.find_element_by_xpath(
        '/html/body/div[1]/div/div[1]/div/div[2]/div[1]/div[2]/ul[2]/li/label/span[2]')
    driver.execute_script("arguments[0].click();", button)
    time.sleep(2)

    apt_list = []
    for i in range(6):
        apart_urls = driver.find_elements_by_xpath('/html/body/div[1]/div/div[2]/div[1]/div/div[2]/ul/li/div/a')
        for url in apart_urls:
            apt_list.append(url.get_attribute('href'))
        button = driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div[1]/div/div[2]/div/div/div/button[2]')
        driver.execute_script("arguments[0].click();", button)
        time.sleep(2)

    # 성수 2동 시작.
    driver.find_element_by_name('keyword').send_keys('성수동2가')
    time.sleep(2)

    button = driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div/div[1]/ul/li[1]/ul/li[1]')
    driver.execute_script("arguments[0].click();", button)
    time.sleep(2)

    button = driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div/div[2]/div[1]/div')
    driver.execute_script("arguments[0].click();", button)
    time.sleep(2)

    apart_urls = driver.find_elements_by_xpath('/html/body/div[1]/div/div[2]/div[1]/div/div[2]/ul/li/div/a')

    for url in apart_urls:
        apt_list.append(url.get_attribute('href'))
    button = driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div[1]/div/div[2]/div/div/div/button[2]')
    driver.execute_script("arguments[0].click();", button)
    time.sleep(2)

    apart_urls = driver.find_elements_by_xpath('/html/body/div[1]/div/div[2]/div[1]/div/div[2]/ul/li/div/a')
    for url in apart_urls:
        apt_list.append(url.get_attribute('href'))
    driver.close()
    return apt_list


def find_urls():
    driver = webdriver.Chrome('/Users/mac/projects/ChromeWebDriver/chromedriver')
    driver.implicitly_wait(3)
    driver.get('https://www.dabangapp.com/search#/map')
    driver.find_element_by_name('keyword').send_keys('성수동1가')
    driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div/div[1]/ul/li[1]/ul/li[1]').click()
    driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div[1]/div/div[1]/a[1]').click()

    time.sleep(2)
    url_all_list = []
    for i in range(0, 3):
        time.sleep(2)
        seongsoo_1dong_detail_list = driver.find_elements_by_xpath(
            "/html/body/div[1]/div/div[2]/div[1]/div/div[2]/ul/li/div/a")
        for data in seongsoo_1dong_detail_list:
            url_all_list.append(data.get_attribute('href'))
        button = driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div[1]/div/div[2]/div/div/div/button[2]')
        driver.execute_script("arguments[0].click();", button)
    print(len(url_all_list))

    driver.find_element_by_name('keyword').send_keys('성수동2가')
    time.sleep(2)
    driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div/div[1]/ul/li[1]/ul/li[1]').click()
    driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div[1]/div/div[1]/a[1]').click()
    time.sleep(2)
    seongsoo_2dong_detail_list = driver.find_elements_by_xpath(
        "/html/body/div[1]/div/div[2]/div[1]/div/div[2]/ul[2]/li/div/a")
    for data in seongsoo_2dong_detail_list:
        url_all_list.append(data.get_attribute('href'))
    for i in range(0, 2):
        time.sleep(2)
        seongsoo_2dong_detail_list = driver.find_elements_by_xpath(
            "/html/body/div[1]/div/div[2]/div[1]/div/div[2]/ul/li/div/a")
        for data in seongsoo_2dong_detail_list[2:]:
            url_all_list.append(data.get_attribute('href'))
        button = driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div[1]/div/div[2]/div/div/div/button[2]')
        driver.execute_script("arguments[0].click();", button)
    print(len(url_all_list))
    driver.close()
    return url_all_list