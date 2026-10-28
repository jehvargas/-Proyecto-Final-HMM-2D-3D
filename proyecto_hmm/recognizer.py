
class Recognizer:
    """Orquesta HMM + Features: clasifica y proyecta trayectoria futura."""

    def __init__(self, loader, extractor, mode="2D"):
        self.loader    = loader
        self.extractor = extractor
        self.mode      = mode
        self.models    = loader.load_all()

    def classify(self, points):
        """
        Calcula P(O_1:t | λ_c) con Forward para cada carácter.
        Retorna lista ordenada descendente:
        [{'char':'a','prob':0.87,'icon':'...'}, ...]
        """
        ...

    def classify_partial(self, points, t):
        ...

    def best_char(self, points):
        """argmax_c P(O|λ_c)."""
        ...


class TrajectoryProjector:
    """Proyecta la trayectoria futura del carácter más probable."""

    def __init__(self, recognizer):
        self.recognizer = recognizer

    def project(self, points, cursor, mode="2D"):
        """
        1. Viterbi sobre O_1:t → estado actual.
        2. Extrae símbolos más probables desde ese estado.
        3. Reconstruye coordenadas desde `cursor`.
        Retorna lista de puntos proyectados.
        """
        ...