from selenium import webdriver
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
import time, keyboard
from bs4 import BeautifulSoup
from gpt import get_answer
import os
import shutil, json
from crop import changephoto_to_camera
import random
last_messages_answered = {}
answers_cache = {}
import json

ignored_users = []

def load_ignored_users():
    ignored_users = []
    try:
        with open('ignored_users.json', 'r') as file:
            ignored_users = json.load(file)
    except FileNotFoundError:
        pass  # Если файл не найден, просто возвращаем пустой список игнорируемых пользователей
    return ignored_users

def write_to_json(user_name):
    ignored_users = load_ignored_users()
    ignored_users.append(user_name)
    with open('ignored_users.json', 'w') as file:
        json.dump(ignored_users, file)


def write_text(message):

    characters_per_minute = 120 * 5
    characters_per_second = characters_per_minute / 60
    
    delay_per_char = 1 / characters_per_second
    
    for char in message:
        keyboard.write(char)
        time.sleep(delay_per_char)
def initialize_driver():
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    chrome_options.add_argument("--use-fake-ui-for-media-stream")
    chrome_options.add_argument("--use-fake-device-for-media-stream")
    chrome_options.add_argument("--use-file-for-fake-video-capture=C:\\Users\\Administrator\\Desktop\\1.mjpeg")
    service = ChromeService(executable_path="chromedriver.exe")
    driver = webdriver.Chrome(service=service, options=chrome_options)
    # driver = webdriver.Safari(options=chrome_options)
    driver.maximize_window()
    return driver

def login(driver, username, password):
    # driver.get("https://accounts.snapchat.com/accounts/v2/login")

    # driver.get("https://accounts.snapchat.com/accounts/v2/login?continue=/accounts/sso")
    driver.get("https://accounts.snapchat.com/accounts/v2/login?continue=%2Faccounts%2Fsso%3Freferrer%3Dhttps%253A%252F%252Fweb.snapchat.com%252F%253Fref%253Dsnapchat_dot_com_login_cta%26tiv_request_info%3DCmsKaQpnCkEEeJ5rOJ6EgvY8ocrpRrPkHa7RxFIZlrYCYtEFZGhAybgBORccAEKJddvv3UFkPwwCEWG7OZHcb%252F14QVQrn%252BDTSBIgg39lkyjYC6LeH%252BOo3j4rTuO1Quh5lywRXQvzylykoQAYCQ%253D%253D%26client_id%3Dweb-calling-corp--prod&tiv_request_info=CmsKaQpnCkEEeJ5rOJ6EgvY8ocrpRrPkHa7RxFIZlrYCYtEFZGhAybgBORccAEKJddvv3UFkPwwCEWG7OZHcb%2F14QVQrn%2BDTSBIgg39lkyjYC6LeH%2BOo3j4rTuO1Quh5lywRXQvzylykoQAYCQ%3D%3D")
    cookie_accept = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//span[text()="Accept All"]')))
    cookie_accept.click()

    account_identifier = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "accountIdentifier")))
    account_identifier.send_keys(username)
    time.sleep(1)
    login_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//div[@class="primary_action login-button"]/button[@type="submit"]')))
    login_button.click()
    password_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "password")))
    password_field.send_keys(password)
    next_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//div[@class="primary_action login-button"]/button[@data-testid="password-submit-button"]')))
    next_button.click()
    time.sleep(1)

def notification_button(driver):
    global ignored_users
    ignored_users = load_ignored_users()

    driver.get("https://web.snapchat.com/accounts/sso")
    while True:
        try:
            cookie_accept = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//span[text()="Not now"]')))
            cookie_accept.click()
            break
        except:
            pass
    #cookie_accept = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, '//span[text()="Not now"]')))
    #cookie_accept.click()
    while True:
        accounts = {}
        listitems = []
        while len(listitems) <= 1:
            listitem = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//div[@role="listitem"]')))
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            listitems = soup.find_all('div', {'role': 'listitem'})
        for listitem in listitems:
            nickname = listitem.find('span', class_='mYSR9 nonIntl')
            if nickname:
                chat_status = listitem.find('span', class_='GQKvA')
                if not nickname.text in "Team Snapchat My AI":
                    if chat_status:
                        # print(chat_status.text)
                        if chat_status.text in "New Chat Received":
                            url = "https://web.snapchat.com/" + "-".join(chat_status.get('id').split("-")[1:])
                            accounts[url] = nickname.text
        for account in accounts:
            if accounts[account] not in ignored_users:
                print(accounts[account], account)
                if driver.current_url != account:
                    driver.get(account)
                process_messages(driver, accounts[account])

