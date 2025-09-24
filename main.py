from bs4 import BeautifulSoup
import requests
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from dotenv import load_dotenv
import os

load_dotenv()

FORM_LINK = os.getenv("FORM_LINK")
ZILLOW_URL = "https://appbrewery.github.io/Zillow-Clone/"

# response = requests.get(ZILLOW_URL).text

# with open("zillow.html", "w") as file:
#     file.write(response)

with open("zillow.html") as file:
    contents = file.read()

soup = BeautifulSoup(contents, "html.parser")

raw_addresses = soup.select(".StyledPropertyCardDataWrapper a address")
addresses = [re.split(r"[,|]", item.text, maxsplit=1)[1].strip() for item in raw_addresses]

raw_prices = soup.select(".PropertyCardWrapper span")
prices = [re.split(r"[+/]", item.text, maxsplit=1)[0].strip() for item in raw_prices]

raw_links = soup.select(".StyledPropertyCardDataWrapper a")
links = [item["href"] for item in raw_links]

options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=options)
driver.get(FORM_LINK)

time.sleep(3)

for n in range(len(prices)):
    time.sleep(2)

    address_input = driver.find_element(By.XPATH, '//span[contains(text(), "What\'s the address of the '
                                                  'property?")]//following::input[1]')
    address_input.send_keys(addresses[n])

    price_input = driver.find_element(By.XPATH, '//span[contains(text(), "What\'s the price per '
                                                'month?")]//following::input[1]')
    price_input.send_keys(prices[n])

    link_input = driver.find_element(By.XPATH, '//span[contains(text(), "What\'s the link to '
                                               'the property?")]//following::input[1]')
    link_input.send_keys(links[n])

    send_btn = driver.find_element(By.XPATH, '//span[contains(text(), "Enviar")]').click()
    refresh_btn = driver.find_element(By.XPATH, '//a[contains(text(), "Enviar outra resposta")]').click()
