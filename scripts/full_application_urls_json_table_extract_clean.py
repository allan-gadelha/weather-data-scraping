# Import necessary libraries
from msedge.selenium_tools import Edge, EdgeOptions
from bs4 import BeautifulSoup
import pandas as pd
import json

with open(r'C:\Users\deimo\Desktop\weather-data-scrapping\data\full_continents_url.json', 'r') as file:
    continents_urls = json.load(file)

# Create a new instance of the Edge driver
path = r"C:/Users/deimo/Desktop/Global_Weather/msedgedriver.exe"
options = EdgeOptions()
options.use_chromium = True
options.add_argument("--headless")
driver = Edge(executable_path=path, options=options)

# Create an empty DataFrame to store the completed data
completed_data = pd.DataFrame()

# Function to clean data
def clean_data(df, continent_name, country_name, city_name):
    # Transpose the DataFrame (swap rows and columns)
    df_clean = df.transpose()

    # Set the first row as the column names
    df_clean.columns = df_clean.iloc[0]
    # Remove the first row
    df_clean = df_clean[1:]

    # Reset the index of the DataFrame
    df_clean.reset_index(drop=True, inplace=True)

    # Add new columns with the continent, country, and city names
    df_clean['Continent'] = continent_name
    df_clean['Country'] = country_name
    df_clean['City'] = city_name

    # Add a new column with the month names
    df_clean['Month'] = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

    # Check if 'avg. Sun hours (hours)' column exists
    if 'avg. Sun hours (hours)' in df_clean.columns:
        df_clean['avg. Sun hours (hours)'] = df_clean['avg. Sun hours (hours)'].fillna(0)
    else:
        df_clean['avg. Sun hours (hours)'] = 0


    # Rearrange the columns of the DataFrame
    df_clean = df_clean[['Continent', 'Country', 'City', 'Month', 'Avg. Temperature °C (°F)', 'Min. Temperature °C (°F)', 'Max. Temperature °C (°F)', 'Precipitation / Rainfall mm (in)', 'Rainy days (d)', 'avg. Sun hours (hours)']]

    # Return the cleaned DataFrame
    return df_clean

# Iterate over the continents, countries, and cities in the dictionary
for continent_name, continent_info in continents_urls.items():
    for country_name, country_info in continent_info["countries"].items():
        for city_name, city_info in country_info["cities"].items():
            url = city_info.get("url")
            # Check if the url is a string
            if isinstance(url, str):
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
                    print(f"Could not find the weather table for {city_name}.")
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

                # Clean the DataFrame
                df_clean = clean_data(df, continent_name, country_name, city_name)

                # Append the cleaned DataFrame to the completed_data DataFrame
                completed_data = pd.concat([completed_data, df_clean], ignore_index=True)
            else:
                print(f"Invalid URL for {city_name}.")

# Close the browser
driver.quit()

# Function to clean temperature
def clean_temperature(df, column):
    # Replace the '\n' in the column with ' ('
    df[column] = df[column].str.replace('\n', ' (')
    
    # Add ')' to the end of the column
    df[column] += ')'
    
    # Extract the numeric values from the column
    df[column] = df[column].str.extract(r'\((-?[0-9\.]*)\) °F', expand=False)
    
    return df

# Function to clean precipitation
def clean_precipitation(df, column):
    # Replace the '\n' in the column with ' '
    df[column] = df[column].str.replace('\n', ' ')
    return df

# Columns to clean
columns_to_clean = ['Avg. Temperature °C (°F)','Min. Temperature °C (°F)', 'Max. Temperature °C (°F)']

# Clean temperature for each column
for column in columns_to_clean:
    completed_data = clean_temperature(completed_data, column)

# Clean precipitation
completed_data = clean_precipitation(completed_data, 'Precipitation / Rainfall mm (in)')

# Save the completed_data DataFrame to a CSV file
completed_data.to_csv(f"data/full_continent_corrected_UTF-8.csv", index=False, encoding='UTF-8', sep=';')