def process_messages(driver, user_name):
    try:
        dialog_div = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//div[@class="IBqK8"]')))
        try:
            dialog_div.click()
        except ElementClickInterceptedException:
            cookie_accept = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//span[text()="Not now"]')))
            cookie_accept.click()
            time.sleep(0.5)
            dialog_div.click()
    except:
        pass
    time.sleep(1)
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')
    message_containers = soup.find_all('li', class_='T1yt2')
    messages = []
    for container in message_containers:
        sender_tag = container.find('span', class_='nonIntl')
        messages_tag = container.find_all('div', class_='p8r1z')
        if sender_tag and messages_tag:
            user_messages = ' '.join([message_tag.get_text(strip=True) for message_tag in messages_tag])
            sender = "assistant" if sender_tag.get_text(strip=True) == "Me" else "user"
            if not "DELETED A " in user_messages:
                messages.append({"role": sender, "content": user_messages.replace("snap", "photo").replace("снап", "фото")})

    if len(messages) > 0:
        process_user_message(driver, messages, user_name)

def process_user_message(driver, messages, user_name):
    last_message = messages[-1]
    
    if last_message["role"] == "user":
        user_message_key = f"{user_name}_{last_message['content']}"

        # Check if the answer for this user and message combination is already in the cache
        if user_message_key in answers_cache:
            raw_answer = answers_cache[user_message_key]
        else:
            while True:
                try:
                    raw_answer = get_answer(messages)
                    break
                except:
                    print("Can't get Answer from GPT. Waiting 3 seconds")
                    time.sleep(3)

            # Store the answer in the cache
            answers_cache[user_message_key] = raw_answer

        answer = raw_answer.replace("📸", "").replace("[фото]", "").replace('"фото"', "").replace("[photo]","")
        print(answer)
        messages_answer = answer.split("\n")
        # Continue with sending the answer and photo if applicable
        chat_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//div[@role="textbox"][@placeholder="Send a chat"]'))
        )
        chat_box.click()
        for msg in messages_answer:
            write_text(msg)
            time.sleep(0.5)
            keyboard.press_and_release('enter')

        if "фото" in raw_answer or "📸" in raw_answer or "photo" in raw_answer.lower():
            send_photo(driver, user_name)
        # Check if the raw answer contains "45456"
        if "45456" in raw_answer:
            write_to_json(user_name)
            ignored_users.append(user_name)
            return
def send_photo(driver, user_name):
    source_path = "C:\\Users\\Administrator\\Desktop\\photo"
    log_file_path = 'sent_photos_log.json'

    # Load existing log or create an empty one
    sent_photos_log = {}
    if os.path.exists(log_file_path):
        with open(log_file_path, 'r') as log_file:
            sent_photos_log = json.load(log_file)

    # Get the list of photos in the source_path
    available_photos = [file for file in os.listdir(source_path) if file.endswith(('.jpg', '.jpeg', '.png'))]

    # Filter out photos that have already been sent to the user
    unsent_photos = [photo for photo in available_photos if photo not in sent_photos_log.get(user_name, [])]

    if unsent_photos:
        # Choose a photo to send
        selected_photo = unsent_photos[0]
        source_file_path = os.path.join(source_path, selected_photo)

        changephoto_to_camera(source_file_path)

        # Update the sent photos log for the user
        if user_name not in sent_photos_log:
            sent_photos_log[user_name] = []
        sent_photos_log[user_name].append(selected_photo)

        # Save the updated log file
        with open(log_file_path, 'w') as log_file:
            json.dump(sent_photos_log, log_file)

        # Rest of your existing code for sending the photo
        snapshot_button = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CLASS_NAME, "cDumY")))
        snapshot_button.click()

        take_snapshot = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CLASS_NAME, "FBYjn")))
        take_snapshot.click()
        
        send_to_element = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//span[@class="nonIntl" and text()="Send"]')))
        send_to_element.click()

    else:
        print(f"No unsent photos available for {user_name}")