from lib2to3.pgen2 import driver
from pydoc import classname
from time import sleep, time
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup as Soup
import argparse


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("account", help="used to login ig")
    parser.add_argument("pwd", help="used to login ig")
    parser.add_argument("login_mode", type=int, default=0, help="0=direct login, 1=login through FB")
    parser.add_argument("url", help='the page you want to crawl')
    parser.add_argument('output_name', default='output_data', help='the name of output file')
    args = parser.parse_args()
    driverOptions = webdriver.ChromeOptions()
    driverOptions.add_argument("--disable-popup-blocking")
    driverOptions.add_argument("--incongito")
    driverOptions.add_argument("--headless")
    driverOptions.add_argument("blink-settings=imagesEnabled=false")
    driverOptions.add_argument("--no-sandbox")
    driverOptions.add_argument("--disalbe-gpu")
    driverOptions.add_argument("--log-level=3")
    
    driver = webdriver.Chrome("./chromedriver", options=driverOptions)
    driver.get('https://www.instagram.com/')
    WebDriverWait(driver, 15).until(EC.presence_of_all_elements_located((By.NAME, "username")))
    if args.login_mode == 0:
        element = driver.find_element_by_name("username")
        element.send_keys(args.account)
        element = driver.find_element_by_name("password")
        element.send_keys(args.pwd)
        element.send_keys(Keys.RETURN)        
    else:
        element = driver.find_element_by_class_name('KPnG0')
        element.click()
        WebDriverWait(driver, 15).until(EC.presence_of_all_elements_located((By.ID, "email")))
        element = driver.find_element_by_id("email")
        element.send_keys(args.account)
        element = driver.find_element_by_id("pass")
        element.send_keys(args.pwd)
        element.send_keys(Keys.RETURN)
        
    try:
        WebDriverWait(driver, 15).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.ku8Bn')))
    except:
        print('Some errors have occur, it might be a situation below:')
        print("1. Account/password wrong")
        print("2. IG has blocked you for a while, it usually lasts for a few time like 2 min")
        exit()
    driver.get(args.url)
    try:
        WebDriverWait(driver, 15).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.ltEKP')))
    except:
        print('Some errors have occur, it might be the url entered is wrong')
        exit()
    print("Start crawling..")
    maxCrawTime = 500
    crawTime = 0
    try:
        while crawTime < maxCrawTime:
            WebDriverWait(driver, 8).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "li div.NUiEW")))
            element = driver.find_element_by_css_selector("li div.NUiEW")
            element.click()
            sleep(1.2)
            crawTime += 1
    except:
        print("End crawling..")
    print('Start Parsing..')
    soup = Soup(driver.page_source, 'lxml')
    driver.quit()
    messages = soup.find_all('ul', {'class': 'Mr508'})
    account_names = []
    contents = []
    for message in messages:
        content = message.find('div', {'class': 'MOdxS'})
        contents.append(content.text)
        account_name = message.find('h3', {'class': '_6lAjh'})
        account_names.append(account_name.text)
    print("End Parsing..")
    # print(account_names, contents)
    with open("{a}.csv".format(a=args.output_name), "w", encoding='UTF-8') as file:
        for i in range(len(account_names)):
            file.write('{a}, {b}\n'.format(a=account_names[i], b=contents[i]))
            
    print('Done')        