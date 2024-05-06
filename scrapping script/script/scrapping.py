import logging 
import sys
import os
from time import sleep
from traceback import format_exc 
#Selenium
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver import ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
#My files
from database import POST_ORM
from post import Post,init
from xpath import TimelinePage

# logging.basicConfig(filename='/var/log/actions.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logging.basicConfig(stream=sys.stdout, level=logging.INFO , format='%(asctime)s - %(levelname)s - %(message)s')


def optionnal_username(login):
    try:
        input = WebDriverWait(driver,5).until(EC.presence_of_element_located((By.XPATH,'input[autocomplete="on"]')))
        logging.info("Unusual activity detected!")
        sleep(0.5)
        input.send_keys(login)
        input.send_keys(Keys.ENTER)
    except:
        logging.info("No unusual activity detected!")
    
def login(login,password):
    username_input = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[autocomplete="username"]')))
    username_input.send_keys(login)
    sleep(0.5)
    username_input.send_keys(Keys.ENTER)
    optionnal_username(login)
    password_input = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[name="password"]')))
    password_input.send_keys(password)
    sleep(0.5)
    password_input.send_keys(Keys.ENTER)

def search_latest(search):
    search_bar = WebDriverWait(driver,60).until(EC.presence_of_element_located((By.XPATH,TimelinePage.search_XPATH)))
    search_bar.send_keys(search)
    search_bar.send_keys(Keys.ENTER)
    latest_button = WebDriverWait(driver,60).until(EC.presence_of_element_located((By.XPATH,TimelinePage.latest_button_XPATH)))
    sleep(10)
    latest_button.click()

def scrap_posts(posts_size = 100):
    logging.info("scrapping %s posts",str(posts_size))
    while Post.counter < posts_size:
        post = Post.next()
        while post == None:
            post = Post.next()
        post.scrap_post()
    logging.info("%s posts scrapped from %s",str(Post.counter),str(posts_size))
    driver.execute_script("window.scrollBy(0,0)","")

def run(username,password,posts_size,search,label):
    print((username,password,posts_size,search,label))
    options = ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    # options.add_argument("--headless=new")
    global driver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)    
    init(driver_value=driver)
    url = "https://twitter.com/i/flow/login"
    driver.get(url)
    try:
        try:
            logging.info("Connecting to database")
            Post.post_orm = POST_ORM()
            logging.info("Connection successful")
        except:
            logging.error(format_exc())
            logging.error("Connection error")
            exit()
        logging.info("logging in...")
        login(username,password)
        logging.info("login successfull!")
        sleep(60)
        logging.info("Searching...")
        search_latest(search)
        logging.info("search successfull!")
        Post.label = label
        scrap_posts(posts_size)
    except:
        logging.error(format_exc())
    finally:
        driver.quit()
        Post.post_orm.close()

if __name__ == "__main__":
    username = os.environ.get("LOGIN")
    password = os.environ.get("PASSWORD")
    posts_size = int(os.environ.get("POSTS_SIZE"))
    search = os.environ.get("SEARCH")
    label = os.environ.get("LABEL")
    run(username,password,posts_size,search,label)
    