import time
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException,TimeoutException
from selenium.webdriver.common.action_chains import ActionChains

driver = None
posts_content = []

class PostPage:
    translated_text_XPATH = "/html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/section/div/div/div[1]/div/div/article/div/div/div[3]/div[1]/div/div[3]/div"
    default_text_XPATH = "/html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/section/div/div/div[1]/div/div/article/div/div/div[3]/div[1]/div/div"
    click_translate_XPATH = "/html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/section/div/div/div[1]/div/div/article/div/div/div[3]/div[1]/div/div[2]/span"
    usertag_XPATH = "/html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/section/div/div/div[1]/div/div/article/div/div/div[2]/div[2]/div/div/div[1]/div/div/div[2]/div/div/a/div/span"
    datetime_XPATH = "/html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/section/div/div/div[1]/div/div/article/div/div/div[3]/div[4]/div/div[1]/div/div/a/time"

class TimelinePage:
    posts_container_XPATH = "/html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/section/div/div"
    usertag_relative_XPATH = "div/div/article/div/div/div[2]/div[2]/div[1]/div/div[1]/div/div/div[2]/div/div[1]/a/div/span"
    click_target_relative_XPATH = "div/div/article/div/div/div[2]/div[2]/div[2]/div"
    search_XPATH = "/html/body/div[1]/div/div/div[2]/main/div/div/div/div[2]/div/div[2]/div/div/div/div[1]/div/div/div/form/div[1]/div/div/div/label/div[2]/div/input"
    latest_button_XPATH = "/html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/div[1]/div[1]/div[2]/nav/div/div[2]/div/div[2]/a"

def login():
    username = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[autocomplete="username"]')))
    username.send_keys("nouredd31162955")
    username.send_keys(Keys.ENTER)
    password = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[name="password"]')))
    password.send_keys("Vt2drLK?Qh^tfQq")
    password.send_keys(Keys.ENTER)

def search_latest(search):
    search_bar = WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.XPATH,TimelinePage.search_XPATH)))
    search_bar.send_keys(search)
    search_bar.send_keys(Keys.ENTER)
    latest_button = WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.XPATH,TimelinePage.latest_button_XPATH)))
    latest_button.click()

def get_posts():
    posts_container = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, TimelinePage.posts_container_XPATH)))
    return posts_container.find_elements(By.XPATH,"div")

def scrap_posts(posts_size = 100):
    time.sleep(5)
    queue = [find_first_non_empty_post(),""]
    scrap_first_post(queue)
    while len(posts_content) < posts_size:
        scrap_post(queue)

def find_first_non_empty_post():
    posts = get_posts()
    for div in posts:
        try:
            driver.execute_script('arguments[0].scrollIntoView(true)', div)
            click_target = div.find_element(By.XPATH,TimelinePage.click_target_relative_XPATH)
            if click_target.text != "":
                return div
            driver.execute_script("arguments[0].click()",click_target)
        except:
            continue
    return find_first_non_empty_post()
       
def find_next_non_empty_post(last_post):
    username = last_post[0]
    posts = get_posts()
    index = find_div_by_username(username,posts)
    if index == -1:
        queue[0] = posts[0]
    else:
        queue[0] = posts[index+1]

def scrap_post(div):
    driver.execute_script('arguments[0].scrollIntoView(true)', div)
    click_target = div.find_element(By.XPATH,TimelinePage.click_target_relative_XPATH)
    driver.execute_script("arguments[0].click()",click_target)
    #now we are in post page
    usertag = driver.find_element(By.XPATH,PostPage.usertag_XPATH).text
    time_date = driver.find_element(By.XPATH,PostPage.datetime_XPATH).text
    #check_post_exists(post_id) => add database check
    default_text = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, PostPage.default_text_XPATH)))
    time.sleep(1)
    try:
        #If not in english a translate button is provided by twitter
        #if non existant => Text is in english => throws error => default behavior in except section.
        translate_target = driver.find_element(By.XPATH,PostPage.click_translate_XPATH)
        print("Non english")
        translate_target.click()
        translated_text = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, PostPage.translated_text_XPATH))) 
        text = translated_text.text
    except NoSuchElementException:
        #Text in english
        print("English : ",default_text.text)
        text = default_text.text
    print({"username":usertag,"time_date":time_date})
    posts_content.append((usertag,time_date,text))
    driver.back()
    #Back to timeline with same posts

def scrap_first_post(queue):
    div = queue[0]
    time.sleep(1)
    driver.execute_script('arguments[0].scrollIntoView(true)', div)
    click_target = div.find_element(By.XPATH,TimelinePage.click_target_relative_XPATH)
    driver.execute_script("arguments[0].click()",click_target)
    #now we are in post page
    default_text = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, PostPage.default_text_XPATH)))
    time.sleep(1)
    try:
        #If not in english a translate button is provided by twitter
        #if non existant => Text is in english => throws error => default behavior in except section.
        translate_target = driver.find_element(By.XPATH,PostPage.click_translate_XPATH)
        print("Non english : ",default_text.text)
        driver.execute_script("arguments[0].click()",translate_target)
        translated_text = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, PostPage.translated_text_XPATH))) 
        text = translated_text.text
    except NoSuchElementException:
        #Text in english
        print("English : ",default_text.text)
        text = default_text.text
    usertag = driver.find_element(By.XPATH,PostPage.usertag_XPATH).text
    time_date = driver.find_element(By.XPATH,PostPage.datetime_XPATH).text
    #check_post_exists(post_id) => add database check
    print({"username":usertag,"time_date":time_date})
    posts_content.append((usertag,time_date,text))
    driver.back()
    #Back to timeline with same posts
    posts = get_posts()
    index = find_div_by_username(posts_content[len(posts_content)-1][0],posts)
    if index == -1:
        queue[0] = posts[0]
    else:
        queue[0] = posts[index+1]
    queue[0].location_once_scrolled_into_view
    

def check_post_exists(post_id):
    pass

#Returns index of div in divs
def find_div_by_username(username,posts):
    index = 0
    while index < len(posts):
        post = posts[index]
        usertag = WebDriverWait(post, 10).until(EC.visibility_of_element_located((By.XPATH,TimelinePage.usertag_relative_XPATH)))
        if usertag.text == username:
            return index
        index = index + 1
    return -1
    