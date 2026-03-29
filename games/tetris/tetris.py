import sys
import random
from PySide6.QtWidgets import QApplication, QWidget, QMessageBox
from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QPainter, QColor

# Config
COLS = 10
ROWS = 20
SIZE = 20
WIDTH = COLS * SIZE
HEIGHT = ROWS * SIZE
SPEED = 300

# Peças (formas)
SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1], [1, 1]],  # O
    [[0, 1, 0], [1, 1, 1]],  # T
    [[1, 0, 0], [1, 1, 1]],  # L
    [[0, 0, 1], [1, 1, 1]],  # J
]

COLORS = [
    QColor("cyan"),
    QColor("yellow"),
    QColor("purple"),
    QColor("orange"),
    QColor("blue"),
]


class Tetris(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tetris")
        self.setFixedSize(WIDTH, HEIGHT)
        self.setAttribute(Qt.WA_DeleteOnClose)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_game)

        self.reset()

    def reset(self):
        self.board = [[0]*COLS for _ in range(ROWS)]
        self.score = 0
        self.spawn_piece()
        self.timer.start(SPEED)

    def spawn_piece(self):
        self.shape = random.choice(SHAPES)
        self.color = COLORS[SHAPES.index(self.shape)]
        self.x = COLS // 2 - len(self.shape[0]) // 2
        self.y = 0

        if self.check_collision(self.x, self.y):
            self.game_over()

    def check_collision(self, x, y, shape=None):
        if shape is None:
            shape = self.shape

        for i, row in enumerate(shape):
            for j, cell in enumerate(row):
                if cell:
                    nx = x + j
                    ny = y + i

                    if nx < 0 or nx >= COLS or ny >= ROWS:
                        return True
                    if ny >= 0 and self.board[ny][nx]:
                        return True
        return False

    def merge(self):
        for i, row in enumerate(self.shape):
            for j, cell in enumerate(row):
                if cell:
                    self.board[self.y + i][self.x + j] = self.color

    def clear_lines(self):
        new_board = [row for row in self.board if any(cell == 0 for cell in row)]
        lines = ROWS - len(new_board)

        for _ in range(lines):
            new_board.insert(0, [0]*COLS)

        self.board = new_board
        self.score += lines

    def rotate(self):
        rotated = list(zip(*self.shape[::-1]))
        rotated = [list(row) for row in rotated]

        if not self.check_collision(self.x, self.y, rotated):
            self.shape = rotated

    def update_game(self):
        if not self.check_collision(self.x, self.y + 1):
            self.y += 1
        else:
            self.merge()
            self.clear_lines()
            self.spawn_piece()

        self.update()

    def keyPressEvent(self, event):
        key = event.key()

        if key == Qt.Key_Left and not self.check_collision(self.x - 1, self.y):
            self.x -= 1
        elif key == Qt.Key_Right and not self.check_collision(self.x + 1, self.y):
            self.x += 1
        elif key == Qt.Key_Down and not self.check_collision(self.x, self.y + 1):
            self.y += 1
        elif key == Qt.Key_Up:
            self.rotate()

        self.update()

    def game_over(self):
        self.timer.stop()
        QMessageBox.information(self, "Game Over", f"Score: {self.score}")
        self.reset()

    def closeEvent(self, event):
        self.timer.stop()
        event.accept()

    def paintEvent(self, event):
        painter = QPainter(self)

        painter.fillRect(0, 0, WIDTH, HEIGHT, QColor("black"))

        # tabuleiro
        for y in range(ROWS):
            for x in range(COLS):
                if self.board[y][x]:
                    painter.setBrush(self.board[y][x])
                    painter.drawRect(x*SIZE, y*SIZE, SIZE, SIZE)

        # peça atual
        painter.setBrush(self.color)
        for i, row in enumerate(self.shape):
            for j, cell in enumerate(row):
                if cell:
                    painter.drawRect(
                        (self.x + j)*SIZE,
                        (self.y + i)*SIZE,
                        SIZE, SIZE
                    )

        # score
        painter.setPen(QColor("white"))
        painter.drawText(5, 15, f"Score: {self.score}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    game = Tetris()
    game.show()
    sys.exit(app.exec())