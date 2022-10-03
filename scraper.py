import csv
import random

from utils import *
import time
import traceback
import os
import json
from datetime import datetime
from selenium.webdriver import ActionChains

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
all_followers = []


def getting_followings(username):
    driver.get(f"https://www.instagram.com/{username}")
    time.sleep(3)
    no_of_following = find_element(driver, "//*[contains(text(), ' following')]//span").text
    all_followings = []

    driver.get(f"https://www.instagram.com/{username}/following/")
    time.sleep(10)
    follower_alias = []
    start_scroll = 0
    end_scroll = 500
    username_alias = None
    # follower_names = driver.find_elements(By.XPATH,
    #                                       "//div[text()='Followers']/ancestor::div[3]/following-sibling::div/div/div/div/div[2]//a/span/div")
    with open(f"{username}-followings.txt", mode="w") as file:
        file.write("")
    with open(f"{username}-followings.txt", mode="r") as file:
        done_followings = file.readlines()
    if not os.path.exists(f"{username}-followings.csv"):
        with open(f"{username}-followings.csv", mode="w", newline="") as headers_file:
            writer = csv.writer(headers_file)
            writer.writerow(['User Name', "Following Name", "Following Alias"])
    with open(f"{username}-followings.csv", mode="a+", newline="") as file:
        writer = csv.writer(file)
        while len(all_followings) != int(str(no_of_following).replace(',', '')):
            for following in driver.find_elements(By.XPATH,
                                                  "//div[@class='_ab8w  _ab94 _ab99 _ab9h _ab9m _ab9o _abcm']//div[@class='_ab8w  _ab94 _ab99 _ab9f _ab9m _ab9p _abcm']"):
                username_alias = None

                name = following.find_element(By.XPATH, ".//a/span//div").text
                name = name.encode('ascii', 'ignore').decode()
                if name + "\n" in done_followings:
                    continue
                try:
                    username_alias = following.find_element(By.XPATH, ".//following-sibling::div/div").text
                    username_alias = username_alias.encode('ascii', 'ignore').decode()
                except:
                    pass
                if name not in all_followings:
                    all_followings.append(name)
                    writer.writerow([username, name, username_alias])
                    with open(f"{username}-followings.txt", mode="a+") as writefile:
                        writefile.write(name + "\n")
                else:
                    pass
            driver.execute_script(f"document.querySelector('div._aano').scrollBy({start_scroll}, {end_scroll})")
            time.sleep(2)
            start_scroll = end_scroll
            end_scroll += 500


def getting_followers(username):
    driver.get(f"https://www.instagram.com/{username}")
    time.sleep(3)
    no_of_followers = find_element(driver, "//*[contains(text(), ' followers')]//span").text

    driver.get(f"https://www.instagram.com/{username}/followers/")
    time.sleep(10)
    follower_alias = []
    start_scroll = 0
    end_scroll = 500
    username_alias = None
    # follower_names = driver.find_elements(By.XPATH,
    #                                       "//div[text()='Followers']/ancestor::div[3]/following-sibling::div/div/div/div/div[2]//a/span/div")
    with open(f"{username}-followers.txt", mode="w") as file:
        file.write("")
    with open(f"{username}-followers.txt", mode="r") as file:
        done_followers = file.readlines()
    if not os.path.exists(f"{username}-followers.csv"):
        with open(f"{username}-followers.csv", mode="w", newline="") as headers_file:
            writer = csv.writer(headers_file)
            writer.writerow(['User Name', "Follower Name", "Follower Alias"])
    with open(f"{username}-followers.csv", mode="a+", newline="") as file:
        writer = csv.writer(file)
        while len(all_followers) != int(str(no_of_followers).replace(',', '')):
            for follower in driver.find_elements(By.XPATH,
                                                 "//div[@class='_ab8w  _ab94 _ab99 _ab9h _ab9m _ab9o _abcm']//div[@class='_ab8w  _ab94 _ab99 _ab9f _ab9m _ab9p _abcm']"):
                username_alias = None

                name = follower.find_element(By.XPATH, ".//a/span//div").text
                name = name.encode('ascii', 'ignore').decode()
                if name + "\n" in done_followers:
                    continue
                try:
                    username_alias = follower.find_element(By.XPATH, ".//following-sibling::div/div").text
                    username_alias = username_alias.encode('ascii', 'ignore').decode()
                except:
                    pass
                if name not in all_followers:
                    all_followers.append(name)
                    writer.writerow([username, name, username_alias])
                    with open(f"{username}-followers.txt", mode="a+") as writefile:
                        writefile.write(name + "\n")
                else:
                    pass
            driver.execute_script(f"document.querySelector('div._aano').scrollBy({start_scroll}, {end_scroll})")
            time.sleep(2)
            start_scroll = end_scroll
            end_scroll += 500


