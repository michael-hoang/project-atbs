import os
import pandas as pd
import time

from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options


class DrugParser:
    """
    A class for parsing drung information from AmerisourceBergen's ABC ordering platform.
    """

    def __init__(self, driver_path, mode='default'):
        self.service = Service(driver_path)
        self.options = Options()
        if mode == 'headless':
            self.options.add_argument('--headless')
        elif mode == 'default':
            self.options.add_experimental_option('detach', True)

        self.driver = webdriver.Edge(
            service=self.service, options=self.options
        )
        self.website_url = 'https://abcorderhs.amerisourcebergen.com/'

    def open_website(self):
        self.driver.get(self.website_url)

    def sign_in(self, username: str, password: str):
        username_input = self.driver.find_element(By.ID, 'logonuidfield')
        username_input.send_keys(username)
        password_input = self.driver.find_element(By.ID, 'logonpassfield')
        password_input.send_keys(password)
        sign_in_btn = self.driver.find_element(By.NAME, 'uidPasswordLogon')
        sign_in_btn.click()

    def go_to_abc_order(self):
        abc_order = self.driver.find_element(By.LINK_TEXT, 'ABC ORDER')
        abc_order.click()

    def search_ndc(self, ndc):
        search_box = self.driver.find_element(By.CLASS_NAME, 'text-input')
        search_box.send_keys(ndc)
        search_btn = self.driver.find_element(
            By.XPATH, '//*[@id="styled-nav-container"]/div[2]/div/div/div[2]/button'
        )
        search_btn.click()


if __name__ == '__main__':
    # Load environment variables from .env file
    load_dotenv()

    # Get environment variables
    USER = os.environ.get('USER')
    PASSWORD = os.environ.get('PASSWORD')

    webdriver_path = r'C:\Users\Mike\OneDrive\Desktop\edgedriver_win64\msedgedriver.exe'
    dp = DrugParser(webdriver_path)
    dp.open_website()
    time.sleep(3)
    dp.sign_in(USER, PASSWORD)
    time.sleep(4)
    dp.go_to_abc_order()
    time.sleep(3)
    dp.search_ndc('metformin')

    # data = pd.read_excel('./assets/data/drugs.xlsx')
    # item_df = pd.DataFrame(data, columns=['Item'])
    # ndc_df = pd.DataFrame(data, columns=['NDC'])

    # unique_ndcs = []
    # unique_drugs = []

    # for ndc in ndc_df['NDC']:
    #     formatted_ndc = str(ndc).zfill(11)
    #     if formatted_ndc not in unique_ndcs:
    #         unique_ndcs.append(formatted_ndc)

    # for item in item_df['Item']:
    #     print(item)

    # print(len(unique_ndcs))
