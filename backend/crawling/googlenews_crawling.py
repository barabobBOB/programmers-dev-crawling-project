from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import sqlite3
from os import path

chrome_options = Options()
# chrome_options.add_experimental_option("detach", True)
chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
chrome_options.add_argument('headless')
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
        dt = feature.find_element(By.CLASS_NAME, "WW6dff.uQIVzc.Sksgp.slhocf").get_attribute("datetime")
        url = feature.find_element(By.CLASS_NAME, "DY5T1d.RZIKme").get_attribute("href")

        titles.append(title)
        dates.append(dt.replace('T',' ').replace('Z',''))
        urls.append(url)
 
    return titles, dates, urls

titles, dates, urls = google_searching(COIN_NAME)

# list to dict
dictnews = {}
for i in range(len(titles)):
    dictnews[i] = [titles[i], dates[i], urls[i]]


if not path.exists('google_news.db'):
    conn = sqlite3.connect('google_news.db')
    cur = conn.cursor()
    conn.execute("create table google (id integer, name text ,titles text, dates text, urls text)")
else:
    conn = sqlite3.connect('google_news.db')
    cur = conn.cursor()

for i in dictnews: 
    title = dictnews[i][0]
    date = dictnews[i][1]
    url = dictnews[i][2]

    title = title.replace("'","''")

    sql = f"insert into google values ({i}, '{COIN_NAME}', '{title}', '{date}', '{url}')"
    cur.execute(sql)

conn.commit()
conn.close()