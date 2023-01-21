from selenium.webdriver.common.by import By
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
from selenium import *
from selenium import webdriver
header = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'}

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('headless')
chrome_options.add_argument('window-size=1920x1080')
chrome_options.add_argument("disable-gpu")
driver = webdriver.Chrome(
    r"C:\Users\Hp\Desktop\chromedriver.exe", chrome_options=chrome_options)
Link = []

driver.get(
    "https://www.monsterindia.com/search/{}-jobs-in-{}".format('data-scientist', 'thane'))
driver.implicitly_wait(10)
print(driver.title)
jobs_list = []
for i in range(1, 5):
    jobs = []
    try:
        xpath = '//*[@id="srp-jobList"]/div/div[{}]/div/div[1]/div/div/h3/a'.format(
            i)
        title = driver.find_element(By.XPATH, xpath)
        if title:
            company = driver.find_element(
                By.XPATH, '//*[@id="srp-jobList"]/div/div[{}]/div/div[1]/div/div/span/a'.format(i))
            location = driver.find_element(
                By.XPATH, '//*[@id="srp-jobList"]/div/div[{}]/div/div[1]/div/div/div/div[1]/span/small'.format(i))
            description = driver.find_element(
                By.XPATH, '//*[@id="srp-jobList"]/div/div[{}]/div/div[1]/div/p'.format(i))
            job_url = title.get_attribute('href')
            job_title = title.get_attribute('innerHTML')
            company_name = company.get_attribute('title')
            job_location = location.get_attribute('innerHTML')
            job_description = description.get_attribute('innerHTML')
            job_location = job_location.replace("<label>", "")
            job_location = job_location.replace("</label>", "")
            job_location = job_location.replace(",", "")
            jobs.append(job_url.strip())
            jobs.append(job_title.strip())
            jobs.append(company_name.strip())
            jobs.append(job_location.strip())
            jobs.append(job_description.strip())
            jobs_list.append(jobs)
    except:
        break

print(jobs_list[0])