def apply_session():
    driver.get("https://instagram.com")
    cfh = open(
        os.path.join(BASE_DIR, "sessions", f"adnan_instagram_cookies.json"),
        encoding="utf-8",
    )
    cookies = json.load(cfh)
    cfh.close()
    sfh = open(
        os.path.join(BASE_DIR, "sessions", f"adnan_instagram_storage.json"),
        encoding="utf-8",
    )
    storage = sfh.read()
    sfh.close()
    time.sleep(3)
    driver.execute_script(
        """var Object_Details = JSON.parse(arguments[0]) ,
                         keys = Object.keys(Object_Details),
                         i = keys.length;
                             while ( i-- ) {
                                 k = keys[i];
                                 localStorage.setItem(k, Object_Details[k]);
                             }""",
        storage,
    )
    for cookie in cookies:
        driver.add_cookie(cookie)
    driver.get(driver.current_url)


def fetch_cookies():
    with open(
            os.path.join("sessions", f"instagram_cookies.json"), "w", encoding="utf-8"
    ) as cfh:
        json_cookies = json.dumps(driver.get_cookies())
        cfh.write(json_cookies)
    with open(
            os.path.join("sessions", f"instagram_storage.json"), "w", encoding="utf-8"
    ) as sfh:
        storage = driver.execute_script(
            """
        var values = {},
            keys = Object.keys(localStorage),
            i = keys.length;
        while ( i-- ) {
            k = keys[i];
            values[k] = localStorage.getItem(k);
        }
        storage_session = JSON.stringify(values);
        console.log(storage_session);
        return storage_session;
        """
        )
        sfh.write(storage)


def parse_post(done_posts, page_info=None):
    actions = ActionChains(driver)
    if not os.path.exists(f"{username}-done_posts.txt"):
        with open(f"{username}-done_posts.txt", mode="w") as file:
            file.write("")
    with open(f"{username}-done_posts.txt", mode="r") as file:
        urls = file.readlines()
    play_count = 0
    for post in driver.find_elements(By.XPATH,
                                     "//div[@class='_ac7v _aang']//a[@role='link'] | //div[@class='_ac7v _abq4']//a[@role='link']"):
        # scroll_to_element_smoothly(driver, post)
        tag_list = []
        play_count += 1
        post_url = post.get_attribute('href')
        if post_url.replace('/p/', '/reel/') + "\n" in urls or post_url + "\n" in urls:
            continue
        if post_url not in done_posts:
            done_posts.append(post_url)
            time.sleep(3)
            try:
                no_of_plays = find_element(post, f"//a[@role='link']//div[@class='_aajy']//span").text
            except:
                no_of_plays = ''

            actions.move_to_element(post).perform()

            try:
                post_likes = post.find_element(By.XPATH, "(.//li[@class='_abpm']//div/span)[1]").text
            except:
                post_likes = ''
            try:
                post_comments = post.find_element(By.XPATH, "(.//li[@class='_abpm']//div/span)[2]").text
            except:
                post_comments = ''
            actions.move_to_element(post).click().perform()
            time.sleep(5)
            try:
                driver.find_element(By.XPATH, "//h2[contains(text(), \"Sorry, this page isn't available.\")]")
                driver.get(driver.current_url)
                with open(f"{username}-done_posts.txt", mode="a+") as file:
                    file.write(post_url + "\n")
                with open(f"{username}-done_posts.txt", mode="r") as file:
                    urls = file.readlines()
            except:
                pass
            for tag in find_elements(driver, "(.//a[contains(@href, '/explore/tags')])"):
                tag_list.append(tag.text)
            try:
                posted_date = find_element(driver, ".//a[@role='link']//div/time").get_attribute('title')
            except:
                posted_date = ''
                print("posted_date not found")
            ele = find_element(driver, ".//div[@class='s8sjc6am mczi3sny pxtik7zl b0ur3jhr']//div[@role='button']")
            actions.move_to_element(ele).click().perform()

            post_info = [posted_date, post_likes, post_comments, no_of_plays, tag_list, post_url,
                         username]
            # post_info.extend(page_info)
            print(post_info)
            with open(output_file_name, mode="a+", newline='', encoding='utf-16') as file:
                writer = csv.writer(file)
                writer.writerow(post_info)
            with open(f"{username}-done_posts.txt", mode="a+") as file:
                file.write(post_url + "\n")


