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
    



data = pd.read_excel('./assets/data/drugs.xlsx')
item_df = pd.DataFrame(data, columns=['Item'])
ndc_df = pd.DataFrame(data, columns=['NDC'])

unique_ndcs = []
unique_drugs = []

for ndc in ndc_df['NDC']:
    formatted_ndc = str(ndc).zfill(11)
    if formatted_ndc not in unique_ndcs:
        unique_ndcs.append(formatted_ndc)
      

for item in item_df['Item']:
    print(item)

print(len(unique_ndcs))
