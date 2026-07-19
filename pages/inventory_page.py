from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from config import DEFAULT_TIMEOUT


class InventoryPage:

    INVENTORY_ITEM_DIV = "inventory_item"
    INVENTORY_NAME_DIV = "inventory_item_name"
    CART_BUTTON = "add-to-cart-" # padrão inicial do nome do botão, será concatenado com o nome do produto

    
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, DEFAULT_TIMEOUT)


    def _get_add_to_cart_button_id(self, product_name):
        return (
            self.CART_BUTTON
            + product_name.lower()
                .replace(" ", "-")
                .replace(".", "")
        )


    def add_product(
            self, 
            product_name,
            product_quantity
        ):
        products = self.wait.until(
            EC.presence_of_all_elements_located(
                (By.CLASS_NAME, self.INVENTORY_ITEM_DIV)
            )
        )

        for product in products:

            name = product.find_element(
                By.CLASS_NAME,
                self.INVENTORY_NAME_DIV
            ).text

            if name == product_name:
                try:
                
                    button_id = self._get_add_to_cart_button_id(product_name)
                    button = self.wait.until(
                        EC.element_to_be_clickable((By.ID, button_id))
                    )
                    button.click()

                    return {
                        "produto": product_name,
                        "quantidade": product_quantity,
                        "sucesso": True,
                        "mensagem": "Produto adicionado ao carrinho"
                    }
                
                except NoSuchElementException:
                     
                     return {
                        "produto": product_name,
                        "quantidade": product_quantity,
                        "sucesso": False,
                        "mensagem": "Produto não encontrado"
                    }
            
        return {
            "produto": product_name,
            "quantidade": product_quantity,
            "sucesso": False,
            "mensagem": "Produto não encontrado"
        }
    