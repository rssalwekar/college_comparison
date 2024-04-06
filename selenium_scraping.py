from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

service = Service(executable_path="chromedriver-mac-arm64/chromedriver")
driver = webdriver.Chrome(service=service)

driver.get("https://google.com")

input_element = driver.find_element(By.CLASS_NAME, "gLFyf")
input_element.send_keys("tech with tim" + Keys.RETURN)

time.sleep(10)

driver.quit()
