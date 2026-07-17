from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class InventoryPage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def add_product(self, product_name):

        products = self.wait.until(
            EC.presence_of_all_elements_located(
                (By.CLASS_NAME, "inventory_item")
            )
        )

        for product in products:

            name = product.find_element(
                By.CLASS_NAME,
                "inventory_item_name"
            ).text

            if name == product_name:

                product.find_element(
                    By.TAG_NAME,
                    "button"
                ).click()

                return True

        return False