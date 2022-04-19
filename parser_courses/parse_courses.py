import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

sort_by_type = 'newest'

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.maximize_window()
delay = 15


def extract_text(soup_obj, tag, attribute_name, attribute_value):
    txt = soup_obj.find(tag, {attribute_name: attribute_value}).text.strip() if soup_obj.find(tag, {
        attribute_name: attribute_value}) else ''
    return txt


rows = []

for page_number in range(1, 4):
    page_url = f'https://www.udemy.com/courses/free/?lang=en&p={page_number}&sort=newest'
    driver.get(page_url)
    time.sleep(5)

    try:
        WebDriverWait(driver, delay).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'course-list--container--3zXPS')))
    except TimeoutException:
        print('Loading exceeds delay time')
        break
    else:
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        course_list = soup.find('div', {'class': 'course-list--container--3zXPS'})
        courses = course_list.find_all('a', {'class': 'udlite-custom-focus-visible browse-course-card--link--3KIkQ'})

        for course in courses:
            course_url = '{0}{1}'.format('https://www.udemy.com', course['href'])
            course_title = course.select('div[class*="course-card--course-title"]')[0].text
            course_headline = extract_text(course, 'p', 'data-purpose',
                                           'safely-set-inner-html:course-card:course-headline')
            author = extract_text(course, 'div', 'data-purpose',
                                  'safely-set-inner-html:course-card:visible-instructors')
            course_rating = extract_text(course, 'span', 'data-purpose', 'rating-number')
            number_of_ratings = extract_text(course, 'span', 'class',
                                             'udlite-text-xs course-card--reviews-text--12UpL')[1:-1]
            course_detail = course.find_all('span', {'class': 'course-card--row--1OMjg'})
            course_length = course_detail[0].text
            number_of_lectures = course_detail[1].text
            difficulity = course_detail[2].text

            rows.append(
                [course_url, course_title, course_headline, author, course_rating, number_of_ratings, course_length,
                 number_of_lectures, difficulity]
            )

columns = ['url', 'Course Title', 'Course Headline', 'Instructor', 'Rating', 'Number of Ratings', 'Course Length',
           'Number of Lectures', 'Difficulity']
df = pd.DataFrame(data=rows, columns=columns)
df.to_csv('Udmey Free Courses.csv', index=False)
driver.quit()