from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLineEdit,
    QPushButton, QListWidget, QLabel
)

from models.cliente import inserir_cliente, listar_clientes
from telas.base import BaseWindow


class TelaCadastroCliente(BaseWindow):
    def __init__(self):
        super().__init__("Cadastro de Clientes")

        self.setWindowTitle("Cadastro de Clientes")
        self.resize(400, 400)

        layout = self.area

        self.input_nome = QLineEdit()
        self.input_nome.setPlaceholderText("Nome")

        self.input_telefone = QLineEdit()
        self.input_telefone.setPlaceholderText("Telefone")

        self.btn_salvar = QPushButton("Salvar")
        self.btn_salvar.clicked.connect(self.salvar)

        self.lista = QListWidget()

        layout.addWidget(QLabel("Cadastro de Clientes"))
        layout.addWidget(self.input_nome)
        layout.addWidget(self.input_telefone)
        layout.addWidget(self.btn_salvar)
        layout.addWidget(self.lista)

        

        self.carregar()

    def salvar(self):
        inserir_cliente(
            self.input_nome.text(),
            self.input_telefone.text()
        )

        self.input_nome.clear()
        self.input_telefone.clear()

        self.carregar()

    def carregar(self):
        self.lista.clear()
        for c in listar_clientes():
            self.lista.addItem(f"{c[1]}")