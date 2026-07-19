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


    def _convert_money(self, value): # converte por exemplo: '$29.99' para: 29.99
        value = (
            value
            .replace("$", "")
            .replace("Item total:", "")
            .replace("Tax:", "")
            .replace("Total:", "")
            .strip()
        )

        return float(value)


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

        return self._convert_money(subtotal.text)


    def get_tax(self):
        tax = self.wait.until(
            EC.visibility_of_element_located((By.CLASS_NAME, self.TAX))
        )

        return self._convert_money(tax.text)


    def get_total(self):
        total = self.wait.until(
            EC.visibility_of_element_located((By.CLASS_NAME, self.TOTAL))
        )

        return self._convert_money(total.text)


    def calculate_expected_subtotal(self):
        prices = self.get_item_prices()

        return round(sum(prices), 2)


    def validate_checkout(self):
        expected_subtotal = self.calculate_expected_subtotal()
        displayed_subtotal = self.get_subtotal()
        expected_total = round(expected_subtotal + self.get_tax(), 2)
        displayed_total = self.get_total()
        subtotal_valid = expected_subtotal == displayed_subtotal
        total_valid = expected_total == displayed_total

        return {
            "expected_subtotal": expected_subtotal,
            "displayed_subtotal": displayed_subtotal,
            "expected_total": expected_total,
            "displayed_total": displayed_total,
            "subtotal_valid": subtotal_valid,
            "total_valid": total_valid
        }


    def finish_purchase(self):
        button = self.wait.until(
            EC.element_to_be_clickable((By.ID, self.FINISH_BUTTON))
        )

        button.click()