def start():
    start_height = 0
    end = 500
    done_posts = []
    #
    url_list = [f"https://www.instagram.com/{username}/reels/", f"https://www.instagram.com/{username}/"]
    for url in url_list:
        driver.get(url)
        time.sleep(10)
        no_of_posts = find_element(driver, "//*[contains(text(), 'posts')]//span").text
        no_of_followers = find_element(driver, "//*[contains(text(), ' followers')]//span").text
        # find_element(driver, "//*[contains(text(), ' followers')]//span").click()
        # getting_followers(driver, no_of_followers)
        no_of_following = find_element(driver, "//*[contains(text(), ' following')]//span").text
        name = find_element(driver, "//main[@role='main']//ul//following-sibling::div/span").text
        try:
            pronoun = driver.find_element(By.XPATH, "//span[@class='_aacl _aacp _aacu _aacy _aad7 _aade']").text
        except:
            pronoun = None
        try:
            business_category = driver.find_element(By.XPATH,
                                                    "//div[@class='_aacl _aacp _aacu _aacy _aad6 _aade']").text
        except:
            business_category = None
        bio = find_elements(driver, "//div[@class='_aacl _aacp _aacu _aacx _aad6 _aade']")[-1].text
        try:
            website = \
                find_elements(driver, "//div[@class='_aacl _aacp _aacu _aacx _aad6 _aade']//following-sibling::a")[
                    -1].get_attribute('href')
        except:
            website = None
        image = find_element(driver, "//header//img[contains(@alt, 'profile picture')]").get_attribute('src')
        page_info = [no_of_posts, no_of_followers, no_of_following, website, name, pronoun, business_category,
                     bio, image]
        with open(f'{date}-{username}-profile-core.csv', "a+", newline="", encoding="utf-16") as core_file:
            writer = csv.writer(core_file)
            writer.writerow(page_info)
        doc_height = driver.execute_script(f"window.scrollTo({start_height}, {150}); return document.body.scrollHeight")
        while end != doc_height:
            try:
                doc_height = driver.execute_script("return document.body.scrollHeight")
                parse_post(done_posts)
                try:
                    driver.execute_script(
                        f"window.scrollTo({doc_height}, document.body.scrollHeight); return document.body.scrollHeight"
                    )
                except:
                    time.sleep(5)
                    driver.execute_script(
                        f"window.scrollTo({doc_height}, document.body.scrollHeight); return document.body.scrollHeight"
                    )
                time.sleep(random.randint(15, 30))
                end = driver.execute_script("return document.body.scrollHeight")
                print(doc_height, end)
            except Exception as e:
                print(traceback.print_exc())
                print(f"Page is not loading more ...", e)


def fetch_followers():
    pass


if __name__ == "__main__":
    # username = "givemeabrake0918"

    driver = create_undetected_driver()
    # fetch_cookies()
    apply_session()
    # with open("following_time.txt", mode="a+", newline="") as file:
    #     file.write(datetime.now().strftime("%H:%M:%S %Y:%m:%d"))
    # getting_followings(username)
    # with open("following_time.txt", mode="a+", newline="") as file:
    #     file.write("\n")
    #     file.write(datetime.now().strftime("%H:%M:%S %Y:%m:%d"))
    # with open("follower_time.txt", mode="a+", newline="") as file:
    #     file.write(datetime.now().strftime("%H:%M:%S %Y:%m:%d"))
    # getting_followers(username)
    # with open("follower_time.txt", mode="a+", newline="") as file:
    #     file.write("\n")
    #     file.write(datetime.now().strftime("%H:%M:%S %Y:%m:%d"))
    with open("usernames.json", mode="r") as json_file:
        usernames = json.load(json_file)
    for username in usernames:
        date = datetime.now().strftime("%Y-%m-%d")
        output_file_name = f'{date}-{username}-post-details.csv'
        profile_core_headers = ['No of Posts',
                                'No of Followers',
                                'No of Followings', 'website', 'Full Name', 'Pronoun', 'Business Category', 'Bio',
                                'Image']
        profile_core_file = f'{date}-{username}-profile-core.csv'
        if not os.path.exists(profile_core_file):
            with open(profile_core_file, mode="w", newline='', encoding="utf-16") as profile_core:
                writer = csv.writer(profile_core)
                writer.writerow(profile_core_headers)
        if not os.path.exists(output_file_name):
            with open(output_file_name, mode="w", newline='') as file:
                writer = csv.writer(file)
                writer.writerow(
                    ['Posted Date', 'Likes', 'Comments', 'No of Plays', 'Hash Tags', 'Post URL', 'UserName'])

        start()
