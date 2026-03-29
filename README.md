## projeto opensource
desenvolvido para uso pessoal
criamos este app para controle de estoque, entrada e saída de materiais em uma empresa de esquadrias 
o arquivo do banco de dados já está estruturado e pronto pra uso, deixei aqui embaixo como foram criadas as tabelas
o app IBOconsole está no repo para facilitar o acesso ao DB, sugiro implementar o projeto na pasta C: do windows ou na pasta raiz 
é possível alterar o caminho do banco de dados no arquivo database/conexao.py na linha 5 dentro da função get_conexao (dsn=r"C:\estoque\BANCO.FDB",)

Python 3.13
Firebird 2.5.9 (Banco de dados)
PySide6 (Interface gráfica)
FDB (Driver Firebird)
ReportLab (Geração de PDF)

Estrutura do Projeto
estoque/

│

├── main.py

├── models/

│   ├── produto.py

│   ├── pedido.py

│   ├── cliente.py

│   ├── fornecedor.py

│   └── nota.py

│

├── telas/

│   ├── base.py

│   ├── menu_principal.py

│   ├── cadastro_produto.py

│   ├── entrada_estoque.py

│   ├── venda.py

│   ├── estoque.py

│   ├── cadastro_cliente.py

│   ├── cadastro_fornecedor.py

│   └── ajuste_estoque.py

│
├── utils/

│   └── pdf.py

│

├── assets/

│   └── logo.png

│

└── styles/

    └── dark.qss
    

##BANCO DE DADOS:
CREATE TABLE PRODUTOS (
    ID INTEGER NOT NULL,
    NOME VARCHAR(100) NOT NULL,
    QUANTIDADE_ATUAL NUMERIC(15,2) DEFAULT 0,
    CONSTRAINT PK_PRODUTOS PRIMARY KEY (ID)
);

CREATE TABLE FORNECEDORES (
    ID INTEGER NOT NULL,
    NOME VARCHAR(100),
    CNPJ VARCHAR(20),
    TELEFONE VARCHAR(20),
    CONSTRAINT PK_FORNECEDORES PRIMARY KEY (ID)
);

CREATE TABLE NOTAS (
    ID INTEGER NOT NULL,
    NUMERO_NOTA VARCHAR(50),
    DATA DATE,
    FORNECEDOR_ID INTEGER,
    CONSTRAINT PK_NOTAS PRIMARY KEY (ID),
    CONSTRAINT FK_NOTA_FORNECEDOR FOREIGN KEY (FORNECEDOR_ID)
        REFERENCES FORNECEDORES(ID)
);

CREATE TABLE ITENS_NOTA (
    ID INTEGER NOT NULL,
    NOTA_ID INTEGER,
    PRODUTO_ID INTEGER,
    QUANTIDADE NUMERIC(15,2),
    VALOR_UNITARIO NUMERIC(15,2),
    CONSTRAINT PK_ITENS_NOTA PRIMARY KEY (ID),
    CONSTRAINT FK_ITEM_NOTA FOREIGN KEY (NOTA_ID)
        REFERENCES NOTAS(ID),
    CONSTRAINT FK_ITEM_PRODUTO FOREIGN KEY (PRODUTO_ID)
        REFERENCES PRODUTOS(ID)
);

CREATE TABLE CLIENTES (
    ID INTEGER NOT NULL,
    NOME VARCHAR(100),
    TELEFONE VARCHAR(20),
    CONSTRAINT PK_CLIENTES PRIMARY KEY (ID)
);

CREATE TABLE PEDIDOS (
    ID INTEGER NOT NULL,
    DATA DATE,
    CLIENTE_ID INTEGER,
    CONSTRAINT PK_PEDIDOS PRIMARY KEY (ID),
    CONSTRAINT FK_PEDIDO_CLIENTE FOREIGN KEY (CLIENTE_ID)
        REFERENCES CLIENTES(ID)
);

CREATE TABLE ITENS_PEDIDO (
    ID INTEGER NOT NULL,
    PEDIDO_ID INTEGER,
    PRODUTO_ID INTEGER,
    QUANTIDADE NUMERIC(15,2),
    VALOR_UNITARIO NUMERIC(15,2),
    CONSTRAINT PK_ITENS_PEDIDO PRIMARY KEY (ID),
    CONSTRAINT FK_ITEM_PEDIDO FOREIGN KEY (PEDIDO_ID)
        REFERENCES PEDIDOS(ID),
    CONSTRAINT FK_ITEM_PEDIDO_PRODUTO FOREIGN KEY (PRODUTO_ID)
        REFERENCES PRODUTOS(ID)
);






