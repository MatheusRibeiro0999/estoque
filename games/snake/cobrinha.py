import sys
import random
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QStackedLayout
)
from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QPainter, QColor

# Config
LARGURA = 400
ALTURA = 400
TAMANHO = 20
VELOCIDADE = 100


class SnakeGame(QWidget):
    def __init__(self, game_over_callback=None):
        super().__init__()
        self.setFixedSize(LARGURA, ALTURA)
        self.game_over_callback = game_over_callback
        self.setAttribute(Qt.WA_DeleteOnClose)

        self.timer = QTimer()
        self.timer.timeout.connect(self.mover)

        self.resetar()

    def resetar(self):
        self.cobra = [(100, 100), (80, 100), (60, 100)]
        self.direcao = "Right"
        self.comida = self.gerar_comida()
        self.score = 0
        self.timer.start(VELOCIDADE)

    def gerar_comida(self):
        x = random.randint(0, (LARGURA // TAMANHO) - 1) * TAMANHO
        y = random.randint(0, (ALTURA // TAMANHO) - 1) * TAMANHO
        return (x, y)

    def keyPressEvent(self, event):
        tecla = event.key()
        if tecla == Qt.Key_Up and self.direcao != "Down":
            self.direcao = "Up"
        elif tecla == Qt.Key_Down and self.direcao != "Up":
            self.direcao = "Down"
        elif tecla == Qt.Key_Left and self.direcao != "Right":
            self.direcao = "Left"
        elif tecla == Qt.Key_Right and self.direcao != "Left":
            self.direcao = "Right"

    def mover(self):
        x, y = self.cobra[0]

        if not self.isVisible():
            return

        if self.direcao == "Up":
            y -= TAMANHO
        elif self.direcao == "Down":
            y += TAMANHO
        elif self.direcao == "Left":
            x -= TAMANHO
        elif self.direcao == "Right":
            x += TAMANHO

        nova = (x, y)

        # colisão
        if (
            x < 0 or x >= LARGURA or
            y < 0 or y >= ALTURA or
            nova in self.cobra
        ):
            self.timer.stop()
            if self.game_over_callback:
                self.game_over_callback(self.score)
            else:
                from PySide6.QtWidgets import QMessageBox
                QMessageBox.information(self, "Game Over", f"Score: {self.score}")
                self.resetar()
            return
        

        self.cobra.insert(0, nova)

        if nova == self.comida:
            self.comida = self.gerar_comida()
            self.score += 1
        else:
            self.cobra.pop()

        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)

        # fundo
        painter.fillRect(0, 0, LARGURA, ALTURA, QColor("black"))

        # cobra
        painter.setBrush(QColor("green"))
        for x, y in self.cobra:
            painter.drawRect(x, y, TAMANHO, TAMANHO)

        # comida
        painter.setBrush(QColor("red"))
        x, y = self.comida
        painter.drawRect(x, y, TAMANHO, TAMANHO)

        # score
        painter.setPen(QColor("white"))
        painter.drawText(10, 20, f"Score: {self.score}")

    def closeEvent(self, event):
        self.timer.stop()
        event.accept()


class Menu(QWidget):
    def __init__(self, iniciar_callback, sair_callback):
        super().__init__()

        layout = QVBoxLayout()

        titulo = QLabel("🐍 Cobrinha")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("font-size: 24px;")

        btn_jogar = QPushButton("Jogar")
        btn_sair = QPushButton("Sair")

        btn_jogar.clicked.connect(iniciar_callback)
        btn_sair.clicked.connect(sair_callback)

        layout.addWidget(titulo)
        layout.addWidget(btn_jogar)
        layout.addWidget(btn_sair)

        self.setLayout(layout)


class GameOver(QWidget):
    def __init__(self, jogar_novamente, voltar_menu):
        super().__init__()

        self.layout = QVBoxLayout()

        self.label = QLabel("")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("font-size: 20px;")

        btn_retry = QPushButton("Jogar novamente")
        btn_menu = QPushButton("Voltar ao menu")

        btn_retry.clicked.connect(jogar_novamente)
        btn_menu.clicked.connect(voltar_menu)

        self.layout.addWidget(self.label)
        self.layout.addWidget(btn_retry)
        self.layout.addWidget(btn_menu)

        self.setLayout(self.layout)

    def set_score(self, score):
        self.label.setText(f"Game Over!\nScore: {score}")


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Snake PySide6")

        self.stack = QStackedLayout()
        self.setLayout(self.stack)

        self.menu = Menu(self.iniciar_jogo, self.close)
        self.jogo = SnakeGame(self.mostrar_game_over)
        self.game_over = GameOver(self.reiniciar_jogo, self.voltar_menu)

        self.stack.addWidget(self.menu)
        self.stack.addWidget(self.jogo)
        self.stack.addWidget(self.game_over)

    def iniciar_jogo(self):
        self.jogo.resetar()
        self.stack.setCurrentWidget(self.jogo)
        self.jogo.setFocus()

    def mostrar_game_over(self, score):
        self.game_over.set_score(score)
        self.stack.setCurrentWidget(self.game_over)

    def reiniciar_jogo(self):
        self.iniciar_jogo()

    def voltar_menu(self):
        self.stack.setCurrentWidget(self.menu)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    janela = MainWindow()
    janela.show()
    sys.exit(app.exec())