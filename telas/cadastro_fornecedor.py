from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLineEdit,
    QPushButton, QListWidget, QLabel
)

from models.fornecedor import inserir_fornecedor, listar_fornecedores
from telas.base import BaseWindow


class TelaCadastroFornecedor(BaseWindow):
    def __init__(self):
        super().__init__("Cadastro de Fornecedores")

        self.setWindowTitle("Cadastro de Fornecedores")
        self.resize(700, 500)

        layout = self.area

        self.input_nome = QLineEdit()
        self.input_nome.setPlaceholderText("Nome")

        self.input_cnpj = QLineEdit()
        self.input_cnpj.setPlaceholderText("CNPJ")

        self.input_telefone = QLineEdit()
        self.input_telefone.setPlaceholderText("Telefone")

        self.btn_salvar = QPushButton("Salvar")
        self.btn_salvar.clicked.connect(self.salvar)

        self.lista = QListWidget()

        layout.addWidget(QLabel("Fornecedor"))
        layout.addWidget(self.input_nome)
        layout.addWidget(self.input_cnpj)
        layout.addWidget(self.input_telefone)
        layout.addWidget(self.btn_salvar)
        layout.addWidget(self.lista)

        

        self.carregar()

    def salvar(self):
        inserir_fornecedor(
            self.input_nome.text(),
            self.input_cnpj.text(),
            self.input_telefone.text()
        )

        self.input_nome.clear()
        self.input_cnpj.clear()
        self.input_telefone.clear()

        self.carregar()

    def carregar(self):
        self.lista.clear()
        for f in listar_fornecedores():
            self.lista.addItem(f"{f[1]}")