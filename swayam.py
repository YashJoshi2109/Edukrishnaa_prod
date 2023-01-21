# from selenium import webdriver
# from selenium.webdriver.common.by import By

# chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument('headless')
# chrome_options.add_argument('window-size=1920x1080')
# chrome_options.add_argument("disable-gpu")
# driver = webdriver.Chrome("chromedriver.exe", chrome_options=chrome_options)


# co_org=[]
# co_prof=[]
# co_url=[]
# co_tit=[]

# base_url="https://swayam.gov.in/explorer?searchText={}"
# def find_courses_swayam(skill):
#     new_url=base_url.format(skill)
#     driver.get(new_url)
#     print(driver.title)
#     driver.implicitly_wait(30)
#     for i in range(1,6):
#         try:
#             xpath='//*[@id="open"]/course-cards/div/div[{}]/course-card/a/div/div[2]/h4/span/strong'.format(i)
#             title=driver.find_element(By.XPATH,xpath)
#             if title:
#                 organization=driver.find_element(By.XPATH,'//*[@id="open"]/course-cards/div/div[{}]/course-card/a/div/div[2]/div[2]/span'.format(i))
#                 professor=driver.find_element(By.XPATH,'//*[@id="open"]/course-cards/div/div[{}]/course-card/a/div/div[2]/div[1]/span'.format(i))
#                 course_url=driver.find_element(By.XPATH,'//*[@id="open"]/course-cards/div/div[{}]/course-card/a'.format(i))
#                 title_content = title.get_attribute('innerHTML')
#                 organization_content = organization.get_attribute('innerHTML')
#                 professor_content=professor.get_attribute('innerHTML')
#                 url_content=course_url.get_attribute('href')

#                 co_tit.append(title_content.strip())
#                 # print(title_content.strip())

#                 co_org.append(organization_content.strip().replace("&nbsp",""))
#                 # print(organization_content.strip().replace("&nbsp",""))

#                 co_prof.append(professor_content.strip())
#                 # print(professor_content.strip())

#                 co_url.append(url_content.strip())
#                 # print(url_content.strip())
#         except:
#             break
# find_courses_swayam("python")#enter python/data

# print(co_tit)
# print()

# print(co_org)
# print()

# print(co_prof)

# print(co_url)
# print()
