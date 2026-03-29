import fdb

def get_conexao():
    conn = fdb.connect(
        dsn=r"C:\estoque\BANCO.FDB",
        user="SYSDBA",
        password="masterkey",
        charset="UTF8"
    )
    return conn