from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from config import DEFAULT_TIMEOUT, PERSONAL_FISRT_NAME, PERSONAL_LAST_NAME, PERSONAL_POSTAL_CODE


class CheckoutPage:

    CHECKOUT_BUTTON = "checkout"
    FIRST_NAME_INPUT = "first-name"
    LAST_NAME_INPUT = "last-name"
    POSTAL_CODE_INPUT = "postal-code"
    CONTINUE_BUTTON = "continue"

    
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, DEFAULT_TIMEOUT)


    def open(self):
        checkout_button = self.wait.until(
            EC.element_to_be_clickable((By.ID, self.CHECKOUT_BUTTON))
        )

        checkout_button.click()


    def populate_personal_data(self):

        first_name = self.wait.until(
            EC.visibility_of_element_located((By.ID, self.FIRST_NAME_INPUT))
        )

        last_name = self.wait.until(
           EC.visibility_of_element_located((By.ID, self.LAST_NAME_INPUT))
        )

        postal_code = self.wait.until(
           EC.visibility_of_element_located((By.ID, self.POSTAL_CODE_INPUT))
        )

        first_name.clear()
        first_name.send_keys(PERSONAL_FISRT_NAME)

        last_name.clear()
        last_name.send_keys(PERSONAL_LAST_NAME)

        postal_code.clear()
        postal_code.send_keys(PERSONAL_POSTAL_CODE)

        
    def continue_checkout(self):

        continue_button = self.wait.until(
            EC.element_to_be_clickable((By.ID, self.CONTINUE_BUTTON))
        )

        continue_button.click()
        