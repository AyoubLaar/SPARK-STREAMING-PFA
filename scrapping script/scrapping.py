import time
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import StaleElementReferenceException,TimeoutException
from selenium import webdriver
from selenium.webdriver import ChromeOptions
import traceback

class EmptyPostException(Exception):
    pass

class Post:
    posts_scrapped = []

    def __init__(self,div) -> None:
        self.div = div
        self.usertag = ""
        self.text = ""
    
    def scrap_post(self):
        self.click_post()
        #now we are in post page
        self.scrap_text()
        driver.back()
        #Back to timeline with same posts

    @staticmethod
    def next():
        posts = get_posts()
        for i in range(len(posts)):
            try:
                posts[i].location_once_scrolled_into_view
                post = Post(posts[i])
                if not post.is_scrapped_Timeline():
                    return post
            except StaleElementReferenceException:
                continue
        return None

    def is_scrapped_Timeline(self):
        try:
            self.usertag = WebDriverWait(self.div, 1).until(EC.presence_of_element_located((By.XPATH,TimelinePage.usertag_relative_XPATH))).text
        except:
            #Ad not wanted
            return True
        for post_content in Post.posts_scrapped:
            if post_content[0] == self.usertag:
                return True
        return False

    def click_post(self):
        click_target = WebDriverWait(self.div, 10).until(EC.presence_of_element_located((By.XPATH,TimelinePage.click_target_relative_XPATH)))
        if click_target.text == "" :
            raise EmptyPostException("empty post") 
        driver.execute_script("arguments[0].click()",click_target)
    
    def scrap_text(self):
        default_text = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, PostPage.default_text_XPATH)))
        time.sleep(1)
        try:
            #If not in english a translate button is provided by twitter
            #if non existant => Text is in english => throws error => default behavior in except section.
            translate_target = WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.XPATH, PostPage.click_translate_XPATH)))
            print("Non english")
            driver.execute_script("arguments[0].click()",translate_target)
            translated_text = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, PostPage.translated_text_XPATH))) 
            translated_text.location_once_scrolled_into_view
            self.text = translated_text.text
        except TimeoutException:
            #Text in english
            print("English : ",default_text.text)
            self.text = default_text.text
        try:
            times = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.TAG_NAME,"time")))
            self.time_date = times[len(times)-1].text
        except TimeoutException:
            pass
        print({"username":self.usertag,"timedate":self.time_date,"text":self.text})
        Post.posts_scrapped.append((self.usertag,self.time_date,self.text))
        
class PostPage:
    translated_text_XPATH = "/html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/section/div/div/div[1]/div/div/article/div/div/div[3]/div[1]/div/div[3]/div"
    default_text_XPATH = "/html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/section/div/div/div[1]/div/div/article/div/div/div[3]/div[1]/div/div"
    click_translate_XPATH = "/html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/section/div/div/div[1]/div/div/article/div/div/div[3]/div[1]/div/div[2]/span"
    usertag_XPATH = "/html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/section/div/div/div[1]/div/div/article/div/div/div[2]/div[2]/div/div/div[1]/div/div/div[2]/div/div/a/div/span"

class TimelinePage:
    posts_container_XPATH = "/html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/section/div/div"
    usertag_relative_XPATH = "div/div/article/div/div/div[2]/div[2]/div[1]/div/div[1]/div/div/div[2]/div/div[1]/a/div/span"
    click_target_relative_XPATH = "div/div/article/div/div/div[2]/div[2]/div[2]/div"
    search_XPATH = "/html/body/div[1]/div/div/div[2]/main/div/div/div/div[2]/div/div[2]/div/div/div/div[1]/div/div/div/form/div[1]/div/div/div/label/div[2]/div/input"
    latest_button_XPATH = "/html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/div[1]/div[1]/div[2]/nav/div/div[2]/div/div[2]/a"

def login():
    username = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[autocomplete="username"]')))
    username.send_keys("nouredd31162955")
    username.send_keys(Keys.ENTER)
    password = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[name="password"]')))
    password.send_keys("Vt2drLK?Qh^tfQq")
    password.send_keys(Keys.ENTER)

def search_latest(search):
    search_bar = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,TimelinePage.search_XPATH)))
    search_bar.send_keys(search)
    search_bar.send_keys(Keys.ENTER)
    latest_button = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,TimelinePage.latest_button_XPATH)))
    latest_button.click()

def get_posts():
    posts_container = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, TimelinePage.posts_container_XPATH)))
    return posts_container.find_elements(By.XPATH,"div")

def scrap_posts(posts_size = 100):
    while len(Post.posts_scrapped) < posts_size:
        post = Post.next()
        while post == None:
            post = Post.next()
        print("usertag : ",post.usertag)
        post.scrap_post()
       
def is_stale(element):
    EC.staleness_of(element)

    

def run():
    options = ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    global driver

    driver = webdriver.Chrome(options=options)
    url = "https://twitter.com/i/flow/login"
    driver.get(url)
    try:
        login()
        search_latest("#palestine #israel")
        while True:
            scrap_posts(posts_size=10)
            print(Post.posts_scrapped)
            driver.execute_script("window.scrollBy(0,0)","")
    except:
        print(traceback.format_exc())
        print(Post.posts_scrapped)
        driver.close()
