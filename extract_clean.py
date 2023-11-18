# Import the pandas library
import pandas as pd
import os
import json  

#Load the dictionary from the text file
with open(r'C:\Users\deimo\Desktop\weather-data-scrapping\country_url_final.txt', 'r') as file:
      country_urls = json.load(file)

# Function to clean data
def clean_data(file_name):
    # Load the data from the CSV file
    # Read the CSV file into a DataFrame
    df = pd.read_csv(file_name, header=None)  
    city_name = os.path.basename(file_name).split('.')[0]

    print(f"Processing file: {file_name}")

    # Select the 'Min. Temperature ºC (ºF)', 'Max. Temperature ºC (ºF)', 'Precipitation / Rainfall mm (in)', 'avg. Sun hours (hours)', and 'Rainy days (d)' rows
    # Filter the DataFrame
    df_clean = df[df[0].isin(['Min. Temperature °C (°F)', 'Max. Temperature °C (°F)', 'Precipitation / Rainfall mm (in)', 'avg. Sun hours (hours)', 'Rainy days (d)'])]  

    # Transpose the DataFrame (swap rows and columns)
    df_clean = df_clean.transpose()  

    # Set the first row as the column names
    df_clean.columns = df_clean.iloc[0]  
    # Remove the first row
    df_clean = df_clean[1:]  

    # Reset the index of the DataFrame
    df_clean.reset_index(drop=True, inplace=True)  

    # Add a new column with the city name
    df_clean['City'] = city_name  

    # Add a new column with the month names
    df_clean['Month'] = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']  

    # Rearrange the columns of the DataFrame
    df_clean = df_clean[['City', 'Month', 'Min. Temperature °C (°F)', 'Max. Temperature °C (°F)', 'Precipitation / Rainfall mm (in)', 'avg. Sun hours (hours)', 'Rainy days (d)']]  

    # Return the cleaned DataFrame
    return df_clean  

# Clean the data for Seville
#df_sevilla = clean_data('Seville.csv', 'Seville')  

# Get a list of all CSV files in the directory
csv_files = [f for f in os.listdir('countries_csv') if f.endswith('.csv')]

# Create an empty DataFrame to store the completed data
completed_data = pd.DataFrame()

# Concatenate the DataFrames into a single DataFrame
#df = pd.concat([df_sevilla])

# Iterate over the CSV files
for file_name in csv_files:
    # Apply the clean_data function to the file
    df = clean_data(f'C:/Users/deimo/Desktop/weather-data-scrapping/countries_csv/{file_name}')

    # Append the DataFrame to the completed_data DataFrame
    completed_data = pd.concat([completed_data, df], ignore_index=True)
   

# Function to clean temperature
def clean_temperature(df, column):
    # Replace the '\n' in the column with ' ('
    df[column] = df[column].str.replace('\n', ' (')
    
    # Add ')' to the end of the column
    df[column] += ')'
    
    # Extract the numeric values from the column
    df[column] = df[column].str.extract(r'\(([0-9\.]*)\) °F', expand=False)
    
    return df

# Columns to clean
columns_to_clean = ['Min. Temperature °C (°F)', 'Max. Temperature °C (°F)']

# Clean temperature for each column
for column in columns_to_clean:
    completed_data = clean_temperature(completed_data, column)

# Function to clean precipitation
def clean_precipitation(df, column):
    # Replace the '\n' in the column with ' '
    df[column] = df[column].str.replace('\n', ' ')
    return df

# Clean precipitation
completed_data = clean_precipitation(completed_data, 'Precipitation / Rainfall mm (in)')

# Print the final DataFrame
print(completed_data)

# Save the DataFrame to a CSV file with ';' as the delimiter
# Encoding ISO-8859-1 because some countries have accent in some words: "ó" "ô"
completed_data.to_csv('completed_data.csv', index=False, encoding='ISO-8859-1', sep=';')