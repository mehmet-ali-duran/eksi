import argparse
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC


MAIN_URL = "https://eksisozluk1923.com/"

def init_argparser():
    parser = argparse.ArgumentParser(
        prog="Entry_Saver", description="An entry saver program for Eksi Sözlük"
    )
    return parser

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
            help="You shoul enter a valid author name usage ex: python eksi.py -a mehmetali",
        )
        parser.add_argument(
            "-t",
            "--topic",
            metavar="TOPİC",
            type=str,
            help="You shoul enter a valid eksisözlük topic url and page number usage ex: python eksi.py -t VALİD_URL 10"
        )
        args = parser.parse_args()
        return args
    except Exception as e:
        print(e)
        raise ValueError

def get_final_url(PAGE_TYPE, NAME):
    types = {"entry":"entry/","author":"biri/"}
    return str(MAIN_URL) + str(types[PAGE_TYPE]) + str(NAME)

def config_options():
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    options.headless = True
    return options

def config_driver(options):
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    driver.implicitly_wait(10)
    return driver

def open_web_page(URL, driver):
    driver.get(URL)

def get_entry_text(driver):
    entry_text = driver.find_element(By.CLASS_NAME,"content content-expanded").text
    return entry_text

def get_entry_title(driver):
    entry_title = driver.find_element(By.XPATH, "//span[contains(@itemprop, 'name')]").text
    
    return entry_title

def get_entry_date(driver):
    entry_date = driver.find_element(By.CLASS_NAME,"entry-date permalink").text
    return entry_date


def get_entry_author(driver):
    entry_author = driver.find_element(By.CLASS_NAME,"entry-author").text
    return entry_author


def save_entry_to_txt(entry_no, entry_title, entry_date, entry_author, entry_text):
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

def true_page_control(driver):
    try:
        error = driver.find_element(By.CLASS_NAME ,'error404')
        print("bu geçerli bir entry no değil böyle bir sayfa yok")
        return False, error
    except NoSuchElementException:
        pass
    try:
        error2 = driver.find_element(By.XPATH, '//*[@title="web2"]')
        print("büyük başarısızlıklar söz konusu")
        return False
    except NoSuchElementException:
        pass
    
    return True
    
def entry_option(entry_no):
    entry_URL = get_final_url("entry",entry_no)
    options = config_options()
    driver = config_driver(options)
    open_web_page(entry_URL, driver)
    control = true_page_control(driver)
    if(control):
        entry_text = get_entry_text(driver)
        entry_title = get_entry_title(driver)
        entry_date = get_entry_date(driver)
        entry_author = get_entry_author(driver)
        save_entry_to_txt(entry_no, entry_title, entry_date, entry_author, entry_text)

def get_author_total_entry_number(driver):
    author_total_entry_nuber = (
        WebDriverWait(driver, 20)
        .until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "/html/body/div[2]/div[2]/div[2]/section/div[3]/ul/li[1]/span[1]",
                )
            )
        )
        .text
    )
    return author_total_entry_nuber


def get_author_follower_number(driver):
    author_follower_number = (
        WebDriverWait(driver, 20)
        .until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "/html/body/div[2]/div[2]/div[2]/section/div[3]/ul/li[2]/span[1]",
                )
            )
        )
        .text
    )
    return author_follower_number


def get_author_following_number(driver):
    author_following_number = (
        WebDriverWait(driver, 20)
        .until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "/html/body/div[2]/div[2]/div[2]/section/div[3]/ul/li[3]/span[1]",
                )
            )
        )

        .text
    )
    return author_following_number

def content_print(author, driver):
    content_body = driver.find_elements(By.CLASS_NAME , 'topic-item')
    all_entries =""
    for i in content_body:
        current_text = i.text
        current_text = current_text.replace(author, "")
        all_entries = all_entries + current_text + "\n\n"
    print(all_entries)
    return all_entries

def content_print_topic(driver):
    content_body = driver.find_elements(By.XPATH, "//ul[@id='entry-item-list']/li")    
    all_entries =""
    for i in content_body:
        current_text = i.text
        all_entries = all_entries + current_text + "\n\n"
    print(all_entries)
    return all_entries

def save_all_entries(author_total_entry_number, driver, author):
    
    if int(author_total_entry_number) == 0:
        print("This author has not made any entries yet.")
    else:
        for i in range((int(author_total_entry_number)-1)//10):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
            driver.find_element(By.LINK_TEXT, 'daha fazla göster').click()
        
        entriler = content_print(author, driver)  
        return entriler

def save_author_to_txt(
    author, author_total_entry_number, author_follower_number, author_following_number, driver
):
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
    entries = save_all_entries(author_total_entry_number, driver, author)
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
            + "\n"
            + "Authors all entries:\n\n"
            + entries
            
        )

    except IOError:
        print("the file was couldn't find or read.")
    else:
        print("The file was saved succesfully.")
        save_file.close()

def author_option(author):
    author_URL = get_final_url("author",author)
    options = config_options()
    driver = config_driver(options)
    open_web_page(author_URL, driver)
    author_total_entry_number = get_author_total_entry_number(driver)
    author_follower_number = get_author_follower_number(driver)
    author_following_number = get_author_following_number(driver)
    save_author_to_txt(
        author,
        author_total_entry_number,
        author_follower_number,
        author_following_number,
        driver,
    )
    
def get_topic(driver):
    tittle = (
        WebDriverWait(driver, 20)
        .until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//span[contains(@itemprop, 'name')]",
                )
            )
        )
        .text
    )
    return tittle

def save_topics_first_page(topic, driver):
    dir_path = os.getcwd()

    saves_topics_klasoru = os.path.join(dir_path, "saves/topics")

    if not os.path.exists(saves_topics_klasoru):
        os.makedirs(saves_topics_klasoru)
        print(f"'saves/topics' klasörü {dir_path} dizininde oluşturuldu.")
    else:
        print(f"'saves/topics' klasörü zaten {dir_path} dizininde mevcut.")

    file_name = f"{topic}.txt"
    dir_path = dir_path + "/saves/topics"
    target_path = os.path.join(dir_path, file_name)
    entries = content_print_topic(driver)

    try:
        save_file = open(target_path, "w")
        save_file.write(
            "Topic: "
            + topic
            + "\n\n\n"
            + "Topics: "
            + entries
        )

    except IOError:
        print("the file was couldn't find or read.")
    else:
        print("The file was saved succesfully.")
        save_file.close()

def topic_option(topic_url):
    options=config_options()
    driver=config_driver(options)
    open_web_page(topic_url, driver)
    topic=get_topic(driver)
    save_topics_first_page(topic, driver)
        


if __name__=="__main__":
    parser = init_argparser()
    args = get_arguments()

    if((args.entry_no) != None):
        entry_option(str(args.entry_no))

    if((args.author) != None):
        author_option(str(args.author))
        
    if((args.topic) != None):
        topic_option(str(args.topic))
        
    
