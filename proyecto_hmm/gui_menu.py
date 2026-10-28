
from PyQt5 import QtCore, QtWidgets
from config import Config
from gui_common import STYLE, button


class MainMenuWindow:
    """Ventana de bienvenida institucional y selección de modo."""
    def __init__(self, on_select_2d, on_select_3d):
        self.on_select_2d, self.on_select_3d = on_select_2d, on_select_3d
        self.window = None

    def build(self):
        self.window = QtWidgets.QMainWindow()
        self.window.setWindowTitle(Config.GUI_TITLE)
        self.window.resize(1000, 700)
        self.window.setStyleSheet(STYLE)
        central = QtWidgets.QWidget()
        self.window.setCentralWidget(central)
        layout = QtWidgets.QVBoxLayout(central)
        layout.setContentsMargins(70, 45, 70, 45)
        for text in ['UNIVERSIDAD DE LOS LLANOS', 'Facultad de Ciencias Básicas e Ingeniería · Ingeniería de Sistemas', 'Procesos Estocásticos · Proyecto final']:
            label = QtWidgets.QLabel(text)
            label.setAlignment(QtCore.Qt.AlignCenter)
            layout.addWidget(label)
        layout.addStretch()
        title = QtWidgets.QLabel('Reconocedor de caracteres\nHMM 2D & 3D')
        title.setObjectName('title')
        title.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(title)
        subtitle = QtWidgets.QLabel('Traza, explora y visualiza predicciones en tiempo real')
        subtitle.setAlignment(QtCore.Qt.AlignCenter)
        subtitle.setObjectName('muted')
        layout.addWidget(subtitle)
        layout.addSpacing(30)
        cards = QtWidgets.QHBoxLayout()
        for mode, description, callback in [
            ('Modo 2D', 'Dibuja sobre un plano cartesiano.\nObserva la clasificación y la trayectoria futura.', self.on_select_2d),
            ('Modo 3D', 'Traza sobre una esfera interactiva.\nGira, acerca y explora el espacio.', self.on_select_3d)]:
            card = QtWidgets.QFrame()
            card.setObjectName('card')
            inner = QtWidgets.QVBoxLayout(card)
            inner.setContentsMargins(25, 25, 25, 25)
            label = QtWidgets.QLabel(description)
            label.setWordWrap(True)
            inner.addWidget(label)
            inner.addSpacing(15)
            inner.addWidget(button(mode, callback, True))
            cards.addWidget(card)
        layout.addLayout(cards)
        layout.addStretch()
        footer = QtWidgets.QLabel('27 letras minúsculas · Modelos ocultos de Markov')
        footer.setAlignment(QtCore.Qt.AlignCenter)
        footer.setObjectName('muted')
        layout.addWidget(footer)

    def show(self):
        self.window.show()

    def close(self):
        if self.window:
            self.window.close()
