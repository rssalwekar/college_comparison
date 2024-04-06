from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

import PyPDF2

import os
import time

# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Define the download directory path
download_directory = os.path.join(script_dir, 'pdf_downloads')

# Ensure the download directory exists
os.makedirs(download_directory, exist_ok=True)

chrome_options = Options()
chrome_options.add_experimental_option('prefs', {
    "download.default_directory": download_directory,  # Change default directory for downloads
    "download.prompt_for_download": False,  # Avoid prompting for download
    "download.directory_upgrade": True,
    "plugins.always_open_pdf_externally": True  # It will not open PDF in Chrome
})

# chrome executable
service = Service(executable_path="chromedriver-mac-arm64/chromedriver")
driver = webdriver.Chrome(service=service)

# website to go to
driver.get("https://catalog.charlotte.edu")

# find catalog
catalog_button = driver.find_element(By.PARTIAL_LINK_TEXT, "Undergraduate Catalogs")
catalog_button.click()

pdf_link = driver.find_element(By.XPATH, '//*[@id="gateway-page"]/body/table/tbody/tr[3]/td[2]/table/tbody/tr[2]/td[2]/table/tbody/tr/td/table/tbody/tr[3]/td/table/tbody/tr[1]/td[2]/p/strong/a')
pdf_link.click()

time.sleep(10)

action = ActionChains(driver)

# if user is on windows
if os.name == 'nt':
    # Windows-specific code
    download_button = driver.find_element(By.ID, "icon")
    download_button.click()
    # action.key_down(Keys.CONTROL).send_keys('f').key_up(Keys.CONTROL).perform()
    # action.send_keys("ITCS").perform()
else:
    print("You're using mac/linux.")
    download_button = driver.find_element(By.ID, "icon")
    download_button.click()
    # For macOS, use Command+F. Adjust accordingly if using Windows/Linux (Ctrl+F).
    # action.key_down(Keys.COMMAND).send_keys('f').key_up(Keys.COMMAND).perform()
    # action.send_keys("ITCS").perform()


time.sleep(120)

driver.quit()
