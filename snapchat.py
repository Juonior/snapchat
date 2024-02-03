from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
import time, keyboard
from bs4 import BeautifulSoup
from gpt import get_answer
import os
import shutil
import random

def initialize_driver():
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    chrome_options.add_argument("--use-fake-ui-for-media-stream")
    chrome_options.add_argument("--use-fake-device-for-media-stream")
    chrome_options.add_argument("--use-file-for-fake-video-capture=D:\\output.mjpeg")
    service = ChromeService(executable_path="chromedriver.exe")
    # driver = webdriver.Chrome(service=service, options=chrome_options)
    driver = webdriver.Safari(options=chrome_options)
    return driver

def login(driver, username, password):
    # driver.get("https://accounts.snapchat.com/accounts/v2/login")

    driver.maximize_window()
    # driver.get("https://accounts.snapchat.com/accounts/v2/login?continue=/accounts/sso")
    driver.get("https://accounts.snapchat.com/accounts/v2/login?continue=%2Faccounts%2Fsso%3Freferrer%3Dhttps%253A%252F%252Fweb.snapchat.com%252F%253Fref%253Dsnapchat_dot_com_login_cta%26tiv_request_info%3DCmsKaQpnCkEEeJ5rOJ6EgvY8ocrpRrPkHa7RxFIZlrYCYtEFZGhAybgBORccAEKJddvv3UFkPwwCEWG7OZHcb%252F14QVQrn%252BDTSBIgg39lkyjYC6LeH%252BOo3j4rTuO1Quh5lywRXQvzylykoQAYCQ%253D%253D%26client_id%3Dweb-calling-corp--prod&tiv_request_info=CmsKaQpnCkEEeJ5rOJ6EgvY8ocrpRrPkHa7RxFIZlrYCYtEFZGhAybgBORccAEKJddvv3UFkPwwCEWG7OZHcb%2F14QVQrn%2BDTSBIgg39lkyjYC6LeH%2BOo3j4rTuO1Quh5lywRXQvzylykoQAYCQ%3D%3D")
    account_identifier = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "accountIdentifier")))
    account_identifier.send_keys(username)
    time.sleep(1)
    login_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//div[@class="primary_action login-button"]/button[@type="submit"]')))
    login_button.click()
    password_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "password")))
    password_field.send_keys(password)
    next_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//div[@class="primary_action login-button"]/button[@data-testid="password-submit-button"]')))
    next_button.click()
    time.sleep(5)

def notification_button(driver):
    driver.get("https://web.snapchat.com/accounts/sso")
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
                    if chat_status.text in "New Chat Recieved":
                        url = "https://web.snapchat.com/" + "-".join(chat_status.get('id').split("-")[1:])
                        accounts[url] = nickname.text
        for account in accounts:
            print(accounts[account], account)
            driver.get(account)
            process_messages(driver)
        break
    # driver.get("https://web.snapchat.com/34a9f1b8-b7ba-5672-9368-0bf878f3c535")
    # not_now_button = WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.XPATH, '//button[@class="NRgbw eKaL7 Bnaur"]')))
    # not_now_button.click()

def process_messages(driver):
    dialog_div = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//div[@class="IBqK8"]')))
    dialog_div.click()
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
                messages.append({"role": sender, "content": user_messages})

    if len(messages) > 0:
        process_user_message(driver, messages)

def process_user_message(driver, messages):
    print(messages[-1]["role"])
    if messages[-1]["role"] == "user":
        while True:
            try:
                raw_answer = get_answer(messages)
                break
            except:
                print("Cant get Answer from GPT. Waiting 3 seconds")
                time.sleep(3)
        answer = raw_answer.replace("📸", "").replace("[фото]", "").replace("фото", "")
        print(answer)

        # chat_box = WebDriverWait(driver, 10).until(
        #     EC.presence_of_element_located((By.XPATH, '//div[@role="textbox"][@placeholder="Send a chat"]'))
        # )
        # chat_box.click()
        # keyboard.write(answer)
        # time.sleep(0.5)
        # keyboard.press_and_release('enter')

        if "фото" in raw_answer or "📸" in raw_answer:
            send_photo(driver)

def send_photo(driver):
    source_path = 'photo'
    destination_path = 'D:\\output.mjpeg'

    file_to_move = random.choice(os.listdir(source_path))
    source_file_path = os.path.join(source_path, file_to_move)

    shutil.move(source_file_path, destination_path)

    snapshot_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "cDumY")))
    snapshot_button.click()

    take_snapshot = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "FBYjn")))
    take_snapshot.click()

    send_to_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//span[@class="nonIntl" and text()="Send To"]')))
    send_to_element.click()

    send_to_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//span[@class="nonIntl" and text()="Send"]')))
    send_to_element.click()
    time.sleep(1)
    print(driver.page_source)