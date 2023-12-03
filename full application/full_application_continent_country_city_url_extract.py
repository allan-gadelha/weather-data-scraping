from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from msedge.selenium_tools import Edge, EdgeOptions
from selenium.webdriver.common.alert import Alert
import pandas as pd
import requests
from bs4 import BeautifulSoup
#Print my Data Structures 
import pprint
import json

# Create a new instance of the Edge driver in InPrivate mode
path = r"C:/Users/deimo/Desktop/Global_Weather/msedgedriver.exe"
options = EdgeOptions()
options.use_chromium = True
options.add_argument("--headless")
driver = Edge(executable_path=path, options=options)

# Define wait
wait = WebDriverWait(driver, 10)

# Handle the alert popup
try:
    alert = Alert(driver)
    alert.accept()
except:
    pass

# Create a dictionary with the continent names and URLs
continents = {
    "North America": {"url": "https://en.climate-data.org/continent/north-america/", "countries": {}},
    "South America": {"url": "https://en.climate-data.org/continent/south-america/", "countries": {}},
    "Africa": {"url": "https://en.climate-data.org/continent/africa/", "countries": {}},
    "Europe": {"url": "https://en.climate-data.org/continent/europe/", "countries": {}},
    "Asia": {"url": "https://en.climate-data.org/continent/asia/", "countries": {}},
    "Oceania": {"url": "https://en.climate-data.org/continent/oceania/", "countries": {}}
}

# First Step
# Iterate over the Continents in the dictionary
for continent_name, continent_info in continents.items():
    # Navigate to the continent URL
    driver.get(continent_info["url"])

    ul_element = driver.find_element_by_css_selector('ul.f16')

    country_elements = ul_element.find_elements_by_tag_name('li')

    # Iterate over the country elements
    for country_element in country_elements:
        # Find the 'a' element inside the country element
        a_element = country_element.find_element_by_tag_name('a')
        
        # Get the URL and text of the 'a' element
        url = a_element.get_attribute('href')
        text = a_element.text

        # Add the country and its URL to the 'countries' dictionary
        continent_info["countries"][text] = {"url": url, "cities": {}}

# Second Step
# Iterate over the Countries in the dictionary
for continent_name, continent_info in continents.items():
    # Iterate over the countries in the continent
    for country_name, country_info in continent_info["countries"].items():
        # Navigate to the country URL
        driver.get(country_info["url"])
        
        # Wait for the table to be present
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//table')))

        # Find the table
        table = driver.find_element_by_xpath('//table')

        # Find all the rows in the table
        rows = table.find_elements_by_xpath('.//tr')

        # Iterate over the rows
        for row in rows:
            try:
                # Find all 'a' elements in the 4th cell of the row
                cells = row.find_elements_by_xpath('.//td[4]/a')

                # Iterate over the 'a' elements
                for cell in cells:
                    # Get the URL from the 'a' element
                    url = cell.get_attribute('href')

                    # Get the text of the 'a' element
                    text = cell.text

                    # Add the city and its URL to the 'cities' dictionary
                    country_info["cities"][text] = {"url": url}
            except:
                # If the 4th cell was not found, skip this row
                continue

# Create a pretty printer
pp = pprint.PrettyPrinter(indent=4)

# Use it to print your dictionary
pp.pprint(continents)

with open('full application/full_continents_url.json.json', 'w') as f:
    # Use json.dump to write the dictionary to the file
    json.dump(continents, f)

driver.quit()