from database.conexao import get_conexao
from datetime import date

def criar_pedido(data=None, cliente_id=None):
    conn = get_conexao()
    cursor = conn.cursor()

    if data is None:
        data = date.today()

    cursor.execute("""
        INSERT INTO PEDIDOS (DATA, CLIENTE_ID)
        VALUES (?, ?)
        RETURNING ID
    """, (data, cliente_id))

    pedido_id = cursor.fetchone()[0]

    conn.commit()
    conn.close()

    return pedido_id

def inserir_item_pedido(pedido_id, produto_id, quantidade):
    conn = get_conexao()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO ITENS_PEDIDO (PEDIDO_ID, PRODUTO_ID, QUANTIDADE, VALOR_UNITARIO)
        VALUES (?, ?, ?, 0)
    """, (pedido_id, produto_id, quantidade))

    conn.commit()
    conn.close()