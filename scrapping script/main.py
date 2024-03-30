from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import utils

options = ChromeOptions()
options.add_argument("--start-maximized")
options.add_experimental_option("excludeSwitches", ["enable-automation"])

driver = webdriver.Chrome(options=options,service=Service(ChromeDriverManager().install()))
utils.driver = driver
url = "https://twitter.com/i/flow/login"

try:
    driver.get(url)
    utils.login()
    utils.search_latest("#palestine")
    utils.scrap_posts()
except:
    print(utils.posts_content)