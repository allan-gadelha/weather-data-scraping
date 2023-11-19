# Import necessary libraries
from msedge.selenium_tools import Edge, EdgeOptions
from bs4 import BeautifulSoup
import pandas as pd
import json

with open(r'C:\Users\deimo\Desktop\weather-data-scrapping\country_url_final.txt', 'r') as file:
    country_urls = json.load(file)

# Create a new instance of the Edge driver
path = r"C:/Users/deimo/Desktop/Global_Weather/msedgedriver.exe"
options = EdgeOptions()
options.use_chromium = True
options.add_argument("--headless")
driver = Edge(executable_path=path, options=options)

# Create an empty DataFrame to store the completed data
completed_data = pd.DataFrame()

# Iterate over the country_urls dictionary
for country, url in country_urls.items():
    # Go to the webpage
    driver.get(url)

    # Get the HTML content of the page
    html = driver.page_source

    # Parse the HTML content
    soup = BeautifulSoup(html, 'html.parser')

    # Find the table with the climate data
    table = soup.find('table', {'id': 'weather_table'})

    # If the table was not found, print an error message and continue with the next iteration
    if table is None:
        print(f"Could not find the weather table for {country}.")
        continue

    # Extract the data from the table header and body
    thead = table.find('thead')
    tbody = table.find('tbody')

    # Extract the data and store it in a DataFrame
    data = []
    for row in thead.find_all('tr') + tbody.find_all('tr'):
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        data.append([ele for ele in cols if ele])

    df = pd.DataFrame(data)

    # Append the DataFrame to the completed_data DataFrame
    completed_data = pd.concat([completed_data, df], ignore_index=True)
    completed_data.to_csv(f"C:/Users/deimo/Desktop/weather-data-scrapping/countries_csv/{country}.csv", index=False)
    completed_data = pd.DataFrame()

# Close the browser
driver.quit()

# Save the completed_data DataFrame to a CSV file
#completed_data.to_csv(f"C:/Users/deimo/Desktop/Global_Weather/countries_csv/{country}.csv", index=False)

# Print the DataFrame
print(completed_data)