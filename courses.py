from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from COLLEGES import colleges
import json


def get_unc_charlotte_courses(driver: webdriver, college_list: list) -> dict:
    """
    goes to link with list of all majors and parses through specified majors for all required courses at unc charlotte
    :param driver: selenium driver
    :param college_list: list of colleges
    :return: dict of majors as keys and courses as values
    """
    
    college = list(college_list)[0]
    print(college)

    all_courses = {}

    for major, courses in colleges[college]["majors"].items():
        bachelors_website = colleges[college]['bachelors_degrees_link']
        driver.get(bachelors_website)

        link_to_major = driver.find_element(By.PARTIAL_LINK_TEXT, major)
        link_to_major.click()

        content = driver.find_element(By.CLASS_NAME, "block_content")
        courses = content.text

        courses = courses.split("Major Courses")[1].split("Degree Total")[0].split("\n")

        all_courses[major] = courses

    return all_courses


def get_unc_chapel_courses(driver: webdriver, college_list: list) -> dict:
    """
    goes to link with list of all majors and parses through specified majors for all required courses at unc chapel hill
    :param driver: selenium driver
    :param college_list: list of colleges
    :return: dict of majors as keys and courses as values
    """
    
    college = list(college_list)[1]
    print(college)

    all_courses = {}

    for major, courses in colleges[college]["majors"].items():
        bachelors_website = colleges[college]['bachelors_degrees_link']
        driver.get(bachelors_website)

        link_to_major = driver.find_element(By.LINK_TEXT, major)
        link_to_major.click()

        major_requirements = driver.find_element(By.ID, "requirementstexttab")
        major_requirements.click()

        # Find all tr elements on the page
        table_rows = driver.find_elements(By.TAG_NAME, "tr")

        # Concatenate the text of each tr element into a single string, separated by new lines
        all_text = "\n".join([row.text for row in table_rows])

        courses = all_text.split("Total")[0].split("\n")

        all_courses[major] = courses

    return all_courses


def get_nc_state_courses(driver: webdriver, college_list: list) -> dict:
    """
    goes to link with list of all majors and parses through specified majors for all required courses at nc state
    :param driver: selenium driver
    :param college_list: list of colleges
    :return: dict of majors as keys and courses as values
    """
    
    college = list(college_list)[2]
    print(college)

    all_courses = {}

    for major, courses in colleges[college]["majors"].items():
        bachelors_website = colleges[college]['bachelors_degrees_link']
        driver.get(bachelors_website)

        link_to_major = driver.find_element(By.LINK_TEXT, major)
        link_to_major.click()

        try:
            major_requirements = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "planrequirementstexttab")))
        except Exception:
            major_requirements = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "programrequirementstexttab")))
        major_requirements.click()

        # Find all tr elements on the page
        table_rows = driver.find_elements(By.TAG_NAME, "tr")

        # Concatenate the text of each tr element into a single string, separated by new lines
        all_text = "\n".join([row.text for row in table_rows])

        # Now split the variable as required
        # First, split by "Total" and take the first part ([0])
        # Then split by new lines ("\n") to get a list of strings
        courses = all_text.split("Total")[0].split("\n")

        all_courses[major] = courses

    return all_courses
        

def convert_to_json(college_list: list, majors_and_courses: dict):
    """
    converts colleges, majors, and courses into a dict
    then converts this dict to json to be read by frontend
    :param college_list: list of colleges
    :param majors_and_courses: dict of majors as keys and courses as values
    :return: void
    """

    all_college_courses_dict = {}
    i = 0

    for college in college_list:
        all_college_courses_dict[college] = majors_and_courses[i]
        i += 1

    # print(all_college_courses_dict)

    with open("exports/courses/courses.json", "w") as file:
        json.dump(all_college_courses_dict, file)


def main():
    # chrome executable
    # chromedriver-mac-arm64/chromedriver for mac
    # chromedriver.exe for windows
    service = Service(executable_path="chromedriver-mac-arm64/chromedriver")
    driver = webdriver.Chrome(service=service)

    college_list = colleges.keys()
    # print(list(college_list))

    unc_charlotte_majors_and_courses = get_unc_charlotte_courses(driver, college_list)
    unc_chapel_majors_and_courses = get_unc_chapel_courses(driver, college_list)
    ncsu_majors_and_courses = get_nc_state_courses(driver, college_list)

    majors_and_courses = [unc_charlotte_majors_and_courses, unc_chapel_majors_and_courses, ncsu_majors_and_courses]

    convert_to_json(college_list, majors_and_courses)

    driver.quit()


main()
