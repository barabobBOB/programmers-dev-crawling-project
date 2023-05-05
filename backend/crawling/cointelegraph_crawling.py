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

titles = []
contents = []
dates = []

for feature in features:

    # 기사가 아닌 카테고리 features는 제외
    if feature.text == 'Features':
        print(feature.text)
        continue
    
    time.sleep(4)
    feature.send_keys(Keys.ENTER)

    # 기사 제목
    current_title = driver.title
    titles.append(current_title)

    '''
    본문 내용 전체
    current_content = driver.find_element(By.CLASS_NAME, "article__inner.body-l").text
    '''

    # 기사 날짜
    current_date = driver.find_element(By.XPATH, "/html/body/div/main/section[1]/div/div[1]/div[1]/div[2]/span[3]").text
    dates.append(current_date)

    # 기사 요약본 (부제목) 
    current_content = driver.find_element(By.CLASS_NAME, "article-top__title__subtitle").text
    contents.append(current_content)
    
    driver.back()

dfresult = pd.DataFrame(zip(titles, dates, contents))
dfresult.columns = ['title', 'date', 'content']
print(dfresult)
