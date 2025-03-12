import unittest
import os
from selenium import webdriver
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import logging

# Setup logging
logging.basicConfig(filename='test-results/test_log.txt', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class TestContactManagement(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.url = "http://127.0.0.1:8000"  # Sesuaikan dengan URL yang digunakan dalam CI/CD
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        cls.browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        logging.info("Browser started in headless mode.")

    def login(self):
        self.browser.get(f"{self.url}/login.php")
        self.browser.find_element(By.ID, "inputUsername").send_keys("admin")
        self.browser.find_element(By.ID, "inputPassword").send_keys("nimda666!")
        self.browser.find_element(By.XPATH, "//button[@type='submit']").click()
        logging.info("Logged in successfully.")

    def wait_for_url(self, url, timeout=10):
        WebDriverWait(self.browser, timeout).until(
            lambda driver: driver.current_url == url
        )

    def test_1_add_new_contact(self):
        self.login()
        self.browser.get(f"{self.url}/create.php")
        self.browser.find_element(By.ID, 'name').send_keys("John Doe")
        self.browser.find_element(By.ID, 'email').send_keys("john.doe@example.com")
        self.browser.find_element(By.ID, 'phone').send_keys("123456789")
        self.browser.find_element(By.ID, 'title').send_keys("Developer")
        self.browser.find_element(By.CSS_SELECTOR, 'input[type="submit"]').click()
        self.wait_for_url(f"{self.url}/index.php")
        logging.info("Test 1: New contact added successfully.")
        assert self.browser.current_url == f"{self.url}/index.php"

    def test_2_delete_contact(self):
        self.login()
        actions_section = self.browser.find_element(By.XPATH, "//tr[@role='row'][1]//td[contains(@class, 'actions')]")
        delete_button = actions_section.find_element(By.XPATH, ".//a[contains(@class, 'btn-danger')]")
        delete_button.click()
        self.browser.switch_to.alert.accept()
        self.wait_for_url(f"{self.url}/index.php")
        logging.info("Test 2: Contact deleted successfully.")
        assert self.browser.current_url == f"{self.url}/index.php"

    def test_3_change_profile_picture(self):
        self.login()
        self.browser.get(f"{self.url}/profil.php")
        file_path = os.path.join(os.getcwd(), 'tests', 'image-change-test.jpg')
        self.browser.find_element(By.ID, 'formFile').send_keys(file_path)
        self.browser.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
        self.wait_for_url(f"{self.url}/profil.php")
        logging.info("Test 3: Profile picture changed successfully.")
        assert self.browser.current_url == f"{self.url}/profil.php"

    def test_4_update_contact(self):
        self.login()
        actions_section = self.browser.find_element(By.XPATH, "//tr[@role='row'][1]//td[contains(@class, 'actions')]")
        update_button = actions_section.find_element(By.XPATH, ".//a[contains(@class, 'btn-success')]")
        update_button.click()
        self.browser.find_element(By.ID, 'name').clear()
        self.browser.find_element(By.ID, 'name').send_keys("Jane Doe")
        self.browser.find_element(By.ID, 'email').clear()
        self.browser.find_element(By.ID, 'email').send_keys("jane.doe@example.com")
        self.browser.find_element(By.ID, 'phone').clear()
        self.browser.find_element(By.ID, 'phone').send_keys("987654321")
        self.browser.find_element(By.ID, 'title').clear()
        self.browser.find_element(By.ID, 'title').send_keys("Designer")
        self.browser.find_element(By.CSS_SELECTOR, 'input[type="submit"]').click()
        self.wait_for_url(f"{self.url}/index.php")
        logging.info("Test 4: Contact updated successfully.")
        assert self.browser.current_url == f"{self.url}/index.php"

    def test_5_test_xss_security(self):
        self.login()
        self.browser.get(f"{self.url}/vpage.php")
        self.browser.find_element(By.NAME, 'thing').send_keys("<script>alert(1)</script>")
        self.browser.find_element(By.NAME, 'submit').click()
        
        try:
            alert = self.browser.switch_to.alert
            alert.accept()
            logging.error("Test 5: XSS vulnerability detected!")
            self.fail("XSS vulnerability detected!")
        except NoAlertPresentException:
            logging.info("Test 5: No XSS vulnerability detected.")
            pass

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        logging.info("Browser closed.")

if __name__ == '__main__':
    unittest.main(verbosity=2, warnings='ignore')