from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLineEdit,
    QPushButton, QListWidget, QLabel
)

from models.produto import inserir_produto, listar_produtos
from telas.base import BaseWindow


class TelaCadastroProduto(BaseWindow):
    def __init__(self):
        super().__init__("Cadastro de Produtos")

        self.setWindowTitle("Cadastro de Produtos")
        self.resize(400, 400)

        layout = self.area

        self.input_nome = QLineEdit()
        self.input_nome.setPlaceholderText("Nome do produto")
        self.input_quantidade = QLineEdit()
        self.input_quantidade.setPlaceholderText("Quantidade inicial")

        self.btn_salvar = QPushButton("Salvar Produto")
        self.btn_salvar.clicked.connect(self.salvar)

        self.lista = QListWidget()

        layout.addWidget(QLabel("Produto"))
        layout.addWidget(self.input_nome)
        layout.addWidget(self.input_quantidade)
        layout.addWidget(self.btn_salvar)
        layout.addWidget(self.lista)

        

        self.carregar()

    def salvar(self):
        nome = self.input_nome.text().strip()
        qtd = self.input_quantidade.text().strip()

        if not nome:
            return

        quantidade = float(qtd) if qtd else 0

        inserir_produto(nome, quantidade)

        self.input_nome.clear()
        self.input_quantidade.clear()

        self.carregar()

    def carregar(self):
        self.lista.clear()
        produtos = listar_produtos()

        for p in produtos:
            self.lista.addItem(f"{p[1]} (Estoque: {p[2]})")