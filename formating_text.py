import pandas as pd
import json

#Need to create here so i could import(?)
list_of_first_words_2 = []

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

# Creating a new list just for the first words
#List from no_result_country to pass it again on the selenium_url_extract
list_of_first_words_2 = [word.split(' ')[0] for word in list_data]


with open('no_result_country.txt_2', 'r') as file:
    list_data_2 = json.load(file)
print(f"Length of list in no_result_country_2.txt: {len(list_data)}")


with open('country_urls_2.txt', 'r') as file:
    dict_data_2 = json.load(file)
print(f"Number of keys in dictionary in country_urls_2.txt: {len(dict_data_2)}")


# Merge the two dictionaries
merged_dict = {**dict_data, **dict_data_2}

# Write the merged dictionary to a new file
with open('country_url_final.txt', 'w') as file:
    json.dump(merged_dict, file)

print(f"Number of keys in dictionary in country_url_final.txt: {len(merged_dict)}")