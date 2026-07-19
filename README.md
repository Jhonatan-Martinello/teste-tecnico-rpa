# Teste Técnico - Automação Web com Python

# Site utilizado

Foi utilizado o site **SauceDemo**.

**URL:**

https://www.saucedemo.com/

### Motivos da escolha

O SauceDemo é uma aplicação amplamente utilizada para testes de automação, oferecendo um fluxo completo de compra composto por:

- Login
- Catálogo de produtos
- Carrinho
- Checkout
- Confirmação de compra

Além disso, o ambiente é estável e não exige cadastro ou integração com meios de pagamento reais.

---

# Tecnologias e ferramentas utilizadas

- Python 3.12
- Selenium WebDriver
- WebDriver Manager
- Pandas
- Python Dotenv
- Logging (biblioteca nativa do Python)
- Page Object Model (POM)
- CSV (massa de testes)
- HTML e TXT para geração de relatórios
- Git
- Visual Studio Code

---

# Estrutura do projeto

```text
teste-tecnico-rpa/

├── data/
│   └── produtos_compra.csv
│
├── logs/
│   ├── automation.log
│   ├── relatorio_compras.txt
│   └── relatorio_compras.html
│
├── pages/
│   ├── login_page.py
│   ├── inventory_page.py
│   ├── cart_page.py
│   ├── checkout_page.py
│   ├── checkout_overview_page.py
│   └── checkout_complete_page.py
│
├── screenshots/
│
├── templates/
│   └── report_template.html
│
├── utils/
│   ├── csv_reader.py
│   ├── driver.py
│   ├── logger.py
│   ├── report.py
│   ├── retry.py
│   └── screenshot.py
│
├── .env
├── config.py
├── main.py
├── requirements.txt
└── README.md
```

---

# Instalação

## 1. Clonar o projeto

```bash
git clone <url-do-repositório>

cd teste-tecnico-rpa
```

---

## 2. Criar ambiente virtual

Windows

```bash
python -m venv .venv
```

Ativar

```bash
.venv\Scripts\activate
```

Linux/Mac

```bash
python3 -m venv .venv

source .venv/bin/activate
```

---

## 3. Instalar as dependências

```bash
pip install -r requirements.txt
```

---

# Dependências utilizadas

- selenium
- webdriver-manager
- python-dotenv

Caso necessário:

```bash
pip install selenium webdriver-manager python-dotenv
```

---

# Configuração

Criar um arquivo `.env` na raiz do projeto.

Exemplo:

```env
URL=https://www.saucedemo.com/

USERNAME=standard_user

PASSWORD=secret_sauce
```

---

# Produtos

Os produtos devem ser informados no arquivo

```
data/produtos_compra.csv
```

Exemplo:

```csv
Produto,Quantidade

Sauce Labs Backpack,1

Sauce Labs Bike Light,2

Sauce Labs Bolt T-Shirt,1
```

---

# WebDriver

Este projeto utiliza a biblioteca **webdriver-manager**.

Dessa forma **não é necessário baixar manualmente o ChromeDriver**.

Na primeira execução o WebDriver compatível com a versão instalada do Google Chrome será baixado automaticamente.

Caso o Google Chrome esteja desatualizado, recomenda-se atualizá-lo antes da execução.

---

# Executando o robô

Basta executar:

```bash
python main.py
```

Durante a execução o robô irá:

- abrir o navegador (caso o modo de execução --headless=new esteja comentado);
- realizar login;
- adicionar os produtos;
- validar o carrinho;
- preencher o checkout;
- validar subtotal e total;
- finalizar a compra;
- gerar logs, screenshots e relatório.

---

# Relatórios

Ao término da execução serão gerados:

```
logs/

automation.log

relatorio_compras.txt

relatorio_compras.html
```

O relatório HTML apresenta uma visualização mais amigável das informações da execução.

---

# Screenshots

Durante a execução são capturadas evidências nos principais momentos do fluxo:

- Carrinho
- Confirmação da compra
- Erros (quando ocorrerem)

As imagens são armazenadas em:

```
screenshots/
```

---

# Logs

A automação utiliza a biblioteca nativa **logging**.

São registrados eventos utilizando os níveis:

- INFO
- WARNING
- ERROR

O log é salvo em:

```
logs/automation.log
```

---

# Funcionalidades implementadas

- Login automatizado
- Leitura de produtos via CSV
- Inclusão de produtos no carrinho
- Validação dos produtos
- Validação de subtotal
- Validação de total
- Finalização da compra
- Geração de relatório TXT
- Geração de relatório HTML
- Captura de screenshots
- Logging da execução
- Retry automático para falhas temporárias
- Organização utilizando Page Object Model

---

# Exemplos de uso

## Executar a automação

```bash
python main.py
```

---

## Alterar os produtos

Editar o arquivo

```
data/produtos_compra.csv
```

Exemplo:

```csv
Produto,Quantidade

Sauce Labs Backpack,1

Sauce Labs Bike Light,1
```

Executar novamente:

```bash
python main.py
```

---

## Alterar usuário

Editar o arquivo

```
.env
```

```env
USERNAME=standard_user

PASSWORD=secret_sauce
```

Executar novamente:

```bash
python main.py
```