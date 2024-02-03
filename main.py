from snapchat import *

username = "juonior99"
password = "q33jk0000"

if __name__ == "__main__":

    driver = initialize_driver()
    login(driver, username, password)
    notification_button(driver)
    # process_messages(driver)