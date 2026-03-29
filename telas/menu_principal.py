from PySide6.QtWidgets import QPushButton
from PySide6.QtCore import Qt

from telas.base import BaseWindow
from telas.cadastro_produto import TelaCadastroProduto
from telas.entrada_estoque import TelaEntradaEstoque
from telas.venda import TelaVenda
from telas.cadastro_fornecedor import TelaCadastroFornecedor
from telas.cadastro_cliente import TelaCadastroCliente
from telas.ajuste_estoque import TelaAjusteEstoque
from telas.estoque import TelaEstoque
from telas.menusecreto import MenuSecreto


class MenuPrincipal(BaseWindow):
    def __init__(self):
        super().__init__("Sistema de Estoque")

        self.setWindowTitle("Sistema de Estoque")
        self.resize(400, 300)

        #↑ ↑ ↓ ↓ ← → ← → B A
        self.sequencia = []
        self.codigo_secreto = [
            Qt.Key_Up, Qt.Key_Up,
            Qt.Key_Down, Qt.Key_Down,
            Qt.Key_Left, Qt.Key_Right,
            Qt.Key_Left, Qt.Key_Right,
            Qt.Key_B, Qt.Key_A
        ]

        self.setFocusPolicy(Qt.StrongFocus)

        layout = self.area

        btn_produtos = QPushButton("Cadastro de Produtos")
        btn_produtos.clicked.connect(self.abrir_produtos)

        btn_entrada = QPushButton("Entrada de Estoque")
        btn_entrada.clicked.connect(self.abrir_entrada)

        btn_venda = QPushButton("Venda / Pedido")
        btn_venda.clicked.connect(self.abrir_venda)

        btn_fornecedor = QPushButton("Fornecedores")
        btn_fornecedor.clicked.connect(self.abrir_fornecedor)

        btn_cliente = QPushButton("Clientes")
        btn_cliente.clicked.connect(self.abrir_cliente)

        btn_ajuste = QPushButton("Ajuste de Estoque")
        btn_ajuste.clicked.connect(self.abrir_ajuste)

        btn_estoque = QPushButton("Ver Estoque")
        btn_estoque.clicked.connect(self.abrir_estoque)

        layout.addWidget(btn_estoque)
        layout.addWidget(btn_fornecedor)
        layout.addWidget(btn_cliente)
        layout.addWidget(btn_ajuste)
        layout.addWidget(btn_produtos)
        layout.addWidget(btn_entrada)
        layout.addWidget(btn_venda)

        self.janelas = {}

    def abrir_janela(self, nome, classe):
        if nome in self.janelas:
            janela = self.janelas[nome]

            if janela and janela.isVisible():
                janela.raise_()
                janela.activateWindow()
                return

        janela = classe()
        janela.show()

        self.janelas[nome] = janela

        janela.destroyed.connect(lambda: self.janelas.pop(nome, None))

    def keyPressEvent(self, event):
        tecla = event.key()

        self.sequencia.append(tecla)

        if len(self.sequencia) > len(self.codigo_secreto):
            self.sequencia.pop(0)

        if self.sequencia == self.codigo_secreto:
            self.abrir_menu_secreto()

    def abrir_menu_secreto(self):
        self.abrir_janela("menu_secreto", MenuSecreto)

    def abrir_produtos(self):
        self.abrir_janela("produtos", TelaCadastroProduto)

    def abrir_entrada(self):
        self.abrir_janela("entrada", TelaEntradaEstoque)

    def abrir_venda(self):
        self.abrir_janela("venda", TelaVenda)

    def abrir_fornecedor(self):
        self.abrir_janela("fornecedor", TelaCadastroFornecedor)

    def abrir_cliente(self):
        self.abrir_janela("cliente", TelaCadastroCliente)

    def abrir_ajuste(self):
        self.abrir_janela("ajuste", TelaAjusteEstoque)

    def abrir_estoque(self):
        self.abrir_janela("estoque", TelaEstoque)