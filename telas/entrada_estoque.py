import sys
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLineEdit, QPushButton, QMessageBox,
    QTableWidget, QTableWidgetItem, QHBoxLayout, QLabel
)

from PySide6.QtWidgets import QComboBox
from models.fornecedor import listar_fornecedores
from models.nota import criar_nota, inserir_item_nota
from models.produto import listar_produtos
from telas.cadastro_produto import TelaCadastroProduto
from telas.base import BaseWindow
import fdb



class TelaEntradaEstoque(BaseWindow):
    def __init__(self):
        super().__init__("Entrada de Nota")

        self.setWindowTitle("Entrada de Nota")
        layout = self.area  

        self.btn_novo_produto = QPushButton("Novo Produto")
        self.btn_novo_produto.clicked.connect(self.abrir_cadastro_produto)
        layout.addWidget(self.btn_novo_produto)

        self.btn_recarregar = QPushButton("Atualizar Produtos")
        self.btn_recarregar.clicked.connect(self.atualizar_produtos)
        layout.addWidget(self.btn_recarregar)

        #fornecedor
        self.combo_fornecedor = QComboBox()
        self.carregar_fornecedores()

        layout.addWidget(QLabel("Fornecedor"))
        layout.addWidget(self.combo_fornecedor)

        #NumNota
        self.input_nota = QLineEdit()
        self.input_nota.setPlaceholderText("Número da Nota")

        #itens
        self.tabela = QTableWidget(0, 3)  
        self.tabela.setHorizontalHeaderLabels([
            "Produto", "Quantidade", "Ação"  
        ])

        #add linha de produto
        btn_add = QPushButton("Adicionar Produto")
        btn_add.clicked.connect(self.adicionar_linha)

        #save
        btn_salvar = QPushButton("Salvar Nota")
        btn_salvar.clicked.connect(self.salvar_nota)

        layout.addWidget(QLabel("Número da Nota"))
        layout.addWidget(self.input_nota)

        layout.addWidget(self.tabela)
        layout.addWidget(btn_add)
        layout.addWidget(btn_salvar)

    def atualizar_produtos(self):
        for row in range(self.tabela.rowCount()):
            combo = self.tabela.cellWidget(row, 0)
            if combo:
                combo.clear()
                for p in listar_produtos():
                    combo.addItem(p[1], p[0])

    def carregar_fornecedores(self):
        self.combo_fornecedor.clear()
        fornecedores = listar_fornecedores()

        for f in fornecedores:
            self.combo_fornecedor.addItem(f"{f[1]}", f[0])

    def adicionar_linha(self):
        row = self.tabela.rowCount()
        self.tabela.insertRow(row)

        produtos = self.carregar_produtos()

        #box de produtos
        combo_produto = QComboBox()
        for p in produtos:
            combo_produto.addItem(p[1], p[0])  

        self.tabela.setCellWidget(row, 0, combo_produto)
        
        self.tabela.setItem(row, 1, QTableWidgetItem("0"))
        
        btn_remover = QPushButton("Remover")
        btn_remover.clicked.connect(lambda _, r=row: self.tabela.removeRow(r))

        self.tabela.setCellWidget(row, 2, btn_remover)

    def salvar_nota(self):
        numero = self.input_nota.text().strip()
        fornecedor_id = self.combo_fornecedor.currentData()
        
        # 21316565 validações slk
        if not numero:
            QMessageBox.warning(
                self,
                "Campo Obrigatório",
                "Por favor, informe o número da nota fiscal."
            )
            return
        
        if fornecedor_id is None:
            QMessageBox.warning(
                self,
                "Fornecedor não selecionado",
                "Por favor, selecione um fornecedor."
            )
            return
        
        if self.tabela.rowCount() == 0:
            QMessageBox.warning(
                self,
                "Nenhum item",
                "Adicione pelo menos um produto à nota fiscal."
            )
            return
        
        for row in range(self.tabela.rowCount()):
            combo = self.tabela.cellWidget(row, 0)
            if combo is None or combo.currentData() is None:
                QMessageBox.warning(
                    self,
                    "Produto inválido",
                    f"produto {row + 1}: Selecione um produto válido."
                )
                return
            
            try:
                quantidade = float(self.tabela.item(row, 1).text())
                if quantidade <= 0:
                    QMessageBox.warning(
                        self,
                        "Quantidade inválida",
                        f"produto {row + 1}: A quantidade deve ser maior que zero."
                    )
                    return
            except ValueError:
                QMessageBox.warning(
                    self,
                    "Quantidade inválida",
                    f"produto {row + 1}: Digite um número válido para quantidade."
                )
                return
        
        try:
            nota_id = criar_nota(numero, "TODAY", fornecedor_id)
                     
            for row in range(self.tabela.rowCount()):
                combo = self.tabela.cellWidget(row, 0)
                produto_id = combo.currentData()
                quantidade = float(self.tabela.item(row, 1).text())
                               
                inserir_item_nota(nota_id, produto_id, quantidade)
                        
            QMessageBox.information( #se der certo retorna msg
                self,
                "Sucesso",
                f"Nota fiscal #{numero} salva com sucesso!\n"
                f"Fornecedor: {self.combo_fornecedor.currentText()}\n"
                f"Itens: {self.tabela.rowCount()}"
            )
                        
            self.limpar_formulario()
            
        except fdb.fbcore.DatabaseError as e: #acesso violento de nota duplicada
            if "-803" in str(e) or "violation of PRIMARY or UNIQUE KEY" in str(e):
                QMessageBox.critical(
                    self,
                    "Nota já cadastrada",
                    f"O número de nota '{numero}' já existe no sistema.\n\n"
                    "Verifique o número da nota fiscal e tente novamente.\n"
                    "Cada nota fiscal deve ter um número único."
                )
            else:
                #erros aleatórios do fdb
                QMessageBox.critical(
                    self,
                    "Erro no Banco de Dados",
                    f"Ocorreu um erro ao salvar a nota fiscal:\n\n{str(e)}"
                )
        except Exception as e:
            #em algum momento, em algum lugar, algo deu errado
            QMessageBox.critical(
                self,
                "Erro Inesperado",
                f"em algum momento, em algum lugar, algo deu errado:\n\n{str(e)}"
            )

    def limpar_formulario(self):        
        self.input_nota.clear()
        self.tabela.setRowCount(0)

    def carregar_produtos(self):
        return listar_produtos()
    
    def abrir_cadastro_produto(self):
        self.tela_produto = TelaCadastroProduto()
        self.tela_produto.show()