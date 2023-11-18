import pandas as pd  # Import the pandas library

# Load the data from the CSV files
df_sevilla = pd.read_csv('Seville.csv', header=None)  # Read the CSV file into a DataFrame

def clean_data(file_name, city_name):
    # Load the data from the CSV file
    df = pd.read_csv(file_name, header=None)  # Read the CSV file into a DataFrame

    # Select the 'Min. Temperature ºC (ºF)', 'Max. Temperature ºC (ºF)', 'Precipitation / Rainfall mm (in)', 'avg. Sun hours (hours)', and 'Rainy days (d)' rows
    df_clean = df[df[0].isin(['Min. Temperature °C (°F)', 'Max. Temperature °C (°F)', 'Precipitation / Rainfall mm (in)', 'avg. Sun hours (hours)', 'Rainy days (d)'])]  # Filter the DataFrame

    # Transpose the DataFrame
    df_clean = df_clean.transpose()  # Transpose the DataFrame (swap rows and columns)

    # Set the first row as the header
    df_clean.columns = df_clean.iloc[0]  # Set the first row as the column names
    df_clean = df_clean[1:]  # Remove the first row

    # Reset the index
    df_clean.reset_index(drop=True, inplace=True)  # Reset the index of the DataFrame

    # Add the city name to the DataFrame
    df_clean['City'] = city_name  # Add a new column with the city name

    # Add the month names to the DataFrame
    df_clean['Month'] = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']  # Add a new column with the month names

    # Rearrange the columns
    df_clean = df_clean[['City', 'Month', 'Min. Temperature °C (°F)', 'Max. Temperature °C (°F)', 'Precipitation / Rainfall mm (in)', 'avg. Sun hours (hours)', 'Rainy days (d)']]  # Rearrange the columns of the DataFrame

    return df_clean  # Return the cleaned DataFrame

# Call the function for each CSV file
df_sevilla = clean_data('Seville.csv', 'Seville')  # Clean the data for Seville

# Concatenate the DataFrames
df = pd.concat([df_sevilla])  # Concatenate the DataFrames into a single DataFrame

# Replace the '\n' in the 'Avg. Temperature °C (°F)' column with ' ('
df['Min. Temperature °C (°F)'] = df['Min. Temperature °C (°F)'].str.replace('\n', ' (')  # Replace newline characters with ' ('
df['Max. Temperature °C (°F)'] = df['Max. Temperature °C (°F)'].str.replace('\n', ' (')  # Replace newline characters with ' ('

# Add ')' to the end of the 'Avg. Temperature °C (°F)' column
df['Min. Temperature °C (°F)'] = df['Min. Temperature °C (°F)'] + ')'  # Add ')' to the end of the string
df['Max. Temperature °C (°F)'] = df['Max. Temperature °C (°F)'] + ')'  # Add ')' to the end of the string

# Extract the Fahrenheit values from the 'Min. Temperature °C (°F)' and 'Max. Temperature °C (°F)' columns
df['Min. Temperature °C (°F)'] = df['Min. Temperature °C (°F)'].str.extract(r'\((.*?) °F\)', expand=False)
df['Max. Temperature °C (°F)'] = df['Max. Temperature °C (°F)'].str.extract(r'\((.*?) °F\)', expand=False)

# Remove the parentheses from the 'Min. Temperature °C (°F)' and 'Max. Temperature °C (°F)' columns
df['Min. Temperature °C (°F)'] = df['Min. Temperature °C (°F)'].str.replace('(', '').str.replace(')', '') + ' °F'
df['Max. Temperature °C (°F)'] = df['Max. Temperature °C (°F)'].str.replace('(', '').str.replace(')', '') + ' °F'

# Remove 'F' from the 'Min. Temperature °C (°F)' and 'Max. Temperature °C (°F)' columns
df['Min. Temperature °C (°F)'] = df['Min. Temperature °C (°F)'].str.replace('F', '')
df['Max. Temperature °C (°F)'] = df['Max. Temperature °C (°F)'].str.replace('F', '')

# Remove 'º' from the 'Min. Temperature °C (°F)' and 'Max. Temperature °C (°F)' columns
df['Min. Temperature °C (°F)'] = df['Min. Temperature °C (°F)'].str.replace('°', '')
df['Max. Temperature °C (°F)'] = df['Max. Temperature °C (°F)'].str.replace('°', '')

# Print the final DataFrame
print(df)

# Save the DataFrame to a CSV file with ';' as the delimiter
#Econding ISO-8859-1 because some countries have accent in some words: "ó" "ô"
df.to_csv('Seville_Clean.csv', index=False, encoding='ISO-8859-1', sep=';')