import sys
from PyQt5.QtWidgets import QApplication

# Importamos nuestras clases
from config import Config
from model_loader import ModelLoader
from feature_extractor import FeatureExtractor2D, FeatureExtractor3D
from recognizer import Recognizer, TrajectoryProjector
from gui_menu import MainMenuWindow
from gui_2d import Canvas2DWindow
from gui_3d import Canvas3DWindow


class App:
    """Punto de entrada: inicializa servicios y lanza Ventana A."""

    def __init__(self):
        print("Iniciando aplicación...")
        # 1. Cargar configuración y componentes
        self.loader = ModelLoader(Config.MODELS_DIR, Config.CHARS, Config.N_STATES, Config.K_2D)
        self.extractor2 = FeatureExtractor2D(Config.K_2D)
        self.extractor3 = FeatureExtractor3D(Config.K_3D)

        # 2. Crear los reconocedores
        self.recognizer_2d = Recognizer(self.loader, self.extractor2, mode="2D")
        self.recognizer_3d = Recognizer(self.loader, self.extractor3, mode="3D")

        # 3. Crear los proyectores
        self.projector_2d = TrajectoryProjector(self.recognizer_2d)
        self.projector_3d = TrajectoryProjector(self.recognizer_3d)

        self.current_window = None

    def open_menu(self):
        """Abre la Ventana A (Menú principal)"""
        print("Abriendo menú principal...")
        # Si había otra ventana abierta, la cerramos
        previous_window = self.current_window

        self.current_window = MainMenuWindow(
            on_select_2d=self.open_2d,
            on_select_3d=self.open_3d
        )
        self.current_window.build()
        self.current_window.show()
        if previous_window:
            previous_window.close()

    def open_2d(self):
        """Abre la Ventana B (Lienzo 2D)"""
        print("Abriendo lienzo 2D...")
        previous_window = self.current_window

        self.current_window = Canvas2DWindow(
            recognizer=self.recognizer_2d,
            projector=self.projector_2d,
            on_back=self.open_menu
        )
        self.current_window.build()
        self.current_window.show()
        if previous_window:
            previous_window.close()

    def open_3d(self):
        """Abre la Ventana C (Lienzo 3D)"""
        print("Abriendo lienzo 3D...")
        previous_window = self.current_window

        self.current_window = Canvas3DWindow(
            recognizer=self.recognizer_3d,
            projector=self.projector_3d,
            on_back=self.open_menu
        )
        self.current_window.build()
        self.current_window.show()
        if previous_window:
            previous_window.close()

    def run(self):
        self.open_menu()


if __name__ == "__main__":
    print("Arrancando el bucle de eventos de PyQt...")
    # ESTO ES VITAL: Inicializa la aplicación gráfica
    qt_app = QApplication(sys.argv)

    # Instanciamos nuestra app y la ejecutamos
    app = App()
    app.run()

    # Mantiene la ventana abierta hasta que el usuario la cierre
    sys.exit(qt_app.exec_())