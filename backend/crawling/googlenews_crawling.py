from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

def data_parsing(COIN_NAME, features):
    result = []
    for feature in features:
        title = feature.find_element(By.CLASS_NAME, "DY5T1d.RZIKme").text
        dt = feature.find_element(By.CLASS_NAME, "WW6dff.uQIVzc.Sksgp.slhocf").get_attribute("datetime")
        url = feature.find_element(By.CLASS_NAME, "DY5T1d.RZIKme").get_attribute("href")

        news = {
            'name': COIN_NAME,
            'title': title,
            'date': dt.replace('T',' ').replace('Z',''),
            'url': url
        }

        result.append(news)
    return result

def news_crawling(coin_name: str):
    chrome_options = Options()
    # chrome_options.add_experimental_option("detach", True)
    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
    chrome_options.add_argument('headless')
    service = Service(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    URL = "https://news.google.com/home?hl=ko&gl=KR&ceid=KR:ko"

    driver.get(URL)

    time.sleep(3)
    
    # 검색창 선택
    element = driver.find_element(By.CLASS_NAME, "Ax4B8.ZAGvjd")
    element.send_keys(coin_name)
    element.send_keys(Keys.ENTER)
    time.sleep(2)

    # 각 기사 박스 선택
    features = driver.find_elements(By.CLASS_NAME, "MQsxIb.xTewfe.R7GTQ.keNKEd.j7vNaf.Cc0Z5d.EjqUne")
    result = data_parsing(coin_name, features)

    return result