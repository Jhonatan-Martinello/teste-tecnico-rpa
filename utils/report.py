from datetime import datetime
from pathlib import Path


class Report:

    def __init__(self, report_path):
        self.report_path = Path(report_path)


    def generate(
        self,
        successful_products,
        failed_products,
        validate_checkout,
        confirmation_message,
        order_number=None
    ):

        timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        self._generate_txt(
            timestamp,
            successful_products,
            failed_products,
            validate_checkout,
            confirmation_message,
            order_number,
        )

        self._generate_html(
            timestamp,
            successful_products,
            failed_products,
            validate_checkout,
            confirmation_message,
            order_number,
        )


    def _generate_txt(
        self,
        timestamp,
        successful_products,
        failed_products,
        validate_checkout,
        confirmation_message,
        order_number
    ):
        
        with open(self.report_path, "w", encoding="utf-8") as file:
            self._write_header(file, timestamp)

            self._write_successful_products(file, successful_products)

            self._write_failed_products(file, failed_products)

            self._write_checkout_validation(file, validate_checkout)

            self._write_order_information(
                file,
                confirmation_message,
                order_number
            )

            self._write_summary(
                file,
                successful_products,
                failed_products
            )

    def _generate_html(
        self,
        timestamp,
        successful_products,
        failed_products,
        validate_checkout,
        confirmation_message,
        order_number
    ):
        html_path = self.report_path.with_suffix(".html")
        template = Path("templates/report_template.html")
        html = template.read_text(encoding="utf-8")
        
        html = html.replace("{{TIMESTAMP}}",timestamp)

        html = html.replace(
            "{{SUCCESS_TABLE}}",
            self._html_success_table(successful_products)
        )

        html = html.replace(
            "{{FAILED_TABLE}}",
            self._html_failed_table(failed_products)
        )

        html = html.replace(
            "{{CHECKOUT}}",
            self._html_checkout(validate_checkout)
        )

        html = html.replace(
            "{{CONFIRMATION_MESSAGE}}",
            confirmation_message
        )

        html = html.replace(
            "{{ORDER_NUMBER}}",
            order_number if order_number else "Não disponível"
        )

        html = html.replace(
            "{{SUMMARY}}",
            self._html_summary(successful_products, failed_products)
        )

        with open(html_path, "w",encoding="utf-8") as file:
            file.write(html)


    def _write_header(self, file, timestamp):
        file.write("=" * 60 + "\n")
        file.write("RELATÓRIO DE EXECUÇÃO\n")
        file.write("=" * 60 + "\n\n")
        file.write(f"Data/Hora: {timestamp}\n\n")


    def _write_successful_products(self, file, successful_products):
        file.write("PRODUTOS PROCESSADOS COM SUCESSO\n")
        file.write("-" * 60 + "\n")

        if not successful_products:
            file.write("Nenhum produto processado.\n\n")
            return

        for product in successful_products:
            file.write(f"✔ Produto: {product['produto']}\n")
            file.write(f"  Quantidade: {product['quantidade']}\n")
            file.write(f"  Resultado : {product['mensagem']}\n\n")


    def _write_failed_products(self, file, failed_products):
        file.write("PRODUTOS COM FALHA\n")
        file.write("-" * 60 + "\n")

        if not failed_products:
            file.write("Nenhuma falha.\n\n")
            return

        for product in failed_products:
            file.write(f"✘ Produto: {product['produto']}\n")
            file.write(f"  Quantidade: {product['quantidade']}\n")
            file.write(f"  Motivo    : {product['mensagem']}\n\n")


    def _write_checkout_validation(self, file, checkout):
        file.write("VALIDAÇÃO DO CHECKOUT\n")
        file.write("-" * 60 + "\n")

        if not checkout:
            file.write("Validação do checkout não disponível.\n\n")
            return

        file.write(
            f"Subtotal esperado : "
            f"{checkout.get('expected_subtotal', 'Não disponível')}\n"
        )
        file.write(
            f"Subtotal exibido  : "
            f"{checkout.get('displayed_subtotal', 'Não disponível')}\n"
        )

        file.write(
            f"Total esperado    : "
            f"{checkout.get('expected_total', 'Não disponível')}\n"
        )
        file.write(
            f"Total exibido     : "
            f"{checkout.get('displayed_total', 'Não disponível')}\n\n"
        )

        subtotal_ok = checkout.get("subtotal_valid", False)
        total_ok = checkout.get("total_valid", False)

        file.write(
            f"Subtotal válido : {'Sim' if subtotal_ok else 'Não'}\n"
        )

        file.write(
            f"Total válido    : {'Sim' if total_ok else 'Não'}\n"
        )

        if subtotal_ok and total_ok:
            file.write(
                "\n✔ Valores do checkout validados com sucesso.\n\n"
            )
        else:
            file.write(
                "\n✘ Foram encontradas divergências nos valores.\n\n"
            )


    def _write_order_information(
        self,
        file,
        confirmation_message,
        order_number
    ):
        file.write("PEDIDO\n")
        file.write("-" * 60 + "\n")

        if confirmation_message:
            file.write(
                f"Mensagem de confirmação:\n"
                f"{confirmation_message}\n\n"
            )
        else:
            file.write("Mensagem de confirmação não disponível.\n\n")

        if order_number:
            file.write(f"Número do pedido: {order_number}\n\n")
        else:
            file.write("Número do pedido: Não disponível\n\n")


    def _write_summary(
        self,
        file,
        successful_products,
        failed_products
    ):
        file.write("=" * 60 + "\n")
        file.write("RESUMO DA EXECUÇÃO\n")
        file.write("=" * 60 + "\n")

        file.write(
            f"Produtos processados com sucesso: "
            f"{len(successful_products)}\n"
        )

        file.write(
            f"Produtos com falha: "
            f"{len(failed_products)}\n"
        )

        file.write(
            f"Total de produtos processados: "
            f"{len(successful_products) + len(failed_products)}\n"
        )


    def _html_success_table(self, successful_products):
        if not successful_products:
            return "<p>Nenhum produto processado.</p>"

        rows = ""
        for product in successful_products:
            rows += (
                f"<tr>"
                f"<td>{product['produto']}</td>"
                f"<td>{product['quantidade']}</td>"
                f"<td>{product['mensagem']}</td>"
                f"</tr>"
            )

        return (
            "<table border='1'>"
            "<tr><th>Produto</th><th>Quantidade</th><th>Resultado</th></tr>"
            f"{rows}"
            "</table>"
        )
    
    def _html_failed_table(self, failed_products):
        if not failed_products:
            return "<p>Nenhuma falha.</p>"

        rows = ""
        for product in failed_products:
            rows += (
                f"<tr>"
                f"<td>{product['produto']}</td>"
                f"<td>{product['quantidade']}</td>"
                f"<td>{product['mensagem']}</td>"
                f"</tr>"
            )

        return (
            "<table border='1'>"
            "<tr><th>Produto</th><th>Quantidade</th><th>Motivo</th></tr>"
            f"{rows}"
            "</table>"
        )
    
    def _html_checkout(self, checkout):
        if not checkout:
            return "<p>Validação do checkout não disponível.</p>"

        subtotal_ok = checkout.get("subtotal_valid", False)
        total_ok = checkout.get("total_valid", False)

        return (
            f"<p>Subtotal esperado: {checkout.get('expected_subtotal', 'Não disponível')}</p>"
            f"<p>Subtotal exibido: {checkout.get('displayed_subtotal', 'Não disponível')}</p>"
            f"<p>Total esperado: {checkout.get('expected_total', 'Não disponível')}</p>"
            f"<p>Total exibido: {checkout.get('displayed_total', 'Não disponível')}</p>"
            f"<p>Subtotal válido: {'Sim' if subtotal_ok else 'Não'}</p>"
            f"<p>Total válido: {'Sim' if total_ok else 'Não'}</p>"
        )
    
    def _html_summary(
        self,
        successful_products,
        failed_products
    ):
        return (
            f"<p>Produtos processados com sucesso: {len(successful_products)}</p>"
            f"<p>Produtos com falha: {len(failed_products)}</p>"
            f"<p>Total de produtos processados: "
            f"{len(successful_products) + len(failed_products)}</p>"
        )
