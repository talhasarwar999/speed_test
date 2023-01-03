import csv
import json
import time
import os
import logging
import calendar
from datetime import datetime, timedelta
from helper_client import *
from appium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)

profile_headers = [
    "No. of posts", "No. of followers", "No. of followings", "Bio/Description", "Pronouns",
    "Website", "Profile Picture", "Email", "Business Category", "Full Name"
]
posts_headers = [
    "Media content", "Date posted", "No. of likes", "No. of comments", "Hashtags", "No. of plays", "Post url"
]

profiles_file = 'scraped_data/{}_profile_data.csv'
posts_file = 'scraped_data/{}_posts_data.csv'

LOOKING_FOR_POSTS_IN_DAYS = 14
MAX_PINNED_POSTS = 3


# helper functions
def save_into_csv(file, header, data):
    """
        This function save data into csv file.
        if file exists then insert data in all cases(duplicated)
        if file not exist,then create file and then insert data into file
    """
    if not os.path.exists(file):
        with open(file, mode="w", newline="", encoding='utf-8') as fp:
            writer = csv.writer(fp)
            writer.writerow(header)

    with open(file, mode="a+", newline="", encoding='utf-8') as fp:
        writer = csv.writer(fp)
        writer.writerow(data)


def clean_data(text):
    """
        This function us used to get numeric value from string.
        e.g. "view 55 comments" -> return 55
             "view 5,555 comments" -> return 5,555
             "view comments" -> return ''
    """
    if text:
        numeric_lst = [x for x in text.split() if x.replace(',', '').isnumeric()] if text else ['']
        if numeric_lst:
            return numeric_lst[0]
    return ''


def simple_scrolling(scroll_length, wait_time=3):
    """
        This function is used to scroll mobile screen for specific length
        e.g. if scroll length is 1000,then it will scroll 1400 to 1000 with speed of 250 ms.
    """
    driver.swipe(525, 1400, 525, scroll_length, 250)
    time.sleep(wait_time)


def scrolling_for_element(element_xpath, scroll_length):
    """
        This function scroll mobile screen until element is not displayed
        e.g. if you passed date of the instagram post,then it will scroll until it find date
    """
    while True:
        try:
            driver.find_element(By.XPATH, element_xpath).is_displayed()
            break
        except NoSuchElementException:
            simple_scrolling(scroll_length)
            continue


def get_contact_details():
    """
        This function is used to get email of the instagram user
        if Contact button is available then it will click on it and get email
        if  Email button is available then it will go to your email box and find email from them.You must have to
        set up email account before this case.

    """
    email = None
    time.sleep(2)
    try:
        driver.find_element(By.XPATH, "//android.widget.Button[@text='Contact']/../..").click()
        email = driver.find_element(
            By.XPATH, "//android.widget.TextView[@text='Email']//following-sibling::android.widget.TextView").text

        driver.back()
    except NoSuchElementException:
        try:
            driver.find_element(By.XPATH, "//android.widget.Button[@text='Email']/../..").click()
            time.sleep(3)
            try:
                driver.find_element(By.XPATH, "//android.widget.Button[@text='OK']").click()
            except NoSuchElementException:
                pass
            email = driver.find_element(By.XPATH,
                                        '//android.widget.Button[@resource-id="com.google.android.gm:id/peoplekit_chip"]').text
            email = email.replace('<', '').replace('>', '').replace(',', '').strip()
            driver.back()
            time.sleep(2)
            driver.back()
        except NoSuchElementException:
            return
    time.sleep(2)
    if email is None:
        return
    return email


def getting_users():
    """
        This function is used to get users data for scraping purposes.You can get data from anywhere like Airflow,google
         sheet or anywhere.You must return a list of usernames in end.
    """
    logging.info('Getting users from file for scraping')
    airtable_client = AirtableClient()
    return airtable_client.get_usernames()


