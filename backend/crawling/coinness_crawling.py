from time import sleep
# import chromedriver_autoinstaller

from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium import webdriver
from typing import Dict

news = []

# 크롤링 데이터 파싱
def parsing(contect) -> Dict:
    date = ''
    # 기사 날짜
    inner_divs = contect.find_elements(By.XPATH, './div[1]')
    for inner_div in inner_divs:
        date = inner_div.text

    for i in range(1, 100):
        try:
            time_list = contect.find_elements(By.XPATH, './div[2]/div[' + str(i) + ']/div/div[1]')
            title_list = contect.find_elements(By.XPATH, './div[2]/div[' + str(i) + ']/div/div/h3')
            content_list = contect.find_elements(By.XPATH, './div[2]/div[' + str(i) + ']/div/div/div[1]')

            for time, title, content in zip(time_list, title_list, content_list):

                if time.text == "공지":
                    continue

                new_dic = {
                    'date': date,
                    'time': time.text,
                    'title': title.text,
                    'content': content.text
                }

                news.append(new_dic)
        except:
            print("해당 날짜 내 파싱 오류")
            break

    return news


def coinness_crawling():
    # chrome driver를 자동으로 설치함
    # chromedriver_autoinstaller.install()

    options = webdriver.ChromeOptions()  # Browser 세팅하기
    options.add_argument('lang=ko_KR')  # 사용언어 한국어
    options.add_argument('disable-gpu')  # 하드웨어 가속 안함
    options.add_argument('headless')  # 창 숨기기

    # 크롤링 할 URL
    url = 'https://coinness.com/'
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    driver.get(url)
    # 사이트 로딩을 위한 시간 10초
    sleep(5)

    for i in range(3):
        # 스크롤 높이 가져옴
        driver.execute_script("return document.body.scrollHeight")

        # 끝까지 스크롤 다운
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        sleep(2)
        
        driver.find_element(By.XPATH, '//*[@id="root"]/div/div[1]/div/main/button').click()
        sleep(2)

    for i in range(1, 100):
        try:
            contect_div = driver.find_element(By.XPATH,
                                              '//*[@id="root"]/div/div[1]/div/main/div[2]/div[' + str(i) + ']')
            data = parsing(contect_div)

        except:
            print('로딩된 기사 모두 추출 완료')

            # driver 종료
            driver.quit()

            break

    return data