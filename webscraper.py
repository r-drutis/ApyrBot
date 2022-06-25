from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from exceptions import UnknownEntryTypeError
import os
from dotenv import load_dotenv

load_dotenv()
USERNAME_R20 = os.getenv('USERNAME_R20')
PASSWORD_R20 = os.getenv('PASSWORD_R20')
CAMPAIGN_R20 = os.getenv('CAMPAIGN_R20')

def intialize_webdriver():
    options = Options()
    options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    #options.add_argument('--start-maximized')
    options.add_argument('--window-size=1920,1080')
    driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), options=options)
    return driver

def login_to_roll20():
    driver.get("https://roll20.net/welcome")
    wait.until(EC.visibility_of_element_located((By.ID,'email')))
    usernameElements = driver.find_element(By.ID,'email')
    passwordElements = driver.find_element(By.ID, 'password')

    usernameElements.send_keys(USERNAME_R20)
    passwordElements.send_keys(PASSWORD_R20)
    driver.find_element(By.ID, 'login').click()
    wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[4]/div/div[1]/div[4]/div[2]/a[1]')))

def navigate_to_external_journal_page():
    driver.get(CAMPAIGN_R20)

def find_entry_url(query):
    journal_entry_url = ""
    if query:
        try:
            WebDriverWait(driver, 3, poll_frequency=1).until(EC.presence_of_element_located((By.XPATH, "//*[translate(text(),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz')='"+query.lower()+"']")))
            query = driver.find_element(By.XPATH, "//*[translate(text(),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz')='"+query.lower()+"']")
            journal_entry_url = query.find_element(By.XPATH, '..').get_attribute('href')
            return journal_entry_url
        except (NoSuchElementException, TimeoutException):
            return journal_entry_url
    return journal_entry_url

def retrieve_journal_entry(query_link):
    journal_content = {}
    driver.get(query_link)
    try:
        entry = scrape_local_journal()
        journal_content["title"] = scrape_entry_title(entry)
        journal_content["avatar"] = scrape_avatar_img(entry)
        journal_content["text"] = scrape_journal_text(entry)
    except (NoSuchElementException, TimeoutException):
        return journal_content
    return journal_content

def scrape_local_journal():
    entry = ""
    try:
        wait.until(EC.visibility_of_element_located((By.XPATH, "//*[@id ='openpages']")))
        entry = driver.find_element(By.XPATH, "//*[@id ='openpages']")
        return entry
    except (NoSuchElementException, TimeoutException):
        return entry
    return entry

def get_entry_type(entry):
    entry_type = ""
    try:
        entry_type = entry.find_element(By.XPATH,
                                             "//div[@class ='entry character open'] | //div[@class ='entry handout open']").get_attribute(
            "class")
        return entry_type
    except (NoSuchElementException, TimeoutException) as element_exception:
        raise element_exception
    return entry_type



def scrape_entry_title(entry):
    entry_title = ""
    try:
        entry_title = entry.find_element(By.XPATH, "//*[@class ='thisname']").text
        return entry_title
    except (NoSuchElementException, TimeoutException):
         return entry_title
    return entry_title

def scrape_journal_text(entry):
    journal_segments = []
    try:
        # Handout and Character pages have a different class name for their text element
        entry_type = get_entry_type(entry)
        if is_character_entry(entry_type):
            paragraph_elements = entry.find_elements(By.XPATH, "//*[@class ='thisbio']")
        elif is_handout_entry(entry_type):
            paragraph_elements = entry.find_elements(By.XPATH, "//*[@class ='thisnotes']")
        else:
            raise UnknownEntryTypeError
        # Scrape the paragraph elements from the page and return them
        for p in  paragraph_elements:
            journal_segments.append(p.text)
        return journal_segments
    except (NoSuchElementException, TimeoutException, UnknownEntryTypeError):
         return journal_segments
    return journal_segments

def is_character_entry(entry_type):
    return entry_type == 'entry character open'

def is_handout_entry(entry_type):
    return entry_type == 'entry handout open'

def scrape_avatar_img(entry):
    avatar_img = ""
    try:
        avatar_img = entry.find_element(By.XPATH, "//*[@class ='thisavatar']").get_attribute("src")
        return avatar_img
    except (NoSuchElementException, TimeoutException):
         return avatar_img
    return avatar_img

def retrieve_query_from_journal(query):
    journal_content = {}
    navigate_to_external_journal_page()
    entry_url = find_entry_url(query)
    if entry_url:
        journal_content = retrieve_journal_entry(entry_url)
        return journal_content
    else:
        print("nothing was found")
        return journal_content

driver = intialize_webdriver()
wait = WebDriverWait(driver, 5)
login_to_roll20()