def getting_web_driver():
    """
        This function is used to get the driver after setting capabilities and creating connection with appium server.
    """
    logging.info("Setting web driver capabilities")
    desired_capabilities = {
        "platformName": "Android",
        "platformVersion": "7.1.1",
        "deviceName": "Android Emulator",
    }
    return webdriver.Remote("http://localhost:4723/wd/hub", desired_capabilities)


def scroll_for_check_length(media_y_position):
    """
        This function is used to check if we need scrolling for content.We have sometimes case where we get content
        above from the next post.We always get accurate data so this function always gives us correct data after
        scrolling.This will compare the Y-axis for both elements and then scroll if possible.
    """
    content_y_position = driver.find_element(
        By.XPATH, '//android.view.View[@resource-id="com.instagram.android:id/gap_view"]').location['y']
    loop_count = 0
    while content_y_position < media_y_position and loop_count < 2:
        driver.swipe(525, 1400, 525, 800, 250)
        time.sleep(3)
        try:
            content_y_position = driver.find_element(
                By.XPATH, '//android.view.View[@resource-id="com.instagram.android:id/gap_view"]').location['y']
        except NoSuchElementException:
            pass
        if content_y_position > media_y_position:
            break
        loop_count += 1


def launch_app():
    """
        This function is used to launch instagram app in emulator.
        e.g. if app crashed then it will terminate app and start app after 2 minute again.
             if app is already launched then it will terminate app and start app until we get instagram element.
             if max tries reached then it will terminate program.
    """
    max_retries = 5
    while True:
        try:
            driver.find_element(By.XPATH, '//android.widget.TextView[@content-desc="Instagram"]').click()
            time.sleep(5)
            try:
                if driver.find_element(By.XPATH, '//android.widget.TextView[@text="Instagram has stopped"]'):
                    raise NoSuchElementException
            except NoSuchElementException:
                break
        except NoSuchElementException:
            logging.error("Unable to start instagram,waiting for 2 minutes to start again...")
            driver.terminate_app('com.instagram.android')
            time.sleep(30)
            max_retries -= 1
            if max_retries == 0:
                raise NoSuchElementException


def finding_text_from_element(xpath):
    """
        This function is used to get text from element.
        e.g. if element has text then return text
            if not element exist or has text attribute then return ''
    """
    text_value = ''
    try:
        text_value = driver.find_element(By.XPATH, xpath).text
    except NoSuchElementException:
        pass
    return text_value


def get_profile_data(username):
    """
        This function is used to get profile data of current scrapping user.It will scrape all things except
        profile image from the profile including email,posts,followers,followings,fullname,business category,pronouns
        bio,website.
    """
    email = get_contact_details()

    posts = finding_text_from_element(
        '//android.widget.TextView[@resource-id="com.instagram.android:id/row_profile_header_textview_post_count"]')

    followers = finding_text_from_element(
        '//android.widget.TextView[@resource-id="com.instagram.android:id/row_profile_header_textview_followers_count"]')

    followings = finding_text_from_element(
        '//android.widget.TextView[@resource-id="com.instagram.android:id/row_profile_header_textview_following_count"]')

    full_name = finding_text_from_element(
        '//android.widget.TextView[@resource-id="com.instagram.android:id/profile_header_full_name"]')

    business_category = finding_text_from_element(
        '//android.widget.TextView[@resource-id="com.instagram.android:id/profile_header_business_category"]')

    pronouns = finding_text_from_element(
        '//android.widget.TextView[@resource-id="com.instagram.android:id/profile_header_pronouns"]')

    bio = finding_text_from_element(
        '//android.widget.TextView[@resource-id="com.instagram.android:id/profile_header_bio_text"]')

    website = finding_text_from_element('//android.widget.Button[@resource-id="com.instagram.android:id/text_1"]')
    profile_picture = driver.find_element(By.XPATH,
                        '//android.widget.ImageView[@resource-id="com.instagram.android:id/row_profile_header_imageview"]').screenshot_as_base64
    airtable_client = AirtableClient()
    engagement_rate = 0
    if isinstance(posts, str):
        posts = airtable_client.convert_str_to_number(posts.replace(',',''))
    if isinstance(followers, str):
        followers = airtable_client.convert_str_to_number(followers.replace(',',''))
    if isinstance(followings, str):
        followings = airtable_client.convert_str_to_number(followings.replace(',',''))
    save_into_csv(
        profiles_file.format(username),
        profile_headers,
        [posts, followers, followings, bio, pronouns, website, profile_picture, email, business_category, full_name]
    )
    airtable_client = AirtableClient()
    airtable_client.push_profile_algolia(username, posts, followers, followings, bio, pronouns, website,profile_picture, email,
                                         business_category, full_name, engagement_rate)
    logging.info(f'{username}\'profile is scraped successfully')


