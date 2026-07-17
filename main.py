from pages.login_page import LoginPage
from utils.driver import create_driver


def main():

    driver = create_driver()

    login = LoginPage(driver)

    login.open()

    login.login()

    input("Login realizado. Pressione ENTER para finalizar.")

    driver.quit()


if __name__ == "__main__":
    main()