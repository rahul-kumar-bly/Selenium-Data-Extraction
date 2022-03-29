# Packages
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import chrome
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from time import sleep
import pandas
from tqdm import tqdm

WEBSITE_URL = "https://rugsforyou.in/shop/"
CSV_FILE = "rugs.xlsx"
opts = Options()
opts.headless = True
s = Service('chromedriver.exe')
driver = webdriver.Chrome(options=opts, service=s)
driver.get(WEBSITE_URL)
product_list = list()

eof = True
while eof:
    try:
        product_title = driver.find_elements(By.CLASS_NAME, value="ms-product-block")
        # product_title = driver.find_elements(By.CLASS_NAME, value="woocommerce-loop-product__title")
        print("#"*40)
        print("URL in use:",driver.current_url)
        for i in tqdm(range(0, len(product_title)), desc="Finding items..."):
            product_list.append(product_title[i].text.split('\n'))
        print("#"*40)
        next_page = driver.find_element(By.XPATH, value="//ul/li/a[contains(@class, 'next')]")
        next_page.click()
    except:
        eof = False

print("-"*50)        
print("Total items found:", len(product_list))
print("-"*50)        

try:
    for i in tqdm(product_list, desc="Generating CSV..."):
        df = pandas.DataFrame(product_list)
        df.to_excel(CSV_FILE)
        sleep(.1)
    print("-"*50)        
    print("CSV File generated in", Path.cwd(),"with name",CSV_FILE)
except ValueError as e:
    print("An error occoured :(", e)
