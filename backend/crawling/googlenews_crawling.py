from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
service = Service(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

URL = "https://news.google.com/home?hl=ko&gl=KR&ceid=KR:ko"
COIN_NAME = 'btc'

driver.get(URL)

time.sleep(3)

def google_searching(coiname):
    # 검색창 선택
    element = driver.find_element(By.CLASS_NAME, "Ax4B8.ZAGvjd")
    element.send_keys(coiname)
    element.send_keys(Keys.ENTER)
    time.sleep(2)

    # 각 기사 박스 선택
    features = driver.find_elements(By.CLASS_NAME, "MQsxIb.xTewfe.R7GTQ.keNKEd.j7vNaf.Cc0Z5d.EjqUne")

    titles = []
    urls = []
    dates = []

    for feature in features:
        title = feature.find_element(By.CLASS_NAME, "DY5T1d.RZIKme").text
        url = feature.find_element(By.CLASS_NAME, "DY5T1d.RZIKme").get_attribute("href")
        dt = feature.find_element(By.CLASS_NAME, "WW6dff.uQIVzc.Sksgp.slhocf").get_attribute("datetime")

        titles.append(title)
        urls.append(url)
        dates.append(dt)

        dfresult = pd.DataFrame(zip(titles, dates, urls))
        dfresult.columns = ['title', 'date', 'url']

    return dfresult

def prep_dt(dfresult):
    dfresult['date'] = dfresult['date'].str.replace('T', ' ')
    dfresult['date'] = dfresult['date'].str.replace('Z', '')
    dfresult['date'] = pd.to_datetime(dfresult['date'])

    return dfresult

dfresult = google_searching(COIN_NAME)
dfresult = prep_dt(dfresult)
print(dfresult)