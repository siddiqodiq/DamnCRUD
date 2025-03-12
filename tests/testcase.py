import unittest
import os
import time
from selenium import webdriver
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

class TestContactManagement(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        options = webdriver.FirefoxOptions()
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--ignore-ssl-errors')
        server = 'http://localhost:4444'  # Sesuaikan dengan endpoint Selenium Grid
        cls.browser = webdriver.Remote(command_executor=server, options=options)
        try:
            cls.url = os.environ['URL']
        except KeyError:
            cls.url = "http://localhost"  # Sesuaikan dengan URL aplikasi

    def login(self):
        self.browser.get(f"{self.url}/login.php")
        time.sleep(2)
        self.browser.find_element(By.ID, "inputUsername").send_keys("admin")
        self.browser.find_element(By.ID, "inputPassword").send_keys("nimda666!")
        self.browser.find_element(By.XPATH, "//button[@type='submit']").click()

    def wait_for_url(self, url, timeout=5):
        WebDriverWait(self.browser, timeout).until(
            lambda driver: driver.current_url == url
        )

    def test_1_add_new_contact(self):
        self.login()
        self.browser.get(f"{self.url}/create.php")
        time.sleep(2)
        self.browser.find_element(By.ID, 'name').send_keys("John Doe")
        self.browser.find_element(By.ID, 'email').send_keys("john.doe@example.com")
        self.browser.find_element(By.ID, 'phone').send_keys("123456789")
        self.browser.find_element(By.ID, 'title').send_keys("Developer")
        time.sleep(1)
        self.browser.find_element(By.CSS_SELECTOR, 'input[type="submit"]').click()
        self.wait_for_url(f"{self.url}/index.php")
        self.assertEqual(self.browser.current_url, f"{self.url}/index.php")

    def test_2_delete_contact(self):
        self.login()
        time.sleep(2)
        actions_section = self.browser.find_element(By.XPATH, "//tr[@role='row'][1]//td[contains(@class, 'actions')]")
        delete_button = actions_section.find_element(By.XPATH, ".//a[contains(@class, 'btn-danger')]")
        delete_button.click()
        self.browser.switch_to.alert.accept()
        self.wait_for_url(f"{self.url}/index.php")
        self.assertEqual(self.browser.current_url, f"{self.url}/index.php")

    def test_3_sign_out(self):
        self.login()
        self.browser.get(f"{self.url}/profil.php")
        time.sleep(2)
        self.browser.find_element(By.XPATH, '/html/body/div[1]/div[1]/div/div/a[3]').click()
        self.wait_for_url(f"{self.url}/login.php")
        self.assertEqual(self.browser.current_url, f"{self.url}/login.php")

    def test_4_update_contact(self):
        self.login()
        time.sleep(2)
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
        self.assertEqual(self.browser.current_url, f"{self.url}/index.php")

    def test_5_test_xss_security(self):
        self.login()
        self.browser.get(f"{self.url}/vpage.php")
        time.sleep(2)
        self.browser.find_element(By.NAME, 'thing').send_keys("<script>alert('xss')</script>")
        self.browser.find_element(By.NAME, 'submit').click()
        time.sleep(2)
        try:
            alert = self.browser.switch_to.alert
            alert.accept()
            self.fail("XSS vulnerability detected!")
        except NoAlertPresentException:
            pass

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()

if __name__ == '__main__':
    unittest.main(verbosity=2, warnings='ignore')
