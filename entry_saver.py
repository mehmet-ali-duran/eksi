import argparse
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

parser = argparse.ArgumentParser(description="An entry saver program for Eksi Sözlük")


def get_arguments():
    try:
        parser.add_argument(
            "entry_no",
            metavar="ENTRY_NO",
            type=int,
            help="You shoul enter a valid entry no usage ex: python entry_saver.py 111111",
        )
        args = parser.parse_args()
        return args
    except Exception as e:
        print(e)
        raise ValueError


args = get_arguments()

# function entryno return url
URL = "https://eksisozluk1923.com/entry/"
entry_no = str(args.entry_no)
URL = URL + entry_no

options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
driver = webdriver.Chrome(options=options)
driver.maximize_window()
driver.implicitly_wait(10)
driver.get(URL)

entry_text = driver.find_element(
    By.XPATH, "/html/body/div[2]/div[2]/div[2]/section/div[1]/ul/li/div[1]"
).text

entry_title = (
    WebDriverWait(driver, 20)
    .until(
        EC.element_to_be_clickable(
            (By.XPATH, "/html/body/div[2]/div[2]/div[2]/section/div[1]/h1/a/span")
        )
    )
    .text
)
entry_date = (
    WebDriverWait(driver, 20)
    .until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                "/html/body/div[2]/div[2]/div[2]/section/div[1]/ul/li/footer/div[2]/div/div[1]/div[2]/a",
            )
        )
    )
    .text
)

entry_author = (
    WebDriverWait(driver, 20)
    .until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                "/html/body/div[2]/div[2]/div[2]/section/div[1]/ul/li/footer/div[2]/div/div[1]/div[1]/div/a",
            )
        )
    )
    .text
)


print(
    "Entry Title: "
    + entry_title
    + "\n"
    + "Entry Date: "
    + entry_date
    + "\n"
    + "Entry Author:"
    + entry_author
    + "\n"
    + "Entry Text:\n"
    + entry_text
)


dir_path = os.getcwd()

saves_klasoru = os.path.join(dir_path, "saves")

if not os.path.exists(saves_klasoru):
    os.makedirs(saves_klasoru)
    print(f"'saves' klasörü {dir_path} dizininde oluşturuldu.")
else:
    print(f"'saves' klasörü zaten {dir_path} dizininde mevcut."),

file_name = f"{entry_no}.txt"
dir_path = dir_path + "/saves"
target_path = os.path.join(dir_path, file_name)
save_file = open(target_path, "w")

save_file.write(
    "Entry Title: "
    + entry_title
    + "\n"
    + "Entry Date: "
    + entry_date
    + "\n"
    + "Entry Author: "
    + entry_author
    + "\n"
    + "Entry Text:\n"
    + entry_text
)
save_file.close()
