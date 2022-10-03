import csv
import os
import time
import os
from datetime import datetime
from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


def save_into_csv(email, phone, username):
    file_path = f'contact-details.csv'
    if not os.path.exists(file_path):
        with open(file_path, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["User Name", "Email", "Phone"])
    with open(file_path, mode="a+", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([username, email, phone])


def get_contact_details(username):
    email = None
    phone = None
    time.sleep(5)
    try:
        driver.find_element(By.XPATH, "//android.widget.Button[@text='Contact']/../..").click()
        email = driver.find_element(By.XPATH,
                                    "//android.widget.TextView[@text='Email']//following-sibling::android.widget.TextView").text

        phone = driver.find_element(By.XPATH,
                                    "//android.widget.TextView[@text='Call']//following-sibling::android.widget.TextView").text

        if 'Request phone number' in phone:
            print("Phone not Found.. !!")
            phone = ''
        driver.back()
    except:
        try:

            driver.find_element(By.XPATH, "//android.widget.Button[@text='Email']/../..").click()
            time.sleep(3)
            try:
                driver.find_element(By.XPATH, "//android.widget.Button[@text='OK']").click()
            except:
                pass
            email = driver.find_element(By.XPATH,
                                        "//android.widget.MultiAutoCompleteTextView[@resource-id='com.google.android.gm:id/to']").text
            email = email.replace('<', '').replace('>', '').replace(',', '').strip()
            print("Email is ... ", email)
            driver.back()
            time.sleep(2)
            driver.back()
        except Exception as e:
            print("Email Not Found ... !!!", e)
            return
    time.sleep(4)
    if email is None:
        print("Email Not Found... !!!")
        return
    save_into_csv(email, phone, username)


def search_user(usernames):
    for username in usernames:
        driver.find_element(By.XPATH, '//android.widget.FrameLayout[@content-desc="Search and explore"]').click()
        time.sleep(5)
        try:
            driver.find_element(By.XPATH,
                                "//android.widget.EditText[@text='Search']").click()
        except:
            driver.find_element(By.XPATH,
                                "//android.widget.EditText[@text='Search']").click()
        driver.find_element(By.XPATH,
                            "//android.widget.TextView[@text='Search']/preceding-sibling::android.widget.EditText").send_keys(
            username)
        time.sleep(3)
        driver.find_element(By.XPATH,
                            f"//android.widget.TextView[@text='{username}' and @resource-id='com.instagram.android:id/row_search_user_username']").click()
        get_contact_details(username)


def launch_app():
    try:
        driver.find_element(By.XPATH, '//android.widget.TextView[@content-desc="Instagram"]').click()
        time.sleep(5)
    except:
        print("Unable to start instagram... please try again")
        raise Exception


if __name__ == '__main__':
    usernames = ['givemeabrake0918', 'artingiftingco']
    desired_capabilities = {
        "platformName": "Android",
        "platformVersion": "9",
        "deviceName": "Android Emulator"
    }
    driver = webdriver.Remote("http://127.0.0.1:4723/wd/hub", desired_capabilities)
    launch_app()
    search_user(usernames)