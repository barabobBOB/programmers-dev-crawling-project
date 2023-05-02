from time import sleep
import os
from turtle import title

# import chromedriver_autoinstaller

from selenium.webdriver.common.by import By
from selenium import webdriver

# chrome driver를 자동으로 설치함
# chromedriver_autoinstaller.install()

options = webdriver.ChromeOptions() # Browser 세팅하기
options.add_argument('lang=ko_KR') # 사용언어 한국어
options.add_argument('disable-gpu') # 하드웨어 가속 안함
options.add_argument('headless') # 창 숨기기

contect_list = []

# 크롤링 데이터 파싱
def parsring(contect, num):
    
    # 기사 날짜
    inner_divs = contect.find_elements(By.XPATH, './div[1]')
    for inner_div in inner_divs:
        contect_list.append(inner_div.text)
    
    for i in range(1, 100):
        try:
            time_list = contect.find_elements(By.XPATH, './div[2]/div['+ str(i) +']/div/div[1]')
            title_list = contect.find_elements(By.XPATH, './div[2]/div['+ str(i) +']/div/div/h3')
            content_list = contect.find_elements(By.XPATH, './div[2]/div['+ str(i) +']/div/div/div[1]')
            for time, title, content in zip(time_list, title_list, content_list):
                
                if time.text == "공지":
                    continue
                
                contect_list.append([time.text, title.text, content.text])
        except:
            print("해당 날짜 내 파싱 오류")
            break
        
    return contect_list

# 크롤링 할 URL
url = 'https://coinness.com/'
driver = webdriver.Chrome()
driver.get(url)

# 사이트 로딩을 위한 시간 10초
sleep(10)

# for i in range(1, 100):
#     try:
#         contect_div = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[1]/div/main/div[2]/div['+ str(i) +']').text
#         for j in range(1, 100):
#             try: 
#                 contect = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[1]/div/main/div[2]/div['+ str(i) +']/div['+ str(j) +']/div['+ str(i) +']').text
#             except:
#                 pass
#         print(parsring(contect))
#     except:
#         print('안돼 돌아가')
#         break

contect = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[1]/div/main/div[2]/div[1]')
print(parsring(contect, 1))