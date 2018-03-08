from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import xlsxwriter
import re
import time

username = "ramavatar000111"
password = "ramavatar@123"
first_username_to_search = "priya.p.varrier"
first_userprofile_link = "https://www.instagram.com/priya.p.varrier/"

def login(driver):
    driver.get('https://www.instagram.com/')
    delay = 5 #seconds
    try:
        myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.LINK_TEXT, 'Log in')))
        print("Page is ready!")
    except TimeoutException:
        print("Loading took too much time!\n\n")
        
    html = driver.page_source
    soup = BeautifulSoup(html, "html5lib")
    ele =  driver.find_element_by_xpath("//a[@href='/accounts/login/']")
    ele.click()
    
    driver.find_element_by_xpath("//input[@name='username']").send_keys(username)
    driver.find_element_by_xpath("//input[@name='password']").send_keys(password)
    
    login_btn = driver.find_element_by_xpath("//button[text()[contains(., 'Log in')]]")
    login_btn.click()
    time.sleep(3)
    return driver


def firstInstaProfile(driver):
    driver.get(first_userprofile_link)
    delay = 5 #seconds
    follower_link = "/" + first_username_to_search + '/followers/'
    follower_xPath = "//a[@href='" + follower_link + "']"
    try:
        myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, follower_xPath)))
        print("Page is ready!")
    except TimeoutException:
        print("Loading took too much time!\n\n")

    html = driver.page_source
    soup = BeautifulSoup(html, "html5lib")
    ele =  driver.find_element_by_xpath(follower_xPath)
    ele.click()
  
    return driver


def fetchUsers(driver):
    users_list = []
    user = {}
    
    time.sleep(2)
        
    html = driver.page_source
    soup = BeautifulSoup(html, "html5lib")
    
    for li in soup.find_all("li", class_ = "_6e4x5"):
        print(li)
        print("\n\n")

#         scrolling the div
#         eula = driver.find_element_by_id('eulaFrame')
#         driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', eula)
        
        
driver = webdriver.Chrome()

driver = login(driver)
driver = firstInstaProfile(driver)
driver = fetchUsers(driver)


# driver.close()
print("Successfully scrapped")
