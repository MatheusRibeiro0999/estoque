from PySide6.QtWidgets import QPushButton
from PySide6.QtWidgets import QLabel
from telas.base import BaseWindow

from telas.cadastro_produto import TelaCadastroProduto
from telas.entrada_estoque import TelaEntradaEstoque
from telas.venda import TelaVenda
from telas.cadastro_fornecedor import TelaCadastroFornecedor
from telas.cadastro_cliente import TelaCadastroCliente
from telas.ajuste_estoque import TelaAjusteEstoque
from telas.estoque import TelaEstoque



class MenuPrincipal(BaseWindow):
    def __init__(self):
        super().__init__("Sistema de Estoque")
        
        self.setWindowTitle("Sistema de Estoque")
        self.resize(400, 300)

        
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

        
        

        #ref das janelas
        self.janelas = []

    def abrir_produtos(self):
        tela = TelaCadastroProduto()
        tela.show()
        self.janelas.append(tela)

    def abrir_entrada(self):
        tela = TelaEntradaEstoque()
        tela.show()
        self.janelas.append(tela)

    def abrir_venda(self):
        tela = TelaVenda()
        tela.show()
        self.janelas.append(tela)

    def abrir_fornecedor(self):
        tela = TelaCadastroFornecedor()
        tela.show()
        self.janelas.append(tela)

    def abrir_cliente(self):
        tela = TelaCadastroCliente()
        tela.show()
        self.janelas.append(tela)

    def abrir_ajuste(self):
        tela = TelaAjusteEstoque()
        tela.show()
        self.janelas.append(tela)

    def abrir_estoque(self):
        tela = TelaEstoque()
        tela.show()
        self.janelas.append(tela)