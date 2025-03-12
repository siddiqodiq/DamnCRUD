from selenium import webdriver
from selenium.webdriver.common.by import By
import os

def get_session():
    option = webdriver.FirefoxOptions()
    option.add_argument('--headless')
    browser = webdriver.Firefox(options=option)

    try:
        try:
            url = os.environ['URL']
        except:
            url = "http://localhost"

        browser.get(url)
        browser.find_element(By.NAME, "username").send_keys("admin")
        browser.find_element(By.NAME, "password").send_keys("nimda666!")
        browser.find_element(By.XPATH, "/html/body/form/button").click()

        session_cookie = browser.get_cookie("PHPSESSID")["value"]
        
        with open("session_file", "w") as file:
            file.write(session_cookie)

    finally:
        browser.quit()

if __name__ == "__main__":
    get_session()