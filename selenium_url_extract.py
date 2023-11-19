import json
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from msedge.selenium_tools import Edge, EdgeOptions
from selenium.webdriver.common.alert import Alert
import pandas as pd
from formating_text import list_of_first_words, list_of_first_words_2

# Create a new instance of the Edge driver in InPrivate mode
path = r"C:/Users/deimo/Desktop/Global_Weather/msedgedriver.exe"
options = EdgeOptions()
options.use_chromium = True
options.add_argument("--headless")
driver = Edge(executable_path=path, options=options)

# Navigate to the target webpage
driver.get("https://en.climate-data.org/")

# Define wait
wait = WebDriverWait(driver, 10)

# Handle the alert popup
try:
    alert = Alert(driver)
    alert.accept()
except:
    pass

# Create an empty dictionary to store the country names and URLs
country_urls = {}

# Create a list to store the country names that didn't have a search result
no_result_countries = []

# Iterate over the list of country names
#Changing to list_of_first_2 to run the code again on the country that didn't get a result on first try
for country in list_of_first_words_2:
    # Click on the search form
    search_form = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#search-form-header > span')))
    driver.execute_script("arguments[0].click();", search_form)   # Use JavaScript to click
    
    # Wait for the search input field to be clickable
    search_input = wait.until(EC.element_to_be_clickable((By.NAME, 'q')))

    # Enter the country name
    search_input.clear()
    search_input.send_keys(country)

    # Submit the form by pressing Enter
    search_input.send_keys(Keys.RETURN)

    try:
        # Click on the first search result
        first_result = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.name')))
        driver.execute_script("arguments[0].click();", first_result)  # Use JavaScript to click

        # Get the URL of the new page
        url = driver.current_url

        # Store the country name and URL in the dictionary
        country_urls[country] = url

        # Save the dictionary to a text file
        with open('country_urls_2.txt', 'w') as file:
           file.write(json.dumps(country_urls))

        #Print the country name and URL for debug
        print(f'Country: {country}, URL: {country_urls[country]}')
        
    except:
        # If the search doesn't yield a result, store the country name in no_result_countries and continue with the next iteration
        no_result_countries.append(country)
        
        #Saving the country that didn't have a result
        with open('no_result_country.txt_2', 'w') as file:
            file.write(json.dumps(no_result_countries))

        continue

# Close the browser driver
driver.quit()