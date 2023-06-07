from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd

# Setup Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")

# Setup WebDriver
webdriver_service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=webdriver_service, options=chrome_options)

# Navigate to the website
driver.get("https://www.zlatakoruna.info/financni-produkty/bankovni-uvery")

# Find all "a" tags inside div with class "basic-info" in the table with id "table-porovnavac"
elements = driver.find_elements(By.CSS_SELECTOR, '#table-porovnavac .basic-info a')

# URLs to visit
urls = [element.get_attribute('href') for element in elements]

# List to store DataFrames
dfs = []

# Visit each URL
for url in urls:
    driver.get(url)

    # Parse the page source with BeautifulSoup
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Find the table with id "comparison"
    table = soup.find('table', {'id': 'comparison'})

    # Dict to store our scraped data
    data = {}

    # Iterate over all the rows in the table
    for row in table.find_all('tr'):
        # Each row has two cells - "field-name" and "field-value"
        cells = row.find_all('td')
        if len(cells) == 2:
            field_name = cells[0].get_text().strip()
            field_value = cells[1].get_text().strip()

            # Add the data to our dict
            data[field_name] = field_value

    # Create a DataFrame from the data dict and add it to the list
    dfs.append(pd.DataFrame([data]))

# Concatenate all DataFrames into one
df = pd.concat(dfs, ignore_index=True)

# Close the WebDriver
driver.quit()

# Write the DataFrame to a CSV file
df.to_csv('output.csv', index=False)
