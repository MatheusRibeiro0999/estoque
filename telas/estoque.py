from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QTableWidget,
    QTableWidgetItem, QPushButton,
    QLabel, QLineEdit
)

from models.produto import listar_estoque
from telas.base import BaseWindow


class TelaEstoque(BaseWindow):
    def __init__(self):
        super().__init__("Estoque")

        self.setWindowTitle("Estoque")
        self.resize(700, 500)

        layout = self.area

        self.input_busca = QLineEdit()
        self.input_busca.setPlaceholderText("Buscar produto...")
        self.input_busca.textChanged.connect(self.carregar)

        self.tabela = QTableWidget(0, 2)
        self.tabela.setHorizontalHeaderLabels([
            "Produto", "Quantidade"
        ])

        self.tabela.setSortingEnabled(True)

        self.label_total = QLabel("Total de itens em estoque: 0")

        btn_atualizar = QPushButton("Atualizar")
        btn_atualizar.clicked.connect(self.carregar)

        layout.addWidget(self.input_busca)
        layout.addWidget(self.tabela)
        layout.addWidget(self.label_total)
        layout.addWidget(btn_atualizar)

        self.carregar()

    def carregar(self):
        self.tabela.setRowCount(0)

        filtro = self.input_busca.text().lower()
        dados = listar_estoque()

        total_itens = 0 

        for linha, item in enumerate(dados):
            nome = item[0]
            quantidade = item[1]

            if filtro and filtro not in nome.lower():
                continue

            total_itens += quantidade 

            row = self.tabela.rowCount()
            self.tabela.insertRow(row)

            self.tabela.setItem(row, 0, QTableWidgetItem(nome))
            self.tabela.setItem(row, 1, QTableWidgetItem(str(quantidade)))

        self.label_total.setText(f"Total de itens em estoque: {total_itens}")