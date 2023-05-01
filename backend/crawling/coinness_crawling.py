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

def parsring(contect, num):
    
    # 오늘 날짜
    inner_divs = contect.find_elements(By.XPATH, './div[1]')
    for inner_div in inner_divs:
        contect_list.append(inner_div.text)
        
    # ha = contect.find_elements(By.XPATH, './div[2]/div[1]/div/div/h3')
    # for h in ha:
    #     print(h.text)
    
    # time_list = contect.find_elements(By.XPATH, './div[2]/div[1]/div/div[1]')
    # title_list = contect.find_elements(By.XPATH, './div[2]/div[1]/div/div/h3')
    # content_list = contect.find_elements(By.XPATH, './div[2]/div[1]/div/div/div[1]')
    
    
    # for time, title, content in zip(time_list, title_list, content_list):
    #     print(time.text, title.text, content.text)
    #     contect_list.append([time.text, title.text, content.text])
    
    for i in range(1, 100):
        try:
            time_list = contect.find_elements(By.XPATH, './div[2]/div['+ str(i) +']/div/div[1]')
            title_list = contect.find_elements(By.XPATH, './div[2]/div['+ str(i) +']/div/div/h3')
            content_list = contect.find_elements(By.XPATH, './div[2]/div['+ str(i) +']/div/div/div[1]')
            for time, title, content in zip(time_list, title_list, content_list):
                contect_list.append([time.text, title.text, content.text])
        except:
            print("안돼..")
            break
        
    # contect = list(map(str, contect.split('\n')))
    
    
    # con_list = []
    # for i in range(len(contect)):
    #     if contect[i - 1] == '공지':
    #         pass
    #     if len(contect[i]) < 5:
    #         pass
    #     else:
    #         con_list.append(contect[i])
            
    # idx = 1
    # contect_list.append(contect[0])
    
    # while idx < len(con_list) - 1:
    #     contect_list.append([con_list[idx], con_list[idx + 1], con_list[idx + 2]])
    #     idx += 3
        
    return contect_list

# 크롤링 할 URL
url = 'https://coinness.com/'
driver = webdriver.Chrome()
driver.get(url)

# 사이트 로딩을 위한 시간 10초
sleep(10)

# //*[@id="root"]/div/div[1]/div/main/div[2]/div[1]/div[2]
# //*[@id="root"]/div/div[1]/div/main/div[2]/div[1]/div[2]/div[1]
# //*[@id="root"]/div/div[1]/div/main/div[2]/div[2]/div[2]
# //*[@id="root"]/div/div[1]/div/main/div[2]/div[2]/div[2]/div[1]
# //*[@id="root"]/div/div[1]/div/main/div[2]/div[2]/div[2]/div[1]/div/div[1]
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

# //*[@id="root"]/div/div[1]/div/main/div[2]/div[1]/div[1]

# inner_divs = driver.find_elements(By.CLASS_NAME, "sc-hZNxer cTyWSA")

# inner_divs = contect.find_elements(By.CLASS_NAME, 'sc-hZNxer cTyWSA')
# print(contect.text)
# print("----")