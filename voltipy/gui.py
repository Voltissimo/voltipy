import sys
from game import Board
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QLabel, QFrame
from PyQt5.QtGui import QIcon, QPainter
from PyQt5.QtSvg import QSvgRenderer


class ChessWindow(QWidget):
    def __init__(self, board: 'Board'):
        super().__init__()
        self.board = board
        self.init_ui()

    def init_ui(self):
        self.setGeometry(300, 100, 700, 520)
        self.setWindowTitle('Chess Board')

        self.main_layout = QGridLayout()
        self.setLayout(self.main_layout)

        self.chess_board = ChessBoard()
        self.main_layout.addWidget(self.chess_board, 0, 0, rowSpan=2)

        self.show()


class ChessBoard(QFrame):
    def __init__(self):
        super().__init__()
        self.main_grid = QGridLayout(self)


class Square(QWidget):
    def __init__(self, color, piece):
        super().__init__()
        self.setGeometry(100, 100, 100, 100)
        self.renderer = QSvgRenderer()
        self.renderer.load('icons\\regular\\bb.svg')
        self.setStyleSheet("""
            background: blue;
        """)

    def paintEvent(self, event):
        if self.renderer is not None:
            painter = QPainter(self)
            self.renderer.render(painter)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    b = Board.from_start_pos()
    gui = ChessWindow(b)
    sys.exit(app.exec_())
