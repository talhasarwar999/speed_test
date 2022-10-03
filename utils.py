from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from time import sleep
import undetected_chromedriver.v2 as uc
from scrapy import Selector
from selenium_stealth import stealth


def get_normal_driver(headless=False):
    try:
        options = webdriver.ChromeOptions()
        options.add_argument('--incognito')
        options.add_argument('--no-sandbox')
        options.add_argument("--log-level=3")
        if headless:
            options.add_argument('--headless')
        options.add_argument('--start-maximized')
        driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        return driver
    except Exception as e:
        print(e)
        print('------------------- Generation the New Driver')
        get_normal_driver(headless)


def click_on_element(driver, xpath):
    scroll_to_element_smoothly(driver, xpath)
    el = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, xpath)))
    el.click()


def get_page_source(driver):
    html = driver.page_source
    return Selector(text=html)


def insert_value_and_press_enter(driver, xpath, text, previouse_clear=False):
    element = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.XPATH, xpath)))
    if previouse_clear:
        element.clear()

    element.send_keys(text)
    element.send_keys(Keys.ENTER)


def create_undetected_driver():
    try:
        driver = None
        # Redirecting to Google Meet Web-Page
        options = uc.ChromeOptions()
        options.add_argument('--incognito')
        options.add_argument("--log-level=3")
        options.add_argument(
            "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.115 Safari/537.36")
        driver = uc.Chrome(version=105, options=options)
        driver.set_window_size(1550, 838)
        size = driver.get_window_size()
        print(size)
        print('----after driver creation')

        stealth(driver,
                user_agent='DN',
                languages=["en-US", "en"],
                vendor="Google Inc.",
                platform="Win32",
                webgl_vendor="Intel Inc.",
                renderer="Intel Iris OpenGL Engine",
                fix_hairline=True,
                )  # Before Login, using stealth
        print('----after stealth')
        return driver
    except Exception as e:
        print(e)
        print('---------------- Generation of New Undetected Driver')
        return driver


def find_elements(driver, xpath):
    return list(driver.find_elements(By.XPATH, xpath))


def find_element(driver, xpath, timeout=20):
    element = WebDriverWait(driver, timeout).until(
        EC.visibility_of_element_located((By.XPATH, xpath)))
    return element


def scroll_to_element_smoothly(driver, element):
    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center', inline: 'nearest'})",
                          element)
