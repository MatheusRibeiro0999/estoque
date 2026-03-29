from database.conexao import get_conexao

def inserir_fornecedor(nome, cnpj=None, telefone=None):
    conn = get_conexao()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO FORNECEDORES (NOME, CNPJ, TELEFONE)
        VALUES (?, ?, ?)
    """, (nome, cnpj, telefone))

    conn.commit()
    conn.close()

def listar_fornecedores():
    conn = get_conexao()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT ID, NOME
        FROM FORNECEDORES
        ORDER BY NOME
    """)

    dados = cursor.fetchall()
    conn.close()

    return dados