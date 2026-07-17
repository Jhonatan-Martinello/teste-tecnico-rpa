from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from config import SAUCE_URL, SAUCE_USERNAME, SAUCE_PASSWORD, DEFAULT_TIMEOUT


class LoginPage:

    USERNAME_INPUT = "user-name"
    PASSWORD_INPUT = "password"
    LOGIN_BUTTON = "login-button"


    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, DEFAULT_TIMEOUT)


    def open(self):
        self.driver.get(SAUCE_URL)


    def login(self):

        username = self.wait.until(
            EC.visibility_of_element_located((By.ID, self.USERNAME_INPUT))
        )

        password = self.wait.until(
            EC.visibility_of_element_located((By.ID, self.PASSWORD_INPUT))
        )

        login_button = self.wait.until(
            EC.element_to_be_clickable((By.ID, self.LOGIN_BUTTON))
        )

        username.clear()
        username.send_keys(SAUCE_USERNAME)

        password.clear()
        password.send_keys(SAUCE_PASSWORD)

        login_button.click()
        