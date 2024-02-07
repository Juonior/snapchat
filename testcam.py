from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
chrome_options.add_argument("--use-fake-ui-for-media-stream")
chrome_options.add_argument("--use-fake-device-for-media-stream")
chrome_options.add_argument("--use-file-for-fake-video-capture=C:\\Users\\Administrator\\Desktop\\1.mjpeg")


service = ChromeService(executable_path="chromedriver.exe")

driver = webdriver.Chrome(service=service, options=chrome_options)


driver.get("https://webcammictest.com/ru/")