def get_posts_data(username):
    """
        This function is used to get all the posts of current scrapping user from the last 14 days.Each post include
        number of likes,number of comments,number of playbacks(reels),content,posted date.
    """
    today = datetime.strptime(datetime.now().strftime('%B %d, %Y'), '%B %d, %Y')
    i = 1
    logging.info(f'{username}\'s posts scraping start')
    while True:
        scrolling_for_element(
            element_xpath='//android.widget.ImageView[@resource-id="com.instagram.android:id/feed_more_button_stub"]',
            scroll_length=650
        )
        time.sleep(3)
        try:
            media_y_position = driver.find_element(
                By.XPATH,
                '//android.view.ViewGroup[@resource-id="com.instagram.android:id/media_header_location"]').location['y']
        except NoSuchElementException:
            media_y_position = driver.find_element(
                By.XPATH,
                '//android.view.ViewGroup[@resource-id="com.instagram.android:id/row_feed_profile_header"]').location[
                'y']
        driver.find_element(By.XPATH,
                            '//android.widget.ImageView[@resource-id="com.instagram.android:id/feed_more_button_stub"]').click()

        time.sleep(3)
        driver.find_element(By.XPATH, "//android.widget.TextView[@text='Link']").click()
        time.sleep(3)
        post_url = driver.get_clipboard_text()
        media_content = 'video' if 'reel' in post_url else 'image'
        time.sleep(3)
        scrolling_for_element(
            element_xpath='//android.view.View[@resource-id="com.instagram.android:id/gap_view"]', scroll_length=850)
        time.sleep(3)
        scroll_for_check_length(media_y_position)
        time.sleep(3)

        date_posted = ''
        date_ago_lst = ['second', 'seconds', 'hour', 'hours', 'minute', 'minutes', 'day', 'days']
        ago_exist = False
        for month in list(calendar.month_name)[1:] + date_ago_lst:
            try:
                date_posted = driver.find_element(By.XPATH,
                                                  f"//android.widget.TextView[contains(@text,'{month}')]").text

                if date_posted.split()[1] in date_ago_lst:
                    ago_exist = True
                    if date_posted.split()[1] in ['second', 'seconds', 'hour', 'hours', 'minute', 'minutes']:
                        date_posted = '0 days ago'
                    date_posted = (today - timedelta(days=int(date_posted.strip().split()[0]))).strftime('%B %d')
                break
            except NoSuchElementException:
                continue
        try:
            post_date = datetime.strptime(date_posted, '%B %d').replace(year=datetime.now().year)
        except ValueError:
            post_date = datetime.strptime(date_posted, '%B %d, %Y')

        days_diff = (today - post_date).days
        if (days_diff > LOOKING_FOR_POSTS_IN_DAYS and i > MAX_PINNED_POSTS) or \
                (days_diff > LOOKING_FOR_POSTS_IN_DAYS and ago_exist):
            airtable_client = AirtableClient()
            user_id = airtable_client.get_user_id(username)
            airtable_client.update_user(user_id, "Success")
            airtable_client.calculate_engagement_rate(username)
            logging.info(f'{username}"s are scraped successfully')
            break
        if days_diff <= LOOKING_FOR_POSTS_IN_DAYS:
            tags_list = []
            time.sleep(3)
            for tag in driver.find_elements(By.XPATH, "//android.widget.Button[contains(@content-desc,'#')]"):
                tags_list.append(tag.text)
            tags = ','.join(tags_list)
            comments = clean_data(finding_text_from_element(
                '//android.widget.Button[@resource-id="com.instagram.android:id/row_feed_view_all_comments_text"]'))
            likes_xpath = '//android.widget.TextView[@resource-id="com.instagram.android:id/row_feed_textview_likes"]'
            likes = clean_data(finding_text_from_element(likes_xpath))
            driver.find_element(By.XPATH, likes_xpath).click()
            time.sleep(3)

            plays = clean_data(finding_text_from_element(
                '//android.widget.TextView[@resource-id="com.instagram.android:id/play_count_text"]'))
            time.sleep(3)
            driver.back()
            time.sleep(3)
            save_into_csv(posts_file.format(username), posts_headers,
                          [media_content, date_posted, likes, comments, tags, plays, post_url])
            time.sleep(3)
            airtable_client = AirtableClient()
            if isinstance(likes, str):
                likes = airtable_client.convert_str_to_number(likes.replace(',',''))
            if isinstance(comments, str):
                comments = airtable_client.convert_str_to_number(comments.replace(',',''))
            if isinstance(plays, str):
                plays = airtable_client.convert_str_to_number(plays.replace(',',''))
            airtable_client = AirtableClient()
            airtable_client.push_posts_algolia(username, media_content, date_posted, likes, comments, tags, plays,
                                               post_url)
            logging.info(f'{username} {i} posts are scraped successfully.')
        else:
            logging.info(f'Pinned post ignored due to days difference')

        i += 1


