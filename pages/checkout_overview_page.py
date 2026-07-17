from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from config import DEFAULT_TIMEOUT


class CheckoutOverviewPage:

    ITEM_NAME = "inventory_item_name"
    ITEM_PRICE = "inventory_item_price"
    SUBTOTAL = "summary_subtotal_label"
    TAX = "summary_tax_label"
    TOTAL = "summary_total_label"
    FINISH_BUTTON = "finish"


    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, DEFAULT_TIMEOUT)


    def get_item_prices(self):

        prices = self.wait.until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, self.ITEM_PRICE))
        )

        return [
            self._convert_money(price.text)
            for price in prices
        ]


    def get_subtotal(self):

        subtotal = self.wait.until(
            EC.visibility_of_element_located((By.CLASS_NAME, self.SUBTOTAL))
        )

        return self._convert_money(
            subtotal.text
        )


    def get_tax(self):

        tax = self.wait.until(
            EC.visibility_of_element_located((By.CLASS_NAME, self.TAX))
        )

        return self._convert_money(
            tax.text
        )


    def get_total(self):

        total = self.wait.until(
            EC.visibility_of_element_located((By.CLASS_NAME, self.TOTAL))
        )

        return self._convert_money(
            total.text
        )


    def calculate_expected_subtotal(self):

        prices = self.get_item_prices()

        return round(sum(prices), 2)


    def validate_subtotal(self):

        expected = self.calculate_expected_subtotal()
        displayed = self.get_subtotal()

        return expected == displayed


    def validate_total(self):

        subtotal = self.get_subtotal()
        tax = self.get_tax()
        total = self.get_total()

        expected_total = round(
            subtotal + tax,
            2
        )

        return expected_total == total


    def validate_checkout(self):

        return {
            "subtotal_valid": self.validate_subtotal(),
            "total_valid": self.validate_total()
        }


    def finish_purchase(self):

        button = self.wait.until(
            EC.element_to_be_clickable((By.ID, self.FINISH_BUTTON))
        )

        button.click()


    def _convert_money(self, value):

        # converte: '$29.99' para:29.99

        value = (
            value
            .replace("$", "")
            .replace("Item total:", "")
            .replace("Tax:", "")
            .replace("Total:", "")
            .strip()
        )

        return float(value)