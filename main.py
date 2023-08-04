import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

def read_csv_and_get_columns(csv_file, columns_to_copy):
    df = pd.read_csv()
    selected_columns = df[columns_to_copy]
    return selected_columns

def setup_webdriver(webdriver_path, website_url):
    driver = webdriver.Chrome(executable_path=webdriver_path)
    driver.get(website_url)
    return driver

def fill_web_form(driver, data_to_fill):
    # Replace these selectors with the appropriate ones for your web form
    input_selectors = ['selector_for_column1_input', 'selector_for_column2_input', ...]

    for index, row in data_to_fill.iterrows():
        for i, column_value in enumerate(row):
            input_element = driver.find_element_by_css_selector(input_selectors[i])
            input_element.clear()  # Clear any previous data in the input field
            input_element.send_keys(str(column_value))
            # Add delay (if needed) to avoid overwhelming the server
            # time.sleep(1)

            # You can also submit the form after filling each row (if desired)
            # input_element.send_keys(Keys.RETURN)

        # Optionally, you can add a delay between filling each row (if needed)
        # time.sleep(2)

def close_webdriver(driver):
    driver.quit()

def main():
    # Replace these with your CSV file path, columns to copy, webdriver path, and website URL
    csv_file = 'ExportedTransactions.csv'
    columns_to_copy = ['column1', 'column2', ...]
    webdriver_path = 'C:\Program Files (x86)\chromedriver-win64\chromedriver.exe'
    website_url = 'https://www.everydollar.com/app/budget/transaction/new'

    data_to_fill = read_csv_and_get_columns(csv_file, columns_to_copy)
    driver = setup_webdriver(webdriver_path, website_url)
    fill_web_form(driver, data_to_fill)
    close_webdriver(driver)

if __name__ == "__main__":
    main()
