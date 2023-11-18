# Import the pandas library
import pandas as pd  

# Load the data from the CSV files
# Read the CSV file into a DataFrame
df_sevilla = pd.read_csv('Seville.csv', header=None)  

# Function to clean data
def clean_data(file_name, city_name):
    # Load the data from the CSV file
    # Read the CSV file into a DataFrame
    df = pd.read_csv(file_name, header=None)  

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
df_sevilla = clean_data('Seville.csv', 'Seville')  

# Concatenate the DataFrames into a single DataFrame
df = pd.concat([df_sevilla])  

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
    df = clean_temperature(df, column)

# Function to clean precipitation
def clean_precipitation(df, column):
    # Replace the '\n' in the column with ' '
    df[column] = df[column].str.replace('\n', ' ')
    return df

# Clean precipitation
df = clean_precipitation(df, 'Precipitation / Rainfall mm (in)')

# Print the final DataFrame
print(df)

# Save the DataFrame to a CSV file with ';' as the delimiter
# Encoding ISO-8859-1 because some countries have accent in some words: "ó" "ô"
df.to_csv('Seville_Clean.csv', index=False, encoding='ISO-8859-1', sep=';')