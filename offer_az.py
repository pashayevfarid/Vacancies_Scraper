import re
import requests
import numpy as np
import pandas as pd
import time
from datetime import datetime
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("start-maximized")
chrome_options.add_argument("disable-infobars")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")

# Initialize WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# URL to scrape
url = 'https://www.offer.az/is-elanlari/'
driver.get(url)

# Lists to store data
job_list = [] 
posted_date_list = []
deadline_list = []
company_name_list = [] 
city_name_list = []
salary_list = []
work_exp_list = []
age_list = []
education_list = []
work_type_list = []
contract_list = []
mail_list = []
phone_number_list = [] 
job_desc_list = []
links_list = []


# It returns how many pages of vacancies there are on the site.
page = driver.find_element(by=By.XPATH, value='/html/body/main/section[2]/div/nav[1]/div/a[2]')
n = int(page.text)


pages = np.arange(1, n)


for p in pages:
    driver.get('https://www.offer.az/is-elanlari/page/'+str(p))
    time.sleep(2)

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    vacancies = soup.find_all('div', class_='job-card')

    if not vacancies:  # If no products found, break the loop
            print("No more vacancies found, scraping is complete.")
            break

    for vacancy in vacancies:
        vacancy_link = vacancy.find('a')['href']
        full_link = f'{vacancy_link}'
        links_list.append(full_link)


        driver.get(links_list[-1])
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'main')))
        vacancies_soup = BeautifulSoup(driver.page_source, 'html.parser')

        main_content = vacancies_soup.find('main')
        
        h1_element = main_content.find('h1', class_='top-banner__title') if main_content else None
        if h1_element:
            for span in h1_element.find_all('span'):
                span.decompose()
            clean_title = h1_element.get_text(strip=True)
        else:
            clean_title = None
        job_list.append(clean_title)

        # Posted date
        posted_li = main_content.find_all('li', class_='post__meta-item')[0]
        posted_date = posted_li.find('span', class_='post__meta-value')
        posted_date = posted_date.get_text(strip=True) if posted_date else None
        if posted_date: 
            try:
                posted_obj = datetime.strptime(posted_date, '%d.%m.%Y')
                posted_date = posted_obj.strftime('%d/%m/%Y')
            except ValueError:
                posted_date = None
        posted_date_list.append(posted_date)

        # Deadline
        deadline_li = main_content.find_all('li', class_='post__meta-item')[1]
        deadline = deadline_li.find('span', class_='post__meta-value')
        deadline = deadline.get_text(strip=True) if deadline else None
        if deadline: 
            try:
                deadline_obj = datetime.strptime(deadline, '%d.%m.%Y')
                deadline = deadline_obj.strftime('%d/%m/%Y')
            except ValueError:
                deadline = None
        deadline_list.append(deadline)

        # Company name
        company_li = main_content.find_all('li', class_='post__meta-item')[2]
        company_name = company_li.find('span', class_='post__meta-value')
        company_name = company_name.get_text(strip=True) if company_name else None
        company_name_list.append(company_name)

        # City
        city_li = main_content.find_all('li', class_='post__meta-item')[3]
        city_name = city_li.find('span', class_='post__meta-value')
        city_name = city_name.get_text(strip=True) if city_name else None
        city_name_list.append(city_name)

        # Salary
        salary_li = main_content.find_all('li', class_='post__meta-item')[4]
        salary = salary_li.find('span', class_='post__meta-value')
        salary = salary.get_text(strip=True) if salary else None
        salary_list.append(salary)

        # Work experience
        work_exp_li = main_content.find_all('li', class_='post__meta-item')[5]
        work_exp = work_exp_li.find('span', class_='post__meta-value')
        work_exp = work_exp.get_text(strip=True) if work_exp else None
        work_exp_list.append(work_exp)

        # Age
        age_li = main_content.find_all('li', class_='post__meta-item')[6]
        age = age_li.find('span', class_='post__meta-value')
        age = age.get_text(strip=True) if age else None
        if age:
            age = age.replace(' yaş', '')
        age_list.append(age)

        # Education
        education_li = main_content.find_all('li', class_='post__meta-item')[7]
        education = education_li.find('span', class_='post__meta-value')
        education = education.get_text(strip=True) if education else None
        education_list.append(education)

        # Working type
        work_type_li = main_content.find_all('li', class_='post__meta-item')[8]
        work_type = work_type_li.find('span', class_='post__meta-value')
        work_type = work_type.get_text(strip=True) if work_type else None
        work_type_list.append(work_type)
        
        # Contract
        contract_li = main_content.find_all('li', class_='post__meta-item')[9]
        contract = contract_li.find('span', class_='post__meta-value')
        contract = contract.get_text(strip=True) if contract else None
        contract_list.append(contract)

        # E-mail
        email_li = main_content.find_all('li', class_='post__meta-item')[10]
        email = email_li.find('span', class_='post__meta-value')
        email = email.get_text(strip=True) if email else None
        mail_list.append(email)

        # Phone number
        phone_number_li = main_content.find_all('li', class_='post__meta-item')
        if len(phone_number_li) > 11:  # Ən azı 12 element varsa, yoxlayırıq
            phone_number = phone_number_li[11].find('span', class_='post__meta-value')
            phone_number = phone_number.get_text(strip=True) if phone_number else None
        else:
            phone_number = None  

        phone_number_list.append(phone_number)

        # Job description
        pat = re.compile(r'\s\w+@\w+\.\w+\s')  # pattern
        job_desc = main_content.find('div', class_='post__content')

        if job_desc:
            job_desc_text = job_desc.get_text(strip=True)  
            job_desc_text = re.sub(pat, '', job_desc_text) 
            job_desc_text = job_desc_text.replace('\n', ' ')
            job_desc_text = job_desc_text.replace('\xa0', ' ')  
            job_desc_text = ' '.join(job_desc_text.split())
            job_desc_list.append(job_desc_text)
        else:
            job_desc_list.append(None)


driver.quit()

# DataFrame
vacancies_df = pd.DataFrame({'job': pd.Series(job_list, dtype='object'),
                            'company': pd.Series(company_name_list),
                            'city': pd.Series(city_name_list),
                            'salary': pd.Series(salary_list),
                            'work_experience': pd.Series(work_exp_list),
                            'age': pd.Series(age_list),
                            'education': pd.Series(education_list),
                            'work_type': pd.Series(work_type_list),
                            'contract': pd.Series(contract_list),
                            'email': pd.Series(mail_list),
                            'phone_number': pd.Series(phone_number_list),
                            'job_descr': pd.Series(job_desc_list, dtype='object'),
                            'links': pd.Series(links_list),
                            'posted_date': pd.Series(posted_date_list),
                            'deadline': pd.Series(deadline_list)                
                    })

vacancies_df.to_csv('vacancies_offer_az.csv', index=False)



