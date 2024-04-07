from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select
import time
from COLLEGES import COLLEGES


#
# service = Service(executable_path="chromedriver.exe")
# driver = webdriver.Chrome(service=service)
#
# ratings = []
#
# university = "University of North Carolina at Charlotte"
# department = "Computer Science"
#
# driver.get(f"https://www.ratemyprofessors.com/search/professors/{COLLEGES[university]}?q")
#
# time.sleep(5)
#
# select = Select(driver.find_element(By.CLASS_NAME, "css-1l6bn5c-control"))
#
# department_button = select.select_by_visible_text(department)
#
# show_more_button = driver.find_element(By.CLASS_NAME, "eUNaBX")
# show_more_button.click()
#
# # Find elements by class name
# elements = driver.find_elements(By.CLASS_NAME, 'your-class-name')
#
# # Filter elements by their text content
# filtered_elements = [element for element in elements if department in element.text]
#
# # Optionally, interact with those elements
# for element in filtered_elements:
#     print(element.text)
#     # You can click on it or interact with it in other ways
#     # element.click()
#
#
# # search_bar = driver.find_element(By.CLASS_NAME, "fwqnjW")
# # search_bar.send_keys("Isaac Sonin" + Keys.RETURN)
#
# time.sleep(15)
#
# driver.quit()

def get_department_link(driver: webdriver, university, department: str) -> str:
    """
    Searches up a school's department on RMP and clicks on the first result before getting the special department
    link for that university
    :param driver: selenium driver
    :param university: target university
    :param department: department to get link for
    :return: web url of all professors in school's department
    """
    query = (f'Rate My Professor "Professor in the {department} '
             f'department at {university}"')

    # Go to google.com
    driver.get("https://google.com")

    # Get search bar
    input_element = WebDriverWait(driver, .5).until(EC.visibility_of_element_located((By.CLASS_NAME, "gLFyf")))
    time.sleep(.5)

    # Input query into search bar
    input_element.send_keys(query + Keys.RETURN)

    # Wait for the search results to load
    WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.ID, "search")))

    # Click on the first search result link
    first_result = driver.find_element(By.CSS_SELECTOR, "h3", )
    first_result.click()

    # Get the school's department link
    department_link = driver.find_element(By.CLASS_NAME, "iMmVHb")

    time.sleep(1)

    return department_link.get_attribute("href")


def get_department_links(driver: webdriver, universities: list, departments: list) -> dict:
    """
    From a departments and universities list, gets all the university's departments
    :param driver: selenium driver
    :param university: list of universities
    :param departments: list of departments to search for each university
    :return: dictionary of all the university's and their departments
    """
    all_department_links = {}
    for university in universities:
        department_links = {}
        for department in departments:
            department_link = get_department_link(driver, university, department)
            department_links[f"{department.replace(' ', '_').lower()}"] = department_link
        all_department_links[university] = department_links

    return all_department_links


def get_ratings(driver: webdriver, universities: list, department_urls: dict):
    """
    Gets 20 ratings and averages them from the department's rate my professor website
    :param driver: selenium webdriver
    :param department_urls: list of department urls to scrape
    :return: average ratings for department
    """
    ratings = {}

    for university in universities:
        for department, url in department_urls[university].items():
            # Go to department link
            driver.get(url)


            # Get show more button and click button four times
            for i in range(4):
                if i > 2:
                    div_num = 4
                else:
                    div_num = 5
                show_more_button = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, f'//*[@id="root"]/div/div/div[4]/div[1]/div[1]/div[{div_num}]/button')))
                show_more_button.click()

            # Get all ratings
            ratings = driver.find_elements(By.CLASS_NAME, "CardNumRating__CardNumRatingNumber-sc-17t4b9u-2")

            print(ratings)


def main():
    universities = ["University of North Carolina at Charlotte", "The University of North Carolina at Chapel Hill"]
    departments = ["Biology", "Business", "Chemistry", "Computer Science", "Economics", "English", "Geography",
                   "History", "Mathematics", "Political Science", "Psychology"]
    print(departments[:5])

    chrome_options = Options()
    chrome_options.page_load_strategy = 'eager'
    service = Service(executable_path="chromedriver.exe")
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # links = get_department_links(driver, universities, departments[:5])

    test = {'University of North Carolina at Charlotte': {
        'biology': 'https://www.ratemyprofessors.com/search/professors/1253?q=*&did=6',
        'business': 'https://www.ratemyprofessors.com/search/professors/1253?q=*&did=7',
        'chemistry': 'https://www.ratemyprofessors.com/search/professors/1253?q=*&did=8',
        'computer_science': 'https://www.ratemyprofessors.com/search/professors/1253?q=*&did=11',
        'economics': 'https://www.ratemyprofessors.com/search/professors/1253?q=*&did=15'},
            'The University of North Carolina at Chapel Hill': {
                'biology': 'https://www.ratemyprofessors.com/search/professors/1232?q=*&did=6',
                'business': 'https://www.ratemyprofessors.com/search/professors/1232?q=*&did=7',
                'chemistry': 'https://www.ratemyprofessors.com/search/professors/1232?q=*&did=8',
                'computer_science': 'https://www.ratemyprofessors.com/search/professors/1232?q=*&did=11',
                'economics': 'https://www.ratemyprofessors.com/search/professors/1232?q=*&did=15'}}

    get_ratings(driver, universities, test)

    driver.quit()


main()
