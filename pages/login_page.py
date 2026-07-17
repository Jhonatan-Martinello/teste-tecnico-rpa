from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from config import URL, USERNAME, PASSWORD


class LoginPage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def open(self):
        self.driver.get(URL)

    def login(self):

        username = self.wait.until(
            EC.visibility_of_element_located((By.ID, "user-name"))
        )

        password = self.driver.find_element(By.ID, "password")

        login_button = self.driver.find_element(By.ID, "login-button")

        username.send_keys(USERNAME)
        password.send_keys(PASSWORD)

        login_button.click()