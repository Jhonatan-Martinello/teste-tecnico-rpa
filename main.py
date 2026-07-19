from datetime import datetime

from config import CSV_FILE
from pages.cart_page import CartPage
from pages.checkout_complete_page import CheckoutCompletePage
from pages.checkout_page import CheckoutPage
from pages.checkout_overview_page import CheckoutOverviewPage
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage
from utils.csv_reader import CsvReader
from utils.driver import create_driver
from utils.logger import configure_logger
from utils.report import Report
from utils.retry import retry
from utils.screenshot import Screenshot


def main():

    # cria automaticamente o ChromeDriver
    driver = create_driver()

    # configura o logger para registrar informações durante a execução
    logger = configure_logger()

    try:
        logger.info("Iniciando execução da automação.")

        # cria o objeto Report para gerar o relatório de execução
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        report = Report(f"logs/relatorio_compras_{timestamp}.txt")

        #cria o objeto Screenshot para capturar screenshots durante a execução
        screenshot = Screenshot(driver)

        #inicializa variavais de controle
        successful_products = []
        failed_products = []
        validation  = []
        confirmation_message = ""

        logger.info("Realizando login na página do SauceDemo.")

        # chama a função que faz o login na página do saucedemo
        login = LoginPage(driver)
        login.open()
        retry(login.login, retries=3, delay=2)

        logger.info("Login realizado com sucesso.")

        logger.info("Lendo arquivo CSV.")

        # le o arquivo CSV que contém os produtos
        reader = CsvReader(CSV_FILE)
        products_list = reader.load_products()

        # se nenhum produto for encontrado, dispara uma exceção
        if not products_list:
            logger.error("Nenhum produto encontrado no CSV")
            raise Exception("Nenhum produto encontrado no CSV")
        
        logger.info(f"Produtos carregados: {len(products_list)}")

        # percorre pelos produtos da lista (CSV) e adiciona eles ao carinho, caso sejam prodtos válidos
        # caso sejam produtos inválidos retorna "sucesso": False e não adiciona ao carinho
        # quantidade não está sendo utilizada, pois o SauceDemo não permite quantidade > 1
        logger.info("Adicionando produtos ao carrinho de compras.")
        inventory = InventoryPage(driver)
        for product in products_list:

            result = inventory.add_product(
                product["Produto"],
                product["Quantidade"]
            )

            if result["sucesso"]:
                logger.info(f"Produto adicionado com sucesso: {result['produto']}")
                successful_products.append(result)
            else:
                logger.warning(f"Falha ao adicionar produto: {result['produto']}. Motivo: {result['mensagem']}")
                failed_products.append(result)

        # abre o carinho de compras, contendo os produtos adicionados
        logger.info("Abrindo carrinho de compras.")
        cart = CartPage(driver)
        cart.open()
        screenshot.capture("carrinho_de_compras")

        # verifica se todos os produtos foram adicionados, ou se existe algum produto ausente
        expected_products = [
            product["produto"] for product in successful_products
        ]
        missing_products = cart.validate_products(expected_products)

        # popula o log, informando os produtos ausentes
        for product in missing_products:
            logger.warning(f"Produto ausente no carrinho: {product}")

            failed_products.append({
                "produto": product,
                "quantidade": 1,
                "sucesso": False,
                "mensagem": "Produto não encontrado no carrinho."
            })

        # remove os produtos ausentes da lista de produtos bem sucedidos
        successful_products = [
            product for product in successful_products
            if product["produto"] not in missing_products
        ]

        # vai para a tela de checkout e preenche as informações pessoais
        logger.info("Acessando a página de checkout.")
        checkout = CheckoutPage(driver)
        checkout.open()
        retry(checkout.populate_personal_data, retries=3, delay=2)
        logger.info("Informações pessoais preenchidas com sucesso.")

        # vai para a proxima etapa do checkout
        # não foram inseridos dados de pagamento, pois o SauceDemo não permite manipulação de dados de pagamento
        logger.info("Continuando para a etapa de revisão do pedido.")
        checkout.continue_checkout()
        overview = CheckoutOverviewPage(driver)

        # valida valores do pedido
        validation = overview.validate_checkout()

        logger.info("Validando valores do pedido.")
        if ( validation["subtotal_valid"] and validation["total_valid"]):
            logger.info("Valores do pedido validados com sucesso. Finalizando compra.")
            retry(overview.finish_purchase, retries=3, delay=2)
        else:
            logger.error("Divergência nos valores do pedido. Compra não finalizada.")
            return

        logger.info("Pegando a mensagem de confirmação do pedido.")
        complete = CheckoutCompletePage(driver)
        confirmation_message = complete.is_order_complete()
        screenshot.capture("confirmacao_pedido")
        logger.info(f"Mensagem de confirmação do pedido: {confirmation_message}")

    except Exception as e:
        screenshot.capture("erro_execucao")
        logger.error(f"Ocorreu um erro durante a execução: {e}", exc_info=True)

    finally:
        report.generate(
            successful_products=successful_products,
            failed_products=failed_products,
            validate_checkout=validation,
            confirmation_message=confirmation_message,
            order_number=None
        )

        logger.info("Pressione ENTER para finalizar.")
        input("Pressione ENTER para finalizar")
        driver.quit()


if __name__ == "__main__":
    main()