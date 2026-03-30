from database.conexao import get_conexao
from datetime import date

data = date.today()

def criar_nota(numero_nota, data, fornecedor_id):
    conn = get_conexao()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO NOTAS (NUMERO_NOTA, DATA, FORNECEDOR_ID)
        VALUES (?, ?, ?)
        RETURNING ID
    """, (numero_nota, data, fornecedor_id))

    nota_id = cursor.fetchone()[0]

    conn.commit()
    conn.close()

    return nota_id

def inserir_item_nota(nota_id, produto_id, quantidade):
    conn = get_conexao()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO ITENS_NOTA (NOTA_ID, PRODUTO_ID, QUANTIDADE)
        VALUES (?, ?, ?)
    """, (nota_id, produto_id, quantidade))

    conn.commit()
    conn.close()

