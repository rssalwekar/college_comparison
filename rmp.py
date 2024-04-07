import selenium.common.exceptions
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select
import time
import json
from typing import Union
from math import floor
from COLLEGES import COLLEGES


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
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "search")))

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
        time.sleep(1)
        department_links = {}
        for department in departments:
            department_link = get_department_link(driver, university, department)
            department_links[f"{department.replace(' ', '_').lower()}"] = department_link
        all_department_links[university] = department_links

        # Create individual json files for each university
        with open(f"exports/department_links/department_links_{university}.json", "w") as outfile:
            json.dump(department_links, outfile)

    # Create combined department link JSON for future use
    with open("exports/department_links/combined_department_links.json", "w") as file:
        json.dump(all_department_links, file)

    return all_department_links


def get_ratings(driver: webdriver, university: str, department_urls: Union[dict, str]) -> dict:
    """
    Gets 20 ratings and averages them from the department's rate my professor website
    :param driver: selenium webdriver
    :param department_urls: list of department urls to scrape
    :return: average ratings for department
    """
    ratings = {}
    first = True

    for department, url in department_urls[university].items():
        #Max pages of professors to get
        max_pages = 4

        # Go to department link
        driver.get(url)


        # Close stupid popup
        if first:
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//button[text()="Close"]'))).click()
            first = False

        # # Ensure that everything is button is loaded before spam pushing it
        # WebDriverWait(driver, 6).until(
        #     EC.presence_of_element_located((By.XPATH, '//button[text()="Show More"]')))

        # If there are fewer than the number of professors, just do that amount
        num_of_professors = int(WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'h1'))).get_attribute("innerHTML").split("professor")[0])
        print(f"{department}: {num_of_professors}")
        if num_of_professors < (max_pages * 8):
            max_pages = floor(num_of_professors / 8)


        count = 0
        # Get show more button and click button four times
        while (count < max_pages):
            # If a pop-up comes up:
            try:
                # If there are less than 8 professors, there is no "show more" button
                if num_of_professors < 8:
                    break
                WebDriverWait(driver, 6).until(
                    EC.presence_of_element_located((By.XPATH, '//button[text()="Show More"]'))).click()
                time.sleep(.5)
                count += 1
            except selenium.common.exceptions.ElementClickInterceptedException:
                WebDriverWait(driver, 4).until(
                    EC.presence_of_element_located((By.XPATH, '//button[text()="×"]'))).click()

            time.sleep(1)

        # Get all ratings
        department_ratings = driver.find_elements(By.CLASS_NAME, "CardNumRating__CardNumRatingNumber-sc-17t4b9u-2")

        department_rating_vals = []

        [department_rating_vals.append(float(rating.get_attribute("innerHTML"))) for rating in department_ratings if
         (float(rating.get_attribute("innerHTML")) != 0.0)]

        ratings_dict = {}

        average = sum(department_rating_vals) / len(department_rating_vals)

        ratings_dict["individual_ratings"] = department_rating_vals
        ratings_dict["average"] = average

        ratings[department] = ratings_dict

    # print(ratings)

    return ratings


def collect_all_ratings(driver: webdriver, universities: list, departments: Union[dict, str]) -> dict:
    """
    Collect all of the average ratings for all of the provided universities and their specified and writes to results.json
    :param driver: selenium web driver
    :param universities: list of universities
    :param departments: list of departments to get ratings for each university
    :return: dictionary of all results
    """
    if departments.endswith(".json"):
        f = open(departments)
        departments = json.load(f)

    all_ratings = {}
    for university in universities:
        university_ratings = get_ratings(driver, university, departments)
        print(university_ratings)

        all_ratings[university] = university_ratings

        # Convert and write JSON object to file
        with open(f"exports/ratings/ratings_{university}.json", "w") as outfile:
            json.dump(all_ratings, outfile)

    return all_ratings


def main():
    universities = ["University of North Carolina at Charlotte", "The University of North Carolina at Chapel Hill",
                    "North Carolina State University"]
    departments = ["Biology", "Business", "Chemistry", "Computer Science", "Economics", "English", "Geography",
                   "History", "Mathematics", "Political Science", "Psychology"]
    print(departments)

    chrome_options = Options()
    chrome_options.page_load_strategy = 'eager'
    chrome_options.add_extension("chrome_assets/adblock.crx")
    service = Service(executable_path="chrome_assets/chromedriver.exe")
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # links = get_department_links(driver, universities, departments)

    collect_all_ratings(driver, universities[2:], "exports/department_links/combined_department_links.json")

    driver.quit()


main()
