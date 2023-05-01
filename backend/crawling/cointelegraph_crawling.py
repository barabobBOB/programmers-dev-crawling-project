from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import pandas as pd

driver = webdriver.Chrome('/Users/Name/Downloads/chromedriver') 
driver.get('https://cointelegraph.com/magazine/')

time.sleep(3)

# 기사 관련 내용만 선택
features = driver.find_elements(By.PARTIAL_LINK_TEXT, "Features")

# news_urls = []
titles = []
contents = []

for feature in features:
    feature.send_keys(Keys.ENTER)
    
    # current_url = driver.current_url
    # news_urls.append(current_url)

    current_title = driver.title
    titles.append(current_title)

    current_content = driver.find_element(By.CLASS_NAME, "article__inner.body-l").text
    contents.append(current_content)

    # 추가되는 페이지에 대해 코드 추가해야 함

    driver.back()

dfresult = pd.DataFrame(zip(titles, contents))
dfresult.columns = ['title', 'content']

