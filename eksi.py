import argparse
import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def init_argparser():
    parser = argparse.ArgumentParser(
        prog="Entry_Saver", description="An entry saver program for Eksi Sözlük"
    )
    return parser


parser = init_argparser()


def get_arguments():
    try:
        parser.add_argument(
            "-e",
            "--entry_no",
            metavar="ENTRY_NO",
            type=int,
            help="You shoul enter a valid entry no usage ex: python eksi.py -e 111111",
        )
        parser.add_argument(
            "-a",
            "--author",
            metavar="AUTHOR",
            type=str,
            help="You shoul enter a valid author name usage ex: python eksi.py -a mehmetali"
        )
        args = parser.parse_args()
        return args
    except Exception as e:
        print(e)
        raise ValueError

#mustafa culcunun son dudugu
args = get_arguments()

entry_no = str(args.entry_no)
author = str(args.author)


def create_entry_URL(entry_no):
    entry_URL = "https://eksisozluk1923.com/entry/"
    entry_URL = entry_URL + entry_no
    return entry_URL

def create_author_URL(author):
    author_URL = "https://eksisozluk1923.com/biri/"
    author_URL = author_URL +  author
    return author_URL


entry_URL = create_entry_URL(entry_no)
author_URL = create_author_URL(author)


def config_options():
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    options.headless = True
    return options


options = config_options()


def config_driver(options):
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    driver.implicitly_wait(10)
    return driver


driver = config_driver(options)

def open_web_page(URL):
    driver.get(URL)

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

def save_entry_to_txt(entry_title, entry_date, entry_author, entry_text):

    dir_path = os.getcwd()

    saves_entry_klasoru = os.path.join(dir_path, "saves/entries")

    if not os.path.exists(saves_entry_klasoru):
        os.makedirs(saves_entry_klasoru)
        print(f"'saves/entries' klasörü {dir_path} dizininde oluşturuldu.")
    else:
        print(f"'saves/entries' klasörü zaten {dir_path} dizininde mevcut.")

    file_name = f"{entry_no}.txt"
    dir_path = dir_path + "/saves/entries"
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

def entry_option(entry_no):

    open_web_page(entry_URL)
    entry_text = get_entry_text()
    entry_title = get_entry_title()
    entry_date = get_entry_date()
    entry_author = get_entry_author()
    save_entry_to_txt(entry_no, entry_title, entry_date, entry_author, entry_text)


    # for control
    print(
         "Entry No: "
        + entry_no
        + "\n"
        + "Entry Title: "
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



#entry_option(entry_no)

def get_author_total_entry_number():
    author_total_entry_nuber = (
        WebDriverWait(driver, 20)
        .until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "/html/body/div[2]/div[2]/div[2]/section/div[3]/ul/li[1]/span[1]",
                )
            )
        ).text
    )
    return author_total_entry_nuber


def get_author_follower_number():
    author_follower_number = (
        WebDriverWait(driver, 20)
        .until(
         EC.element_to_be_clickable(
               (
                    By.XPATH,
                    "/html/body/div[2]/div[2]/div[2]/section/div[3]/ul/li[2]/span[1]",
                )
            )
        ).text
    )
    return author_follower_number


def get_author_following_number():
    author_following_number = (
        WebDriverWait(driver, 20)
        .until(
         EC.element_to_be_clickable(
               (
                    By.XPATH,
                    "/html/body/div[2]/div[2]/div[2]/section/div[3]/ul/li[3]/span[1]",
                )
            )
        ).text
    )
    return author_following_number  

def save_author_to_txt(author, author_total_entry_number, author_follower_number, author_following_number):

    dir_path = os.getcwd()

    saves_author_klasoru = os.path.join(dir_path, "saves/authors")

    if not os.path.exists(saves_author_klasoru):
        os.makedirs(saves_author_klasoru)
        print(f"'saves/authors' klasörü {dir_path} dizininde oluşturuldu.")
    else:
        print(f"'saves/authors' klasörü zaten {dir_path} dizininde mevcut.")

    file_name = f"{author}.txt"
    dir_path = dir_path + "/saves/authors"
    target_path = os.path.join(dir_path, file_name)

    try:
        save_file = open(target_path, "w")
        save_file.write(
            "Author Name: "
            + author
            + "\n"
            + "Author Total Entry Number: "
            + author_total_entry_number
            + "\n"
            + "Author Follower Number: "
            + author_follower_number
            + "\n"
            + "Author Following Number: "
            + author_following_number
            + "Authors all entries:\n"
            
        )

    except IOError:
        print("the file was couldn't find or read.")
    else:
        print("The file was saved succesfully.")
        save_file.close()
       

def author_option(author):

    open_web_page(author_URL)
    author_total_entry_number = get_author_total_entry_number()
    author_follower_number = get_author_follower_number()
    author_following_number = get_author_following_number()
    save_author_to_txt(author, author_total_entry_number, author_follower_number, author_following_number)

author_option(author)
    