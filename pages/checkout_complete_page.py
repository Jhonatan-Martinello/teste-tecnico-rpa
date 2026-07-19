from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from config import DEFAULT_TIMEOUT


class CheckoutCompletePage:

    COMPLETE_HEADER = "complete-header"
    COMPLETE_TEXT = "complete-text"
    
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, DEFAULT_TIMEOUT)

    def is_order_complete(self):
        complete_header = self.wait.until(
            EC.visibility_of_element_located((By.CLASS_NAME, "complete-header"))
        )

        complete_text = self.wait.until(
            EC.visibility_of_element_located((By.CLASS_NAME, "complete-text"))
        )

        confirmation_message = complete_header.text + " " + complete_text.text

        return confirmation_message
    