from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel
)
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt


class BaseWindow(QMainWindow):
    def __init__(self, titulo="Sistema"):
        super().__init__()

        self.setWindowTitle(titulo)
        
        central = QWidget()
        self.setCentralWidget(central)

        layout_principal = QVBoxLayout()
        central.setLayout(layout_principal)

        topo = QHBoxLayout()

        titulo_label = QLabel(titulo)
        titulo_label.setStyleSheet("font-size: 20px; font-weight: bold;")

        logo = QLabel()
        pixmap = QPixmap("assets/logo.png")

        if not pixmap.isNull():
            logo.setPixmap(pixmap.scaled(120, 60, Qt.KeepAspectRatio))

        topo.addWidget(titulo_label)
        topo.addStretch()
        topo.addWidget(logo)

        layout_principal.addLayout(topo)

        container = QWidget()
        self.area = QVBoxLayout()
        container.setLayout(self.area)

        layout_principal.addWidget(container)