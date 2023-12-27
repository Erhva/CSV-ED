import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException  
from selenium.webdriver.chrome.options import Options
import gui

def main():
    # Replace these with your CSV file path, columns to copy, webdriver path, and website URL
    csv_file = 'ExportedTransactions.csv' #Change to your csv file, store in same directory
    columns_to_copy = ['Amount', 'Posting Date', 'Description'] #Change depending on CSV format
    webdriver_path = r"C:\Users\ehall\AppData\Local\Google\Chrome\chrome-win64\chrome.exe" #Change this to your webdriver path
    website_url = 'https://www.everydollar.com/app/budget/transaction/new'
    login_url = 'https://id.ramseysolutions.com/login'

    # Replace with your login credentials
    username = gui.username
    password = gui.password

    data_to_fill = read_csv_and_get_columns(csv_file, columns_to_copy)
    driver = setup_webdriver(webdriver_path, website_url)

    login(driver, login_url, username, password)
    fill_web_form(driver, website_url, data_to_fill)
    time.sleep(1)

def read_csv_and_get_columns(csv_file, columns_to_copy):
    df = pd.read_csv(csv_file)
    df['Amount'] = pd.to_numeric(df['Amount'], errors='coerce')
    selected_columns = df[columns_to_copy]
    return selected_columns

def setup_webdriver(webdriver_path, website_url):
    options = webdriver.ChromeOptions()
    options.binary_location = webdriver_path

    driver = webdriver.Chrome(options=options)
    return driver

def fill_web_form(driver, website_url, data_to_fill):
    # Navigate directly to new transaction form, run it multiple times to brute force past all the pop-ups
    # TODO: Implement a better pop-up solution
    driver.get(website_url)
    driver.get(website_url)
    driver.get(website_url)

    input_selectors = ['input[name="amount"]', 'input[name="date"]', 'input[name="merchant"]']

    for index, row in data_to_fill.iterrows():
        driver.get(website_url)
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[name="amount"]')))
        for i, column_value in enumerate(row):
            if isinstance(column_value, (int, float)) and column_value > 0:
                WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div[class="rds-Radio TransactionForm-typeOption TransactionForm-typeOption--income"]')))
                income_click = driver.find_element(By.CSS_SELECTOR, 'div[class="rds-Radio TransactionForm-typeOption TransactionForm-typeOption--income"]').click()     
            else: None
            input_element = driver.find_element(By.CSS_SELECTOR, input_selectors[i])
            input_element.clear()  # Clear any previous data in the input field
            input_element.send_keys(str(column_value))
        submit_button = driver.find_element(By.CSS_SELECTOR, 'button[id="TransactionModal_submit"][type="submit"]').click()
        time.sleep(1)

def login(driver, login_url, username, password):
    driver.get(login_url)

    try:
        # Wait for the email input field to be visible
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[name="email"][id="1-email"]'))).click()
        
        # Find the input fields for username and password
        username_input = driver.find_element(By.CSS_SELECTOR, 'input[name="email"][id="1-email"]')
        password_input = driver.find_element(By.CSS_SELECTOR, 'input[name="password"]')

        # Fill in the login credentials
        username_input.send_keys(username)
        password_input.send_keys(password)

        # Locate and click the login/submit button
        try:
            login_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[name="submit"][id="1-submit"]'))).click()
        except NoSuchElementException:
            print("Login button not found. Please check the CSS selector.")


    except TimeoutException:
        print("Login failed. URL did not change. Please check your login credentials.")
    
    # Wait for successful login
    WebDriverWait(driver, 10).until(EC.url_changes(login_url))

def close_webdriver(driver):
    driver.quit()


if __name__ == "__main__":
    main()
