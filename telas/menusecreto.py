from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel
from PySide6.QtCore import Qt
import subprocess

from games.snake.cobrinha import SnakeGame
from games.tetris.tetris import Tetris


class MenuSecreto(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("👀 Menu Secreto")
        self.resize(400, 300)

        layout = QVBoxLayout()

        titulo = QLabel("🎮 Área Secreta")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("font-size: 20px;")

        btn_snake = QPushButton("🐍 Snake")
        btn_tetris = QPushButton("🧩 Tetris")
        btn_doom = QPushButton("🔥 DOOM")

        btn_snake.clicked.connect(self.abrir_snake)
        btn_tetris.clicked.connect(self.abrir_tetris)
        btn_doom.clicked.connect(self.abrir_doom)

        layout.addWidget(titulo)
        layout.addWidget(btn_snake)
        layout.addWidget(btn_tetris)
        layout.addWidget(btn_doom)

        self.setLayout(layout)

        self.janelas = []

    def abrir_snake(self):
        tela = SnakeGame()
        tela.show()
        self.janelas.append(tela)

    def abrir_tetris(self):
        tela = Tetris()
        tela.show()
        self.janelas.append(tela)

    def abrir_doom(self):
        subprocess.Popen([
            r"C:\estoque\games\doom\chocolate-doom",
            "-iwad", r"C:\estoque\games\doom\doom1.wad"
        ])