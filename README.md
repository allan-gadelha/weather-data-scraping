# Weather Data Scraping Project

## Overview

This project focuses on scraping comprehensive weather data from the website Climate Data (https://en.climate-data.org/). The objective is to gather insights into weather patterns for 350 destinations worldwide over a 30-year span (1991-2021). As of recent updates the new dataset contains data from 3,833 destinations from 6 Continents.

## Project Structure

The project is organized as follows:

- **`data/`**: Contains data files generated during the scraping and cleaning process.
  - `full_continents_url.json`: JSON file with URLs for each city, organized by continent, country, and city.

  - `full_continent_corrected_UTF-8.csv`: Cleaned CSV file with weather data for 3,833 destinations, including Min. Temperature, Max. Temperature, Precipitation/Rainfall, Average Sun Hours, Rainy Days, and more.

- **`notebooks/`**: Contains Jupyter notebooks for analysis.
  - `analysis.ipynb`: Notebook for analyzing the extracted and cleaned weather data.

- **`scripts/`**: Contains Python scripts for web scraping and data processing.
  - `full_application_continent_country_city_url_extract.py`: Initial scraping to obtain URLs for each city, organized in a nested dictionary format (`full_continents_url.json`).

  - `full_application_urls_json_table_extract_clean.py`: Secondary scraping to access the URLs and extract data from tables. The extracted data includes weather variables such as Min. Temperature, Max. Temperature, Precipitation/Rainfall, Average Sun Hours, Rainy Days, and more. The output is a cleaned CSV file (`full_continent_corrected_UTF-8.csv`). An older version is also available as `full_continent_extract_clean_UTF-8.csv`.

- **`.gitignore`**: File to specify files and directories that should be ignored by version control (e.g., `__pycache__`, `*.pyc`, `*.csv`, etc.).

- **`README.md`**: Project documentation.

- **`requirements.txt`**: List of Python packages and versions required for the project.

## Getting Started

To get started with the project, follow these steps:

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/allan-gadelha/weather-data-scraping.git
   cd weather-data-scraping

2. **Install Dependencies:**
    ```bash
    pip install -r requirementes.txt
    ```

3. **Run Scripts and Notebooks:**
    - Run `scripts/full_application_continent_country_city_url_extract.py` to perform the initial scraping and obtain city URLs.
    
    - Run `scripts/full_application_urls_json_table_extract_clean.py` to perform the secondary scraping, extracting and cleaning weather data.

    - Explore and analyze the extracted data using `notebooks/analysis.ipynb`.

4. **Explore Cleaned Data:**
    - Find the cleaned weather data in the `data/full_continent_corrected_UTF-8.csv` file.

## Requeriments

- Selenium
- BeautifulSoup
- Pandas
- Pprint
- Json

## Contact

For any questions or issues, feel free to contact the project owner:

- Email: [Allan Gadelha](mailto:c.allan.gadelha@gmail.com)
- GitHub: [Allan Gadelha](https://github.com/allan-gadelha)