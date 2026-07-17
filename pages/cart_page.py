from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from config import DEFAULT_TIMEOUT


class CartPage:

    CART_LINK = "shopping_cart_link"
    CART_ITEM_DIV = "cart_item"
    INVENTORY_NAME_DIV = "inventory_item_name"

    
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, DEFAULT_TIMEOUT)


    def open(self):
        cart_button = self.wait.until(
            EC.element_to_be_clickable((By.CLASS_NAME, self.CART_LINK))
        )

        cart_button.click()


    def get_products(self):

        products = self.wait.until(
            EC.presence_of_all_elements_located(
                (By.CLASS_NAME, self.CART_ITEM_DIV)
            )
        )

        product_names = []

        for product in products:
            name = product.find_element(
                By.CLASS_NAME,
                self.INVENTORY_NAME_DIV
            ).text

            product_names.append(name)

        return product_names
    
    
    def validate_products(self, expected_products):

        cart_products = self.get_products()

        missing_products = []

        for product in expected_products:

            if product not in cart_products:
                missing_products.append(product)

        return missing_products
    