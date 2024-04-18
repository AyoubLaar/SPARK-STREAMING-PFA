import time
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import StaleElementReferenceException,TimeoutException
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver import ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
import traceback
from database import POST_ORM


class EmptyPostException(Exception):
    pass

class Post:
    blacklist_users = []
    post_orm = None
    label = None
    successive_save_exceptions = 0
    counter = 0

    def __init__(self,div) -> None:
        self.div = div
        self.usertag = ""
        self.text = ""
    
    def scrap_post(self):
        try:
            time.sleep(0.5)
            self.click_post()
            #now we are in post page
            time.sleep(0.5)
            self.scrap_text()
            time.sleep(0.5)
            driver.back()
            #Back to timeline with same posts
            print("posts scrapped ",Post.counter)
        except EmptyPostException:
            print("empty")

    @staticmethod
    def  next():
        posts = get_posts()
        i = 0 
        while i < len(posts) and not is_element_visible_in_viewpoint(posts[i]):
            i = i + 1
        while i < len(posts):
            try:
                posts[i].location_once_scrolled_into_view
                post = Post(posts[i])
                if not post.is_scrapped_Timeline():
                    return post 
                i = i + 1
            except (StaleElementReferenceException,TimeoutException) as e:
                posts = get_posts()
                i = 0 
                while i < len(posts) and not is_element_visible_in_viewpoint(posts[i]):
                    i = i + 1
                posts[i+1].location_once_scrolled_into_view
                i = i + 1
        return None

    def is_scrapped_Timeline(self):
        self.usertag = WebDriverWait(self.div, 1).until(EC.presence_of_element_located((By.XPATH,TimelinePage.usertag_relative_XPATH))).text
        return self.usertag in Post.blacklist_users

    def click_post(self):
        click_target = WebDriverWait(self.div, 10).until(EC.presence_of_element_located((By.XPATH,TimelinePage.click_target_relative_XPATH)))
        if click_target.text == "" :
            usertag = WebDriverWait(self.div, 10).until(EC.presence_of_element_located((By.XPATH,TimelinePage.usertag_relative_XPATH))).text
            Post.blacklist_users.append(usertag)
            raise EmptyPostException("empty post")
        driver.execute_script("arguments[0].click()",click_target)
    
    def scrap_text(self):
        default_text = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, PostPage.default_text_XPATH)))
        #time.sleep(1)
        try:
            #If not in english a translate button is provided by twitter
            #if non existant => Text is in english => throws error => default behavior in except section.
            click_element(PostPage.click_translate_XPATH)
            translated_text = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, PostPage.translated_text_XPATH))) 
            translated_text.location_once_scrolled_into_view
            self.text = translated_text.text
        except TimeoutException:
            #Text in english
            #time.sleep(1)
            self.text = default_text.text
        try:
            times = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.TAG_NAME,"time")))
            self.time_date = times[0].get_attribute("datetime").replace("T"," ",1)[:19]
        except TimeoutException:
            self.time_date = "unknown"
        try:
            Post.post_orm.save(self)
            Post.counter = Post.counter + 1
            Post.successive_save_exceptions = 0
        except:
            traceback.print_exception()
            Post.successive_save_exceptions = Post.successive_save_exceptions + 1
        finally:
            Post.blacklist_users.append(self.usertag)

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
    filter_XPATH = "/html/body/div[1]/div/div/div[2]/main/div/div/div/div[2]/div/div[2]/div/div/div/div[2]/div/div[2]/a/div"
    filter_replies_XPATH = "/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[8]/label/div/div[2]/input"
    filter_search_XPATH = "/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[1]/div/label/div/div[2]/div/input"

def login(login,password):
    username_input = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[autocomplete="username"]')))
    username_input.send_keys(login)
    username_input.send_keys(Keys.ENTER)
    password_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[name="password"]')))
    password_input.send_keys(password)
    password_input.send_keys(Keys.ENTER)

def search_latest(search):
    filter = "-filter:replies"
    search_bar = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,TimelinePage.search_XPATH)))
    search_bar.send_keys(search + " " +filter)
    search_bar.send_keys(Keys.ENTER)
    latest_button = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,TimelinePage.latest_button_XPATH)))
    latest_button.click()

def test_search(login,password,search) -> list:
    try:
        message = ["driver doesn't connect","","",""]
        options = ChromeOptions()
        options.add_argument("--start-maximized")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument("--headless=new")
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)    
        url = "https://twitter.com/i/flow/login"
        driver.get(url)
        message[0] = "driver connects!"
        message[1] = "login doesn't work"
        username_input = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[autocomplete="username"]')))
        username_input.send_keys(login)
        username_input.send_keys(Keys.ENTER)
        password_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[name="password"]')))
        password_input.send_keys(password)
        password_input.send_keys(Keys.ENTER)
        message[1] = "login works!"
        message[2] = "search doesn't work"
        filter = "-filter:replies"
        search_bar = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,TimelinePage.search_XPATH)))
        search_bar.send_keys(search + " " +filter)
        search_bar.send_keys(Keys.ENTER)
        latest_button = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,TimelinePage.latest_button_XPATH)))
        latest_button.click()
        message[2] = "search works!"
        message[3] = "post scrapping doesn't work"
        post = Post.next()
        if post == None:
            return message
        post.scrap_post()
        message[3] = "post scrapping works!"
        return message
    except:
        return message


def get_posts():
    posts_container = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, TimelinePage.posts_container_XPATH)))
    return posts_container.find_elements(By.XPATH,"div")

def scrap_posts(posts_size = 100):
    while Post.counter < posts_size and Post.successive_save_exceptions < 10:
        post = Post.next()
        while post == None:
            post = Post.next()
        post.scrap_post()

def click_element(XPATH,wait=0):
    element = WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.XPATH, XPATH)))
    time.sleep(wait)
    driver.execute_script("arguments[0].click()",element)

def is_element_visible_in_viewpoint(element) -> bool:
    try: 
        return driver.execute_script("var elem = arguments[0],                 " 
                                 "  box = elem.getBoundingClientRect(),    " 
                                 "  cx = box.left + box.width / 2,         " 
                                 "  cy = box.top + box.height / 2,         " 
                                 "  e = document.elementFromPoint(cx, cy); " 
                                 "for (; e; e = e.parentElement) {         " 
                                 "  if (e === elem)                        " 
                                 "    return true;                         " 
                                 "}                                        " 
                                 "return false;                            "
                                 , element)
    except:
        return False

def run(username,password,posts_size,search,label):
    options = ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("--headless=new")
    
    global driver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)    
    url = "https://twitter.com/i/flow/login"
    driver.get(url)
    try:
        count = 0
        while count < 5:
            try:
                print("Connecting to database")
                Post.post_orm = POST_ORM()
                print("Connection successful")
                break
            except:
                traceback.print_exc()
                print("Connection error")
                count = count + 1
                time.sleep(1)
        if count == 5:
            print("attempted connection 5 times, now exiting.....")
            raise Exception()
        print("logging in...")
        login(username,password)
        print("login successfull!")
        print("Searching...")
        search_latest(search)
        print("search successfull!")
        Post.label = label
        scrap_posts(posts_size)
        driver.execute_script("window.scrollBy(0,0)","")
        driver.close()
        Post.post_orm.close()
    except:
        print(traceback.format_exc())
        driver.close()
        Post.post_orm.close()
        raise Exception()