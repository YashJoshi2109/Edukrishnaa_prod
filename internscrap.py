import pandas as pd
import time
import re
import requests
import bs4
from bs4 import BeautifulSoup

int_title = []
int_company = []
int_loc = []
int_link = []


def extract_job_title_from_result(job_div, job_post):
    if job_div.find is not None:
        for a in job_div.find(name="div", attrs={"class": "company"}).find(name="div", attrs={"class": "profile"}).find(name="a"):
            job_post.append(a)
            int_title.append(a)


def extract_company_from_result(job_div, job_post):
    for a in job_div.find(name="div", attrs={"class": "individual_internship_header"}).find(name="div", attrs={"class": "company"}).find(name="div", attrs={"class": "company_name"}).find(name="a"):
        job_post.append(str(a).strip())
        int_company.append(str(a).strip())


def extract_location_from_result(job_div, job_post):
    for a in job_div.find(name="div", attrs={"class": "individual_internship_details"}).find(name="div", attrs={"id": "location_names"}).find(name="a", attrs={"class": "location_link"}):
        job_post.append(str(a).strip())
        int_loc.append(str(a).strip())


def extract_company_from_result(job_div, job_post):
    for a in job_div.find(name="div", attrs={"class": "individual_internship_header"}).find(name="div", attrs={"class": "company"}).find(name="div", attrs={"class": "company_name"}).find(name="a"):
        job_post.append(str(a).strip())
        int_company.append(str(a).strip())


def extract_location_from_result(job_div, job_post):
    for a in job_div.find(name="div", attrs={"class": "individual_internship_details"}).find(name="div", attrs={"id": "location_names"}).find(name="a", attrs={"class": "location_link"}):
        job_post.append(str(a).strip())
        int_loc.append(str(a).strip())


def Get_URL_Of_page(base_url, skill, city):
    url = base_url + "/internships/"+skill + \
        "-internship"+"-in"+"-{}/".format(city)
    int_link.append(url)
    return url


def Get_total_pages(url):
    # get total number of pages
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser", from_encoding="utf-8")
    total_pages = soup.find(name="span", attrs={"id": "total_pages"})
    return int(total_pages.text.strip())


def Get_Internship_Description_Page_Url(job_div, base_url):
    for a in job_div.find(name="div", attrs={"class": "button_container"}).find_all(name="a", attrs={"class": "view_detail_button"}, href=True):
        return base_url + a['href']



    
# # scraping code:
# base_url = "https://internshala.com"
# skill = i_roles
# location = "mumbai"

def Scrap_Internshala(base_url, skill, location):
    url = Get_URL_Of_page(base_url, skill, location)
    print(url)
    print('')
    total_pages = Get_total_pages(url)
    print(total_pages)
    for page_number in range(total_pages):
        page = requests.get(url)
        soup = BeautifulSoup(page.text, "html.parser", from_encoding="utf-8")
        for div in soup.find_all(name="div", attrs={"class": "individual_internship"})[:-1]:
            # creating an empty list to hold the data for each posting
            job_post = []
            # grabbing job title
            extract_job_title_from_result(div, job_post)
            # grabbing company name
            extract_company_from_result(div, job_post)
            # grabbing location name
            extract_location_from_result(div, job_post)
            job_post.append(Get_Internship_Description_Page_Url(div, base_url))
            # print(job_post)



    print(int_title)
    print()
    print(int_company)
    print()
    print(int_loc)
    print()
    print(int_link)
    print()
