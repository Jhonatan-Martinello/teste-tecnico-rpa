from config import CSV_FILE
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage
from utils.csv_reader import CsvReader
from utils.driver import create_driver


def main():

    driver = create_driver()

    login = LoginPage(driver)
    login.open()
    login.login()

    reader = CsvReader(CSV_FILE)

    products = reader.load_products()

    inventory = InventoryPage(driver)

    for product in products:

        inventory.add_product(
            product["Produto"]
        )

    input("Produtos adicionados.")

    driver.quit()


if __name__ == "__main__":
    main()