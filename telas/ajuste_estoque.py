from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QMessageBox, 
    QComboBox, QLineEdit, QLabel
)

from models.produto import listar_produtos, ajustar_estoque
from telas.base import BaseWindow


class TelaAjusteEstoque(BaseWindow):
    def __init__(self):
        super().__init__("Ajuste de Estoque")

        self.setWindowTitle("Ajuste de Estoque")
        self.resize(700, 500)

        layout = self.area

        self.combo_produto = QComboBox()
        self.carregar_produtos()

        self.input_quantidade = QLineEdit()
        self.input_quantidade.setPlaceholderText("Quantidade (+ ou -)")

        self.btn_salvar = QPushButton("Aplicar Ajuste")
        self.btn_salvar.clicked.connect(self.aplicar)

        layout.addWidget(QLabel("Produto"))
        layout.addWidget(self.combo_produto)
        layout.addWidget(self.input_quantidade)
        layout.addWidget(self.btn_salvar)

       

    def carregar_produtos(self):
        for p in listar_produtos():
            self.combo_produto.addItem(p[1], p[0])

    def aplicar(self):
        produto_id = self.combo_produto.currentData()
        quantidade = float(self.input_quantidade.text())

        ajustar_estoque(produto_id, quantidade)

        QMessageBox.information(
            self, 
            "Estoque ajustado")