from time import sleep
import os

# import chromedriver_autoinstaller

from selenium.webdriver.common.by import By
from selenium import webdriver

# chrome driver를 자동으로 설치함
# chromedriver_autoinstaller.install() 

options = webdriver.ChromeOptions() # Browser 세팅하기
options.add_argument('lang=ko_KR') # 사용언어 한국어
options.add_argument('disable-gpu') # 하드웨어 가속 안함
options.add_argument('headless') # 창 숨기기

# 크롤링 할 URL
url = 'https://coinness.com/'
driver = webdriver.Chrome()
driver.get(url)

# 사이트 로딩을 위한 시간 10초
sleep(10)

content_xpath = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[1]/div/main/div[2]')

content_list = list(map(str, content_xpath.text.split('\n')))

print(content_list)
day = ['오늘', '어제', '2023년']

