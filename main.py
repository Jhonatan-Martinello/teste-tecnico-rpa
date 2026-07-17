from config import CSV_FILE
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.checkout_overview_page import CheckoutOverviewPage
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage
from utils.csv_reader import CsvReader
from utils.driver import create_driver


def main():

    # cria automaticamente o ChromeDriver
    driver = create_driver()

    try:
        # chama a função que faz o login na página do saucedemo
        login = LoginPage(driver)
        login.open()
        login.login()

        # le o arquivo CSV que contém os produtos
        reader = CsvReader(CSV_FILE)
        products_list = reader.load_products()
        
        # se nenhum produto for encontrado, dispara uma exceção
        if not products_list:
            raise Exception("Nenhum produto encontrado no CSV")

        # percorre pelos produtos da lista (CSV) e adiciona eles ao carinho, caso sejam prodtos válidos
        # caso sejam produtos inválidos retorna "sucesso": False e não adiciona ao carinho
        # quantidade não está sendo utilizada, pois o SauceDemo não permite quantidade > 1
        inventory = InventoryPage(driver)
        for product in products_list:

            inventory.add_product(
                product["Produto"]
            )

        # abre o carinho de compras, contendo os produtos adicionados
        cart = CartPage(driver)
        cart.open()

        # verifica se todos os produtos foram adicionados, ou se existe algum produto ausente
        expected_products = [
            product["Produto"] for product in products_list
        ]
        missing_products = cart.validate_products(expected_products)

        # popula o log, informando se houve produtos ausentes ou não 
        if not missing_products:
            print("Todos os produtos foram encontrados no carrinho.")
        else:
            print("Produtos ausentes:")

            for product in missing_products:
                print(f"- {product}")

        # vai para a tela de checkout e preenche as informações pessoais
        checkout = CheckoutPage(driver)
        checkout.open()
        checkout.populate_personal_data()

        #vai para a proxima etapa od checkout
        checkout.continue_checkout()
        overview = CheckoutOverviewPage(driver)

        # valida valores do pedido
        validation = overview.validate_checkout()

        if ( validation["subtotal_valid"] and validation["total_valid"]):
            print( "Valores validados com sucesso.")
            overview.finish_purchase()
        else:
            print("Erro na validação dos valores.")

    finally:
        input("ENTER para finalizar")
        driver.quit()


if __name__ == "__main__":
    main()