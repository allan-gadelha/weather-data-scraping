# Import necessary libraries
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd

# URL for Sevilla's climate data
url = "https://en.climate-data.org/europe/spain/andalusia/seville-2933/"

# Create a new instance of the Edge driver
# Make sure to replace the path with the path where your Edge driver is located
path = r"C:/Users/deimo/Desktop/Global_Weather/msedgedriver.exe"
driver = webdriver.Edge(executable_path=path)

# Navigate to the webpage
driver.get(url)

# Get the HTML content of the page
html = driver.page_source

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(html, 'html.parser')

# Find the table with the climate data
table = soup.find('table', {'id': 'weather_table'})

# If the table was not found, print an error message and exit
if table is None:
    print("Could not find the weather table.")
    driver.quit()
    exit()

# Extract the data from the table header and body
thead = table.find('thead')
tbody = table.find('tbody')

# Extract the data and store it in a DataFrame
data = []
# Loop through each row in the table header and body
for row in thead.find_all('tr') + tbody.find_all('tr'):
    # Find all the columns in the row
    cols = row.find_all('td')
    # Strip any extra whitespace from the text in the columns
    cols = [ele.text.strip() for ele in cols]
    # Add the columns to the data list if they are not empty
    data.append([ele for ele in cols if ele])

# Convert the data list into a DataFrame
df = pd.DataFrame(data)

# Save the DataFrame to a CSV file
df.to_csv("Seville.csv", index=False)

# Close the browser
driver.quit()

# Print the DataFrame to the console
print(df)