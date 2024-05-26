from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import StaleElementReferenceException,TimeoutException
from traceback import format_exc 
import logging 
from xpath import PostPage,TimelinePage

driver = None

def init(driver_value):
    global driver
    driver = driver_value

class EmptyPostException(Exception):
    pass

class Post:
    blacklist_users = []
    label = None
    counter = 0
    post_orm = None

    def __init__(self,div) -> None:
        self.div = div
        self.usertag = ""
        self.text = ""
    
    def scrap_post(self):
        try:
            sleep(0.5)
            self.click_post()
            #now we are in post page
            sleep(0.5)
            self.scrap_text()
            sleep(0.5)
            driver.back()
            #Back to timeline with same posts
            logging.info("posts scrapped %s",str(Post.counter))
        except EmptyPostException:
            logging.warning("empty")

    @staticmethod
    def  next():
        posts = get_posts()
        while posts is None:
            sleep(1)
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
                logging.warning("AD")
                posts = get_posts()
                i = 0 
                while i < len(posts) and not is_element_visible_in_viewpoint(posts[i]):
                    i = i + 1
                if i + 1 <  len(posts):
                    #The post at the i index is already scrapped
                    posts[i+1].location_once_scrolled_into_view
                i = i + 1
        return None
    
    def is_scrapped_Timeline(self):
        self.usertag = WebDriverWait(self.div, 5).until(EC.presence_of_element_located((By.XPATH,TimelinePage.usertag_relative_XPATH))).text
        return self.usertag in Post.blacklist_users

    def click_post(self):
        click_target = WebDriverWait(self.div, 60).until(EC.presence_of_element_located((By.XPATH,TimelinePage.click_target_relative_XPATH)))
        if click_target.text == "" :
            usertag = WebDriverWait(self.div, 60).until(EC.presence_of_element_located((By.XPATH,TimelinePage.usertag_relative_XPATH))).text
            Post.blacklist_users.append(usertag)
            raise EmptyPostException("empty post")
        driver.execute_script("arguments[0].click()",click_target)
    
    def scrap_text(self):
        default_text = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, PostPage.default_text_XPATH)))
        #sleep(1)
        self.text = default_text.text
        try:
            times = WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.TAG_NAME,"time")))
            self.time_date = times[0].get_attribute("datetime").replace("T"," ",1)[:19]
        except TimeoutException:
            self.time_date = "unknown"
        try:
            Post.post_orm.save(self)
            Post.counter = Post.counter + 1
        except:
            logging.error(format_exc())
        finally:
            Post.blacklist_users.append(self.usertag)

def get_posts():
    try:
        posts_container = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, TimelinePage.posts_container_XPATH)))
        divs = WebDriverWait(posts_container, 60).until(EC.presence_of_all_elements_located((By.XPATH, "div")))
        return divs
    except:
        logging.error(format_exc())

def click_element(XPATH,wait=0):
    element = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, XPATH)))
    sleep(wait)
    driver.execute_script("arguments[0].click()",element)

def scroll_by(height=1000):
    driver.execute_script(f"window.scrollBy(0,{str(height)})")
    sleep(1)

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