#!/usr/bin/env python3

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

service = Service("/usr/local/bin/chromedriver")

options = webdriver.ChromeOptions()

driver = webdriver.Chrome(service=service, options=options)

nightlight_website_url = "https://nightlight.gg/shrine"


def get_shrine_from_nightlight():
    shrine_perks = []
    driver.get(nightlight_website_url)

    # find element by class name
    div_elements = driver.find_elements(By.CLASS_NAME, "cidahu2")

    for div in div_elements:
        a_tag = div.find_element(By.TAG_NAME, "a")
        shrine_perks.append(a_tag.text)

    driver.quit()

    return shrine_perks


if __name__ == "__main__":
    shrine = get_shrine_from_nightlight()

    # write the shrine to a file
    with open("shrine.txt", "w") as f:
        for perk in shrine:
            f.write(f"{perk}\n")
