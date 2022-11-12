from selenium import webdriver
import time
from selenium.webdriver.common.by import By


PATH = "/home/utkarsh/Downloads/chromedriver"
driver = webdriver.Chrome(PATH)
driver.get("https://www.nseindia.com/market-data/live-equity-market")

final_data = list()
time.sleep(2)
search = driver.find_element(by=By.TAG_NAME, value="table")
tbody = search.find_element(by=By.TAG_NAME, value='tbody')
tr_list = tbody.find_elements(by=By.TAG_NAME, value='tr')
for tr in tr_list[1:]:
    td_list = tr.find_elements(by=By.TAG_NAME, value='td')
    td = [t.text for t in td_list]
    if td:
        if td[0]:
            final_data.append(td)

print(final_data)
time.sleep(2)
driver.close()