def scrape_users(usernames):
    """
        This function is used to scrapped all the users one by one and save data into csv files.Two csvs are generated
        for each user(profile data,posts data).
    """
    logging.info(f'Starting with {len(usernames)} accounts')
    for username in usernames:
        logging.info(f'{username} is processing')
        driver.find_element(By.XPATH, '//android.widget.FrameLayout[@content-desc="Search and explore"]').click()
        time.sleep(3)
        driver.find_element(By.XPATH, "//android.widget.EditText[@text='Search']").click()
        driver.find_element(
            By.XPATH, "//android.widget.TextView[@text='Search']/preceding-sibling::android.widget.EditText"
        ).send_keys(username)
        time.sleep(3)
        try:
            driver.find_element(
                By.XPATH,
                f"//android.widget.TextView[@text='{username}' and @resource-id='com.instagram.android:id/row_search_user_username']").click()
            time.sleep(3)
            try:
                get_profile_data(username)
                time.sleep(3)
                scrolling_for_element(
                    element_xpath='//android.widget.ImageView[@content-desc="Grid view"]', scroll_length=400)
                driver.find_elements(
                    By.XPATH,
                    '//androidx.recyclerview.widget.RecyclerView//android.widget.LinearLayout//android.widget.Button')[
                    0].click()
                time.sleep(3)
                get_posts_data(username)
            except NoSuchElementException:
                logging.info("Account exist but something wrong occured while scraping")
                continue

        except NoSuchElementException:
            airtable_client = AirtableClient()
            user_id = airtable_client.get_user_id(username)
            logging.info(f"{user_id}, USER_ID")
            airtable_client.update_user(user_id, "Failed")
            airtable_client.calculate_engagement_rate(username)
            logging.info(f'{username}\'account is not found')
            driver.back()


if __name__ == '__main__':
    try:
        driver = getting_web_driver()
        users = getting_users()
        launch_app()
        scrape_users(['adornedbybritt'])

    except NoSuchElementException:
        logging.error(
            "Something bad happened.Cannot start scraping right now.Please restart your device and try again.")
