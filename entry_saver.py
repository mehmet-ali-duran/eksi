import argparse
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def init_argparser():
    parser = argparse.ArgumentParser(
        prog="Entry_Saver", description="An entry saver program for Eksi Sözlük"
    )
    return parser


parser = init_argparser()


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


entry_no = str(args.entry_no)


def create_target_URL():
    URL = "https://eksisozluk1923.com/entry/"
    URL = URL + entry_no
    return URL


URL = create_target_URL()


def config_options():
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    options.headless = True
    return options


options = config_options()


def config_driver_and_open_browser(options, URL):
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    driver.implicitly_wait(10)
    driver.get(URL)
    return driver


driver = config_driver_and_open_browser(options, URL)


def get_entry_text():
    entry_text = (
        WebDriverWait(driver, 20)
        .until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "/html/body/div[2]/div[2]/div[2]/section/div[1]/ul/li/div[1]",
                )
            )
        )
        .text
    )
    return entry_text


entry_text = get_entry_text()


def get_entry_title():
    entry_title = (
        WebDriverWait(driver, 20)
        .until(
            EC.element_to_be_clickable(
                (By.XPATH, "/html/body/div[2]/div[2]/div[2]/section/div[1]/h1/a/span")
            )
        )
        .text
    )
    return entry_title


entry_title = get_entry_title()


def get_entry_date():
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
    return entry_date


entry_date = get_entry_date()


def get_entry_author():
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
    return entry_author


entry_author = get_entry_author()

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
    print(f"'saves' klasörü zaten {dir_path} dizininde mevcut.")

file_name = f"{entry_no}.txt"
dir_path = dir_path + "/saves"
target_path = os.path.join(dir_path, file_name)

try:
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

except IOError:
    print("the file was couldn't find or read.")
else:
    print("The file was saved succesfully.")
    save_file.close()
