import argparse
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

parser = argparse.ArgumentParser(description="An entry saver program for Eksi Sözlük")
parser.add_argument(
    "entry_no",
    metavar="ENTRY_NO",
    type=int,
    help="You shoul enter a valid entry no usage ex: python entry_saver.py 111111",
)
args = parser.parse_args()
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
save_file.write(entry_text)
save_file.close()
