import pandas as pd
import json

# Read the CSV file
df = pd.read_csv('Destination Places-Destination List.csv', header=None)

# Split each line at the comma and take the first word
df[0] = df[0].str.split(',').str[0]

# Split each line at the '+' and take the first part
df[0] = df[0].str.split('+').str[0].str.strip()

# Convert the DataFrame column to a list
list_of_first_words = df[0].tolist()

# Open the second file and load the dictionary
with open('country_urls.txt', 'r') as file:
    dict_data = json.load(file)
print(f"Number of keys in dictionary in country_urls.txt: {len(dict_data)}")

# Open the first file and load the list
with open('no_result_country.txt', 'r') as file:
    list_data = json.load(file)
print(f"Length of list in no_result_country.txt: {len(list_data)}")