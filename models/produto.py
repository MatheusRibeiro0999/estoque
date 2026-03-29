from database.conexao import get_conexao

def inserir_produto(nome, quantidade=0):
    conn = get_conexao()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO PRODUTOS (NOME, QUANTIDADE_ATUAL)
        VALUES (?, ?)
    """, (nome, quantidade))

    conn.commit()
    conn.close()

def listar_produtos():
    conn = get_conexao()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT ID, NOME, QUANTIDADE_ATUAL
        FROM PRODUTOS
        ORDER BY NOME
    """)

    dados = cursor.fetchall()
    conn.close()

    return dados

def buscar_produto(id_produto):
    conn = get_conexao()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT ID, NOME, QUANTIDADE_ATUAL
        FROM PRODUTOS
        WHERE ID = ?
    """, (id_produto,))

    produto = cursor.fetchone()
    conn.close()

    return produto

def atualizar_produto(id_produto, nome):
    conn = get_conexao()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE PRODUTOS
        SET NOME = ?
        WHERE ID = ?
    """, (nome, id_produto))

    conn.commit()
    conn.close()

def deletar_produto(id_produto):
    conn = get_conexao()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM PRODUTOS
        WHERE ID = ?
    """, (id_produto,))

    conn.commit()
    conn.close()

def obter_estoque(produto_id):
    conn = get_conexao()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT QUANTIDADE_ATUAL
        FROM PRODUTOS
        WHERE ID = ?
    """, (produto_id,))

    estoque = cursor.fetchone()[0]
    conn.close()
    return estoque

def ajustar_estoque(produto_id, quantidade):
    conn = get_conexao()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE PRODUTOS
        SET QUANTIDADE_ATUAL = QUANTIDADE_ATUAL + ?
        WHERE ID = ?
    """, (quantidade, produto_id))

    conn.commit()
    conn.close()

def listar_estoque():
    conn = get_conexao()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 
            P.NOME,
            P.QUANTIDADE_ATUAL
        FROM PRODUTOS P
        ORDER BY P.NOME
    """)

    dados = cursor.fetchall()
    conn.close()

    return dados