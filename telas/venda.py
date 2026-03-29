from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton,
    QTableWidget, QTableWidgetItem, QComboBox, QLabel,
    QMessageBox
)

from models.produto import listar_produtos
from models.pedido import criar_pedido, inserir_item_pedido
from PySide6.QtWidgets import QComboBox
from models.cliente import listar_clientes
from telas.base import BaseWindow
from utils.pdf import gerar_pdf_pedido
from models.cliente import listar_clientes


class TelaVenda(BaseWindow):
    def __init__(self):
        super().__init__("Venda / Pedido")
        self.setWindowTitle("Venda / Pedido")
        self.resize(700, 500)

        self.combo_cliente = QComboBox()
        self.carregar_clientes()
          
        layout = self.area

        self.tabela = QTableWidget(0, 3)
        self.tabela.setHorizontalHeaderLabels([
            "Produto", "Quantidade", "Ação"
        ])

        btn_add = QPushButton("Adicionar Produto")
        btn_add.clicked.connect(self.adicionar_linha)

        btn_salvar = QPushButton("Finalizar Venda")
        btn_salvar.clicked.connect(self.salvar)

        layout.addWidget(QLabel("Cliente"))
        layout.addWidget(self.combo_cliente)

        layout.addWidget(QLabel("Itens da venda"))
        layout.addWidget(self.tabela)
        layout.addWidget(btn_add)
        layout.addWidget(btn_salvar)

    def carregar_clientes(self):
        for c in listar_clientes():
            self.combo_cliente.addItem(c[1], c[0])

    def adicionar_linha(self):
        row = self.tabela.rowCount()
        self.tabela.insertRow(row)

        combo = QComboBox()
        produtos = listar_produtos()

        for p in produtos:
            combo.addItem(p[1], p[0])

        self.tabela.setCellWidget(row, 0, combo)
        self.tabela.setItem(row, 1, QTableWidgetItem("1"))

        btn = QPushButton("Remover")
        btn.clicked.connect(lambda _, r=row: self.tabela.removeRow(r))

        self.tabela.setCellWidget(row, 2, btn)

    def salvar(self):
        from models.produto import obter_estoque
        from models.pedido import criar_pedido, inserir_item_pedido

        cliente_id = self.combo_cliente.currentData()
        cliente_nome = self.combo_cliente.currentText()

        if self.tabela.rowCount() == 0:            
            QMessageBox.warning(
                self,
                "Aviso",
                "Nenhum item na venda! Adicione pelo menos um produto."
            )
            return

        itens = []

        for row in range(self.tabela.rowCount()):
            combo = self.tabela.cellWidget(row, 0)
            produto_id = combo.currentData()
            produto_nome = combo.currentText()
            
            try:
                quantidade = float(self.tabela.item(row, 1).text())
            except ValueError:
                QMessageBox.critical(
                    self,
                    "Erro",
                    f"Quantidade inválida para o produto '{produto_nome}'. Use um número válido."
                )
                return

            estoque = obter_estoque(produto_id)

            if quantidade > estoque:
                QMessageBox.critical( #estoque insuficiente negão
                    self,
                    "Estoque Insuficiente",
                    f"Estoque insuficiente para o produto '{produto_nome}'.\n"
                    f"Estoque disponível: {estoque}\n"
                    f"Solicitado: {quantidade}"
                )
                return

            itens.append({
                "produto_id": produto_id,
                "nome": produto_nome,
                "quantidade": quantidade
            })

        pedido_id = criar_pedido(None, cliente_id)

        for item in itens:
            inserir_item_pedido(
                pedido_id,
                item["produto_id"],
                item["quantidade"]
            )

        gerar_pdf_pedido(pedido_id, cliente_nome, itens)

        QMessageBox.information(
            self,
            "Sucesso",
            f"Venda finalizada com sucesso!\n"
            f"Pedido #{pedido_id}\n"
            f"PDF gerado: pedido_{pedido_id}.pdf"
        )

        self.limpar_tela()

    def limpar_tela(self):
        """Limpa a tela para um novo pedido"""
        self.tabela.setRowCount(0)
        if self.combo_cliente.count() > 0:
            self.combo_cliente.setCurrentIndex(0)