from database.conexao import get_conexao

def inserir_cliente(nome, telefone):
    conn = get_conexao()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO CLIENTES (NOME, TELEFONE)
        VALUES (?, ?)
    """, (nome, telefone))

    conn.commit()
    conn.close()


def listar_clientes():
    conn = get_conexao()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT ID, NOME FROM CLIENTES
    """)

    dados = cursor.fetchall()
    conn.close()

    return dados