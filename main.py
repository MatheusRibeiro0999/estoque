import sys
from PySide6.QtWidgets import QApplication

from telas.menu_principal import MenuPrincipal


def carregar_estilo(app):
    with open("styles/dark.qss", "r") as f:
        app.setStyleSheet(f.read())


app = QApplication(sys.argv)

carregar_estilo(app)

janela = MenuPrincipal()
janela.show()

app.exec()