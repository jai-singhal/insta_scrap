from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys

import csv
import re
import time

username = "ramavtar000112"
password = "ramavtar@123"
first_username_to_search = "priya.p.varrier"
first_userprofile_link = "https://www.instagram.com/priya.p.varrier/"

def login(driver):
    driver.get('https://www.instagram.com/')
    delay = 5 #seconds
    try:
        myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.LINK_TEXT, 'Log in')))
        print("Login Page is ready!")
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
        print(firstInstaProfile + " page is ready!")
    except TimeoutException:
        print("Loading took too much time!\n\n")

    html = driver.page_source
    soup = BeautifulSoup(html, "html5lib")
    ele =  driver.find_element_by_xpath(follower_xPath)
    ele.click()
  
    return driver


def fetchUsers(driver):
    csv_output = open('output.csv', 'w')
    
    time.sleep(2)
    html = driver.page_source
    soup = BeautifulSoup(html, "html5lib")
    
    driver.find_element_by_class_name('_b9n99').click()
    for i in range(100):    
        driver.find_element_by_tag_name('body').send_keys(Keys.END)
        time.sleep(0.2)
   
    time.sleep(2)
    html = driver.page_source
    soup = BeautifulSoup(html, "html5lib")
    time.sleep(1)
    
    for li in soup.find_all("li", class_ = "_6e4x5"):
        user = {}
        user['profile_link'] = li.find_all("a")[0]['href']
        user['img_src'] = li.find("img")['src']
        user['username'] = li.find(attrs={"class" : "_2g7d5"}).text
        user['name'] = li.find(attrs={"class" : "_9mmn5"}).text
        w = csv.DictWriter(csv_output, user.keys())
        w.writerow(user)
        
    csv_output.close()   
        
        
        
driver = webdriver.Chrome()
driver = login(driver)
driver = firstInstaProfile(driver)
driver = fetchUsers(driver)


driver.close()
print("Successfully scrapped")
